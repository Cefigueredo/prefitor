"""
Agent system prompts and prompt templates for the Fitness AI Advisor.
This module centralizes all LLM prompts to improve maintainability and
consistency.
"""

from typing import Any

# System Prompts for Each Agent
TRAINING_SPECIALIST_SYSTEM_PROMPT = """You are an expert fitness trainer and
strength coach with 15+ years of experience.
Your expertise includes:
- Strength training and muscle building
- Cardiovascular fitness
- Sports-specific training
- Injury prevention and rehabilitation
- Progressive overload principles
- Exercise form and technique

Provide detailed, practical workout recommendations that are:
- Safe and appropriate for the user's fitness level
- Progressive and sustainable
- Specific to their goals
- Include sets, reps, frequency, and progression strategies
"""

NUTRITION_SPECIALIST_SYSTEM_PROMPT = """You are a certified sports nutritionist
and registered dietitian with expertise in:
- Sports nutrition and performance
- Weight management and body composition
- Macronutrient optimization
- Meal timing and frequency
- Supplementation (when appropriate)
- Dietary restrictions and preferences

Provide evidence-based nutrition recommendations that:
- Support the user's fitness goals
- Are practical and sustainable
- Include specific calorie and macro targets
- Consider their training schedule
"""

COOKING_SPECIALIST_SYSTEM_PROMPT = """You are a culinary expert and meal prep
specialist with expertise in:
- Healthy cooking techniques
- Meal prep and batch cooking
- Recipe development for fitness goals
- Time-efficient cooking methods
- Budget-friendly meal planning
- Dietary restrictions and preferences

Provide practical cooking and meal prep advice that:
- Supports the nutrition recommendations
- Fits into busy schedules
- Is cost-effective and delicious
- Includes specific recipes and techniques
"""

SUPERVISOR_SYSTEM_PROMPT = """You are a senior fitness and wellness coordinator
who oversees multiple specialists.
Your role is to:
- Coordinate recommendations from different specialists
- Ensure consistency across all advice
- Create a comprehensive, actionable plan
- Prioritize recommendations based on user goals
- Identify potential conflicts or gaps in advice

Create a final, integrated recommendation that combines all specialist input
into a cohesive plan.
"""


# Prompt Templates
def create_training_prompt(user_profile: dict[str, Any]) -> str:
    """
    Create a detailed training specialist prompt based on user profile.

    Args:
        user_profile: User fitness profile data

    Returns:
        Formatted prompt string
    """
    return f"""
Based on the following user profile, provide comprehensive training
recommendations:

User Profile:
- Weight: {user_profile.get("weight", "Not specified")}
- Training Intensity: {user_profile.get("training_intensity", "Not specified")}
- Height: {user_profile.get("height", "Not specified")}
- Body Goal: {user_profile.get("body_goal", "Not specified")}
- Time Availability: {user_profile.get("time_availability", "Not specified")}
- Equipment Access: {user_profile.get("equipment_access", "Not specified")}

Please provide:
1. **Workout Split**: How to organize training days
2. **Exercise Selection**: Specific exercises for their goals
3. **Sets & Reps**: Detailed rep schemes and set counts
4. **Progression Plan**: How to increase intensity over time
5. **Recovery Strategy**: Rest days and recovery techniques
6. **Timeline**: Expected progress milestones

Make recommendations practical, safe, and tailored to their specific profile.
"""


def create_nutrition_prompt(
    user_profile: dict[str, Any], training_advice: str
) -> str:
    """
    Create a detailed nutrition specialist prompt.

    Args:
        user_profile: User fitness profile data
        training_advice: Training recommendations from training specialist

    Returns:
        Formatted prompt string
    """
    return f"""
Based on the following user profile and their training plan, provide
comprehensive nutrition recommendations:

User Profile:
- Weight: {user_profile.get("weight", "Not specified")}
- Training Intensity: {user_profile.get("training_intensity", "Not specified")}
- Height: {user_profile.get("height", "Not specified")}
- Body Goal: {user_profile.get("body_goal", "Not specified")}
- Dietary Restrictions: {user_profile.get("dietary_restrictions", "None")}

Training Plan Context:
{training_advice}

Please provide:
1. **Caloric Needs**: Daily calorie targets for their goal
2. **Macronutrient Breakdown**: Protein, carbs, and fat ratios
3. **Meal Timing**: When to eat relative to workouts
4. **Food Recommendations**: Specific food choices and portions
5. **Hydration Strategy**: Fluid intake recommendations
6. **Supplementation**: If any supplements are recommended

Make recommendations practical, affordable, and aligned with their training
schedule.
"""


def create_cooking_prompt(
    user_profile: dict[str, Any], nutrition_advice: str
) -> str:
    """
    Create a detailed cooking specialist prompt.

    Args:
        user_profile: User fitness profile data
        nutrition_advice: Nutrition recommendations from nutrition specialist

    Returns:
        Formatted prompt string
    """
    return f"""
Based on the following user profile and nutrition recommendations, provide
practical cooking and meal prep advice:

User Profile:
- Weight: {user_profile.get("weight", "Not specified")}
- Training Intensity: {user_profile.get("training_intensity", "Not specified")}
- Height: {user_profile.get("height", "Not specified")}
- Body Goal: {user_profile.get("body_goal", "Not specified")}
- Time Availability: {user_profile.get("time_availability", "Not specified")}
- Dietary Restrictions: {user_profile.get("dietary_restrictions", "None")}

Nutrition Recommendations:
{nutrition_advice}

Please provide:
1. **Meal Prep Strategy**: Weekly meal prep plan and schedule
2. **Cooking Techniques**: Healthy cooking methods and tips
3. **Recipe Recommendations**: 5-7 specific recipes for their goals
4. **Shopping List**: Weekly grocery shopping guide
5. **Time Management**: How to cook efficiently
6. **Equipment Recommendations**: Essential kitchen tools

Focus on practical, time-efficient, and budget-friendly solutions.
"""


def create_supervisor_prompt(
    user_profile: dict[str, Any],
    training_advice: str,
    nutrition_advice: str,
    cooking_advice: str,
) -> str:
    """
    Create a comprehensive supervisor prompt that integrates all specialist
    advice.

    Args:
        user_profile: User fitness profile data
        training_advice: Training specialist recommendations
        nutrition_advice: Nutrition specialist recommendations
        cooking_advice: Cooking specialist recommendations

    Returns:
        Formatted prompt string
    """
    return f"""
As the supervisor, create a comprehensive, integrated fitness and wellness plan
by combining the recommendations from all specialists.

User Profile:
- Weight: {user_profile.get("weight", "Not specified")}
- Training Intensity: {user_profile.get("training_intensity", "Not specified")}
- Height: {user_profile.get("height", "Not specified")}
- Body Goal: {user_profile.get("body_goal", "Not specified")}
- Time Availability: {user_profile.get("time_availability", "Not specified")}
- Equipment Access: {user_profile.get("equipment_access", "Not specified")}
- Dietary Restrictions: {user_profile.get("dietary_restrictions", "None")}

Training Specialist Recommendations:
{training_advice}

Nutrition Specialist Recommendations:
{nutrition_advice}

Cooking Specialist Recommendations:
{cooking_advice}

Please create a final, integrated plan that includes:
1. **Executive Summary**: Key takeaways and priorities
2. **Weekly Schedule**: Integrated training and meal plan
3. **Implementation Guide**: Step-by-step action plan
4. **Progress Tracking**: How to measure success
5. **Troubleshooting**: Common challenges and solutions
6. **Next Steps**: Immediate actions to take

Ensure the plan is cohesive, practical, and addresses all aspects of their
fitness journey.
"""
