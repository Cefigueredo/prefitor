"""
Fitness Advice Entity
Core business entity representing comprehensive fitness advice.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entities.user_profile import UserProfile


@dataclass(frozen=True)
class FitnessAdvice:
    """
    Comprehensive fitness advice entity.

    Contains all specialist recommendations and final integrated plan.
    """

    training_advice: str
    nutrition_advice: str
    cooking_advice: str
    final_recommendations: str
    user_profile: UserProfile | None = None

    def __post_init__(self) -> None:
        """Validate the fitness advice after initialization."""
        self._validate()

    def _validate(self) -> None:
        """
        Validate fitness advice data.

        Raises:
            ValueError: If advice data is invalid or incomplete
        """
        if not self.training_advice:
            raise ValueError("Training advice is required")
        if not self.nutrition_advice:
            raise ValueError("Nutrition advice is required")
        if not self.cooking_advice:
            raise ValueError("Cooking advice is required")
        if not self.final_recommendations:
            raise ValueError("Final recommendations are required")

    def to_dict(self) -> dict:
        """Convert to dictionary for compatibility."""
        result = {
            "training_advice": self.training_advice,
            "nutrition_advice": self.nutrition_advice,
            "cooking_advice": self.cooking_advice,
            "final_recommendations": self.final_recommendations,
        }

        if self.user_profile:
            result["user_profile"] = self.user_profile.to_dict()

        return result

    @classmethod
    def from_dict(cls, data: dict) -> FitnessAdvice:
        """Create FitnessAdvice from dictionary."""
        from .user_profile import UserProfile

        user_profile = None
        if "user_profile" in data:
            user_profile = UserProfile.from_dict(data["user_profile"])

        return cls(
            training_advice=data.get("training_advice", ""),
            nutrition_advice=data.get("nutrition_advice", ""),
            cooking_advice=data.get("cooking_advice", ""),
            final_recommendations=data.get("final_recommendations", ""),
            user_profile=user_profile,
        )
