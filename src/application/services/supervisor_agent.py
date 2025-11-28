"""Supervisor Agent Service."""

from typing import Any

from src.application.prompts import (
    SUPERVISOR_SYSTEM_PROMPT,
    create_supervisor_prompt,
)
from src.domain.interfaces import LLMProvider

from .base_agent import BaseAgentService


class SupervisorAgentService(BaseAgentService):
    """Supervisor agent service that integrates all specialist advice."""

    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize supervisor agent.

        Args:
            llm_provider: LLM provider instance
        """
        super().__init__(
            llm_provider=llm_provider,
            agent_name="supervisor",
            system_prompt=SUPERVISOR_SYSTEM_PROMPT,
        )

    def _create_prompt(self, context: dict[str, Any]) -> str:
        """Create supervisor prompt from context."""
        user_profile = context.get("user_profile", {})
        training_advice = context.get("training_advice", "")
        nutrition_advice = context.get("nutrition_advice", "")
        cooking_advice = context.get("cooking_advice", "")

        return create_supervisor_prompt(
            user_profile, training_advice, nutrition_advice, cooking_advice
        )
