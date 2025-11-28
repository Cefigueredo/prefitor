"""
Get Fitness Advice Use Case

This use case orchestrates the multi-agent workflow to generate
comprehensive fitness advice for a user.
"""

import logging
from typing import Any

from src.domain.entities import FitnessAdvice, UserProfile
from src.domain.exceptions import AgentExecutionError, UserProfileError
from src.domain.interfaces import FitnessAgent

logger = logging.getLogger(__name__)


class GetFitnessAdviceUseCase:
    """
    Use case for getting comprehensive fitness advice.

    This orchestrates the workflow of multiple specialist agents
    to generate personalized fitness recommendations.
    """

    def __init__(
        self,
        training_agent: FitnessAgent,
        nutrition_agent: FitnessAgent,
        cooking_agent: FitnessAgent,
        supervisor_agent: FitnessAgent,
    ):
        """
        Initialize the use case with specialist agents.

        Args:
            training_agent: Training specialist agent
            nutrition_agent: Nutrition specialist agent
            cooking_agent: Cooking specialist agent
            supervisor_agent: Supervisor agent for integration
        """
        self.training_agent = training_agent
        self.nutrition_agent = nutrition_agent
        self.cooking_agent = cooking_agent
        self.supervisor_agent = supervisor_agent

    def execute(self, user_profile_data: dict[str, Any]) -> FitnessAdvice:
        """
        Execute the use case to get comprehensive fitness advice.

        Args:
            user_profile_data: User's fitness profile data

        Returns:
            FitnessAdvice entity with all recommendations

        Raises:
            UserProfileError: If user profile is invalid
            AgentExecutionError: If any agent fails
        """
        logger.info("Starting Get Fitness Advice use case")

        try:
            # Create and validate user profile
            user_profile = UserProfile.from_dict(user_profile_data)
            logger.info(
                f"User profile created for goal: {user_profile.body_goal}"
            )

            # Execute agents in sequence
            context = {"user_profile": user_profile.to_dict()}

            # Step 1: Training advice
            logger.info("Executing training specialist...")
            training_advice = self.training_agent.execute(context)
            context["training_advice"] = training_advice

            # Step 2: Nutrition advice
            logger.info("Executing nutrition specialist...")
            nutrition_advice = self.nutrition_agent.execute(context)
            context["nutrition_advice"] = nutrition_advice

            # Step 3: Cooking advice
            logger.info("Executing cooking specialist...")
            cooking_advice = self.cooking_agent.execute(context)
            context["cooking_advice"] = cooking_advice

            # Step 4: Supervisor integration
            logger.info("Executing supervisor for final integration...")
            final_recommendations = self.supervisor_agent.execute(context)

            # Create fitness advice entity
            fitness_advice = FitnessAdvice(
                training_advice=training_advice,
                nutrition_advice=nutrition_advice,
                cooking_advice=cooking_advice,
                final_recommendations=final_recommendations,
                user_profile=user_profile,
            )

            logger.info("Use case completed successfully")
            return fitness_advice

        except (UserProfileError, AgentExecutionError):
            raise
        except Exception as e:
            error_msg = (
                f"Unexpected error in Get Fitness Advice use case: {str(e)}"
            )
            logger.error(error_msg)
            raise AgentExecutionError(error_msg) from e
