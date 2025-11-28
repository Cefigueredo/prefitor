"""
Base Agent Service
Base implementation for all specialist agent services.
"""

import logging
from typing import Any

from src.domain.exceptions import AgentExecutionError
from src.domain.interfaces import FitnessAgent, LLMProvider

logger = logging.getLogger(__name__)


class BaseAgentService(FitnessAgent):
    """
    Base agent service implementing common functionality.

    All specialist agents inherit from this base class.
    """

    def __init__(
        self, llm_provider: LLMProvider, agent_name: str, system_prompt: str
    ):
        """
        Initialize base agent service.

        Args:
            llm_provider: LLM provider instance (injected dependency)
            agent_name: Name identifier for the agent
            system_prompt: System prompt defining agent's role
        """
        self.llm_provider = llm_provider
        self.agent_name = agent_name
        self.system_prompt = system_prompt

    def execute(self, context: dict[str, Any]) -> str:
        """
        Execute the agent's task.

        Args:
            context: Dictionary containing user profile and other context

        Returns:
            Agent's advice as a string

        Raises:
            AgentExecutionError: If execution fails
        """
        try:
            # Create the full prompt
            user_prompt = self._create_prompt(context)
            full_prompt = f"{self.system_prompt}\n\n{user_prompt}"

            # Invoke LLM
            response = self.llm_provider.invoke(full_prompt)

            logger.info(f"{self.agent_name} completed successfully")
            return response

        except Exception as e:
            error_msg = f"Error in {self.agent_name}: {str(e)}"
            logger.error(error_msg)
            raise AgentExecutionError(error_msg) from e

    def get_agent_name(self) -> str:
        """Get the name of the agent."""
        return self.agent_name

    def _create_prompt(self, context: dict[str, Any]) -> str:
        """
        Create the user prompt from context.

        This method should be overridden by subclasses.

        Args:
            context: Context dictionary

        Returns:
            Formatted prompt string
        """
        raise NotImplementedError("Subclasses must implement _create_prompt")
