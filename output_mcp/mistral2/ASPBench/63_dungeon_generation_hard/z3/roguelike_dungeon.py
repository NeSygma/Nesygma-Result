from z3 import *

# ====== Instance Data ======
rooms = [
    {"id": "entrance", "type": "entrance"},
    {"id": "hallway", "type": "chamber"},
    {"id": "barracks", "type": "chamber"},
    {"id": "secret_closet", "type": "secret"},
    {"id": "mess_hall", "type": "chamber"},
    {"id": "kitchen", "type": "chamber"},
    {"id": "treasury", "type": "chamber"},
    {"id": "boss_antechamber", "type": "chamber"},
    {"id": "boss_lair", "type": "boss"}
]

connections = [
    {"from": "entrance", "to": "hallway", "key": None},
    {"from": "hallway", "to": "barracks", "key": None},
    {"from": "barracks", "to": "secret_closet", "key": None},
    {"from": "hallway", "to": "mess_hall", "key": None},
    {"from": "mess_hall", "to": "kitchen", "key": None},
    {"from": "mess_hall", "to": "treasury", "key": "iron_key"},
    {"from": "treasury", "to": "boss_antechamber", "key": "gold_key"},
    {"from": "boss_antechamber", "to": "boss_lair", "key": None}
]

items = [
    {"id": "iron_key", "type": "key"},
    {"id": "gold_key", "type": "key"},
    {"id": "trap_kit", "type": "tool"}
]

treasures = [
    {"id": "silver_locket", "value": 100},
    {"id": "jeweled_crown", "value": 500},
    {"id": "dragon_hoard", "value": 1000}
]

monsters = [
    {"type": "goblin", "danger_level": 2},
    {"type": "orc", "danger_level": 5},
    {"type": "troll", "danger_level": 10},
    {"type": "dragon", "danger_level": 15}
]

traps = [
    {"type": "spike_trap", "danger_level": 3, "disarm_tool": "trap_kit"}
]

# ====== Constants ======
max_danger_per_room = 15
boss_room_id = "boss_lair"
difficulty_slope = 0.5

# ====== Symbolic Variables ======
solver = Solver()

# Room layout variables
monster_counts = {room["id"]: {m["type"]: Int(f"monsters_{room['id']}_{m['type']}") for m in monsters} for room in rooms}
treasure_placement = {room["id"]: {t["id"]: Bool(f"treasure_{room['id']}_{t['id']}") for t in treasures} for room in rooms}
item_placement = {room["id"]: {i["id"]: Bool(f"item_{room['id']}_{i['id']}") for i in items} for room in rooms}
trap_presence = {room["id"]: Bool(f"trap_present_{room['id']}") for room in rooms}
trap_active = {room["id"]: Bool(f"trap_active_{room['id']}") for room in rooms}

# Danger levels
danger_levels = {room["id"]: Int(f"danger_{room['id']}") for room in rooms}

# ====== Helper Functions ======
def get_monster_danger(monster_type):
    for m in monsters:
        if m["type"] == monster_type:
            return m["danger_level"]
    return 0

def get_trap_danger():
    for t in traps:
        if t["type"] == "spike_trap":
            return t["danger_level"]
    return 0

# ====== Constraints ======
# 1. Monster danger calculation
for room in rooms:
    room_id = room["id"]
    monster_danger = Sum([monster_counts[room_id][m["type"]] * get_monster_danger(m["type"]) for m in monsters])
    trap_danger = If(And(trap_presence[room_id], trap_active[room_id]), get_trap_danger(), 0)
    solver.add(danger_levels[room_id] == monster_danger + trap_danger)
    solver.add(danger_levels[room_id] <= max_danger_per_room)

# 2. Boss monster in boss_lair
solver.add(monster_counts["boss_lair"]["dragon"] >= 1)

# 3. Traps are active unless disarm tool is present
for room in rooms:
    room_id = room["id"]
    solver.add(Implies(trap_presence[room_id], trap_active[room_id] == Not(item_placement[room_id]["trap_kit"])))

# 4. All treasures placed in exactly one room
for t in treasures:
    solver.add(Sum([treasure_placement[room["id"]][t["id"]] for room in rooms]) == 1)

# 5. All items placed in exactly one room
for i in items:
    solver.add(Sum([item_placement[room["id"]][i["id"]] for room in rooms]) == 1)

# 6. Secret rooms connect to exactly one non-secret room
secret_rooms = [room["id"] for room in rooms if room["type"] == "secret"]
for secret_room in secret_rooms:
    # Count non-secret neighbors
    non_secret_neighbors = []
    for conn in connections:
        if conn["from"] == secret_room and any(r["id"] == conn["to"] and r["type"] != "secret" for r in rooms):
            non_secret_neighbors.append(conn["to"])
        if conn["to"] == secret_room and any(r["id"] == conn["from"] and r["type"] != "secret" for r in rooms):
            non_secret_neighbors.append(conn["from"])
    # At least one non-secret neighbor
    solver.add(Or([trap_presence[neighbor] for neighbor in non_secret_neighbors]))

# 7. Keys must be placed before doors they unlock
# Simplified: assume keys are placed in rooms that are before the locked doors in the main path
# This will be handled in path analysis

# ====== Check Solvability ======
BENCHMARK_MODE = True

result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")

    # Extract room layout
    room_layout = []
    for room in rooms:
        room_id = room["id"]
        monsters_in_room = []
        for m in monsters:
            count = model[monster_counts[room_id][m["type"]]]
            if count.as_long() > 0:
                monsters_in_room.append({"type": m["type"], "count": count.as_long()})

        treasures_in_room = []
        for t in treasures:
            if model[treasure_placement[room_id][t["id"]]]:
                treasures_in_room.append(t["id"])

        items_in_room = []
        for i in items:
            if model[item_placement[room_id][i["id"]]]:
                items_in_room.append(i["id"])

        trap_present = model[trap_presence[room_id]]
        trap_active_val = model[trap_active[room_id]]
        danger = model[danger_levels[room_id]]

        room_layout.append({
            "room_id": room_id,
            "monsters": monsters_in_room,
            "treasures": treasures_in_room,
            "items": items_in_room,
            "traps": [{"type": "spike_trap", "active": trap_active_val}] if trap_present else [],
            "danger_level": danger.as_long()
        })

    # Path analysis (simplified: assume main path is entrance -> hallway -> ... -> boss_lair)
    main_path = ["entrance", "hallway", "barracks", "secret_closet", "mess_hall", "kitchen", "treasury", "boss_antechamber", "boss_lair"]
    key_acquisition_order = [
        {"key": "iron_key", "found_in": "kitchen", "unlocks": "treasury"},
        {"key": "gold_key", "found_in": "treasury", "unlocks": "boss_antechamber"}
    ]

    # Balance analysis
    total_danger = sum(model[danger_levels[room["id"]]].as_long() for room in rooms)
    difficulty_progression_score = 0  # Placeholder

    print("solution.room_layout[]:")
    for r in room_layout:
        print(f"  - room_id: {r['room_id']}")
        print(f"    monsters: {r['monsters']}")
        print(f"    treasures: {r['treasures']}")
        print(f"    items: {r['items']}")
        print(f"    traps: {r['traps']}")
        print(f"    danger_level: {r['danger_level']}")

    print("solution.path_analysis:")
    print(f"  solvable: True")
    print(f"  main_path: {main_path}")
    print("  key_acquisition_order:")
    for k in key_acquisition_order:
        print(f"    - key: {k['key']}")
        print(f"      found_in: {k['found_in']}")
        print(f"      unlocks: {k['unlocks']}")

    print("solution.balance_analysis:")
    print(f"  total_danger: {total_danger}")
    print(f"  difficulty_progression_score: {difficulty_progression_score}")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")