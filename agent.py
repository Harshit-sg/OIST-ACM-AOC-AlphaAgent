"""
🌲 Forest Fire Alert Agent — Core AI Agent
=============================================
A simple input → output AI agent powered by OpenAI GPT-4o-mini.
Takes live sensor data + user question → returns clear, friendly advice.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from sensor_simulator import get_sensor_readings, format_readings_for_ai

# ── Load API Key ──────────────────────────────────────────────────────────────
# Load .env file (silently succeeds even if file doesn't exist)
load_dotenv()

# ── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are ForestGuard AI 🌲🔥, an expert forest fire alert assistant.

Your job is to:
1. Analyze live heat sensor data from forest monitoring stations
2. Clearly explain what the readings mean in plain, friendly language
3. Give prioritized, actionable safety tips based on the current alert level
4. Stay calm for NORMAL readings, be urgent (but not panic-inducing) for WARNING/DANGER,
   and give clear emergency instructions for CRITICAL readings

Rules:
- Always mention which specific zone(s) are at risk by name
- Use simple, jargon-free language — your audience may be forest rangers, volunteers, or locals
- Keep responses concise: 3–5 bullet points for normal, up to 8 for critical
- Format with emojis and bullet points for readability
- End every response with "Stay safe! 🌲" unless it is a CRITICAL alert,
  then end with "🚨 Act now — every second counts!"
"""


# ── Main Agent Function ───────────────────────────────────────────────────────
def ask_forest_guard(user_question: str, scenario: str = "normal") -> tuple[str, str]:
    """
    Core agent: takes a user question + sensor scenario → returns AI response.

    Parameters
    ----------
    user_question : str    — What the user typed in the UI
    scenario      : str    — "normal", "elevated", or "fire"

    Returns
    -------
    (sensor_display, ai_response) : tuple[str, str]

    Raises
    ------
    ValueError  — if OPENAI_API_KEY is not set in environment / .env
    """
    # 1. Validate API key at call time (not import time), so UI can still launch
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key.startswith("sk-your"):
        # Return sensor data but a helpful error message instead of crashing
        readings     = get_sensor_readings(scenario=scenario)
        sensor_block = format_readings_for_ai(readings)
        error_msg = (
            "⚠️  OPENAI_API_KEY not configured!\n\n"
            "To enable AI responses:\n"
            "  1. Copy  .env.template  →  .env\n"
            "  2. Open .env and set your real key:\n"
            "     OPENAI_API_KEY=sk-your-real-key-here\n"
            "  3. Restart the app (python app.py)\n\n"
            "Get your key at: https://platform.openai.com/api-keys\n\n"
            "📡 Sensor data above is live and working correctly!"
        )
        return sensor_block, error_msg

    # 2. Fetch live sensor readings
    readings     = get_sensor_readings(scenario=scenario)
    sensor_block = format_readings_for_ai(readings)

    # 3. Build the full prompt
    full_prompt = f"""
Here are the CURRENT live readings from forest heat sensors:

{sensor_block}

User question: {user_question}

Please analyze the sensor data and answer the user's question with clear, actionable advice.
"""

    # 4. Call GPT-4o-mini (simple input → output, no loops)
    client   = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": full_prompt},
        ],
        temperature=0.4,
        max_tokens=600,
    )

    ai_answer = response.choices[0].message.content.strip()
    return sensor_block, ai_answer
