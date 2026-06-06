from z3 import *

solver = Solver()

NUM_ROOMS = 8
NUM_KEYS = 3
room_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# === EXPLORATION ORDER ===
# order[r] = step at which room r is first visited (0-based)
order = [Int(f'order_{i}') for i in range(NUM_ROOMS)]
for i in range(NUM_ROOMS):
    solver.add(order[i] >= 0, order[i] < NUM_ROOMS)
solver.add(Distinct(order))
solver.add(order[0] == 0)  # Room A visited first (starting room)

# === KEY LOCATIONS ===
# key_room[k] = room index where key (k+1) is located
key_room = [Int(f'key_room_{k}') for k in range(NUM_KEYS)]
for k in range(NUM_KEYS):
    solver.add(key_room[k] >= 0, key_room[k] < NUM_ROOMS)
solver.add(Distinct(key_room))  # Each key in a different room

# key_obtained[k] = exploration step at which key (k+1) is first collected
key_obtained = [Int(f'key_obtained_{k}') for k in range(NUM_KEYS)]
for k in range(NUM_KEYS):
    # key_obtained[k] equals the order of the room containing key k+1
    solver.add(Or([And(key_room[k] == i, key_obtained[k] == order[i]) for i in range(NUM_ROOMS)]))

# Progressive difficulty: key1 obtained before key2 before key3
solver.add(key_obtained[0] < key_obtained[1])
solver.add(key_obtained[1] < key_obtained[2])

# === CONNECTIONS ===
# has_conn[i][j] = True if directed edge from room i to room j exists
# req_key[i][j] = which key is required (0=none, 1=key1, 2=key2, 3=key3)
has_conn = [[Bool(f'conn_{i}_{j}') if i != j else None for j in range(NUM_ROOMS)] for i in range(NUM_ROOMS)]
req_key = [[Int(f'req_{i}_{j}') if i != j else None for j in range(NUM_ROOMS)] for i in range(NUM_ROOMS)]

for i in range(NUM_ROOMS):
    for j in range(NUM_ROOMS):
        if i != j:
            solver.add(req_key[i][j] >= 0, req_key[i][j] <= NUM_KEYS)
            # If no connection exists, requirement is 0 (irrelevant)
            solver.add(Implies(Not(has_conn[i][j]), req_key[i][j] == 0))

# === STRUCTURAL CONSTRAINTS ===
# Reasonable number of connections (not too sparse, not too dense)
total_conns = Sum([If(has_conn[i][j], 1, 0) for i in range(NUM_ROOMS) for j in range(NUM_ROOMS) if i != j])
solver.add(total_conns >= 9, total_conns <= 18)

# Each key must gate at least one connection
for k in range(NUM_KEYS):
    solver.add(Or([And(has_conn[i][j], req_key[i][j] == k + 1)
                   for i in range(NUM_ROOMS) for j in range(NUM_ROOMS) if i != j]))

# Several connections require no key (basic traversal)
no_key_conns = Sum([If(And(has_conn[i][j], req_key[i][j] == 0), 1, 0)
                    for i in range(NUM_ROOMS) for j in range(NUM_ROOMS) if i != j])
solver.add(no_key_conns >= 5)

# Starting room A must have at least one free (no-key) exit
solver.add(Or([And(has_conn[0][j], req_key[0][j] == 0) for j in range(1, NUM_ROOMS)]))

# === REACHABILITY (NO SOFT-LOCKS) ===
# For each room r != A, there must exist a predecessor room s such that:
#   1. A directed connection s -> r exists
#   2. Room s is visited before room r (order[s] < order[r])
#   3. Any key required by the connection has already been obtained
for r in range(1, NUM_ROOMS):
    predecessors = []
    for s in range(NUM_ROOMS):
        if s == r:
            continue
        # Key availability: either no key needed, or the required key was obtained by step order[s]
        key_ok = Or(
            req_key[s][r] == 0,
            And(req_key[s][r] == 1, key_obtained[0] <= order[s]),
            And(req_key[s][r] == 2, key_obtained[1] <= order[s]),
            And(req_key[s][r] == 3, key_obtained[2] <= order[s])
        )
        predecessors.append(And(has_conn[s][r], order[s] < order[r], key_ok))
    solver.add(Or(predecessors))

# === SOLVE ===
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print()
    print("rooms:", room_names)
    print()

    # Exploration order
    order_vals = {}
    for i in range(NUM_ROOMS):
        val = m[order[i]].as_long()
        order_vals[val] = room_names[i]
    print("Exploration order (progressive unlock):")
    for step in range(NUM_ROOMS):
        print(f"  Step {step}: Room {order_vals[step]}")
    print()

    # Key locations
    print("item_locations:")
    for k in range(NUM_KEYS):
        room_idx = m[key_room[k]].as_long()
        print(f"  key{k + 1}: Room {room_names[room_idx]}")
    print()

    # Connections
    print("connections:")
    conn_list = []
    for i in range(NUM_ROOMS):
        for j in range(NUM_ROOMS):
            if i != j and is_true(m.evaluate(has_conn[i][j])):
                key_val = m[req_key[i][j]].as_long()
                key_str = f"key{key_val}" if key_val > 0 else "null"
                conn_list.append((room_names[i], room_names[j], key_str))
                print(f"  {{from: {room_names[i]}, to: {room_names[j]}, requires: {key_str}}}")
    print()

    # Summary verification
    print("reachability_verified: True")
    print()
    print(f"Total connections: {len(conn_list)}")
    key_gated = sum(1 for _, _, k in conn_list if k != "null")
    print(f"Key-gated connections: {key_gated}")
    print(f"Free connections: {len(conn_list) - key_gated}")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")