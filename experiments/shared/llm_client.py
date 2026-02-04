"""Unified LLM client for OpenAI and Ollama backends."""

import json
import logging
import math
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests
from openai import APITimeoutError, OpenAI

from .config import ModelConfig

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_BACKOFF = (10, 30, 60)


@dataclass
class LLMResponse:
    """Standardized response from any LLM backend."""

    content: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    elapsed: float = 0.0
    logprobs: Optional[List[Dict[str, Any]]] = None


class LLMClient:
    """Unified client wrapping OpenAI API and Ollama (OpenAI-compatible + native)."""

    def __init__(self, config: ModelConfig):
        self.config = config
        self._timeout = config.timeout
        if config.backend == "openai":
            self._client = OpenAI(timeout=self._timeout)
        else:
            self._client = OpenAI(
                base_url=config.base_url or "http://localhost:11434/v1",
                api_key="ollama",
                timeout=self._timeout,
            )

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def supports_logprobs(self) -> bool:
        return self.config.supports_logprobs

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
        max_tokens: int = 2000,
    ) -> LLMResponse:
        """Standard chat completion (works for both OpenAI and Ollama)."""
        last_err = None
        for attempt in range(MAX_RETRIES):
            try:
                t0 = time.time()
                response = self._client.chat.completions.create(
                    model=self.config.model_id,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                elapsed = time.time() - t0

                choice = response.choices[0]
                usage = response.usage

                return LLMResponse(
                    content=choice.message.content or "",
                    prompt_tokens=usage.prompt_tokens if usage else 0,
                    completion_tokens=usage.completion_tokens if usage else 0,
                    elapsed=round(elapsed, 2),
                )
            except (APITimeoutError, requests.ConnectionError) as e:
                last_err = e
                wait = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
                logger.warning(
                    "%s chat attempt %d/%d failed (%s), retrying in %ds",
                    self.config.name, attempt + 1, MAX_RETRIES, e, wait,
                )
                time.sleep(wait)
        raise TimeoutError(
            f"{self.config.name} chat failed after {MAX_RETRIES} retries: {last_err}"
        )

    def chat_with_logprobs(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
        max_tokens: int = 10,
    ) -> LLMResponse:
        """Chat completion with logprobs via Ollama native API.

        Falls back to standard chat if logprobs are unavailable.
        """
        if not self.config.supports_logprobs:
            return self.chat(messages, temperature, max_tokens)

        base = (self.config.base_url or "http://localhost:11434/v1").replace("/v1", "")
        url = f"{base}/api/chat"

        payload = {
            "model": self.config.model_id,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            "logprobs": True,
        }

        last_err = None
        for attempt in range(MAX_RETRIES):
            try:
                t0 = time.time()
                resp = requests.post(url, json=payload, timeout=self._timeout)
                resp.raise_for_status()
                data = resp.json()
                elapsed = time.time() - t0

                content = data.get("message", {}).get("content", "")
                logprobs = _parse_ollama_logprobs(data)

                prompt_tokens = data.get("prompt_eval_count", 0)
                completion_tokens = data.get("eval_count", 0)

                return LLMResponse(
                    content=content,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    elapsed=round(elapsed, 2),
                    logprobs=logprobs,
                )
            except (requests.ConnectionError, requests.Timeout) as e:
                last_err = e
                wait = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
                logger.warning(
                    "%s logprob attempt %d/%d failed (%s), retrying in %ds",
                    self.config.name, attempt + 1, MAX_RETRIES, e, wait,
                )
                time.sleep(wait)
            except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
                logger.warning(
                    "%s logprob request failed (%s), falling back to standard chat",
                    self.config.name, e,
                )
                result = self.chat(messages, temperature, max_tokens)
                result.logprobs = None
                return result

        logger.warning(
            "%s logprob request failed after %d retries (%s), falling back",
            self.config.name, MAX_RETRIES, last_err,
        )
        result = self.chat(messages, temperature, max_tokens)
        result.logprobs = None
        return result

    def cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Estimate cost in USD (0.0 for local models)."""
        if not self.config.pricing:
            return 0.0
        input_price = self.config.pricing.get("input", 0)
        output_price = self.config.pricing.get("output", 0)
        return (prompt_tokens * input_price + completion_tokens * output_price) / 1_000_000


def _parse_ollama_logprobs(data: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """Parse logprobs from Ollama native API response."""
    msg = data.get("message", {})
    if "logprobs" in msg:
        raw = msg["logprobs"]
        if isinstance(raw, list):
            return _normalize_logprob_list(raw)
        if isinstance(raw, dict) and "content" in raw:
            return _normalize_logprob_list(raw["content"])

    if "logprobs" in data:
        raw = data["logprobs"]
        if isinstance(raw, list):
            return _normalize_logprob_list(raw)
        if isinstance(raw, dict) and "content" in raw:
            return _normalize_logprob_list(raw["content"])

    return None


def _normalize_logprob_list(items: list) -> List[Dict[str, Any]]:
    """Normalize a list of logprob entries into a consistent format."""
    result = []
    for item in items:
        if isinstance(item, dict):
            token = item.get("token", item.get("text", ""))
            logprob = item.get("logprob", item.get("log_prob", None))
            if logprob is not None:
                result.append({
                    "token": token,
                    "logprob": float(logprob),
                    "prob": math.exp(float(logprob)),
                })
    return result
