from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Rooms: A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7
# Keys: key1=0, key2=1, key3=2

solver = Solver()

# Decision variables for connections: up to 12 connections
# Each connection is (from_room, to_room, required_key)
# required_key: -1 for no key, 0 for key1, 1 for key2, 2 for key3
conn_from = [Int(f"conn_from_{i}") for i in range(12)]
conn_to = [Int(f"conn_to_{i}") for i in range(12)]
conn_key = [Int(f"conn_key_{i}") for i in range(12)]

# Decision variables for key locations: each key is in exactly one room
key_room = [Int(f"key_room_{k}") for k in range(3)]

# Room reachability: reachable[i] is True if room i is reachable from A
# Use Z3 Array to avoid symbolic indexing issues
reachable = [Bool(f"reachable_{chr(65+i)}") for i in range(8)]

# Key possession: has_key[k] is True if key k has been obtained
has_key = [Bool(f"has_key_{k}") for k in range(3)]

# Constraints

# 1. Starting room A is reachable
solver.add(reachable[0] == True)

# 2. Each key is located in exactly one room (0-7)
for k in range(3):
    solver.add(key_room[k] >= 0, key_room[k] <= 7)

# 3. For each key, has_key[k] is True if its room is reachable
# Use Or-loop pattern to avoid symbolic indexing
for k in range(3):
    solver.add(has_key[k] == Or([And(key_room[k] == i, reachable[i]) for i in range(8)]))

# 4. For each connection, encode reachability constraints
# Use Or-loop pattern to avoid symbolic indexing
for i in range(12):
    # Connection exists only if from_room and to_room are valid
    solver.add(conn_from[i] >= 0, conn_from[i] <= 7)
    solver.add(conn_to[i] >= 0, conn_to[i] <= 7)
    # required_key is -1 or 0-2
    solver.add(Or(conn_key[i] == -1, And(conn_key[i] >= 0, conn_key[i] <= 2)))
    
    # If the connection is "active" (i.e., the conditions are met), then reachable[to] is True.
    # We model this as: if reachable[from] and (no key or has_key[required_key]), then reachable[to] is True.
    # Use Or-loop pattern to avoid symbolic indexing
    solver.add(Implies(
        And(
            Or([And(conn_from[i] == j, reachable[j]) for j in range(8)]),
            Or(
                conn_key[i] == -1,
                Or([And(conn_key[i] == k, has_key[k]) for k in range(3)])
            )
        ),
        Or([And(conn_to[i] == j, reachable[j]) for j in range(8)])
    ))

# 5. All rooms must be reachable
for i in range(8):
    solver.add(reachable[i] == True)

# 6. Ensure that connections are not self-loops (optional, but reasonable)
for i in range(12):
    solver.add(conn_from[i] != conn_to[i])

# Check for a solution
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("\nConnections:")
    for i in range(12):
        from_room = model[conn_from[i]]
        to_room = model[conn_to[i]]
        required_key = model[conn_key[i]]
        key_name = "none"
        if required_key.as_long() == 0:
            key_name = "key1"
        elif required_key.as_long() == 1:
            key_name = "key2"
        elif required_key.as_long() == 2:
            key_name = "key3"
        print(f"  Connection {i+1}: {chr(65+from_room.as_long())} -> {chr(65+to_room.as_long())} (requires {key_name})")
    
    print("\nKey locations:")
    for k in range(3):
        room = model[key_room[k]]
        key_name = f"key{k+1}"
        print(f"  {key_name} is in room {chr(65+room.as_long())}")
    
    print("\nReachability:")
    for i in range(8):
        print(f"  Room {chr(65+i)} is reachable: {model[reachable[i]]}")
    
    print("\nKey possession:")
    for k in range(3):
        print(f"  has_key_{k}: {model[has_key[k]]}")
    
    # Verify all rooms are reachable in the model
    all_reachable = all(model[reachable[i]] for i in range(8))
    print(f"\nAll rooms reachable: {all_reachable}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")