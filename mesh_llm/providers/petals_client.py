"""
petals_client - STUB

Status: Scaffold. Active per Mesh-LLM phased rollout.

Implements the Provider interface for petals.
"""

import logging
logger = logging.getLogger(__name__)


def deploy_inference_endpoint(model_name: str, vram_gb: int) -> str:
    """Deploy LLM inference endpoint on petals."""
    raise NotImplementedError("petals client activates in Mesh-LLM Phase 1.")


def query(endpoint: str, prompt: str, max_tokens: int = 2048) -> str:
    """Query a deployed endpoint."""
    raise NotImplementedError("petals query activates in Phase 1.")


def estimate_cost_per_million_tokens() -> float:
    """Cost in USDC per million tokens."""
    return 0.0
