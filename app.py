"""
Fitness AI Advisor - Main Entry Point

This is the main entry point for the Streamlit application.
It follows Clean Architecture principles with proper dependency injection.
"""

import logging

import streamlit as st

from src.application.services import (
    CookingAgentService,
    NutritionAgentService,
    SupervisorAgentService,
    TrainingAgentService,
)
from src.application.use_cases import GetFitnessAdviceUseCase
from src.domain.entities import FitnessAdvice
from src.domain.exceptions import (
    AgentExecutionError,
    FitnessAdvisorError,
    UserProfileError,
)
from src.infrastructure.config.constants import (
    APP_LAYOUT,
    BODY_GOAL_OPTIONS,
    DIETARY_RESTRICTIONS_OPTIONS,
    EQUIPMENT_ACCESS_OPTIONS,
    HEIGHT_DEFAULT_INDEX,
    HEIGHT_MAX_CM,
    HEIGHT_MIN_CM,
    HEIGHT_STEP_CM,
    LLM_PRESET_OPTIONS,
    MAIN_HEADER_TEXT,
    PAGE_ICON,
    PAGE_TITLE,
    SESSION_AGENT_RESULTS,
    SESSION_AGENTS_COMPLETED,
    SESSION_RUN_AGENTS,
    SESSION_USER_DATA,
    TEMPERATURE_DEFAULT,
    TEMPERATURE_MAX,
    TEMPERATURE_MIN,
    TEMPERATURE_STEP,
    TIME_AVAILABILITY_OPTIONS,
    TRAINING_INTENSITY_OPTIONS,
    WEIGHT_DEFAULT_INDEX,
    WEIGHT_MAX_KG,
    WEIGHT_MIN_KG,
    WEIGHT_STEP_KG,
)
from src.infrastructure.llm import LLMFactory
from src.presentation.ui.ui_components import (
    apply_custom_styling,
    create_dropdown_options,
    display_llm_status_card,
    display_main_header,
    display_ready_indicator,
    display_results_section,
    display_setup_instructions,
    format_recommendations_for_download,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Global LLM provider instance (can be replaced with dependency injection
# container)
_llm_provider = None
_current_config = {
    "provider": "ollama",
    "model": "tinyllama:latest",
    "temperature": 0.7,
}


def get_llm_provider():
    """Get or create LLM provider instance."""
    global _llm_provider
    if _llm_provider is None:
        try:
            _llm_provider = LLMFactory.create_provider(
                provider=_current_config["provider"],
                model=_current_config["model"],
                temperature=_current_config["temperature"],
            )
        except Exception as e:
            st.error(f"Error creating LLM provider: {e}")
            return None
    return _llm_provider


def update_llm_configuration(
    provider: str, model: str, temperature: float
) -> None:
    """Update LLM configuration."""
    global _llm_provider, _current_config
    _current_config = {
        "provider": provider,
        "model": model,
        "temperature": temperature,
    }
    _llm_provider = None  # Reset provider to force recreation


def check_llm_status() -> dict[str, str]:
    """Check LLM provider status."""
    try:
        provider = get_llm_provider()
        if provider:
            return {
                "status": "success",
                "message": f"✅ {provider.get_provider_name()} with "
                f"{provider.get_model_name()} is ready",
            }
        else:
            return {
                "status": "error",
                "message": "❌ LLM provider not initialized",
            }
    except Exception as e:
        return {"status": "error", "message": f"❌ Error: {str(e)}"}


def configure_page() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=APP_LAYOUT
    )


def render_sidebar_configuration() -> None:
    """Render the LLM configuration sidebar."""
    with st.sidebar:
        st.markdown("### 🤖 LLM Configuration")

        # Presets
        st.markdown("#### Quick Presets")
        preset = st.selectbox(
            "Choose a preset configuration:", LLM_PRESET_OPTIONS
        )

        if preset != "Custom":
            preset_configs = {
                "TinyLlama": ("ollama", "tinyllama:latest", 0.7),
                "Llama3.2": ("ollama", "llama3.2:1b", 0.7),
                "GPT-4": ("openai", "gpt-4", 0.7),
                "Claude": ("anthropic", "claude-3-sonnet-20240229", 0.7),
            }
            if preset in preset_configs:
                provider, model, temp = preset_configs[preset]
                update_llm_configuration(provider, model, temp)

        # Custom configuration
        st.markdown("#### Custom Configuration")

        provider = st.selectbox("Provider:", ["ollama", "openai", "anthropic"])

        available_models = LLMFactory.get_available_models(provider)
        model = st.selectbox("Model:", available_models.get(provider, []))

        temperature = st.slider(
            "Temperature:",
            min_value=TEMPERATURE_MIN,
            max_value=TEMPERATURE_MAX,
            value=TEMPERATURE_DEFAULT,
            step=TEMPERATURE_STEP,
        )

        if st.button("Apply Configuration"):
            update_llm_configuration(provider, model, temperature)
            st.success("Configuration updated!")

        # Show current status
        st.markdown("#### Current Configuration")
        status = check_llm_status()
        display_llm_status_card(status)


def collect_user_profile() -> dict[str, str]:
    """Collect user profile information from input controls."""
    col1, col2 = st.columns([1, 1])

    with col1:
        weight = st.selectbox(
            "Weight",
            create_dropdown_options(
                WEIGHT_MIN_KG, WEIGHT_MAX_KG, WEIGHT_STEP_KG, "kg"
            ),
            index=WEIGHT_DEFAULT_INDEX,
        )
        training_intensity = st.selectbox(
            "Training Intensity", TRAINING_INTENSITY_OPTIONS, index=1
        )

    with col2:
        height = st.selectbox(
            "Height",
            create_dropdown_options(
                HEIGHT_MIN_CM, HEIGHT_MAX_CM, HEIGHT_STEP_CM, "cm"
            ),
            index=HEIGHT_DEFAULT_INDEX,
        )
        body_goal = st.selectbox("Body Goal", BODY_GOAL_OPTIONS, index=0)

    st.markdown("### 🎯 Additional Preferences")
    col3, col4, col5 = st.columns(3)

    with col3:
        time_availability = st.selectbox(
            "Time Availability", TIME_AVAILABILITY_OPTIONS
        )

    with col4:
        equipment_access = st.selectbox(
            "Equipment Access", EQUIPMENT_ACCESS_OPTIONS
        )

    with col5:
        dietary_restrictions = st.selectbox(
            "Dietary Restrictions", DIETARY_RESTRICTIONS_OPTIONS
        )

    return {
        "weight": weight,
        "training_intensity": training_intensity,
        "height": height,
        "body_goal": body_goal,
        "time_availability": time_availability,
        "equipment_access": equipment_access,
        "dietary_restrictions": dietary_restrictions,
    }


def execute_use_case(
    user_profile_data: dict[str, str],
) -> FitnessAdvice | None:
    """Execute the Get Fitness Advice use case."""
    try:
        # Get LLM provider
        llm_provider = get_llm_provider()
        if not llm_provider:
            st.error("LLM provider not available")
            return None

        # Create agent services (dependency injection)
        training_agent = TrainingAgentService(llm_provider)
        nutrition_agent = NutritionAgentService(llm_provider)
        cooking_agent = CookingAgentService(llm_provider)
        supervisor_agent = SupervisorAgentService(llm_provider)

        # Create use case
        use_case = GetFitnessAdviceUseCase(
            training_agent=training_agent,
            nutrition_agent=nutrition_agent,
            cooking_agent=cooking_agent,
            supervisor_agent=supervisor_agent,
        )

        # Execute use case
        fitness_advice = use_case.execute(user_profile_data)
        return fitness_advice

    except UserProfileError as e:
        st.error(f"Invalid profile: {e}")
        return None
    except AgentExecutionError as e:
        st.error(f"Agent execution error: {e}")
        return None
    except FitnessAdvisorError as e:
        st.error(f"Error: {e}")
        return None


def render_profile_input_tab() -> None:
    """Render the profile input tab content."""
    st.markdown("### 📊 Your Fitness Profile")

    user_data = collect_user_profile()

    if st.button(
        "🚀 Generate Comprehensive Fitness Plan", use_container_width=True
    ):
        st.session_state[SESSION_USER_DATA] = user_data
        st.session_state[SESSION_RUN_AGENTS] = True

    if st.session_state.get(SESSION_RUN_AGENTS, False):
        st.markdown("### 🔄 Agent Execution Progress")

        with st.spinner("🤖 Multi-agent system is analyzing your profile..."):
            result = execute_use_case(st.session_state[SESSION_USER_DATA])

            if result:
                st.session_state[SESSION_AGENT_RESULTS] = result.to_dict()
                st.session_state[SESSION_AGENTS_COMPLETED] = True
                st.success(
                    "🎉 Comprehensive fitness plan generated successfully!"
                )
                display_ready_indicator()
            else:
                st.session_state[SESSION_AGENTS_COMPLETED] = False

        st.session_state[SESSION_RUN_AGENTS] = False

    elif st.session_state.get(SESSION_AGENTS_COMPLETED, False):
        display_ready_indicator()


def render_results_tab() -> None:
    """Render the results tab content."""
    st.markdown("### 📋 Comprehensive Fitness Plan")

    if not st.session_state.get(SESSION_AGENTS_COMPLETED, False):
        st.info(
            "👆 Please go to the Profile Input tab and generate your fitness "
            "plan first."
        )
        return

    if not st.session_state.get(SESSION_AGENT_RESULTS):
        st.warning(
            "No results available. Please generate a fitness plan first."
        )
        return

    results = st.session_state[SESSION_AGENT_RESULTS]
    display_results_section(results)

    # Download options
    st.markdown("### 📥 Download Options")
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📥 Download Final Plan",
            data=results.get("final_recommendations", ""),
            file_name="comprehensive_fitness_plan.md",
            mime="text/markdown",
        )

    with col2:
        all_recommendations = format_recommendations_for_download(results)
        st.download_button(
            label="📥 Download All Recommendations",
            data=all_recommendations,
            file_name="complete_fitness_recommendations.md",
            mime="text/markdown",
        )


def main() -> None:
    """Main application entry point."""
    configure_page()
    apply_custom_styling()

    display_main_header(MAIN_HEADER_TEXT)
    st.markdown("### Multi-Agent System with Clean Architecture")

    render_sidebar_configuration()

    status = check_llm_status()
    display_llm_status_card(status)

    if status["status"] != "success":
        display_setup_instructions()
        return

    tab1, tab2 = st.tabs(["📊 Profile Input", "📋 Results"])

    with tab1:
        render_profile_input_tab()

    with tab2:
        render_results_tab()


if __name__ == "__main__":
    main()
