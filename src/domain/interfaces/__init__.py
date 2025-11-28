"""Domain interfaces - Ports for external dependencies."""

from .fitness_agent import FitnessAgent
from .llm_provider import LLMProvider

__all__ = ["LLMProvider", "FitnessAgent"]
