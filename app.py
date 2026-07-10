"""
🌲 Forest Fire Alert Agent — Gradio UI
========================================
Clean, interactive web interface for the Forest Fire Alert Agent.
Run with: python app.py
"""

import gradio as gr
from agent import ask_forest_guard

# ── Scenario map: display label → internal key ────────────────────────────────
SCENARIO_CHOICES = [
    "🟢 Normal Conditions",
    "🟡 Elevated Heat Warning",
    "🔴 Active Fire Emergency",
]
SCENARIO_MAP = {
    "🟢 Normal Conditions":    "normal",
    "🟡 Elevated Heat Warning": "elevated",
    "🔴 Active Fire Emergency": "fire",
}

# ── Example Questions (must match SCENARIO_CHOICES labels exactly) ────────────
EXAMPLES = [
    ["Is it safe to hike in the forest today?",              "🟢 Normal Conditions"],
    ["I see smoke near the east slope — what should I do?",  "🟡 Elevated Heat Warning"],
    ["EMERGENCY — we see flames! What are the immediate steps?", "🔴 Active Fire Emergency"],
    ["What does a WARNING alert mean for nearby villages?",   "🟡 Elevated Heat Warning"],
    ["Give me a safety briefing for park rangers on duty.",   "🟢 Normal Conditions"],
]

# ── Custom CSS ────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
/* ── Fonts ───────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

/* ── Global Reset ─────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

body {
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
    background: #0a160a !important;
}

.gradio-container {
    background: linear-gradient(145deg, #0a160a 0%, #0f2210 40%, #091409 100%) !important;
    min-height: 100vh !important;
    max-width: 1200px !important;
}

/* ── Header Card ──────────────────────────────────────────── */
#header-card {
    background: linear-gradient(135deg, rgba(22,65,22,0.9) 0%, rgba(14,44,14,0.95) 100%);
    border: 1px solid rgba(80,200,80,0.25);
    border-radius: 18px;
    padding: 30px 36px;
    text-align: center;
    backdrop-filter: blur(12px);
    box-shadow:
        0 8px 32px rgba(0,0,0,0.5),
        0 0 60px rgba(40,180,40,0.06),
        inset 0 1px 0 rgba(100,255,100,0.08);
    margin-bottom: 4px;
}
#header-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #6eff6e;
    text-shadow: 0 0 24px rgba(80,255,80,0.5);
    margin: 0 0 10px 0;
    letter-spacing: -1px;
}
#header-sub {
    color: rgba(160,240,160,0.65);
    font-size: 0.95rem;
    margin: 0;
    letter-spacing: 0.3px;
}

/* ── Panel Labels ─────────────────────────────────────────── */
.label-green { color: #7de87d !important; font-weight: 700 !important; }

/* ── Textboxes ────────────────────────────────────────────── */
textarea, input[type="text"] {
    background: rgba(8,24,8,0.85) !important;
    border: 1px solid rgba(80,180,80,0.3) !important;
    border-radius: 12px !important;
    color: #d4ffd4 !important;
    font-size: 0.93rem !important;
    line-height: 1.65 !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    padding: 12px 14px !important;
}
textarea:focus, input[type="text"]:focus {
    border-color: rgba(80,220,80,0.6) !important;
    box-shadow: 0 0 0 3px rgba(60,200,60,0.12) !important;
    outline: none !important;
}

/* ── Radio Buttons ────────────────────────────────────────── */
fieldset { border: none !important; padding: 0 !important; }
.gr-radio-group label {
    color: #a8e8a8 !important;
    font-size: 0.92rem !important;
}
input[type="radio"]:checked + span {
    color: #6eff6e !important;
    font-weight: 700 !important;
}

/* ── Primary Button ───────────────────────────────────────── */
#submit-btn {
    background: linear-gradient(135deg, #1a7a1a 0%, #26b026 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    padding: 14px 24px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    box-shadow: 0 4px 18px rgba(40,180,40,0.35) !important;
    letter-spacing: 0.3px !important;
}
#submit-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 24px rgba(40,210,40,0.5) !important;
}
#submit-btn:active {
    transform: translateY(0) !important;
}

/* ── Tips Card ────────────────────────────────────────────── */
#tips-card {
    background: rgba(30,80,30,0.3);
    border: 1px solid rgba(100,200,100,0.2);
    border-radius: 12px;
    padding: 14px 18px;
    color: #c0ecc0;
    font-size: 0.87rem;
    line-height: 1.8;
}

/* ── Output Textboxes override ────────────────────────────── */
#sensor-out textarea, #ai-out textarea {
    font-family: 'Courier New', 'Consolas', monospace !important;
    background: rgba(4,14,4,0.92) !important;
    border-color: rgba(60,160,60,0.25) !important;
    color: #aaf0aa !important;
    font-size: 0.87rem !important;
}

/* ── Examples section ─────────────────────────────────────── */
.gr-examples .label-wrap span { color: #7de87d !important; }
.gr-examples table { color: #b0dfb0 !important; font-size: 0.87rem !important; }

/* ── Footer ───────────────────────────────────────────────── */
#footer {
    text-align: center;
    color: rgba(100,200,100,0.3);
    font-size: 0.8rem;
    padding: 16px 0 8px 0;
}
"""


# ── Handler ───────────────────────────────────────────────────────────────────
def handle_query(user_question: str, scenario_label: str) -> tuple[str, str]:
    """Bridge between Gradio UI and the AI agent."""
    if not user_question or not user_question.strip():
        return "", "⚠️  Please type a question in the box above, then click Analyze & Alert!"

    scenario_key = SCENARIO_MAP.get(scenario_label, "normal")
    sensor_block, ai_answer = ask_forest_guard(user_question.strip(), scenario_key)
    return sensor_block, ai_answer


# ── Build Gradio UI ───────────────────────────────────────────────────────────
def build_ui() -> gr.Blocks:
    with gr.Blocks(
        css=CUSTOM_CSS,
        title="🌲 Forest Fire Alert Agent",
        theme=gr.themes.Base(
            primary_hue=gr.themes.colors.green,
            secondary_hue=gr.themes.colors.emerald,
            neutral_hue=gr.themes.colors.neutral,
            font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
        ),
    ) as demo:

        # ── Header ────────────────────────────────────────────────────────────
        gr.HTML("""
        <div id="header-card">
            <p id="header-title">🌲🔥 Forest Fire Alert Agent</p>
            <p id="header-sub">
                Powered by OpenAI GPT-4o-mini &nbsp;·&nbsp;
                Live Heat Sensor Monitoring &nbsp;·&nbsp;
                Real-time Safety Advice
            </p>
        </div>
        """)

        with gr.Row(equal_height=False):

            # ── Left Column: Controls ──────────────────────────────────────────
            with gr.Column(scale=1, min_width=280):

                scenario = gr.Radio(
                    choices=SCENARIO_CHOICES,
                    value=SCENARIO_CHOICES[0],
                    label="📡  Select Forest Sensor Scenario",
                )

                question = gr.Textbox(
                    label="💬  Your Question",
                    placeholder=(
                        "e.g. Is it safe to enter the forest?\n"
                        "e.g. I see smoke — what should I do?\n"
                        "e.g. EMERGENCY! There are flames!"
                    ),
                    lines=4,
                    max_lines=8,
                )

                submit_btn = gr.Button(
                    "🚨  Analyze & Alert",
                    elem_id="submit-btn",
                    variant="primary",
                )

                gr.HTML("""
                <div id="tips-card">
                    <strong>💡 Quick Tips</strong><br>
                    • Switch scenario to simulate different conditions<br>
                    • Ask about specific zones (North Ridge, Valley Stream…)<br>
                    • Request evacuation routes or ranger procedures<br>
                    • Click any example below to auto-fill the form
                </div>
                """)

            # ── Right Column: Outputs ──────────────────────────────────────────
            with gr.Column(scale=2, min_width=400):

                sensor_output = gr.Textbox(
                    label="📊  Live Sensor Readings (5 Forest Zones)",
                    lines=9,
                    max_lines=12,
                    interactive=False,
                    elem_id="sensor-out",
                )

                ai_output = gr.Textbox(
                    label="🤖  ForestGuard AI — Safety Response",
                    lines=14,
                    max_lines=20,
                    interactive=False,
                    elem_id="ai-out",
                )

        # ── Wire interactions ──────────────────────────────────────────────────
        submit_btn.click(
            fn=handle_query,
            inputs=[question, scenario],
            outputs=[sensor_output, ai_output],
        )
        question.submit(
            fn=handle_query,
            inputs=[question, scenario],
            outputs=[sensor_output, ai_output],
        )

        # ── Examples ──────────────────────────────────────────────────────────
        gr.Examples(
            examples=EXAMPLES,
            inputs=[question, scenario],
            label="📋  Example Questions — Click Any Row to Try",
            examples_per_page=5,
        )

        # ── Footer ─────────────────────────────────────────────────────────────
        gr.HTML("""
        <div id="footer">
            🌲 ForestGuard AI &nbsp;·&nbsp; Powered by OpenAI GPT-4o-mini &nbsp;·&nbsp;
            For demonstration &amp; educational purposes
        </div>
        """)

    return demo


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print()
    print("=" * 54)
    print("  🌲  Forest Fire Alert Agent — Starting Up")
    print("=" * 54)
    print("  🔗  URL: http://127.0.0.1:7860")
    print("  ℹ️   Make sure your .env file has OPENAI_API_KEY set")
    print("  ⌨️   Press Ctrl+C to stop the server")
    print("=" * 54)
    print()

    ui = build_ui()
    ui.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,       # Set to True to get a public Gradio share link
        inbrowser=True,    # Auto-opens your default browser
        show_error=True,
    )
