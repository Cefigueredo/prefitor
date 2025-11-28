"""Cooking Specialist Agent Service."""

from typing import Any

from src.application.prompts import (
    COOKING_SPECIALIST_SYSTEM_PROMPT,
    create_cooking_prompt,
)
from src.domain.interfaces import LLMProvider

from .base_agent import BaseAgentService


class CookingAgentService(BaseAgentService):
    """Cooking specialist agent service."""

    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize cooking agent.

        Args:
            llm_provider: LLM provider instance
        """
        super().__init__(
            llm_provider=llm_provider,
            agent_name="cooking_specialist",
            system_prompt=COOKING_SPECIALIST_SYSTEM_PROMPT,
        )

    def _create_prompt(self, context: dict[str, Any]) -> str:
        """Create cooking specialist prompt from context."""
        user_profile = context.get("user_profile", {})
        nutrition_advice = context.get("nutrition_advice", "")
        return create_cooking_prompt(user_profile, nutrition_advice)
