"""Shared configuration for all CFA experiments."""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ModelConfig:
    """Configuration for a single model."""

    name: str
    model_id: str
    backend: str  # "openai" or "ollama"
    base_url: Optional[str] = None
    supports_logprobs: bool = False
    pricing: Dict[str, float] = field(default_factory=dict)  # per 1M tokens
    timeout: int = 300  # request timeout in seconds


# ---------------------------------------------------------------------------
# Model registry
# ---------------------------------------------------------------------------

MODEL_REGISTRY: Dict[str, ModelConfig] = {
    "gpt-4o-mini": ModelConfig(
        name="gpt-4o-mini",
        model_id="gpt-4o-mini",
        backend="openai",
        supports_logprobs=False,
        pricing={"input": 0.15, "cached_input": 0.075, "output": 0.60},
    ),
    "gpt-4o": ModelConfig(
        name="gpt-4o",
        model_id="gpt-4o",
        backend="openai",
        supports_logprobs=False,
        pricing={"input": 2.50, "cached_input": 1.25, "output": 10.00},
    ),
    "gpt-4.1": ModelConfig(
        name="gpt-4.1",
        model_id="gpt-4.1",
        backend="openai",
        supports_logprobs=False,
        pricing={"input": 2.00, "cached_input": 0.50, "output": 8.00},
    ),
    "gpt-4.1-mini": ModelConfig(
        name="gpt-4.1-mini",
        model_id="gpt-4.1-mini",
        backend="openai",
        supports_logprobs=False,
        pricing={"input": 0.40, "cached_input": 0.10, "output": 1.60},
    ),
    "gpt-4.1-nano": ModelConfig(
        name="gpt-4.1-nano",
        model_id="gpt-4.1-nano",
        backend="openai",
        supports_logprobs=False,
        pricing={"input": 0.10, "cached_input": 0.025, "output": 0.40},
    ),
    "gpt-5-mini": ModelConfig(
        name="gpt-5-mini",
        model_id="gpt-5-mini",
        backend="openai",
        supports_logprobs=False,
        pricing={"input": 0.25, "cached_input": 0.025, "output": 2.00},
    ),
    "qwen3:32b": ModelConfig(
        name="qwen3:32b",
        model_id="qwen3:32b",
        backend="ollama",
        base_url="http://localhost:11434/v1",
        supports_logprobs=True,
        pricing={},
        timeout=600,
    ),
    "llama3.1:8b": ModelConfig(
        name="llama3.1:8b",
        model_id="llama3.1:8b",
        backend="ollama",
        base_url="http://localhost:11434/v1",
        supports_logprobs=True,
        pricing={},
    ),
    "deepseek-r1:14b": ModelConfig(
        name="deepseek-r1:14b",
        model_id="deepseek-r1:14b",
        backend="ollama",
        base_url="http://localhost:11434/v1",
        supports_logprobs=True,
        pricing={},
    ),
}

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_ANSWERS = {"A", "B", "C"}
DEFAULT_TEMPERATURE = 0.0
