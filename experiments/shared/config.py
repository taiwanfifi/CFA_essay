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
        pricing={"input": 0.15, "output": 0.60},
    ),
    "gpt-4o": ModelConfig(
        name="gpt-4o",
        model_id="gpt-4o",
        backend="openai",
        supports_logprobs=False,
        pricing={"input": 2.50, "output": 10.00},
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
