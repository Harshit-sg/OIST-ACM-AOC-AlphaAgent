"""
🌲 Forest Fire Alert Agent — Test Suite
=========================================
Run: python test_agent.py
Tests sensor simulator (no key needed) + full agent (key needed).
"""

import sys
import os
import traceback

# ── Force UTF-8 output on Windows (fixes emoji in terminal) ──────────────────
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ─────────────────────────────────────────────────────────────────────────────
def section(title: str):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)

def ok(msg):   print(f"  [PASS]  {msg}")
def warn(msg): print(f"  [WARN]  {msg}")
def fail(msg): print(f"  [FAIL]  {msg}")

# ─────────────────────────────────────────────────────────────────────────────
def test_sensor_simulator():
    section("TEST 1 -- Sensor Simulator (no API key needed)")
    try:
        from sensor_simulator import (
            get_sensor_readings,
            format_readings_for_ai,
            SENSOR_ZONES,
            THRESHOLD_WARNING,
            THRESHOLD_DANGER,
            THRESHOLD_CRITICAL,
        )

        assert len(SENSOR_ZONES) == 5, "Should have 5 sensor zones"
        ok(f"Zones loaded: {len(SENSOR_ZONES)}")
        ok(f"Thresholds -- Warning:{THRESHOLD_WARNING}C  "
           f"Danger:{THRESHOLD_DANGER}C  Critical:{THRESHOLD_CRITICAL}C")

        for scenario in ("normal", "elevated", "fire"):
            readings = get_sensor_readings(scenario=scenario)
            assert len(readings) == 5, f"Expected 5 readings for scenario={scenario}"
            block = format_readings_for_ai(readings)
            assert "LIVE FOREST HEAT SENSOR READINGS" in block, \
                "block should contain header"
            # Validate each reading has required keys
            for r in readings:
                for key in ("zone_id", "zone_name", "temp_c", "alert", "timestamp"):
                    assert key in r, f"Missing key '{key}' in reading"
            print(f"\n  Scenario: {scenario.upper()}")
            print(block)

        ok("Sensor simulator -- ALL ASSERTIONS PASSED")
        return True

    except Exception as exc:
        fail(f"Sensor simulator test FAILED: {exc}")
        traceback.print_exc()
        return False


# ─────────────────────────────────────────────────────────────────────────────
def test_agent():
    section("TEST 2 -- AI Agent (requires OPENAI_API_KEY in .env)")
    try:
        from agent import ask_forest_guard

        sensor_block, response = ask_forest_guard(
            "Is it safe to go hiking today?",
            scenario="normal",
        )

        assert sensor_block, "Sensor block should not be empty"
        assert response,     "AI response should not be empty"

        if "OPENAI_API_KEY not configured" in response:
            warn("API key not set -- skipping live AI call")
            warn("Sensor data is returning correctly though:")
            print(sensor_block)
            warn("To enable AI responses, set OPENAI_API_KEY in .env")
            return None   # Partial pass — expected without a real key

        ok("Sensor block received")
        print(sensor_block)
        ok("AI Response:")
        print(response)
        return True

    except Exception as exc:
        fail(f"Agent test FAILED: {exc}")
        traceback.print_exc()
        return False


# ─────────────────────────────────────────────────────────────────────────────
def test_ui_imports():
    section("TEST 3 -- UI Imports & Logic Validation")
    try:
        import gradio as gr
        ok(f"Gradio version: {gr.__version__}")

        # Import the UI builder without launching it
        from app import build_ui, handle_query, SCENARIO_MAP, EXAMPLES

        assert len(SCENARIO_MAP) == 3, "Should have 3 scenarios"
        assert len(EXAMPLES)    == 5, "Should have 5 examples"

        # Verify all example scenario labels exist in SCENARIO_MAP
        for ex in EXAMPLES:
            label = ex[1]
            assert label in SCENARIO_MAP, (
                f"Example scenario '{label}' not in SCENARIO_MAP!\n"
                f"  Available: {list(SCENARIO_MAP.keys())}"
            )

        ok(f"SCENARIO_MAP: {list(SCENARIO_MAP.keys())}")
        ok(f"Examples: {len(EXAMPLES)} entries, all scenario labels valid")
        ok("UI build_ui function importable")
        return True

    except Exception as exc:
        fail(f"UI import test FAILED: {exc}")
        traceback.print_exc()
        return False


# ─────────────────────────────────────────────────────────────────────────────
def test_empty_question_guard():
    section("TEST 4 -- Empty Question Guard")
    try:
        from app import handle_query
        # Test empty string
        _, ai_out = handle_query("", "Normal Conditions")
        assert "Please type" in ai_out or "question" in ai_out.lower(), \
            f"Expected guard message, got: {ai_out!r}"
        ok("Empty string correctly returns helpful prompt message")

        # Test whitespace-only
        _, ai_out2 = handle_query("   ", "Normal Conditions")
        assert "Please type" in ai_out2 or "question" in ai_out2.lower(), \
            f"Expected guard message, got: {ai_out2!r}"
        ok("Whitespace-only string also returns helpful prompt message")
        return True

    except Exception as exc:
        fail(f"Guard test FAILED: {exc}")
        traceback.print_exc()
        return False


# ─────────────────────────────────────────────────────────────────────────────
def test_all_scenarios():
    section("TEST 5 -- All Scenario Values Round-Trip")
    try:
        from app import SCENARIO_MAP, handle_query

        for display_label, internal_key in SCENARIO_MAP.items():
            sensor_out, ai_out = handle_query(
                "What is the current forest status?",
                display_label,
            )
            assert sensor_out, f"No sensor output for scenario '{display_label}'"
            assert ai_out,     f"No AI output for scenario '{display_label}'"
            ok(f"Scenario '{display_label}' -> '{internal_key}': OK")

        return True

    except Exception as exc:
        fail(f"Scenario round-trip test FAILED: {exc}")
        traceback.print_exc()
        return False


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  FOREST FIRE ALERT AGENT -- FULL TEST SUITE")
    print("=" * 60)

    results = {
        "Sensor Simulator":        test_sensor_simulator(),
        "Agent (AI)":              test_agent(),
        "UI Imports & Validation": test_ui_imports(),
        "Empty Question Guard":    test_empty_question_guard(),
        "All Scenarios Round-Trip":test_all_scenarios(),
    }

    section("SUMMARY")
    all_passed = True
    for name, result in results.items():
        if result is True:
            status = "[PASS]   "
        elif result is None:
            status = "[PARTIAL]"
        else:
            status = "[FAIL]   "
            all_passed = False
        print(f"  {status}  {name}")

    print()
    if all_passed:
        print("  All tests passed! Run: python app.py  to start the UI.")
    else:
        print("  Some tests failed -- check output above for details.")
    print()
    sys.exit(0 if all_passed else 1)
