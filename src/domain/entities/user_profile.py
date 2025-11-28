"""
User Profile Entity
Core business entity representing a user's fitness profile.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class UserProfile:
    """
    User fitness profile entity.

    This is a value object representing the user's fitness profile.
    It's immutable and contains validation logic.
    """

    weight: str
    height: str
    body_goal: str
    training_intensity: str | None = None
    time_availability: str | None = None
    equipment_access: str | None = None
    dietary_restrictions: str | None = "None"

    def __post_init__(self) -> None:
        """Validate the user profile after initialization."""
        self._validate()

    def _validate(self) -> None:
        """
        Validate user profile data.

        Raises:
            ValueError: If profile data is invalid
        """
        if not self.weight:
            raise ValueError("Weight is required")
        if not self.height:
            raise ValueError("Height is required")
        if not self.body_goal:
            raise ValueError("Body goal is required")

    def to_dict(self) -> dict:
        """Convert to dictionary for compatibility."""
        return {
            "weight": self.weight,
            "height": self.height,
            "body_goal": self.body_goal,
            "training_intensity": self.training_intensity,
            "time_availability": self.time_availability,
            "equipment_access": self.equipment_access,
            "dietary_restrictions": self.dietary_restrictions,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UserProfile":
        """Create UserProfile from dictionary."""
        return cls(
            weight=data.get("weight", ""),
            height=data.get("height", ""),
            body_goal=data.get("body_goal", ""),
            training_intensity=data.get("training_intensity"),
            time_availability=data.get("time_availability"),
            equipment_access=data.get("equipment_access"),
            dietary_restrictions=data.get("dietary_restrictions", "None"),
        )
