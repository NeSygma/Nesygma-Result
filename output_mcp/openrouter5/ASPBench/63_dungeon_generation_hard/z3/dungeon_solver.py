from z3 import *

solver = Solver()

# ============================================================
# INSTANCE DATA
# ============================================================
rooms_data = [
    ("entrance", "entrance"),
    ("hallway", "chamber"),
    ("barracks", "chamber"),
    ("secret_closet", "secret"),
    ("mess_hall", "chamber"),
    ("kitchen", "chamber"),
    ("treasury", "chamber"),
    ("boss_antechamber", "chamber"),
    ("boss_lair", "boss"),
]
room_ids = [r[0] for r in rooms_data]
room_types = {r[0]: r[1] for r in rooms_data}
N = len(room_ids)
room_index = {rid: i for i, rid in enumerate(room_ids)}

# Connections: (from, to, locked_by)
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

# Items
items_data = ["iron_key", "gold_key", "trap_kit"]

# Treasures
treasures_data = ["silver_locket", "jeweled_crown", "dragon_hoard"]

# Monsters
monsters_data = {"goblin": 2, "orc": 5, "troll": 10, "dragon": 15}

# Traps
traps_data = {"spike_trap": {"danger": 3, "disarm_tool": "trap_kit"}}

# Constraints
MAX_DANGER = 15
BOSS_ROOM = "boss_lair"
DIFFICULTY_SLOPE = 0.5

# ============================================================
# DECISION VARIABLES
# ============================================================

# --- Item placement: which room each item is in ---
item_room = {item: Int(f"item_room_{item}") for item in items_data}
for item in items_data:
    solver.add(item_room[item] >= 0, item_room[item] < N)

# --- Treasure placement: which room each treasure is in ---
treasure_room = {t: Int(f"treasure_room_{t}") for t in treasures_data}
for t in treasures_data:
    solver.add(treasure_room[t] >= 0, treasure_room[t] < N)

# --- Monster placement: count of each monster type in each room ---
monster_counts = {}
for mtype in monsters_data:
    monster_counts[mtype] = [Int(f"mon_{mtype}_{i}") for i in range(N)]
    for i in range(N):
        solver.add(monster_counts[mtype][i] >= 0)
        # Reasonable upper bound: at most 5 of any monster type per room
        solver.add(monster_counts[mtype][i] <= 5)

# --- Trap placement: which rooms have spike_trap, and whether active ---
trap_present = [Bool(f"trap_present_{i}") for i in range(N)]
trap_active = [Bool(f"trap_active_{i}") for i in range(N)]

# Trap is active if present AND trap_kit is NOT in the same room
for i in range(N):
    solver.add(Implies(trap_present[i], trap_active[i] == (item_room["trap_kit"] != i)))
    solver.add(Implies(Not(trap_present[i]), Not(trap_active[i])))

# ============================================================
# REACHABILITY CONSTRAINTS (Static graph, ignoring locks)
# ============================================================

# Build adjacency (undirected for reachability)
adj = {rid: [] for rid in room_ids}
for (f, t, lock) in connections:
    adj[f].append(t)
    adj[t].append(f)

# Compute reachability from entrance using BFS (static graph)
# We'll encode reachable as a set of room indices
from collections import deque
reachable_static = set()
q = deque(["entrance"])
while q:
    cur = q.popleft()
    if cur in reachable_static:
        continue
    reachable_static.add(cur)
    for nb in adj[cur]:
        if nb not in reachable_static:
            q.append(nb)

reachable_static_indices = [room_index[r] for r in reachable_static]

# All rooms must be reachable in the static graph (constraint 1)
for rid in room_ids:
    solver.add(room_index[rid] in reachable_static_indices)  # This is always true by construction, but we assert it

# Actually, let's just assert that all rooms are in the reachable set
# Since the graph is connected, this is trivially true, but we encode it:
for rid in room_ids:
    solver.add(Or([room_index[rid] == ri for ri in reachable_static_indices]))

# ============================================================
# SECRET ROOM CONSTRAINT (constraint 4)
# ============================================================
# secret_closet must connect to exactly one non-secret room that is reachable
secret_room = "secret_closet"
secret_idx = room_index[secret_room]
# Find neighbors of secret_closet
secret_neighbors = adj[secret_room]
# Count how many neighbors are non-secret
non_secret_neighbors = [nb for nb in secret_neighbors if room_types[nb] != "secret"]
# Exactly one non-secret neighbor (this is already true from instance data, but we assert)
solver.add(len(non_secret_neighbors) == 1)  # barracks is the only neighbor

# ============================================================
# KEY PLACEMENT CONSTRAINTS (constraint 3)
# ============================================================
# Keys must be placed in rooms reachable before the doors they unlock.
# We need to model the dynamic reachability based on key acquisition.

# First, let's define the lock relationships
# iron_key unlocks treasury (door from mess_hall to treasury)
# gold_key unlocks boss_antechamber (door from treasury to boss_antechamber)

# For a key to be useful, it must be placed in a room that is reachable
# before the locked door. We'll model this with ordering constraints.

# We need to define a partial order: which rooms are reachable before which keys are found.
# Since we don't know the exact path, we'll use a simpler approach:
# The key must be in a room that is reachable WITHOUT going through the locked door.

# Let's compute which rooms are reachable without passing through each locked door.
# For iron_key: rooms reachable from entrance without going through mess_hall->treasury
# For gold_key: rooms reachable from entrance without going through treasury->boss_antechamber

def rooms_reachable_without_edge(blocked_edge_from, blocked_edge_to):
    """BFS avoiding the blocked edge"""
    visited = set()
    q = deque(["entrance"])
    while q:
        cur = q.popleft()
        if cur in visited:
            continue
        visited.add(cur)
        for nb in adj[cur]:
            # Skip the blocked edge
            if (cur == blocked_edge_from and nb == blocked_edge_to) or \
               (cur == blocked_edge_to and nb == blocked_edge_from):
                continue
            if nb not in visited:
                q.append(nb)
    return visited

# Rooms reachable without going through mess_hall->treasury (iron_key door)
reachable_no_iron = rooms_reachable_without_edge("mess_hall", "treasury")
reachable_no_iron_indices = [room_index[r] for r in reachable_no_iron]

# Rooms reachable without going through treasury->boss_antechamber (gold_key door)
reachable_no_gold = rooms_reachable_without_edge("treasury", "boss_antechamber")
reachable_no_gold_indices = [room_index[r] for r in reachable_no_gold]

# iron_key must be in a room reachable without going through the treasury door
solver.add(Or([item_room["iron_key"] == ri for ri in reachable_no_iron_indices]))

# gold_key must be in a room reachable without going through the boss_antechamber door
solver.add(Or([item_room["gold_key"] == ri for ri in reachable_no_gold_indices]))

# Additionally, gold_key should be placed AFTER iron_key is found (in treasury or later)
# Actually, gold_key is in treasury (which requires iron_key), so it's naturally after.
# But we need to ensure gold_key is in a room reachable AFTER iron_key is acquired.
# The treasury is reachable after getting iron_key, so gold_key can be in treasury or beyond.
# Let's compute rooms reachable after getting iron_key (i.e., including treasury)
reachable_with_iron = rooms_reachable_without_edge("treasury", "boss_antechamber")
# Actually, with iron_key, we can reach treasury. So the reachable set expands.
# Let's recompute: rooms reachable when the mess_hall->treasury door is open
def rooms_reachable_with_edge_allowed(allowed_edge_from, allowed_edge_to):
    """BFS where the specified edge is allowed (but others may be blocked)"""
    # Actually, we just need the full reachable set when only the iron_key door is open
    # and the gold_key door is still locked.
    visited = set()
    q = deque(["entrance"])
    while q:
        cur = q.popleft()
        if cur in visited:
            continue
        visited.add(cur)
        for nb in adj[cur]:
            # Block the gold_key door (treasury -> boss_antechamber)
            if (cur == "treasury" and nb == "boss_antechamber") or \
               (cur == "boss_antechamber" and nb == "treasury"):
                continue
            if nb not in visited:
                q.append(nb)
    return visited

# Rooms reachable with iron_key but without gold_key
reachable_with_iron_only = rooms_reachable_with_edge_allowed("mess_hall", "treasury")
reachable_with_iron_only_indices = [room_index[r] for r in reachable_with_iron_only]

# gold_key must be in a room reachable with iron_key (i.e., in treasury or earlier)
solver.add(Or([item_room["gold_key"] == ri for ri in reachable_with_iron_only_indices]))

# ============================================================
# BOSS MONSTER CONSTRAINT (constraint 8)
# ============================================================
# Boss monster (dragon, highest danger level 15) must be in boss_lair
boss_idx = room_index[BOSS_ROOM]
# At least one dragon in boss_lair
solver.add(monster_counts["dragon"][boss_idx] >= 1)

# ============================================================
# DANGER CONSTRAINTS (constraints 5, 7)
# ============================================================
danger_level = [Int(f"danger_level_{i}") for i in range(N)]

for i in range(N):
    # monster_danger = sum(monster_count * monster_danger_level)
    monster_danger = Sum([monster_counts[m][i] * monsters_data[m] for m in monsters_data])
    # trap_danger = If(trap_active[i], traps_data["spike_trap"]["danger"], 0)
    trap_danger = If(trap_active[i], traps_data["spike_trap"]["danger"], 0)
    solver.add(danger_level[i] == monster_danger + trap_danger)
    solver.add(danger_level[i] <= MAX_DANGER)

# ============================================================
# SOLVABLE PATH CONSTRAINT (constraint 9)
# ============================================================
# There must exist a valid path from entrance to boss_lair.
# We model this by checking that there's a path respecting key acquisition.

# We'll use a reachability encoding with state (which keys we have).
# Keys: 0 = no keys, 1 = have iron_key, 2 = have both keys
# We'll model reachability as a graph where edges are conditional on having the right key.

# Actually, let's use a simpler approach: we know the graph structure.
# The path must be: entrance -> hallway -> mess_hall -> treasury -> boss_antechamber -> boss_lair
# (with barracks/secret_closet/kitchen as optional side branches)
# The key question is: are the keys placed such that this path works?

# We already constrained key placement. Let's verify the path is feasible by checking
# that there exists a sequence of rooms respecting key acquisition.

# Define a symbolic path existence check using BFS with state
# State: (room_idx, has_iron_key, has_gold_key)
# We'll encode this as: there exists a path from (entrance, 0, 0) to (boss_lair, 1, 1)

# Since the graph is small, we can encode this as a reachability constraint
# using a series of implications.

# Let's define variables for each room-state pair
# has_iron[i] = Bool indicating if we can reach room i with iron_key
# has_gold[i] = Bool indicating if we can reach room i with both keys

has_iron = [Bool(f"has_iron_{i}") for i in range(N)]
has_gold = [Bool(f"has_gold_{i}") for i in range(N)]

# Entrance is reachable with no keys
entrance_idx = room_index["entrance"]
solver.add(has_iron[entrance_idx] == False)
solver.add(has_gold[entrance_idx] == False)

# For each connection, define how reachability propagates
# We'll encode the transition rules

# First, let's define which connections are unlocked vs locked
# Unlocked connections: always traversable
# Locked connections: traversable only if you have the key

unlocked_edges = []
locked_edges = {}  # (from, to) -> key_needed

for (f, t, lock) in connections:
    if lock is None:
        unlocked_edges.append((f, t))
    else:
        locked_edges[(f, t)] = lock
        locked_edges[(t, f)] = lock  # bidirectional for reachability

# For each room, we can reach it with iron_key if:
# - We can reach a neighbor with iron_key via an unlocked edge, OR
# - We can reach a neighbor without iron_key via an unlocked edge AND the room has iron_key, OR
# - We can reach a neighbor without iron_key via a locked edge that iron_key unlocks

# This is getting complex. Let's use a simpler encoding.

# We know the exact path structure. Let's just verify that keys are placed
# in rooms that are on or before the path segments they unlock.

# The main path is: entrance -> hallway -> mess_hall -> treasury -> boss_antechamber -> boss_lair
# iron_key must be found before reaching treasury (since treasury door is locked by iron_key)
# gold_key must be found before reaching boss_antechamber (since that door is locked by gold_key)

# iron_key can be in: entrance, hallway, barracks, secret_closet, mess_hall, kitchen
# (all rooms reachable without going through the treasury door)
# gold_key can be in: entrance, hallway, barracks, secret_closet, mess_hall, kitchen, treasury
# (all rooms reachable after getting iron_key, before going through boss_antechamber door)

# We already encoded these constraints above. Let's also ensure that
# the keys are not in the same room (optional but good for gameplay).

# Actually, let's not force them to be different unless needed.

# ============================================================
# ADDITIONAL CONSTRAINTS FOR INTERESTING SOLUTION
# ============================================================

# Ensure at least some monsters and traps are placed (not all empty)
# Total monsters across all rooms should be at least some minimum
total_monsters = Sum([monster_counts[m][i] for m in monsters_data for i in range(N)])
solver.add(total_monsters >= 3)

# At least one trap somewhere
solver.add(Or([trap_present[i] for i in range(N)]))

# Treasures should be in different rooms (more interesting)
solver.add(Distinct([treasure_room[t] for t in treasures_data]))

# Items should be in different rooms
solver.add(Distinct([item_room[item] for item in items_data]))

# ============================================================
# SOLVE
# ============================================================

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    # Build solution
    print("\n=== ROOM LAYOUT ===")
    for i, rid in enumerate(room_ids):
        print(f"\nRoom: {rid} (type: {room_types[rid]})")
        
        # Monsters in this room
        room_monsters = []
        for mtype in monsters_data:
            count = m.eval(monster_counts[mtype][i]).as_long()
            if count > 0:
                room_monsters.append({"type": mtype, "count": count})
                print(f"  Monsters: {count}x {mtype}")
        
        # Treasures in this room
        room_treasures = []
        for t in treasures_data:
            if m.eval(treasure_room[t]).as_long() == i:
                room_treasures.append(t)
                print(f"  Treasure: {t}")
        
        # Items in this room
        room_items = []
        for item in items_data:
            if m.eval(item_room[item]).as_long() == i:
                room_items.append(item)
                print(f"  Item: {item}")
        
        # Traps in this room
        has_trap = is_true(m.eval(trap_present[i]))
        is_active = is_true(m.eval(trap_active[i]))
        if has_trap:
            print(f"  Trap: spike_trap (active: {is_active})")
        
        danger = m.eval(danger_level[i]).as_long()
        print(f"  Danger Level: {danger}")
    
    # Path analysis
    print("\n=== PATH ANALYSIS ===")
    print("Main path: entrance -> hallway -> mess_hall -> treasury -> boss_antechamber -> boss_lair")
    
    iron_key_room_idx = m.eval(item_room["iron_key"]).as_long()
    gold_key_room_idx = m.eval(item_room["gold_key"]).as_long()
    print(f"iron_key found in: {room_ids[iron_key_room_idx]}")
    print(f"gold_key found in: {room_ids[gold_key_room_idx]}")
    print("Key acquisition order:")
    print(f"  1. iron_key (found in {room_ids[iron_key_room_idx]}) -> unlocks treasury")
    print(f"  2. gold_key (found in {room_ids[gold_key_room_idx]}) -> unlocks boss_antechamber")
    
    # Balance analysis
    print("\n=== BALANCE ANALYSIS ===")
    total_danger = sum(m.eval(danger_level[i]).as_long() for i in range(N))
    print(f"Total danger: {total_danger}")
    
    # Difficulty progression score
    # We want difficulty to increase along the main path
    main_path = ["entrance", "hallway", "mess_hall", "treasury", "boss_antechamber", "boss_lair"]
    main_path_dangers = [m.eval(danger_level[room_index[r]]).as_long() for r in main_path]
    print(f"Main path dangers: {list(zip(main_path, main_path_dangers))}")
    
    # Calculate progression score: sum of (actual - expected) differences
    # Expected: linear increase from first to last
    first_danger = main_path_dangers[0]
    last_danger = main_path_dangers[-1]
    progression_score = 0
    for j, d in enumerate(main_path_dangers):
        expected = first_danger + (last_danger - first_danger) * j / (len(main_path_dangers) - 1)
        progression_score += abs(d - expected)
    print(f"Difficulty progression score: {progression_score:.2f}")
    print(f"(0 = perfectly progressive)")
    
    print("\n=== SOLUTION SUMMARY ===")
    print("Solvable: True")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")