"""Nutrition Specialist Agent Service."""

from typing import Any

from src.application.prompts import (
    NUTRITION_SPECIALIST_SYSTEM_PROMPT,
    create_nutrition_prompt,
)
from src.domain.interfaces import LLMProvider

from .base_agent import BaseAgentService


class NutritionAgentService(BaseAgentService):
    """Nutrition specialist agent service."""

    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize nutrition agent.

        Args:
            llm_provider: LLM provider instance
        """
        super().__init__(
            llm_provider=llm_provider,
            agent_name="nutrition_specialist",
            system_prompt=NUTRITION_SPECIALIST_SYSTEM_PROMPT,
        )

    def _create_prompt(self, context: dict[str, Any]) -> str:
        """Create nutrition specialist prompt from context."""
        user_profile = context.get("user_profile", {})
        training_advice = context.get("training_advice", "")
        return create_nutrition_prompt(user_profile, training_advice)
