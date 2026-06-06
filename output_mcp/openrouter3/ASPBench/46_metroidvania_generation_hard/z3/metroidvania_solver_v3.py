from z3 import *

# Initialize solver
solver = Solver()

# Room names
rooms = ["Start", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "Goal"]
room_to_idx = {room: i for i, room in enumerate(rooms)}
N = len(rooms)

# Item names
items = ["RedKey", "BlueKey", "GreenKey", "YellowKey", "Boots", "Grapple"]
item_to_idx = {item: i for i, item in enumerate(items)}
M = len(items)

# Special room types
special_types = ["Flooded", "Chasm"]

# 1. Special room assignments (which room is Flooded, which is Chasm)
# Must be from R1-R10 (indices 1-10)
flooded_room = Int('flooded_room')
chasm_room = Int('chasm_room')
solver.add(flooded_room >= 1, flooded_room <= 10)  # R1-R10
solver.add(chasm_room >= 1, chasm_room <= 10)
solver.add(flooded_room != chasm_room)  # Different rooms

# 2. Item placements (which room contains each item)
# All items must be in R1-R10 (indices 1-10)
item_locations = [Int(f'item_loc_{item}') for item in items]
for loc in item_locations:
    solver.add(loc >= 1, loc <= 10)

# YellowKey must be in Chasm room
solver.add(item_locations[item_to_idx["YellowKey"]] == chasm_room)

# Equipment cannot be in their respective special rooms
solver.add(item_locations[item_to_idx["Boots"]] != flooded_room)
solver.add(item_locations[item_to_idx["Grapple"]] != chasm_room)

# All items must be in distinct rooms (one item per room)
solver.add(Distinct(item_locations))

# 3. Connection graph
# Create connection variables for each ordered pair
connected_vars = [[Bool(f'conn_{i}_{j}') for j in range(N)] for i in range(N)]
key_req_vars = [[Int(f'key_{i}_{j}') for j in range(N)] for i in range(N)]

# Key requirements: 0 = no key, 1 = RedKey, 2 = BlueKey, 3 = GreenKey, 4 = YellowKey
for i in range(N):
    for j in range(N):
        solver.add(key_req_vars[i][j] >= 0, key_req_vars[i][j] <= 4)
        # If not connected, key requirement must be 0
        solver.add(Implies(Not(connected_vars[i][j]), key_req_vars[i][j] == 0))

# Bidirectional connections constraint: if A->B requires key, then B->A must be keyless
# Also, if A->B is connected, then B->A must be connected (bidirectional)
for i in range(N):
    for j in range(N):
        if i != j:
            # Bidirectionality: if i->j is connected, j->i must be connected
            solver.add(Implies(connected_vars[i][j], connected_vars[j][i]))
            # Key constraint: if i->j requires a key, then j->i must be keyless
            solver.add(Implies(key_req_vars[i][j] > 0, key_req_vars[j][i] == 0))

# Goal room constraints: exactly one incoming connection, no outgoing
goal_idx = room_to_idx["Goal"]
for i in range(N):
    if i != goal_idx:
        solver.add(Not(connected_vars[goal_idx][i]))  # No outgoing from Goal

# Exactly one incoming to Goal
incoming_to_goal = [If(connected_vars[i][goal_idx], 1, 0) for i in range(N) if i != goal_idx]
solver.add(Sum(incoming_to_goal) == 1)

# 4. One-way connection constraint
# We need exactly one one-way connection in addition to the mandatory one to Goal
# Let's create a variable for the special one-way connection
one_way_from = Int('one_way_from')
one_way_to = Int('one_way_to')
solver.add(one_way_from >= 0, one_way_from < N)
solver.add(one_way_to >= 0, one_way_to < N)
solver.add(one_way_from != one_way_to)
solver.add(one_way_to != goal_idx)  # Not the Goal (that's the mandatory one)

# For the special one-way connection, we allow asymmetry
# For all other pairs (except involving Goal), enforce bidirectionality
for i in range(N):
    for j in range(N):
        if i != j and i != goal_idx and j != goal_idx:
            # Check if this is the special one-way pair
            # We need to use Or-Loop pattern since one_way_from/one_way_to are symbolic
            is_special_pair = Or([And(one_way_from == ii, one_way_to == jj) for ii in range(N) for jj in range(N) if ii != jj and ii != goal_idx and jj != goal_idx])
            
            # For non-special pairs, enforce bidirectionality
            # But we can't use is_special_pair directly in Implies because it's a complex expression
            # Let's use a different approach

# Let's simplify: we'll create a boolean variable for each possible one-way pair
one_way_pairs = []
for i in range(N):
    for j in range(N):
        if i != j and i != goal_idx and j != goal_idx:
            one_way_pairs.append(Bool(f'one_way_{i}_{j}'))

# Exactly one of these one-way pairs should be True
solver.add(Sum([If(ow, 1, 0) for ow in one_way_pairs]) == 1)

# For each pair, if it's the one-way pair, allow asymmetry; otherwise enforce bidirectionality
pair_idx = 0
for i in range(N):
    for j in range(N):
        if i != j and i != goal_idx and j != goal_idx:
            ow_var = one_way_pairs[pair_idx]
            pair_idx += 1
            
            # If this is the one-way pair, allow connected[i][j] but not connected[j][i]
            # Otherwise, enforce bidirectionality
            solver.add(Implies(Not(ow_var), connected_vars[i][j] == connected_vars[j][i]))
            
            # If this is the one-way pair, connected[i][j] must be True and connected[j][i] must be False
            solver.add(Implies(ow_var, connected_vars[i][j] == True))
            solver.add(Implies(ow_var, connected_vars[j][i] == False))

# 5. Count bidirectional pairs
bidirectional_pairs = []
for i in range(N):
    for j in range(i+1, N):
        is_bidirectional = And(connected_vars[i][j], connected_vars[j][i])
        bidirectional_pairs.append(is_bidirectional)

bidirectional_count = Sum([If(bp, 1, 0) for bp in bidirectional_pairs])
solver.add(bidirectional_count >= 10, bidirectional_count <= 15)

# 6. Ensure Start has outgoing connections
start_idx = room_to_idx["Start"]
solver.add(Or([connected_vars[start_idx][j] for j in range(N) if j != start_idx]))

# 7. Ensure Goal is reachable (has incoming connection)
solver.add(Or([connected_vars[i][goal_idx] for i in range(N) if i != goal_idx]))

# 8. Ensure no direct connection from Start to Goal
solver.add(Not(connected_vars[start_idx][goal_idx]))

# 9. Ensure all rooms are connected (graph is connected)
# We'll use a simple constraint: each room (except Start) must have at least one incoming connection
for i in range(N):
    if i != start_idx:
        incoming = [If(connected_vars[j][i], 1, 0) for j in range(N) if j != i]
        solver.add(Sum(incoming) >= 1)

# Let's try to find a solution with the current constraints
print("Checking satisfiability...")
result = solver.check()

if result == sat:
    print("STATUS: sat")
    m = solver.model()
    
    # Extract special rooms
    flooded_idx = m[flooded_room].as_long()
    chasm_idx = m[chasm_room].as_long()
    print(f"Special rooms: Flooded={rooms[flooded_idx]}, Chasm={rooms[chasm_idx]}")
    
    # Extract item locations
    print("Item locations:")
    for item in items:
        loc_idx = m[item_locations[item_to_idx[item]]].as_long()
        print(f"  {item}: {rooms[loc_idx]}")
    
    # Extract connections
    print("Connections:")
    connections = []
    for i in range(N):
        for j in range(N):
            if i != j:
                conn_val = m.evaluate(connected_vars[i][j])
                if conn_val.as_long() == 1:
                    key_req_val = m.evaluate(key_req_vars[i][j]).as_long()
                    key_name = "null" if key_req_val == 0 else items[key_req_val-1]
                    connections.append({
                        "from": rooms[i],
                        "to": rooms[j],
                        "requires": key_name
                    })
    
    # Print connections (grouped by bidirectional pairs)
    printed_pairs = set()
    for conn in connections:
        pair = tuple(sorted([conn["from"], conn["to"]]))
        if pair not in printed_pairs:
            printed_pairs.add(pair)
            # Find both directions
            forward = [c for c in connections if c["from"] == conn["from"] and c["to"] == conn["to"]]
            backward = [c for c in connections if c["from"] == conn["to"] and c["to"] == conn["from"]]
            if forward and backward:
                print(f"  {forward[0]}")
                print(f"  {backward[0]}")
            else:
                print(f"  {conn} (one-way)")
    
    # Check solution validity flags
    print("Solution validity:")
    print("  All rooms reachable: (needs detailed check)")
    print("  Goal is last: (needs detailed check)")
    
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")