import networkx as nx

def heuristic(a, b):
    return 1


# -----------------------------
# BUILD GRAPH WITH WEIGHTS
# -----------------------------
def build_graph():
    G = nx.Graph()

    edges = [
        ("Room A", "Corridor 1"),
        ("Room B", "Corridor 1"),
        ("Room C", "Corridor 2"),
        ("Room D", "Corridor 2"),
        ("Room E", "Corridor 3"),
        ("Room F", "Corridor 3"),
        ("Room G", "Corridor 4"),
        ("Room H", "Corridor 4"),

        ("Corridor 1", "Corridor 2"),
        ("Corridor 2", "Corridor 3"),
        ("Corridor 3", "Corridor 4"),

        ("Corridor 1", "Stairs Left"),
        ("Corridor 2", "Stairs Center"),
        ("Corridor 4", "Stairs Right"),

        ("Stairs Left", "Exit 1"),
        ("Stairs Center", "Exit 2"),
        ("Stairs Right", "Exit 3"),

        ("Corridor 3", "Exit 3"),
    ]

    for u, v in edges:
        G.add_edge(u, v, weight=1)

    return G


# -----------------------------
# APPLY COMPLEX CONDITIONS
# -----------------------------
def apply_conditions(G, emergency_type, severity, congestion, blocked_nodes):

    # 🔥 FIRE: Increase risk weights instead of removing
    if emergency_type == "fire":
        for u, v in G.edges():
            if "Corridor 2" in (u, v):
                G[u][v]['weight'] += 5  # avoid fire zone

        if severity == "high":
            if "Corridor 2" in G:
                G.remove_node("Corridor 2")

    # 🟠 GAS: spreading risk
    if emergency_type == "gas":
        for u, v in G.edges():
            if "Corridor 3" in (u, v):
                G[u][v]['weight'] += 4

    # ⚫ SECURITY: restrict zones
    if emergency_type == "security":
        if "Stairs Right" in G:
            G.remove_node("Stairs Right")

    # 🟡 CROWD DENSITY EFFECT
    if congestion == "high":
        for u, v in G.edges():
            G[u][v]['weight'] += 3

    elif congestion == "medium":
        for u, v in G.edges():
            G[u][v]['weight'] += 1

    # 🚧 ADMIN BLOCK
    for node in blocked_nodes:
        if node in G:
            G.remove_node(node)

    return G


# -----------------------------
# FIND BEST PATH (WEIGHTED)
# -----------------------------
def find_path(G, start):

    exits = ["Exit 1", "Exit 2", "Exit 3"]

    best_path = None
    best_cost = float("inf")

    for ex in exits:
        try:
            path = nx.astar_path(G, start, ex, heuristic, weight="weight")

            cost = 0
            for i in range(len(path) - 1):
                cost += G[path[i]][path[i+1]]['weight']

            if cost < best_cost:
                best_cost = cost
                best_path = path

        except:
            continue

    return best_path


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def get_evacuation_path(
    emergency_type,
    start_location="Room B",
    severity="medium",
    congestion="low",
    blocked_nodes=None
):

    if blocked_nodes is None:
        blocked_nodes = []

    G = build_graph()

    G = apply_conditions(
        G,
        emergency_type,
        severity,
        congestion,
        blocked_nodes
    )

    if start_location not in G:
        return "Unsafe start location"

    path = find_path(G, start_location)

    if path:
        return " → ".join(path)
    else:
        return "No safe evacuation path"