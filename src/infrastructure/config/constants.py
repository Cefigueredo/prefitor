"""
Constants and configuration values for the Fitness AI Advisor application.
This module centralizes all magic numbers, strings, and configuration values.
"""

# UI Configuration
PAGE_TITLE = "Fitness AI Advisor - Multi-Agent System (Modular LLM)"
PAGE_ICON = "🏋️"
APP_LAYOUT = "wide"
MAIN_HEADER_TEXT = "🏋️ Fitness AI Advisor"

# Weight and Height Ranges
WEIGHT_MIN_KG = 40
WEIGHT_MAX_KG = 150
WEIGHT_STEP_KG = 5
WEIGHT_DEFAULT_INDEX = 10  # 90kg

HEIGHT_MIN_CM = 140
HEIGHT_MAX_CM = 210
HEIGHT_STEP_CM = 5
HEIGHT_DEFAULT_INDEX = 10  # 185cm

# Training Intensity Options
TRAINING_INTENSITY_OPTIONS = [
    "Beginner (0-6 months experience)",
    "Intermediate (6 months - 2 years)",
    "Advanced (2+ years experience)",
    "Elite (Competitive athlete)",
]

# Body Goal Options
BODY_GOAL_OPTIONS = [
    "Build Muscle Mass",
    "Lose Fat",
    "Improve Strength",
    "Increase Endurance",
    "General Fitness",
    "Athletic Performance",
    "Body Recomposition",
]

# Time Availability Options
TIME_AVAILABILITY_OPTIONS = [
    "30-45 minutes",
    "45-60 minutes",
    "60-90 minutes",
    "90+ minutes",
]

# Equipment Access Options
EQUIPMENT_ACCESS_OPTIONS = [
    "Home gym (basic)",
    "Commercial gym",
    "Bodyweight only",
    "Full home gym",
]

# Dietary Restrictions Options
DIETARY_RESTRICTIONS_OPTIONS = [
    "None",
    "Vegetarian",
    "Vegan",
    "Gluten-free",
    "Dairy-free",
    "Other",
]

# LLM Preset Options
LLM_PRESET_OPTIONS = ["Custom", "TinyLlama", "Llama3.2", "GPT-4", "Claude"]

# Status Icons
STATUS_ICONS: dict[str, str] = {
    "pending": "⏳",
    "running": "🔄",
    "completed": "✅",
    "error": "❌",
}

# Agent Names
AGENT_TRAINING = "Training Specialist"
AGENT_NUTRITION = "Nutrition Specialist"
AGENT_COOKING = "Cooking Specialist"
AGENT_SUPERVISOR = "Supervisor"

# File Names
FINAL_PLAN_FILENAME = "comprehensive_fitness_plan.md"
ALL_RECOMMENDATIONS_FILENAME = "complete_fitness_recommendations.md"

# API Timeouts
OLLAMA_CONNECTION_TIMEOUT = 5

# Temperature Slider Config
TEMPERATURE_MIN = 0.0
TEMPERATURE_MAX = 1.0
TEMPERATURE_DEFAULT = 0.7
TEMPERATURE_STEP = 0.1

# CSS Classes
CSS_CLASS_SUCCESS = "success"
CSS_CLASS_WARNING = "warning"
CSS_CLASS_ERROR = "error"

# Progress Values
PROGRESS_INITIAL = 0
PROGRESS_TRAINING_COMPLETE = 25
PROGRESS_NUTRITION_COMPLETE = 50
PROGRESS_COOKING_COMPLETE = 75
PROGRESS_FINAL_COMPLETE = 100

# Session State Keys
SESSION_USER_DATA = "user_data"
SESSION_RUN_AGENTS = "run_agents"
SESSION_AGENT_RESULTS = "agent_results"
SESSION_AGENTS_COMPLETED = "agents_completed"
