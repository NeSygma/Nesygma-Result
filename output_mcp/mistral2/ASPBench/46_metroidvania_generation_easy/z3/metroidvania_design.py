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
# reachable[room] = True if the room is reachable from A, considering key requirements
reachable = [Bool(f'reachable_{room}') for room in rooms]

# Start room is reachable
solver.add(reachable[start_room_idx] == True)

# For each room v, it is reachable if there is a connection from a reachable room u to v
# and the key requirements for the connection are satisfied.
for room_idx in range(len(rooms)):
    if room_idx == start_room_idx:
        continue
    # At least one connection to this room must be valid
    possible_connections = [
        And(
            reachable[u_idx],
            Or(
                # No key required
                connection_requires_key[conn_idx] == -1,
                # Key required and u has the key
                (key_bitvector[u_idx] & (1 << connection_requires_key[conn_idx])) != 0
            )
        )
        for conn_idx, (u_idx, v_idx) in enumerate([(connection_from[i], connection_to[i]) for i in range(num_connections)])
        if v_idx == room_idx
    ]
    solver.add(reachable[room_idx] == Or(possible_connections))

# All rooms must be reachable
solver.add(And(reachable))

# --- No Circular Dependencies ---
# Ensure that no key is required to obtain itself.
# For each key k, the room where k is located must not require k to reach it.
for key_idx, key in enumerate(keys):
    loc_room_idx = item_locations[key]
    # For each connection to loc_room_idx, if it requires a key, it must not require key_idx
    for conn_idx in range(num_connections):
        solver.add(
            Implies(
                And(
                    connection_to[conn_idx] == loc_room_idx,
                    connection_requires_key[conn_idx] != -1
                ),
                connection_requires_key[conn_idx] != key_idx
            )
        )

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
        reach = model[reachable[room_idx]]
        print(f"Room {room} is reachable: {is_true(reach)}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")