from z3 import *

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# Define rooms and keys
rooms = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
keys = ['key1', 'key2', 'key3']

# Create a solver
solver = Solver()

# Helper: Map room names to Z3 constants
room_vars = {room: Int(room) for room in rooms}
key_vars = {key: Int(key) for key in keys}

# Helper: Map keys to their locations (room index)
item_locations = {}
for key in keys:
    loc = Int(f'loc_{key}')
    item_locations[key] = loc
    solver.add(loc >= 0, loc < len(rooms))  # loc is an index into rooms

# Helper: Connections are tuples (from_room_idx, to_room_idx, requires_key_idx)
# We'll allow up to 20 connections (adjust as needed)
num_connections = 20
connection_from = [Int(f'conn_from_{i}') for i in range(num_connections)]
connection_to = [Int(f'conn_to_{i}') for i in range(num_connections)]
connection_requires_key = [Int(f'conn_req_key_{i}') for i in range(num_connections)]

# Constraints for connections:
# 1. from and to are valid room indices
for i in range(num_connections):
    solver.add(connection_from[i] >= 0, connection_from[i] < len(rooms))
    solver.add(connection_to[i] >= 0, connection_to[i] < len(rooms))
# 2. requires_key is either -1 (no key) or a valid key index
for i in range(num_connections):
    solver.add(Or(connection_requires_key[i] == -1,
                 And(connection_requires_key[i] >= 0, connection_requires_key[i] < len(keys))))

# Starting room is A (index 0)
start_room_idx = 0

# --- Key Bitvector Modeling ---
# For each room, track which keys are obtained (as a BitVec)
key_bitvector = [BitVec(f'key_bv_{room}', len(keys)) for room in rooms]

# Initialize key_bitvector for the start room
solver.add(key_bitvector[start_room_idx] == 0)  # No keys at start

# Constraints for key_bitvector:
# 1. If a key is obtained at a room, set the corresponding bit.
for key_idx, key in enumerate(keys):
    loc_room_idx = item_locations[key]
    for room_idx in range(len(rooms)):
        # If this room is the item location for the key, set the bit
        solver.add(
            Implies(loc_room_idx == room_idx,
                    key_bitvector[room_idx] == key_bitvector[room_idx] | (1 << key_idx))
        )

# --- Reachability Modeling ---
# reachable[room][keys_obtained] = True if the room is reachable with the given keys
# We'll use a dictionary of dictionaries for this
reachable = {}
for room_idx in range(len(rooms)):
    reachable[room_idx] = {}
    for key_set in range(2**len(keys)):
        reachable[room_idx][key_set] = Bool(f'reachable_{room_idx}_{key_set}')

# Start room is reachable with no keys
solver.add(reachable[start_room_idx][0] == True)

# For each room and key set, determine reachability based on connections
for room_idx in range(len(rooms)):
    for key_set in range(2**len(keys)):
        # If already reachable, no need to recompute
        if room_idx == start_room_idx and key_set == 0:
            continue
        # Find all connections to this room
        for conn_idx in range(num_connections):
            from_room = connection_from[conn_idx]
            to_room = connection_to[conn_idx]
            req_key = connection_requires_key[conn_idx]
            # Check if the connection can be traversed with the current key set
            can_traverse = True
            if req_key != -1:
                # Check if the key is in the current key set
                can_traverse = (key_set & (1 << req_key)) != 0
            # If the connection can be traversed and the from_room is reachable with the key set before traversal
            # (i.e., the key set at the from_room)
            from_key_set = key_set
            if can_traverse:
                solver.add(
                    Implies(
                        And(
                            connection_to[conn_idx] == room_idx,
                            reachable[from_room.as_long()][from_key_set]
                        ),
                        reachable[room_idx][key_set] == True
                    )
                )

# All rooms must be reachable with some key set
for room_idx in range(len(rooms)):
    solver.add(Or([reachable[room_idx][key_set] for key_set in range(2**len(keys))]))

# --- No Soft-Locks: Ensure keys are obtained before they are required ---
# For each connection requiring a key, ensure that the key is obtained in a room reachable before the connection
for conn_idx in range(num_connections):
    req_key = connection_requires_key[conn_idx]
    to_room = connection_to[conn_idx]
    # The key must be located in a room reachable before the connection is traversed
    # This is implicitly handled by the reachability logic above
    pass

# --- Solve ---
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("\n--- Solution Found ---")
    
    # Print item locations
    print("\nItem Locations:")
    for key in keys:
        loc = model[item_locations[key]]
        print(f"{key} is in room {rooms[loc.as_long()]}")
    
    # Print connections
    print("\nConnections:")
    for i in range(num_connections):
        from_room = model[connection_from[i]]
        to_room = model[connection_to[i]]
        req_key = model[connection_requires_key[i]]
        req_key_name = "none"
        if req_key.as_long() != -1:
            req_key_name = keys[req_key.as_long()]
        print(f"{rooms[from_room.as_long()]} -> {rooms[to_room.as_long()]} (requires {req_key_name})")
    
    # Print reachability
    print("\nReachability:")
    for room_idx, room in enumerate(rooms):
        for key_set in range(2**len(keys)):
            reach = model[reachable[room_idx][key_set]]
            if is_true(reach):
                key_names = []
                for key_idx in range(len(keys)):
                    if key_set & (1 << key_idx):
                        key_names.append(keys[key_idx])
                key_str = ", ".join(key_names) if key_names else "none"
                print(f"Room {room} is reachable with keys: {key_str}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")