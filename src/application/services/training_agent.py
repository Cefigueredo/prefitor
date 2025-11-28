"""Training Specialist Agent Service."""

from typing import Any

from src.application.prompts import (
    TRAINING_SPECIALIST_SYSTEM_PROMPT,
    create_training_prompt,
)
from src.domain.interfaces import LLMProvider

from .base_agent import BaseAgentService


class TrainingAgentService(BaseAgentService):
    """Training specialist agent service."""

    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize training agent.

        Args:
            llm_provider: LLM provider instance
        """
        super().__init__(
            llm_provider=llm_provider,
            agent_name="training_specialist",
            system_prompt=TRAINING_SPECIALIST_SYSTEM_PROMPT,
        )

    def _create_prompt(self, context: dict[str, Any]) -> str:
        """Create training specialist prompt from context."""
        user_profile = context.get("user_profile", {})
        return create_training_prompt(user_profile)
