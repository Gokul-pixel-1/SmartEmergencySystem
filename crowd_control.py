def crowd_control(
    total_people,
    exits,
    path_width,
    risk_level,
    congestion="low",
    special_needs=0,
    exit_capacities=None,
    hazard_nearby=False,
    panic=False,
    weather="normal",
    lighting="good",
    communication="normal"
):

    result = {}

    # -----------------------------
    # BASE CAPACITY
    # -----------------------------
    capacity = path_width * 5

    # -----------------------------
    # ENVIRONMENTAL FACTORS
    # -----------------------------
    if weather == "rain":
        capacity *= 0.7
        result["weather"] = "Slippery conditions"

    if lighting == "low":
        capacity *= 0.8
        result["lighting"] = "Low visibility"

    if communication == "delay":
        capacity *= 0.85
        result["communication"] = "Delayed instructions"

    # -----------------------------
    # PANIC EFFECT
    # -----------------------------
    if panic:
        capacity *= 0.6
        result["panic"] = "Uncontrolled crowd movement"

    # -----------------------------
    # CONGESTION EFFECT
    # -----------------------------
    if congestion == "high":
        capacity *= 0.5
    elif congestion == "medium":
        capacity *= 0.75

    capacity = int(capacity)
    result["capacity"] = capacity

    # -----------------------------
    # EXIT FAILURE SCENARIO
    # -----------------------------
    if exit_capacities:
        blocked_exits = [i for i in exit_capacities if i == 0]
        if blocked_exits:
            result["exit_failure"] = "One or more exits blocked"
            exits -= len(blocked_exits)

    # -----------------------------
    # HAZARD NEAR EXIT
    # -----------------------------
    if hazard_nearby:
        result["hazard"] = "Avoid nearest exit"
        exits = max(1, exits - 1)

    # -----------------------------
    # RISK HANDLING
    # -----------------------------
    if risk_level == "high":
        result["mode"] = "Immediate evacuation"
        result["per_exit"] = total_people // max(1, exits)

    elif risk_level == "medium":
        result["mode"] = "Controlled evacuation"
        result["batch"] = capacity

    else:
        result["mode"] = "Organized movement"
        result["rows"] = 4

    # -----------------------------
    # CROWD WAVES
    # -----------------------------
    waves = 5
    result["waves"] = waves
    result["per_wave"] = total_people // waves

    # -----------------------------
    # LANE CONTROL
    # -----------------------------
    lanes = min(4, path_width)
    result["lanes"] = lanes
    result["per_lane"] = total_people // lanes

    # -----------------------------
    # SPECIAL NEEDS
    # -----------------------------
    if special_needs > 0:
        result["special"] = f"{special_needs} assisted evacuees"

    # -----------------------------
    # DYNAMIC ADAPTATION
    # -----------------------------
    result["adaptive"] = "Adjust based on real-time crowd conditions"

    # -----------------------------
    # SAFETY BUFFER
    # -----------------------------
    safe_limit = int(capacity * 0.9)
    result["safe_limit"] = safe_limit

    # -----------------------------
    # FLOW CONTROL
    # -----------------------------
    interval = max(3, int(total_people / (capacity + 1)))
    result["interval"] = f"Release every {interval} sec"

    # -----------------------------
    # FINAL DECISION MESSAGE
    # -----------------------------
    result["decision"] = "System dynamically balances safety and speed"

    return result