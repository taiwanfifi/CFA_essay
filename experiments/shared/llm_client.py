"""Unified LLM client for OpenAI, Anthropic, Google Gemini, DeepSeek, and Ollama backends."""

import json
import logging
import math
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_BACKOFF = (10, 30, 60)
# Reasoning models (gpt-5-*, o1, o3) use thinking tokens that count toward
# max_completion_tokens.  A low limit silently produces empty visible output.
_REASONING_MIN_TOKENS = 16384


@dataclass
class LLMResponse:
    """Standardized response from any LLM backend."""

    content: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    elapsed: float = 0.0
    logprobs: Optional[List[Dict[str, Any]]] = None
    model: str = ""


class LLMClient:
    """Unified client wrapping OpenAI, Anthropic, Gemini, DeepSeek, and Ollama APIs."""

    def __init__(self, config: "ModelConfig"):
        from .config import ModelConfig  # Avoid circular import

        self.config = config
        self._timeout = config.timeout
        self._client = None

        # Initialize the appropriate client based on backend
        if config.backend == "openai":
            self._init_openai()
        elif config.backend == "anthropic":
            self._init_anthropic()
        elif config.backend == "gemini":
            self._init_gemini()
        elif config.backend == "deepseek":
            self._init_deepseek()
        elif config.backend == "ollama":
            self._init_ollama()
        else:
            raise ValueError(f"Unknown backend: {config.backend}")

    def _init_openai(self):
        """Initialize OpenAI client."""
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self._client = OpenAI(api_key=api_key, timeout=self._timeout)

    def _init_anthropic(self):
        """Initialize Anthropic client."""
        try:
            import anthropic
        except ImportError:
            raise ImportError("Please install anthropic: pip install anthropic")

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        self._client = anthropic.Anthropic(api_key=api_key)

    def _init_gemini(self):
        """Initialize Google Gemini client."""
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("Please install google-generativeai: pip install google-generativeai")

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")
        genai.configure(api_key=api_key)
        self._client = genai

    def _init_deepseek(self):
        """Initialize DeepSeek client (OpenAI-compatible API)."""
        from openai import OpenAI
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not set")
        self._client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1",
            timeout=self._timeout,
        )

    def _init_ollama(self):
        """Initialize Ollama client (OpenAI-compatible API)."""
        from openai import OpenAI
        base_url = self.config.base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        self._client = OpenAI(
            base_url=base_url,
            api_key="ollama",  # Ollama doesn't need real API key
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
        """Standard chat completion - routes to appropriate backend."""
        if self.config.backend == "anthropic":
            return self._chat_anthropic(messages, temperature, max_tokens)
        elif self.config.backend == "gemini":
            return self._chat_gemini(messages, temperature, max_tokens)
        else:
            # OpenAI, DeepSeek, Ollama all use OpenAI-compatible API
            return self._chat_openai_compatible(messages, temperature, max_tokens)

    def _chat_openai_compatible(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> LLMResponse:
        """Chat using OpenAI-compatible API (OpenAI, DeepSeek, Ollama)."""
        from openai import APITimeoutError, BadRequestError

        last_err = None
        model_id = self.config.model_id
        is_reasoning = any(model_id.startswith(p) for p in ("gpt-5", "o1", "o3"))

        # Reasoning models need much higher token budget for thinking + output.
        effective_max = max(max_tokens, _REASONING_MIN_TOKENS) if is_reasoning else max_tokens

        for attempt in range(MAX_RETRIES):
            try:
                t0 = time.time()
                # Newer OpenAI models (gpt-5-*, o1, o3, etc.) require
                # max_completion_tokens instead of max_tokens.
                token_kwarg = {}
                if is_reasoning:
                    token_kwarg["max_completion_tokens"] = effective_max
                else:
                    token_kwarg["max_tokens"] = effective_max

                # Newer OpenAI reasoning models (gpt-5-*, o1, o3) only
                # support temperature=1 (the default).
                temp_kwarg = {}
                if not is_reasoning:
                    temp_kwarg["temperature"] = temperature

                response = self._client.chat.completions.create(
                    model=model_id,
                    messages=messages,
                    **temp_kwarg,
                    **token_kwarg,
                )
                elapsed = time.time() - t0

                choice = response.choices[0]
                usage = response.usage
                content = choice.message.content or ""

                # Reasoning models may exhaust tokens on thinking, leaving
                # empty visible output.  Retry once with a larger budget.
                if is_reasoning and len(content.strip()) == 0 and effective_max < 32768:
                    effective_max = min(effective_max * 2, 32768)
                    logger.warning(
                        "%s returned empty content (reasoning tokens exhausted), "
                        "retrying with %d max_completion_tokens",
                        self.config.name, effective_max,
                    )
                    continue

                return LLMResponse(
                    content=content,
                    prompt_tokens=usage.prompt_tokens if usage else 0,
                    completion_tokens=usage.completion_tokens if usage else 0,
                    elapsed=round(elapsed, 2),
                    model=self.config.model_id,
                )
            except BadRequestError as e:
                # GPT-5/o1/o3 throw 400 when max_completion_tokens is hit
                if "max_tokens" in str(e) or "model output limit" in str(e):
                    effective_max = min(effective_max * 2, 32768)
                    logger.warning(
                        "%s hit max_tokens limit, retrying with %d tokens",
                        self.config.name, effective_max,
                    )
                    continue
                raise  # re-raise non-token-limit BadRequestErrors
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

    def _chat_anthropic(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> LLMResponse:
        """Chat using Anthropic Claude API."""
        # Extract system message if present
        system_content = ""
        chat_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_content = msg["content"]
            else:
                chat_messages.append(msg)

        last_err = None
        for attempt in range(MAX_RETRIES):
            try:
                t0 = time.time()

                kwargs = {
                    "model": self.config.model_id,
                    "max_tokens": max_tokens,
                    "messages": chat_messages,
                }
                if temperature > 0:
                    kwargs["temperature"] = temperature
                if system_content:
                    kwargs["system"] = system_content

                response = self._client.messages.create(**kwargs)
                elapsed = time.time() - t0

                content = ""
                if response.content:
                    content = response.content[0].text

                return LLMResponse(
                    content=content,
                    prompt_tokens=response.usage.input_tokens if response.usage else 0,
                    completion_tokens=response.usage.output_tokens if response.usage else 0,
                    elapsed=round(elapsed, 2),
                    model=self.config.model_id,
                )
            except Exception as e:
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

    def _chat_gemini(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> LLMResponse:
        """Chat using Google Gemini API."""
        # Convert messages to Gemini format
        system_instruction = ""
        gemini_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            elif msg["role"] == "user":
                gemini_messages.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                gemini_messages.append({"role": "model", "parts": [msg["content"]]})

        last_err = None
        for attempt in range(MAX_RETRIES):
            try:
                t0 = time.time()

                # Create model with optional system instruction
                model_kwargs = {}
                if system_instruction:
                    model_kwargs["system_instruction"] = system_instruction

                model = self._client.GenerativeModel(
                    self.config.model_id,
                    **model_kwargs
                )

                # Configure generation
                generation_config = self._client.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature if temperature > 0 else None,
                )

                # Start chat or generate
                if len(gemini_messages) == 1:
                    response = model.generate_content(
                        gemini_messages[0]["parts"][0],
                        generation_config=generation_config,
                    )
                else:
                    chat = model.start_chat(history=gemini_messages[:-1])
                    response = chat.send_message(
                        gemini_messages[-1]["parts"][0],
                        generation_config=generation_config,
                    )

                elapsed = time.time() - t0

                content = response.text if response.text else ""

                # Token counting (approximate if not available)
                prompt_tokens = 0
                completion_tokens = 0
                if hasattr(response, 'usage_metadata'):
                    prompt_tokens = getattr(response.usage_metadata, 'prompt_token_count', 0)
                    completion_tokens = getattr(response.usage_metadata, 'candidates_token_count', 0)

                return LLMResponse(
                    content=content,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    elapsed=round(elapsed, 2),
                    model=self.config.model_id,
                )
            except Exception as e:
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

        # Only Ollama supports logprobs in our setup
        if self.config.backend != "ollama":
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
                    model=self.config.model_id,
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


# ---------------------------------------------------------------------------
# Convenience functions
# ---------------------------------------------------------------------------

def get_client(model_name: str) -> LLMClient:
    """Get an LLMClient by model name from the registry."""
    from .config import MODEL_REGISTRY

    if model_name not in MODEL_REGISTRY:
        available = ", ".join(sorted(MODEL_REGISTRY.keys()))
        raise ValueError(f"Unknown model: {model_name}. Available: {available}")

    return LLMClient(MODEL_REGISTRY[model_name])


def list_available_models() -> List[str]:
    """List all available model names."""
    from .config import MODEL_REGISTRY
    return sorted(MODEL_REGISTRY.keys())
