"""
LLM Factory

Creates LLM provider instances based on configuration.
This is the factory pattern for creating LLM providers.
"""

import os

from langchain_anthropic import ChatAnthropic
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI

from src.domain.exceptions import (
    APIKeyMissingError,
    InvalidModelError,
    InvalidProviderError,
    LLMConfigurationError,
)
from src.domain.interfaces import LLMProvider

from .langchain_provider import LangChainLLMProvider


class LLMFactory:
    """
    Factory for creating LLM provider instances.

    This encapsulates the creation logic for different LLM providers.
    """

    # Available providers and models
    PROVIDERS = {
        "ollama": "Ollama (Local)",
        "openai": "OpenAI (Cloud)",
        "anthropic": "Anthropic (Cloud)",
    }

    MODELS = {
        "ollama": [
            "tinyllama:latest",
            "llama3.2:1b",
            "llama3.2:latest",
            "codellama:latest",
            "mistral:latest",
        ],
        "openai": [
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4o",
            "gpt-3.5-turbo",
        ],
        "anthropic": [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3.5-sonnet-20241022",
        ],
    }

    @classmethod
    def create_provider(
        cls,
        provider: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        base_url: str | None = None,
    ) -> LLMProvider:
        """
        Create an LLM provider instance.

        Args:
            provider: Provider name ('ollama', 'openai', 'anthropic')
            model: Model name
            temperature: Temperature for generation
            max_tokens: Maximum tokens for generation
            base_url: Base URL for Ollama (optional)

        Returns:
            LLMProvider instance

        Raises:
            InvalidProviderError: If provider is not supported
            InvalidModelError: If model is not available
            APIKeyMissingError: If API key is missing
            LLMConfigurationError: If configuration fails
        """
        # Validate provider
        if provider not in cls.PROVIDERS:
            raise InvalidProviderError(
                f"Invalid provider: {provider}. "
                f"Available: {list(cls.PROVIDERS.keys())}"
            )

        # Validate model
        if model not in cls.MODELS.get(provider, []):
            available_models = cls.MODELS.get(provider, [])
            raise InvalidModelError(
                f"Invalid model '{model}' for provider '{provider}'. "
                f"Available: {available_models}"
            )

        try:
            if provider == "ollama":
                return cls._create_ollama_provider(
                    model, temperature, base_url
                )
            if provider == "openai":
                return cls._create_openai_provider(
                    model, temperature, max_tokens
                )
            if provider == "anthropic":
                return cls._create_anthropic_provider(
                    model, temperature, max_tokens
                )
            raise InvalidProviderError(f"Unsupported provider: {provider}")

        except (InvalidProviderError, InvalidModelError, APIKeyMissingError):
            raise
        except Exception as e:
            raise LLMConfigurationError(
                f"Error creating LLM provider for {provider}: {str(e)}"
            ) from e

    @classmethod
    def _create_ollama_provider(
        cls, model: str, temperature: float, base_url: str | None
    ) -> LLMProvider:
        """Create Ollama provider."""
        llm = Ollama(
            model=model,
            temperature=temperature,
            base_url=base_url or "http://localhost:11434",
        )
        return LangChainLLMProvider(llm, "ollama", model)

    @classmethod
    def _create_openai_provider(
        cls, model: str, temperature: float, max_tokens: int
    ) -> LLMProvider:
        """Create OpenAI provider."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise APIKeyMissingError(
                "OPENAI_API_KEY environment variable not set"
            )

        llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
            max_tokens=max_tokens,
        )
        return LangChainLLMProvider(llm, "openai", model)

    @classmethod
    def _create_anthropic_provider(
        cls, model: str, temperature: float, max_tokens: int
    ) -> LLMProvider:
        """Create Anthropic provider."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise APIKeyMissingError(
                "ANTHROPIC_API_KEY environment variable not set"
            )

        llm = ChatAnthropic(
            model=model,
            temperature=temperature,
            api_key=api_key,
            max_tokens=max_tokens,
        )
        return LangChainLLMProvider(llm, "anthropic", model)

    @classmethod
    def get_available_models(cls, provider: str | None = None) -> dict:
        """Get available models for a provider or all providers."""
        if provider:
            if provider not in cls.MODELS:
                raise InvalidProviderError(f"Invalid provider: {provider}")
            return {provider: cls.MODELS[provider]}
        return cls.MODELS.copy()
