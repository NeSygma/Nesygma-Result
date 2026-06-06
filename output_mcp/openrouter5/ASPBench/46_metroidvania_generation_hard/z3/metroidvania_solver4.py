from z3 import *

solver = Solver()

# Rooms
rooms = ["Start", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "Goal"]
room_indices = {r: i for i, r in enumerate(rooms)}
n_rooms = len(rooms)

# Items
items = ["RedKey", "BlueKey", "GreenKey", "YellowKey", "Boots", "Grapple"]
item_indices = {it: i for i, it in enumerate(items)}
n_items = len(items)

# ========== DECISION VARIABLES ==========

# Item locations: each item placed in one of R1-R10 (indices 1-10)
item_loc = [Int(f"item_loc_{it}") for it in items]
for it_idx in range(n_items):
    solver.add(item_loc[it_idx] >= 1)  # R1
    solver.add(item_loc[it_idx] <= 10) # R10

# Special room types
flooded_room = Int("flooded_room")
chasm_room = Int("chasm_room")
solver.add(flooded_room >= 1, flooded_room <= 10)
solver.add(chasm_room >= 1, chasm_room <= 10)
solver.add(flooded_room != chasm_room)

# Connections: exists[i][j] = Bool, req[i][j] = Int (0=null, 1=RedKey, 2=BlueKey, 3=GreenKey, 4=YellowKey)
exists = [[Bool(f"exists_{i}_{j}") for j in range(n_rooms)] for i in range(n_rooms)]
req = [[Int(f"req_{i}_{j}") for j in range(n_rooms)] for i in range(n_rooms)]

for i in range(n_rooms):
    for j in range(n_rooms):
        if i == j:
            solver.add(exists[i][j] == False)
            solver.add(req[i][j] == 0)
        else:
            solver.add(req[i][j] >= 0, req[i][j] <= 4)
            solver.add(Implies(Not(exists[i][j]), req[i][j] == 0))

# Constraint 2: Goal room has exactly one incoming connection and no outgoing connections
solver.add(Sum([If(exists[i][room_indices["Goal"]], 1, 0) for i in range(n_rooms)]) == 1)
solver.add(Sum([If(exists[room_indices["Goal"]][j], 1, 0) for j in range(n_rooms)]) == 0)

# Count bidirectional and one-way connections
bidir_count = Sum([If(And(exists[i][j], exists[j][i]), 1, 0) for i in range(n_rooms) for j in range(n_rooms) if i < j])
oneway_count = Sum([If(And(exists[i][j], Not(exists[j][i])), 1, 0) for i in range(n_rooms) for j in range(n_rooms) if i < j])

solver.add(bidir_count >= 10, bidir_count <= 15)
solver.add(oneway_count == 2)

# Constraint 2: For each bidirectional pair, if one direction requires a key, the other must be keyless
for i in range(n_rooms):
    for j in range(n_rooms):
        if i < j:
            solver.add(Implies(And(exists[i][j], exists[j][i], req[i][j] > 0), req[j][i] == 0))
            solver.add(Implies(And(exists[i][j], exists[j][i], req[j][i] > 0), req[i][j] == 0))

# Constraint 3: Equipment cannot be in the room of the type it enables
solver.add(item_loc[item_indices["Boots"]] != flooded_room)
solver.add(item_loc[item_indices["Grapple"]] != chasm_room)

# Constraint 4: YellowKey must be in the Chasm room
solver.add(item_loc[item_indices["YellowKey"]] == chasm_room)

# ========== REACHABILITY MODELING ==========

# We'll model first visit order
first_visit = [Int(f"fv_{r}") for r in range(n_rooms)]
solver.add(first_visit[room_indices["Start"]] == 0)
for r in range(n_rooms):
    if r != room_indices["Start"]:
        solver.add(first_visit[r] >= 1, first_visit[r] <= 11)
solver.add(Distinct(first_visit))

# Goal must be last
solver.add(first_visit[room_indices["Goal"]] == 11)

# Items collected up to each step (0-11)
# items_up_to[k] = bitmask of items in rooms with first_visit <= k
# Use individual bits as Bool variables to avoid bitwise ops on ArithRef
item_bit = [[Bool(f"item_bit_{it}_{k}") for k in range(12)] for it in range(n_items)]

for it_idx in range(n_items):
    for k in range(12):
        # item_bit[it_idx][k] is True iff item it_idx is collected by step k
        # item is collected by step k if first_visit[item_loc[it_idx]] <= k
        cond = Or([And(item_loc[it_idx] == r, first_visit[r] <= k) for r in range(1, 11)])
        solver.add(item_bit[it_idx][k] == cond)

# For each room r (not Start), there must be a predecessor s visited earlier
# such that exists[s][r] and requirements are met
for r in range(n_rooms):
    if r == room_indices["Start"]:
        continue
    
    conditions = []
    for s in range(n_rooms):
        if s == r:
            continue
        
        # Key requirement: req[s][r] == 0 OR (req[s][r] >= 1 and corresponding key bit is set)
        req_conds = []
        for key_val in range(0, 5):  # 0 = null, 1-4 = keys
            if key_val == 0:
                req_conds.append(req[s][r] == 0)
            else:
                # Check if bit (key_val-1) is set at step first_visit[s]
                bit_check = Or([And(first_visit[s] == k, item_bit[key_val - 1][k]) for k in range(12)])
                req_conds.append(And(req[s][r] == key_val, bit_check))
        req_cond = Or(req_conds)
        
        # Special room entry requirements
        # If r is Flooded, need Boots (bit 4 = item index 4)
        boots_cond = Or(flooded_room != r, 
                        Or([And(first_visit[s] == k, item_bit[4][k]) for k in range(12)]))
        # If r is Chasm, need Grapple (bit 5 = item index 5)
        grapple_cond = Or(chasm_room != r, 
                          Or([And(first_visit[s] == k, item_bit[5][k]) for k in range(12)]))
        
        cond = And(
            first_visit[s] < first_visit[r],
            exists[s][r],
            req_cond,
            boots_cond,
            grapple_cond
        )
        conditions.append(cond)
    
    solver.add(Or(conditions))

print("Checking satisfiability...")
result = solver.check()
print(f"Result: {result}")

if result == sat:
    m = solver.model()
    
    print("STATUS: sat")
    print()
    
    # Special room types
    flooded = m[flooded_room].as_long()
    chasm = m[chasm_room].as_long()
    print(f"special_room_types:")
    print(f"  Flooded: {rooms[flooded]}")
    print(f"  Chasm: {rooms[chasm]}")
    print()
    
    # Item locations
    print(f"item_locations:")
    for it_idx, it_name in enumerate(items):
        loc = m[item_loc[it_idx]].as_long()
        print(f"  {it_name}: {rooms[loc]}")
    print()
    
    # Connections
    print(f"connections:")
    for i in range(n_rooms):
        for j in range(n_rooms):
            if i == j:
                continue
            if is_true(m[exists[i][j]]):
                req_val = m[req[i][j]].as_long()
                req_str = "null" if req_val == 0 else items[req_val - 1]
                print(f"  {{from: {rooms[i]}, to: {rooms[j]}, requires: {req_str}}}")
    print()
    
    # First visit order
    print(f"first_visit_order:")
    order = [(m[first_visit[r]].as_long(), rooms[r]) for r in range(n_rooms)]
    order.sort()
    for step, rname in order:
        print(f"  {rname}: step {step}")
    print()
    
    # Verify with simulation
    print("Verifying with simulation...")
    
    # Build graph
    edges = {}
    for i in range(n_rooms):
        for j in range(n_rooms):
            if i == j:
                continue
            if is_true(m[exists[i][j]]):
                req_val = m[req[i][j]].as_long()
                edges[(i, j)] = req_val
    
    item_rooms = {}
    for it_idx, it_name in enumerate(items):
        loc = m[item_loc[it_idx]].as_long()
        item_rooms[it_name] = loc
    
    special_rooms = {
        "Flooded": flooded,
        "Chasm": chasm
    }
    
    # Simulate progressive unlocking
    items_owned = 0
    visited = {room_indices["Start"]}
    first_visit_order = [room_indices["Start"]]
    
    while True:
        # Find all rooms reachable with current items
        new_reachable = set(visited)
        changed = True
        while changed:
            changed = False
            for (i, j), req_val in list(edges.items()):
                if i in new_reachable and j not in new_reachable:
                    can_traverse = True
                    if req_val >= 1 and req_val <= 4:
                        if not ((items_owned >> (req_val - 1)) & 1):
                            can_traverse = False
                    if j == special_rooms["Flooded"]:
                        if not ((items_owned >> 4) & 1):
                            can_traverse = False
                    if j == special_rooms["Chasm"]:
                        if not ((items_owned >> 5) & 1):
                            can_traverse = False
                    if can_traverse:
                        new_reachable.add(j)
                        changed = True
        
        newly_visited = new_reachable - visited
        if not newly_visited:
            break
        
        for r in newly_visited:
            first_visit_order.append(r)
        
        visited = set(new_reachable)
        
        for it_name, room_idx in item_rooms.items():
            if room_idx in visited:
                it_idx = item_indices[it_name]
                items_owned |= (1 << it_idx)
    
    print(f"Simulated visit order: {[rooms[r] for r in first_visit_order]}")
    
    goal_idx = room_indices["Goal"]
    all_reachable = len(visited) == n_rooms
    goal_is_last = goal_idx in first_visit_order and first_visit_order.index(goal_idx) == len(first_visit_order) - 1
    
    print(f"All rooms reachable: {all_reachable}")
    print(f"Goal is last: {goal_is_last}")
    
    if all_reachable and goal_is_last:
        print("\nCONCLUSION: Valid solution found!")
        print("solution_validity:")
        print("  all_rooms_reachable: true")
        print("  goal_is_last: true")
    else:
        print("\nCONCLUSION: Invalid - need to refine")
else:
    print("STATUS: unsat")
    print("No solution found")