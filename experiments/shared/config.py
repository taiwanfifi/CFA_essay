"""Shared configuration for all CFA experiments.

Supports 5 backends: OpenAI, Anthropic, Google Gemini, DeepSeek, Ollama.

Required environment variables (set in .env or models/.env):
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- GEMINI_API_KEY
- DEEPSEEK_API_KEY
- OLLAMA_BASE_URL (optional, defaults to http://localhost:11434)
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ModelConfig:
    """Configuration for a single model."""

    name: str
    model_id: str
    backend: str  # "openai", "anthropic", "gemini", "deepseek", "ollama"
    base_url: Optional[str] = None
    supports_logprobs: bool = False
    pricing: Dict[str, float] = field(default_factory=dict)  # per 1M tokens
    timeout: int = 300  # request timeout in seconds


# ---------------------------------------------------------------------------
# Model registry - All available models
# ---------------------------------------------------------------------------

MODEL_REGISTRY: Dict[str, ModelConfig] = {
    # =========================================================================
    # OpenAI Models
    # =========================================================================
    "gpt-4o": ModelConfig(
        name="gpt-4o",
        model_id="gpt-4o",
        backend="openai",
        supports_logprobs=False,
        pricing={"input": 2.50, "cached_input": 1.25, "output": 10.00},
    ),
    "gpt-4o-mini": ModelConfig(
        name="gpt-4o-mini",
        model_id="gpt-4o-mini",
        backend="openai",
        supports_logprobs=False,
        pricing={"input": 0.15, "cached_input": 0.075, "output": 0.60},
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

    # =========================================================================
    # Anthropic Claude Models
    # =========================================================================
    "claude-opus-4.5": ModelConfig(
        name="claude-opus-4.5",
        model_id="claude-opus-4-5-20251101",
        backend="anthropic",
        supports_logprobs=False,
        pricing={"input": 5.00, "cached_input": 0.50, "output": 25.00},
        timeout=600,  # Opus can be slow
    ),
    "claude-sonnet-4.5": ModelConfig(
        name="claude-sonnet-4.5",
        model_id="claude-sonnet-4-5-20250929",
        backend="anthropic",
        supports_logprobs=False,
        pricing={"input": 3.00, "cached_input": 0.30, "output": 15.00},
    ),
    "claude-haiku-4.5": ModelConfig(
        name="claude-haiku-4.5",
        model_id="claude-haiku-4-5-20251001",
        backend="anthropic",
        supports_logprobs=False,
        pricing={"input": 0.25, "cached_input": 0.025, "output": 1.25},
    ),

    # =========================================================================
    # Google Gemini Models
    # =========================================================================
    "gemini-2.5-pro": ModelConfig(
        name="gemini-2.5-pro",
        model_id="gemini-2.5-pro-preview-05-06",
        backend="gemini",
        supports_logprobs=False,
        pricing={"input": 1.25, "output": 10.00},
    ),
    "gemini-2.5-flash": ModelConfig(
        name="gemini-2.5-flash",
        model_id="gemini-2.5-flash-preview-05-20",
        backend="gemini",
        supports_logprobs=False,
        pricing={"input": 0.15, "output": 0.60},
    ),
    "gemini-2.0-flash": ModelConfig(
        name="gemini-2.0-flash",
        model_id="gemini-2.0-flash",
        backend="gemini",
        supports_logprobs=False,
        pricing={"input": 0.10, "output": 0.40},
    ),
    "gemini-3-pro": ModelConfig(
        name="gemini-3-pro",
        model_id="gemini-3-pro-preview",
        backend="gemini",
        supports_logprobs=False,
        pricing={"input": 1.25, "output": 10.00},  # Estimated
    ),

    # =========================================================================
    # DeepSeek Cloud API
    # =========================================================================
    "deepseek-chat": ModelConfig(
        name="deepseek-chat",
        model_id="deepseek-chat",
        backend="deepseek",
        supports_logprobs=False,
        pricing={"input": 0.14, "output": 0.28},  # Very cheap
    ),
    "deepseek-reasoner": ModelConfig(
        name="deepseek-reasoner",
        model_id="deepseek-reasoner",
        backend="deepseek",
        supports_logprobs=False,
        pricing={"input": 0.55, "output": 2.19},
        timeout=600,
    ),

    # =========================================================================
    # Local Models (Ollama)
    # =========================================================================
    "qwen3:32b": ModelConfig(
        name="qwen3:32b",
        model_id="qwen3:32b",
        backend="ollama",
        base_url="http://localhost:11434/v1",
        supports_logprobs=True,
        pricing={},  # Free (local)
        timeout=600,
    ),
    "qwen3:4b": ModelConfig(
        name="qwen3:4b",
        model_id="qwen3:4b",
        backend="ollama",
        base_url="http://localhost:11434/v1",
        supports_logprobs=True,
        pricing={},
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
        timeout=600,
    ),
    "phi3.5:3.8b": ModelConfig(
        name="phi3.5:3.8b",
        model_id="phi3.5:3.8b-mini-instruct-q4_K_M",
        backend="ollama",
        base_url="http://localhost:11434/v1",
        supports_logprobs=True,
        pricing={},
    ),
    "gemma3": ModelConfig(
        name="gemma3",
        model_id="gemma3:latest",
        backend="ollama",
        base_url="http://localhost:11434/v1",
        supports_logprobs=True,
        pricing={},
    ),
}


# ---------------------------------------------------------------------------
# Model Groups (for batch experiments)
# ---------------------------------------------------------------------------

MODEL_GROUPS = {
    # Cross-validation: Different training data sources
    "cross_cloud": ["gpt-4o", "claude-sonnet-4.5", "gemini-2.5-pro"],
    "cross_cloud_fast": ["gpt-4o-mini", "claude-haiku-4.5", "gemini-2.5-flash"],
    "cross_local": ["deepseek-r1:14b", "qwen3:32b", "llama3.1:8b"],

    # By provider
    "openai": ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano"],
    "anthropic": ["claude-opus-4.5", "claude-sonnet-4.5", "claude-haiku-4.5"],
    "gemini": ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash"],
    "deepseek": ["deepseek-chat", "deepseek-reasoner"],
    "ollama": ["qwen3:32b", "qwen3:4b", "llama3.1:8b", "deepseek-r1:14b", "phi3.5:3.8b", "gemma3"],

    # By cost tier
    "cheap": ["gpt-4o-mini", "gpt-4.1-nano", "claude-haiku-4.5", "gemini-2.0-flash", "deepseek-chat"],
    "mid": ["gpt-4o", "gpt-4.1", "claude-sonnet-4.5", "gemini-2.5-pro"],
    "premium": ["claude-opus-4.5", "deepseek-reasoner"],
    "free": ["qwen3:32b", "qwen3:4b", "llama3.1:8b", "deepseek-r1:14b", "phi3.5:3.8b", "gemma3"],

    # Recommended for CFA experiments
    "cfa_main": ["gpt-4o-mini", "claude-sonnet-4.5", "gemini-2.5-flash"],
    "cfa_judge": ["gpt-4o", "claude-sonnet-4.5"],  # For LLM-as-Judge
}


# ---------------------------------------------------------------------------
# Default settings
# ---------------------------------------------------------------------------

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_JUDGE_MODEL = "gpt-4o-mini"  # For LLM-as-Judge evaluations
VALID_ANSWERS = {"A", "B", "C"}
DEFAULT_TEMPERATURE = 0.0


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_models_by_backend(backend: str) -> list:
    """Get all model names for a specific backend."""
    return [name for name, config in MODEL_REGISTRY.items() if config.backend == backend]


def get_models_by_group(group: str) -> list:
    """Get all model names in a group."""
    if group not in MODEL_GROUPS:
        raise ValueError(f"Unknown group: {group}. Available: {list(MODEL_GROUPS.keys())}")
    return MODEL_GROUPS[group]


def estimate_cost(model_name: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Estimate cost in USD for a given model and token count."""
    if model_name not in MODEL_REGISTRY:
        return 0.0
    config = MODEL_REGISTRY[model_name]
    if not config.pricing:
        return 0.0
    input_price = config.pricing.get("input", 0)
    output_price = config.pricing.get("output", 0)
    return (prompt_tokens * input_price + completion_tokens * output_price) / 1_000_000
