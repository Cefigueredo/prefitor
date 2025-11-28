"""
Custom exceptions for the Fitness AI Advisor application.
This module defines specific exception types for better error handling.
"""


class FitnessAdvisorError(Exception):
    """Base exception for all Fitness Advisor errors."""

    pass


class LLMConfigurationError(FitnessAdvisorError):
    """Raised when there's an issue with LLM configuration."""

    pass


class LLMProviderError(FitnessAdvisorError):
    """Raised when an LLM provider is unavailable or misconfigured."""

    pass


class InvalidModelError(FitnessAdvisorError):
    """Raised when an invalid model is specified for a provider."""

    pass


class InvalidProviderError(FitnessAdvisorError):
    """Raised when an invalid provider is specified."""

    pass


class APIKeyMissingError(FitnessAdvisorError):
    """Raised when a required API key is missing."""

    pass


class AgentExecutionError(FitnessAdvisorError):
    """Raised when an agent fails to execute properly."""

    pass


class UserProfileError(FitnessAdvisorError):
    """Raised when there's an issue with the user profile data."""

    pass
