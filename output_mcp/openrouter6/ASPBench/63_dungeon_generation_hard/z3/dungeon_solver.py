from z3 import *

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# Define rooms
rooms = ["entrance", "hallway", "barracks", "secret_closet", "mess_hall", "kitchen", "treasury", "boss_antechamber", "boss_lair"]
room_index = {r: i for i, r in enumerate(rooms)}

# Define items
items = ["iron_key", "gold_key", "trap_kit"]
# Define treasures
treasures = ["silver_locket", "jeweled_crown", "dragon_hoard"]
# Define monster types
monster_types = ["goblin", "orc", "troll", "dragon"]
monster_danger = {"goblin": 2, "orc": 5, "troll": 10, "dragon": 15}

# Define trap
trap_type = "spike_trap"
trap_danger = 3

# Variables for monster counts
monster_count = {}
for t in monster_types:
    for r in rooms:
        monster_count[(t, r)] = Int(f"monster_{t}_{r}")

# Variables for treasure placement
treasure_in_room = {}
for tr in treasures:
    for r in rooms:
        treasure_in_room[(tr, r)] = Bool(f"treasure_{tr}_{r}")

# Variables for item placement
item_in_room = {}
for it in items:
    for r in rooms:
        item_in_room[(it, r)] = Bool(f"item_{it}_{r}")

# Variable for spike trap count in each room
spike_trap_count = {}
for r in rooms:
    spike_trap_count[r] = Int(f"spike_trap_{r}")

solver = Solver()

# Constraint: each treasure in exactly one room
for tr in treasures:
    solver.add(Sum([If(treasure_in_room[(tr, r)], 1, 0) for r in rooms]) == 1)

# Constraint: each item in exactly one room
for it in items:
    solver.add(Sum([If(item_in_room[(it, r)], 1, 0) for r in rooms]) == 1)

# Constraint: spike trap in exactly one room
solver.add(Sum([spike_trap_count[r] for r in rooms]) == 1)
for r in rooms:
    solver.add(Or(spike_trap_count[r] == 0, spike_trap_count[r] == 1))

# Constraint: monster counts are non-negative
for t in monster_types:
    for r in rooms:
        solver.add(monster_count[(t, r)] >= 0)

# Constraint: dragon must be in boss_lair (exactly one)
solver.add(monster_count[("dragon", "boss_lair")] == 1)

# Constraint: danger per room <= 15
for r in rooms:
    danger = Sum([monster_count[(t, r)] * monster_danger[t] for t in monster_types])
    # Trap is active if spike_trap_count[r] == 1 and trap_kit not in room r
    trap_active = And(spike_trap_count[r] == 1, Not(item_in_room[("trap_kit", r)]))
    danger += If(trap_active, trap_danger, 0)
    solver.add(danger <= 15)

# Constraint: iron_key placement (must be in rooms reachable without iron_key)
iron_key_rooms = ["entrance", "hallway", "barracks", "secret_closet", "mess_hall", "kitchen"]
solver.add(Or([item_in_room[("iron_key", r)] for r in iron_key_rooms]))

# Constraint: gold_key placement (must be in rooms reachable without gold_key)
gold_key_rooms = ["entrance", "hallway", "barracks", "secret_closet", "mess_hall", "kitchen", "treasury"]
solver.add(Or([item_in_room[("gold_key", r)] for r in gold_key_rooms]))

# Constraint: secret room connection (already satisfied by graph)

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract placement from model
    def get_int_value(var):
        return int(str(model.eval(var, model_completion=True)))
    
    def get_bool_value(var):
        val = model.eval(var, model_completion=True)
        return str(val) == "True"
    
    # Build room_layout
    room_layout = []
    for r in rooms:
        # Monsters in this room
        monsters = []
        for t in monster_types:
            count = get_int_value(monster_count[(t, r)])
            if count > 0:
                monsters.append({"type": t, "count": count})
        
        # Treasures in this room
        treasures_in_room = []
        for tr in treasures:
            if get_bool_value(treasure_in_room[(tr, r)]):
                treasures_in_room.append(tr)
        
        # Items in this room
        items_in_room = []
        for it in items:
            if get_bool_value(item_in_room[(it, r)]):
                items_in_room.append(it)
        
        # Traps in this room
        traps = []
        trap_count = get_int_value(spike_trap_count[r])
        if trap_count > 0:
            # Trap is active if trap_kit not in this room
            trap_kit_present = get_bool_value(item_in_room[("trap_kit", r)])
            active = not trap_kit_present
            traps.append({"type": trap_type, "active": active})
        
        # Calculate danger level
        danger_level = 0
        for t in monster_types:
            count = get_int_value(monster_count[(t, r)])
            danger_level += count * monster_danger[t]
        if trap_count > 0 and not get_bool_value(item_in_room[("trap_kit", r)]):
            danger_level += trap_danger
        
        room_layout.append({
            "room_id": r,
            "monsters": monsters,
            "treasures": treasures_in_room,
            "items": items_in_room,
            "traps": traps,
            "danger_level": danger_level
        })
    
    # Compute path analysis
    # Define graph with lock information
    graph = {
        "entrance": [("hallway", None)],
        "hallway": [("barracks", None), ("mess_hall", None)],
        "barracks": [("secret_closet", None)],
        "secret_closet": [],
        "mess_hall": [("kitchen", None), ("treasury", "iron_key")],
        "kitchen": [],
        "treasury": [("boss_antechamber", "gold_key")],
        "boss_antechamber": [("boss_lair", None)],
        "boss_lair": []
    }
    
    # Get key locations from model
    key_locations = {}
    for key in ["iron_key", "gold_key"]:
        for r in rooms:
            if get_bool_value(item_in_room[(key, r)]):
                key_locations[key] = r
                break
    
    # BFS to find shortest path from entrance to boss_lair
    from collections import deque
    
    def find_path():
        # State: (current_room, keys_collected)
        start_state = ("entrance", frozenset())
        queue = deque([(start_state, [])])
        visited = set([start_state])
        
        while queue:
            (room, keys), path = queue.popleft()
            if room == "boss_lair":
                return path + [room]
            
            for next_room, required_key in graph[room]:
                # Check if we can traverse this edge
                can_traverse = True
                new_keys = keys
                if required_key:
                    if required_key not in keys:
                        # Check if we can pick up the key in current room or along the path
                        # For simplicity, we assume we pick up keys when we visit their room
                        # We'll check if the key is in a room we've already visited
                        key_loc = key_locations.get(required_key)
                        if key_loc and key_loc in [p for p in path] + [room]:
                            new_keys = keys | {required_key}
                        else:
                            can_traverse = False
                
                if can_traverse:
                    new_state = (next_room, new_keys)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, path + [room]))
        
        return None
    
    main_path = find_path()
    solvable = main_path is not None
    
    # Compute key acquisition order
    key_acquisition_order = []
    if solvable:
        keys_found = set()
        for room in main_path:
            for key in ["iron_key", "gold_key"]:
                if key not in keys_found and key_locations.get(key) == room:
                    keys_found.add(key)
                    # Find what the key unlocks
                    unlocks = None
                    if key == "iron_key":
                        unlocks = "treasury"
                    elif key == "gold_key":
                        unlocks = "boss_antechamber"
                    key_acquisition_order.append({
                        "key": key,
                        "found_in": room,
                        "unlocks": unlocks
                    })
    
    path_analysis = {
        "solvable": solvable,
        "main_path": main_path if solvable else [],
        "key_acquisition_order": key_acquisition_order
    }
    
    # Compute balance analysis
    total_danger = sum(room["danger_level"] for room in room_layout)
    
    # Difficulty progression score: slope of danger along main path
    if solvable and len(main_path) > 1:
        dangers = []
        for room_id in main_path:
            for room in room_layout:
                if room["room_id"] == room_id:
                    dangers.append(room["danger_level"])
                    break
        # Linear regression slope
        n = len(dangers)
        if n > 1:
            x = list(range(n))
            sum_x = sum(x)
            sum_y = sum(dangers)
            sum_xy = sum(x[i] * dangers[i] for i in range(n))
            sum_x2 = sum(x[i] * x[i] for i in range(n))
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        else:
            slope = 0
    else:
        slope = 0
    
    balance_analysis = {
        "total_danger": total_danger,
        "difficulty_progression_score": float(slope)
    }
    
    # Build instance data
    instance = {
        "rooms": [{"id": r, "type": "entrance" if r == "entrance" else "boss" if r == "boss_lair" else "secret" if r == "secret_closet" else "chamber"} for r in rooms],
        "items": [{"id": it, "type": "key" if it in ["iron_key", "gold_key"] else "tool"} for it in items],
        "treasures": [{"id": tr, "value": 100 if tr == "silver_locket" else 500 if tr == "jeweled_crown" else 1000} for tr in treasures],
        "monsters": [{"id": t, "danger_level": monster_danger[t]} for t in monster_types],
        "traps": [{"id": trap_type, "danger_level": trap_danger, "disarm_tool": "trap_kit"}]
    }
    
    # Print solution
    print("instance:", instance)
    print("solution.room_layout:", room_layout)
    print("solution.path_analysis:", path_analysis)
    print("solution.balance_analysis:", balance_analysis)
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")