"""
UI components and styling for the Fitness AI Advisor Streamlit application.
This module contains all UI-related functions and CSS styling.
"""

import streamlit as st

from src.infrastructure.config.constants import STATUS_ICONS

# Custom CSS for the application
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .agent-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
    }
    .supervisor-card {
        background-color: #e3f2fd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1976d2;
        margin-bottom: 1rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
    .progress-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .status-card {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .status-card.success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .status-card.warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    .status-card.error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .config-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    .ready-indicator {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
"""


def apply_custom_styling() -> None:
    """Apply custom CSS styling to the Streamlit application."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def display_status_card(status: dict[str, str]) -> None:
    """
    Display a status card with appropriate styling based on status type.

    Args:
        status: Dictionary containing 'status' and 'message' keys
    """
    status_class = status.get("status", "error")
    message = status.get("message", "Unknown status")

    st.markdown(
        f"""
    <div class="status-card {status_class}">
        <strong>Status:</strong> {message}
    </div>
    """,
        unsafe_allow_html=True,
    )


def display_llm_status_card(status: dict[str, str]) -> None:
    """
    Display LLM status card with appropriate styling.

    Args:
        status: Dictionary containing 'status' and 'message' keys
    """
    status_class = status.get("status", "error")
    message = status.get("message", "Unknown status")

    st.markdown(
        f"""
    <div class="status-card {status_class}">
        <strong>LLM Status:</strong> {message}
    </div>
    """,
        unsafe_allow_html=True,
    )


def display_agent_progress(agent_name: str, status: str = "pending") -> None:
    """
    Display agent progress with status indicators.

    Args:
        agent_name: Name of the agent
        status: Current status ('pending', 'running', 'completed', 'error')
    """
    icon = STATUS_ICONS.get(status, STATUS_ICONS["pending"])

    st.markdown(
        f"""
    <div class="agent-card">
        <h4>{icon} {agent_name}</h4>
        <p>Status: {status.title()}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def display_ready_indicator(message: str = None) -> None:
    """
    Display a ready indicator when processing is complete.

    Args:
        message: Optional custom message to display
    """
    default_message = """
    Your comprehensive fitness plan has been generated successfully.
    Check the Results tab to view your personalized recommendations!
    """

    display_message = message or default_message

    st.markdown(
        f"""
    <div class="ready-indicator">
        <h4>✅ Ready!</h4>
        <p>{display_message}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def display_setup_instructions() -> None:
    """Display setup instructions for different LLM providers."""
    st.markdown("""
    ### 🔧 Setup Instructions

    **For Ollama:**
    1. Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
    2. Start Ollama: `ollama serve`
    3. Pull a model: `ollama pull tinyllama:latest`

    **For OpenAI:**
    1. Set environment variable: `export OPENAI_API_KEY='your-key'`

    **For Anthropic:**
    1. Set environment variable: `export ANTHROPIC_API_KEY='your-key'`

    **Change Model:**
    Use the sidebar to select different models and providers.
    """)


def create_dropdown_options(
    min_val: int, max_val: int, step: int, unit: str
) -> list[str]:
    """
    Create a list of dropdown options for numeric ranges.

    Args:
        min_val: Minimum value
        max_val: Maximum value
        step: Step size
        unit: Unit string (e.g., 'kg', 'cm')

    Returns:
        List of formatted option strings
    """
    return [f"{i} {unit}" for i in range(min_val, max_val + 1, step)]


def format_recommendations_for_download(results: dict[str, str]) -> str:
    """
    Format all recommendations into a single markdown document for download.

    Args:
        results: Dictionary containing all specialist recommendations

    Returns:
        Formatted markdown string
    """
    return f"""
# Comprehensive Fitness Plan

## Final Integrated Plan
{results.get("final_recommendations", "")}

## Training Specialist Recommendations
{results.get("training_advice", "")}

## Nutrition Specialist Recommendations
{results.get("nutrition_advice", "")}

## Cooking Specialist Recommendations
{results.get("cooking_advice", "")}
"""


def display_main_header(text: str) -> None:
    """
    Display the main application header.

    Args:
        text: Header text to display
    """
    st.markdown(f'<h1 class="main-header">{text}</h1>', unsafe_allow_html=True)


def display_results_section(results: dict[str, str]) -> None:
    """
    Display all fitness plan results with expandable sections.

    Args:
        results: Dictionary containing all specialist recommendations
    """
    # Display final recommendations
    st.markdown("### 🎯 Final Integrated Plan")
    st.markdown(
        results.get("final_recommendations", "No recommendations available")
    )

    # Display individual specialist recommendations
    with st.expander("🏋️ Training Specialist Recommendations"):
        st.markdown(
            results.get("training_advice", "No training advice available")
        )

    with st.expander("🍎 Nutrition Specialist Recommendations"):
        st.markdown(
            results.get("nutrition_advice", "No nutrition advice available")
        )

    with st.expander("👨‍🍳 Cooking Specialist Recommendations"):
        st.markdown(
            results.get("cooking_advice", "No cooking advice available")
        )
