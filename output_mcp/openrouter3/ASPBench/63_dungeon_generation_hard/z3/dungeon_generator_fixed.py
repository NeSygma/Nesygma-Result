from z3 import *

# ==================== INSTANCE DATA ====================
rooms_data = [
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
    ("entrance", "hallway", None),
    ("hallway", "barracks", None),
    ("barracks", "secret_closet", None),
    ("hallway", "mess_hall", None),
    ("mess_hall", "kitchen", None),
    ("mess_hall", "treasury", "iron_key"),
    ("treasury", "boss_antechamber", "gold_key"),
    ("boss_antechamber", "boss_lair", None)
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

# ==================== Z3 MODEL ====================
solver = Solver()

# Map room IDs to indices
room_ids = [r["id"] for r in rooms_data]
room_index = {room_id: i for i, room_id in enumerate(room_ids)}
num_rooms = len(room_ids)

# Decision variables for room contents
# For each room, which monsters are present (count)
monster_counts = {}
for room in room_ids:
    for monster in monsters:
        var_name = f"monster_{room}_{monster['type']}"
        monster_counts[(room, monster["type"])] = Int(var_name)
        solver.add(monster_counts[(room, monster["type"])] >= 0)

# For each room, which treasures are present (0/1)
treasure_presence = {}
for room in room_ids:
    for treasure in treasures:
        var_name = f"treasure_{room}_{treasure['id']}"
        treasure_presence[(room, treasure["id"])] = Int(var_name)
        solver.add(Or(treasure_presence[(room, treasure["id"])] == 0, 
                      treasure_presence[(room, treasure["id"])] == 1))

# For each room, which items are present (0/1)
item_presence = {}
for room in room_ids:
    for item in items:
        var_name = f"item_{room}_{item['id']}"
        item_presence[(room, item["id"])] = Int(var_name)
        solver.add(Or(item_presence[(room, item["id"])] == 0, 
                      item_presence[(room, item["id"])] == 1))

# For each room, which traps are active (0/1)
trap_active = {}
for room in room_ids:
    for trap in traps:
        var_name = f"trap_{room}_{trap['type']}"
        trap_active[(room, trap["type"])] = Int(var_name)
        solver.add(Or(trap_active[(room, trap["type"])] == 0, 
                      trap_active[(room, trap["type"])] == 1))

# ==================== CONSTRAINTS ====================

# 1. Each treasure, item, and trap must be placed exactly once
for treasure in treasures:
    solver.add(Sum([treasure_presence[(room, treasure["id"])] for room in room_ids]) == 1)

for item in items:
    solver.add(Sum([item_presence[(room, item["id"])] for room in room_ids]) == 1)

for trap in traps:
    solver.add(Sum([trap_active[(room, trap["type"])] for room in room_ids]) == 1)

# 2. Danger level calculation per room
room_danger = {}
for room in room_ids:
    danger_expr = Sum([
        monster_counts[(room, m["type"])] * m["danger_level"] 
        for m in monsters
    ])
    for trap in traps:
        danger_expr += trap_active[(room, trap["type"])] * trap["danger_level"]
    room_danger[room] = danger_expr
    solver.add(room_danger[room] <= 15)  # Max danger per room

# 3. Boss monster (dragon) must be in boss_lair
solver.add(monster_counts[("boss_lair", "dragon")] >= 1)

# 4. Key-door relationships
# iron_key unlocks mess_hall -> treasury
# gold_key unlocks treasury -> boss_antechamber

# Keys must be placed in rooms reachable before the doors they unlock
# iron_key can be in: entrance, hallway, barracks, secret_closet, mess_hall, kitchen
iron_key_rooms = ["entrance", "hallway", "barracks", "secret_closet", "mess_hall", "kitchen"]
solver.add(Or([item_presence[(room, "iron_key")] == 1 for room in iron_key_rooms]))

# gold_key must be in treasury (since it's needed to unlock boss_antechamber)
solver.add(item_presence[("treasury", "gold_key")] == 1)

# 5. Trap disarm constraint: trap is inactive if trap_kit is in same room
for room in room_ids:
    for trap in traps:
        # If trap_kit is in room, trap must be inactive
        solver.add(Implies(
            item_presence[(room, "trap_kit")] == 1,
            trap_active[(room, trap["type"])] == 0
        ))

# 6. Ensure all rooms have some content (optional, for realism)
for room in room_ids:
    if room != "entrance":
        content_sum = Sum([
            Sum([monster_counts[(room, m["type"])] for m in monsters]),
            Sum([treasure_presence[(room, t["id"])] for t in treasures]),
            Sum([item_presence[(room, i["id"])] for i in items])
        ])
        solver.add(content_sum >= 1)

# 7. Difficulty progression: rooms should have increasing danger
solver.add(room_danger["boss_lair"] >= room_danger["boss_antechamber"])
solver.add(room_danger["boss_antechamber"] >= room_danger["treasury"])

# ==================== CHECK AND OUTPUT ====================
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("\n=== DUNGEON LAYOUT ===")
    
    # Print room contents
    for room in room_ids:
        print(f"\n{room}:")
        
        # Monsters
        monsters_in_room = []
        for monster in monsters:
            count = m.evaluate(monster_counts[(room, monster["type"])])
            # Convert to Python int for comparison
            try:
                count_val = int(str(count))
                if count_val > 0:
                    monsters_in_room.append(f"{monster['type']} x{count_val}")
            except:
                pass
        if monsters_in_room:
            print(f"  Monsters: {', '.join(monsters_in_room)}")
        
        # Treasures
        treasures_in_room = []
        for treasure in treasures:
            present = m.evaluate(treasure_presence[(room, treasure["id"])])
            try:
                present_val = int(str(present))
                if present_val == 1:
                    treasures_in_room.append(treasure["id"])
            except:
                pass
        if treasures_in_room:
            print(f"  Treasures: {', '.join(treasures_in_room)}")
        
        # Items
        items_in_room = []
        for item in items:
            present = m.evaluate(item_presence[(room, item["id"])])
            try:
                present_val = int(str(present))
                if present_val == 1:
                    items_in_room.append(item["id"])
            except:
                pass
        if items_in_room:
            print(f"  Items: {', '.join(items_in_room)}")
        
        # Traps
        traps_in_room = []
        for trap in traps:
            active = m.evaluate(trap_active[(room, trap["type"])])
            try:
                active_val = int(str(active))
                if active_val == 1:
                    traps_in_room.append(f"{trap['type']} (active)")
                else:
                    traps_in_room.append(f"{trap['type']} (inactive)")
            except:
                pass
        if traps_in_room:
            print(f"  Traps: {', '.join(traps_in_room)}")
        
        # Danger level
        danger = m.evaluate(room_danger[room])
        try:
            danger_val = int(str(danger))
            print(f"  Danger Level: {danger_val}")
        except:
            print(f"  Danger Level: {danger}")
    
    # Path analysis
    print("\n=== PATH ANALYSIS ===")
    print("Main path: entrance -> hallway -> mess_hall -> treasury -> boss_antechamber -> boss_lair")
    print("Key acquisition: iron_key found before treasury, gold_key found in treasury")
    print("Solvable: Yes")
    
    # Balance analysis
    total_danger = 0
    for room in room_ids:
        danger = m.evaluate(room_danger[room])
        try:
            total_danger += int(str(danger))
        except:
            pass
    print(f"\n=== BALANCE ANALYSIS ===")
    print(f"Total danger: {total_danger}")
    print("Difficulty progression: Increasing (boss room has highest danger)")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")