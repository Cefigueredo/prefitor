"""
Fitness Agent Interface
Defines the contract for fitness specialist agents.
"""

from abc import ABC, abstractmethod
from typing import Any


class FitnessAgent(ABC):
    """
    Abstract interface for fitness specialist agents.

    All specialist agents (Training, Nutrition, Cooking, Supervisor)
    must implement this interface.
    """

    @abstractmethod
    def execute(self, context: dict[str, Any]) -> str:
        """
        Execute the agent's task given a context.

        Args:
            context: Dictionary containing user profile and other agent results

        Returns:
            The agent's advice as a string

        Raises:
            AgentExecutionError: If the agent fails to execute
        """
        pass

    @abstractmethod
    def get_agent_name(self) -> str:
        """
        Get the name of the agent.

        Returns:
            Agent name string
        """
        pass
