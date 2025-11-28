"""
LLM Provider Interface
Defines the contract for LLM providers (port in hexagonal architecture).
"""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Abstract interface for LLM providers.

    This is a port in hexagonal architecture - it defines what we need
    from an LLM without depending on any specific implementation.
    """

    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """
        Invoke the LLM with a prompt.

        Args:
            prompt: The input prompt

        Returns:
            The LLM's response as a string

        Raises:
            LLMProviderError: If the invocation fails
        """
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """
        Get the name of the current model.

        Returns:
            Model name string
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the name of the provider.

        Returns:
            Provider name string
        """
        pass
