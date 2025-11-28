"""
LangChain LLM Provider Implementation

This is an adapter that implements the LLMProvider interface
using LangChain as the underlying implementation.
"""

from langchain_core.language_models import BaseLanguageModel

from src.domain.exceptions import LLMProviderError
from src.domain.interfaces import LLMProvider


class LangChainLLMProvider(LLMProvider):
    """
    LangChain adapter implementing the LLMProvider interface.

    This allows us to use any LangChain LLM while keeping our
    domain layer independent of LangChain.
    """

    def __init__(
        self, llm: BaseLanguageModel, provider_name: str, model_name: str
    ):
        """
        Initialize LangChain provider adapter.

        Args:
            llm: LangChain LLM instance
            provider_name: Name of the provider (e.g., "ollama", "openai")
            model_name: Name of the model
        """
        self._llm = llm
        self._provider_name = provider_name
        self._model_name = model_name

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
        try:
            # LangChain expects messages for chat models
            if hasattr(self._llm, "invoke"):
                response = self._llm.invoke(prompt)

                # Handle different response types
                if hasattr(response, "content"):
                    return response.content
                if isinstance(response, str):
                    return response
                return str(response)
            raise LLMProviderError("LLM does not support invoke method")

        except Exception as e:
            raise LLMProviderError(f"Error invoking LLM: {str(e)}") from e

    def get_model_name(self) -> str:
        """Get the name of the current model."""
        return self._model_name

    def get_provider_name(self) -> str:
        """Get the name of the provider."""
        return self._provider_name
