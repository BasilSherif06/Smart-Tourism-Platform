import time
from typing import Any, Dict, List

ACTION_LABELS = {
    0: "NO_CHANGE",
    1: "MINOR_ADJUSTMENT",
    2: "MODERATE_REPLAN",
    3: "FULL_REPLAN",
}


def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Keeps any normalized state metric safely bounded between 0.0 and 1.0."""
    return max(min_val, min(max_val, float(value)))

def select_action(state_vector):
    severity, category, days_left, affected_stops, budget_left, pacing, time_overlap = [
        clamp(x) for x in state_vector
    ]

    # Rule 0: If zero stops are actually hit, don't touch the itinerary
    if affected_stops == 0.0:
        return 0

    # Rule 3 (FULL_REPLAN): Massive disruption or full day wiped, plenty of trip left, AND enough budget
    if (severity > 0.80 or affected_stops >= 0.90) and days_left >= 0.60 and budget_left >= 0.20:
        return 3

    # Rule 2 (MODERATE_REPLAN): Medium-high hit or 2-3 stops blocked, with tomorrow still available
    if (severity >= 0.50 or affected_stops >= 0.40) and days_left >= 0.25:
        return 2

    # Rule 1 (MINOR_ADJUSTMENT): At least 1 stop hit, or fast-paced schedule with tight time overlap
    if affected_stops > 0.0 or (pacing > 0.70 and time_overlap > 0.15):
        return 1

    # Fallback: Absorb into existing buffer
    return 0

def decide_replan(trip_id, disruption_id, state_vector, current_day=1, total_days=5):
    start_time = time.perf_counter()
    action_code = select_action(state_vector)

    # Set which days the Itinerary LLM is allowed to touch[cite: 5]
    if action_code == 0:
        replan_window = []
    elif action_code == 1:
        replan_window = [current_day]
    elif action_code == 2:
        replan_window = [current_day, min(total_days, current_day + 1)]
    else:
        replan_window = list(range(current_day, total_days + 1))

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    return {
        "trip_id": trip_id,
        "disruption_id": disruption_id,
        "action_code": action_code,
        "action_label": ACTION_LABELS[action_code],
        "execution_metadata": {
            "engine_type": "RULE_BASED_STUB_V1",
            "inference_time_ms": elapsed_ms,
            "scope_parameters": {
                "replan_window_days": replan_window,
                "preserve_locked_bookings": True,
            },
        },
    }


if __name__ == "__main__":
    # Quick sanity check across 4 scenarios
    tests = [
        ("3 AM delay, 0 stops hit", [0.80, 0.00, 0.80, 0.00, 0.90, 0.50, 0.00]),
        ("1 museum closed, Day 2 of 5", [0.35, 0.66, 0.60, 0.25, 0.80, 0.50, 0.20]),
        ("3-hr storm, 2 stops hit, Day 2 of 5", [0.65, 0.33, 0.60, 0.50, 0.70, 0.60, 0.35]),
        ("Flight canceled Day 1, high budget", [0.95, 0.00, 0.80, 1.00, 0.85, 0.50, 0.80]),
    ]

    for name, vec in tests:
        res = decide_replan("trip_001", "dis_001", vec, current_day=2, total_days=5)
        print(f"{name} -> Action {res['action_code']} ({res['action_label']}) | Window: {res['execution_metadata']['scope_parameters']['replan_window_days']}")

