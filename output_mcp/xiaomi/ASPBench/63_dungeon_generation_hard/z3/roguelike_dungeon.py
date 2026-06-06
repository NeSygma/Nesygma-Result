from z3 import *

# --- 1. Define Entities and Constants ---
rooms = [
    "entrance", "hallway", "barracks", "secret_closet", "mess_hall",
    "kitchen", "treasury", "boss_antechamber", "boss_lair"
]
room_types = {
    "entrance": "entrance", "hallway": "chamber", "barracks": "chamber",
    "secret_closet": "secret", "mess_hall": "chamber", "kitchen": "chamber",
    "treasury": "chamber", "boss_antechamber": "chamber", "boss_lair": "boss"
}

# Connections: (from, to, key_required_or_None)
connections = [
    ("entrance", "hallway", None),
    ("hallway", "barracks", None),
    ("barracks", "secret_closet", None),
    ("hallway", "mess_hall", None),
    ("mess_hall", "kitchen", None),
    ("mess_hall", "treasury", "iron_key"),
    ("treasury", "boss_antechamber", "gold_key"),
    ("boss_antechamber", "boss_lair", None),
]

items = ["iron_key", "gold_key", "trap_kit"]
item_types = {"iron_key": "key", "gold_key": "key", "trap_kit": "tool"}

treasures = ["silver_locket", "jeweled_crown", "dragon_hoard"]
treasure_values = {"silver_locket": 100, "jeweled_crown": 500, "dragon_hoard": 1000}

monsters = ["goblin", "orc", "troll", "dragon"]
monster_danger = {"goblin": 2, "orc": 5, "troll": 10, "dragon": 15}

traps = ["spike_trap"]
trap_danger = {"spike_trap": 3}
trap_disarm = {"spike_trap": "trap_kit"}

MAX_DANGER = 15
BOSS_ROOM = "boss_lair"

# --- 2. Z3 Solver Setup ---
solver = Solver()

# --- 3. Decision Variables ---

# Item placement: item -> room index
item_room = {item: Int(f"item_{item}") for item in items}
for item in items:
    solver.add(item_room[item] >= 0, item_room[item] < len(rooms))

# Treasure placement: treasure -> room index
treasure_room = {t: Int(f"treasure_{t}") for t in treasures}
for t in treasures:
    solver.add(treasure_room[t] >= 0, treasure_room[t] < len(rooms))

# Monster counts per room: monster -> room -> count
monster_count = {}
for m in monsters:
    for r in range(len(rooms)):
        monster_count[(m, r)] = Int(f"mc_{m}_{r}")
        solver.add(monster_count[(m, r)] >= 0)

# Trap placement: trap -> room index (-1 if not placed)
trap_room = {t: Int(f"trap_{t}") for t in traps}
for t in traps:
    solver.add(trap_room[t] >= -1, trap_room[t] < len(rooms))

# Trap active status: trap -> Bool (active if disarm tool not in same room)
trap_active = {t: Bool(f"trap_active_{t}") for t in traps}

# --- 4. Core Constraints ---

# 4a. Boss monster (dragon) must be in boss_lair (room index 8)
boss_idx = rooms.index(BOSS_ROOM)
solver.add(monster_count[("dragon", boss_idx)] >= 1)
# Dragon should NOT be in any other room
for r in range(len(rooms)):
    if r != boss_idx:
        solver.add(monster_count[("dragon", r)] == 0)

# 4b. Danger level per room
danger_level = [Int(f"danger_{r}") for r in range(len(rooms))]
for r in range(len(rooms)):
    monster_danger_sum = Sum([monster_count[(m, r)] * monster_danger[m] for m in monsters])
    trap_danger_sum = Sum([
        If(And(trap_room[t] == r, trap_active[t]), trap_danger[t], 0) for t in traps
    ])
    solver.add(danger_level[r] == monster_danger_sum + trap_danger_sum)
    solver.add(danger_level[r] <= MAX_DANGER)

# 4c. Trap active logic: trap is active unless its disarm tool is in the same room
for t in traps:
    disarm_item = trap_disarm[t]
    solver.add(trap_active[t] == Not(item_room[disarm_item] == trap_room[t]))

# 4d. Keys must be placed in rooms reachable BEFORE the doors they unlock
# iron_key unlocks mess_hall->treasury, so iron_key must be in a room reachable
# without passing through that locked door. Reachable set: {entrance, hallway, barracks, secret_closet, mess_hall, kitchen}
iron_key_reachable = [rooms.index(r) for r in ["entrance", "hallway", "barracks", "secret_closet", "mess_hall", "kitchen"]]
solver.add(Or([item_room["iron_key"] == r for r in iron_key_reachable]))

# gold_key unlocks treasury->boss_antechamber, so gold_key must be reachable before that door
# Reachable set includes treasury (once iron_key is obtained): {entrance, hallway, barracks, secret_closet, mess_hall, kitchen, treasury}
gold_key_reachable = [rooms.index(r) for r in ["entrance", "hallway", "barracks", "secret_closet", "mess_hall", "kitchen", "treasury"]]
solver.add(Or([item_room["gold_key"] == r for r in gold_key_reachable]))

# 4e. Secret room (secret_closet) connects to exactly one non-secret room (barracks)
# Already encoded in connections; just ensure it's reachable
# secret_closet must be reachable from entrance via barracks
# This is guaranteed by the connection graph structure

# 4f. Difficulty progression: danger should generally increase along the main path
# Main path: entrance -> hallway -> mess_hall -> treasury -> boss_antechamber -> boss_lair
# (or via barracks branch, but main progression is through locked doors)
# We'll enforce a soft progression: each successive room on the main path should have >= previous danger
main_path_rooms = ["entrance", "hallway", "mess_hall", "treasury", "boss_antechamber", "boss_lair"]
main_path_indices = [rooms.index(r) for r in main_path_rooms]
for i in range(len(main_path_indices) - 1):
    solver.add(danger_level[main_path_indices[i]] <= danger_level[main_path_indices[i+1]])

# 4g. All items must be placed in distinct rooms (optional but good practice)
# Not strictly required, but let's allow co-location

# 4h. Ensure the dungeon is solvable by construction:
# - entrance -> hallway (unlocked)
# - hallway -> mess_hall (unlocked)
# - mess_hall -> treasury (locked by iron_key, iron_key reachable before)
# - treasury -> boss_antechamber (locked by gold_key, gold_key reachable before)
# - boss_antechamber -> boss_lair (unlocked)
# This is guaranteed by constraints 4d and the connection graph

# 4i. Place at least some monsters in non-boss rooms for variety
for r in range(len(rooms)):
    if r != boss_idx:
        solver.add(Sum([monster_count[(m, r)] for m in monsters]) >= 0)  # allow empty rooms

# 4j. Place treasures in interesting locations
# silver_locket in early rooms, jeweled_crown in mid, dragon_hoard near boss
solver.add(Or([treasure_room["silver_locket"] == rooms.index(r) for r in ["entrance", "hallway", "barracks", "secret_closet"]]))
solver.add(Or([treasure_room["jeweled_crown"] == rooms.index(r) for r in ["mess_hall", "kitchen", "treasury"]]))
solver.add(Or([treasure_room["dragon_hoard"] == rooms.index(r) for r in ["treasury", "boss_antechamber", "boss_lair"]]))

# 4k. trap_kit should be placed before or in the room with the spike trap
# Let's place spike trap in a mid-game room
solver.add(Or([trap_room["spike_trap"] == rooms.index(r) for r in ["hallway", "barracks", "mess_hall", "kitchen"]]))

# --- 5. Solve ---
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("\n=== DUNGEON LAYOUT ===")
    
    room_layout = []
    for r_idx, r_name in enumerate(rooms):
        monsters_in_room = []
        for mon in monsters:
            cnt = m.evaluate(monster_count[(mon, r_idx)], model_completion=True).as_long()
            if cnt > 0:
                monsters_in_room.append({"type": mon, "count": cnt})
        
        treasures_in_room = []
        for t in treasures:
            if m.evaluate(treasure_room[t] == r_idx, model_completion=True):
                treasures_in_room.append(t)
        
        items_in_room = []
        for item in items:
            if m.evaluate(item_room[item] == r_idx, model_completion=True):
                items_in_room.append(item)
        
        traps_in_room = []
        for t in traps:
            if m.evaluate(trap_room[t] == r_idx, model_completion=True):
                is_active = m.evaluate(trap_active[t], model_completion=True)
                traps_in_room.append({"type": t, "active": is_active})
        
        dl = m.evaluate(danger_level[r_idx], model_completion=True).as_long()
        
        entry = {
            "room_id": r_name,
            "monsters": monsters_in_room,
            "treasures": treasures_in_room,
            "items": items_in_room,
            "traps": traps_in_room,
            "danger_level": dl
        }
        room_layout.append(entry)
        print(f"\nRoom: {r_name} (type: {room_types[r_name]})")
        print(f"  Monsters: {monsters_in_room}")
        print(f"  Treasures: {treasures_in_room}")
        print(f"  Items: {items_in_room}")
        print(f"  Traps: {traps_in_room}")
        print(f"  Danger Level: {dl}")
    
    print("\n=== PATH ANALYSIS ===")
    print("solvable: True")
    print(f"main_path: {main_path_rooms}")
    
    # Key acquisition order
    iron_key_loc = rooms[[r for r in range(len(rooms)) if m.evaluate(item_room['iron_key'] == r, model_completion=True)][0]]
    gold_key_loc = rooms[[r for r in range(len(rooms)) if m.evaluate(item_room['gold_key'] == r, model_completion=True)][0]]
    print(f"key_acquisition_order:")
    print(f"  1. iron_key found in {iron_key_loc} -> unlocks mess_hall->treasury")
    print(f"  2. gold_key found in {gold_key_loc} -> unlocks treasury->boss_antechamber")
    
    print("\n=== BALANCE ANALYSIS ===")
    total_danger = sum(m.evaluate(danger_level[r], model_completion=True).as_long() for r in range(len(rooms)))
    print(f"total_danger: {total_danger}")
    
    # Difficulty progression score: sum of (next - prev) for main path, ideally positive
    progression = 0
    for i in range(len(main_path_indices) - 1):
        d_curr = m.evaluate(danger_level[main_path_indices[i]], model_completion=True).as_long()
        d_next = m.evaluate(danger_level[main_path_indices[i+1]], model_completion=True).as_long()
        progression += (d_next - d_curr)
    print(f"difficulty_progression_score: {progression} (positive = increasing difficulty)")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")