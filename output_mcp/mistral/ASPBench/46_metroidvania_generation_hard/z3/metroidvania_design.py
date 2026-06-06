from z3 import *

# ============================================================================
# Problem: Metroidvania-Style Game World Design
# ============================================================================

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# ----------------------------------------------------------------------------
# 1. Declare symbolic domains and constants
# ----------------------------------------------------------------------------

# Rooms: Start, R1-R10, Goal
rooms = ['Start', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'Goal']

# Items: 4 Keys + 2 Equipment
items = ['RedKey', 'BlueKey', 'GreenKey', 'YellowKey', 'Boots', 'Grapple']

# Special room types as an enumeration
RoomType = Datatype('RoomType')
RoomType.declare('NORMAL')
RoomType.declare('FLOODED')
RoomType.declare('CHASM')
RoomType = RoomType.create()
NORMAL, FLOODED, CHASM = RoomType

# Connection requirement types as an enumeration
ReqType = Datatype('ReqType')
ReqType.declare('NONE')
ReqType.declare('RedKey')
ReqType.declare('BlueKey')
ReqType.declare('GreenKey')
ReqType.declare('YellowKey')
ReqType.declare('Boots')
ReqType.declare('Grapple')
ReqType = ReqType.create()
NONE, RedKey, BlueKey, GreenKey, YellowKey, Boots, Grapple = ReqType

# ----------------------------------------------------------------------------
# 2. Declare decision variables
# ----------------------------------------------------------------------------

solver = Solver()

# Room types for R1-R10 only (Start and Goal are fixed as NORMAL)
room_type = {r: Const(f'room_type_{r}', RoomType) for r in rooms if r not in ['Start', 'Goal']}
for r in room_type:
    solver.add(Or(room_type[r] == NORMAL, room_type[r] == FLOODED, room_type[r] == CHASM))

# Item locations: map each item to a room in R1-R10
item_location = {it: Const(f'item_loc_{it}', StringSort()) for it in items}
for it in items:
    solver.add(Or([item_location[it] == Str(r) for r in ['R1','R2','R3','R4','R5','R6','R7','R8','R9','R10']]))

# Connections: we will represent connections as tuples (from_room, to_room, requires)
# We need 10-15 bidirectional connections + 2 one-way connections = 12-17 total connections
# We'll model connections as a list of tuples with symbolic requirements

# We'll use a bounded number of possible connections: all ordered pairs except self-loops and Start->Goal, Goal->anything
possible_connections = [(f, t) for f in rooms for t in rooms if f != t and not (f == 'Start' and t == 'Goal')]

# We'll allow up to 20 possible connections to choose from
connection_vars = [Bool(f'conn_{f}_{t}') for (f,t) in possible_connections]

# For each active connection, we need a requirement
conn_req = {idx: Const(f'req_{idx}', ReqType) for idx in range(len(possible_connections))}

# One-way connections: exactly 2 one-way connections (in addition to the mandatory one to Goal)
# We'll track which connections are one-way
one_way_flags = [Bool(f'one_way_{idx}') for idx in range(len(possible_connections))]

# ----------------------------------------------------------------------------
# 3. Add constraints
# ----------------------------------------------------------------------------

# Constraint 1: Exactly 2 special rooms among R1-R10: one FLOODED, one CHASM
special_rooms = [r for r in room_type]
solver.add(Sum([If(room_type[r] == FLOODED, 1, 0) for r in special_rooms]) == 1)
solver.add(Sum([If(room_type[r] == CHASM, 1, 0) for r in special_rooms]) == 1)

# Constraint 2: Equipment items cannot be placed in rooms of the type they enable
# Boots cannot be in a FLOODED room
flooded_room = [r for r in room_type if room_type[r] == FLOODED][0] if any(room_type[r] == FLOODED for r in room_type) else None
if flooded_room:
    solver.add(item_location['Boots'] != Str(flooded_room))

# Grapple cannot be in a CHASM room
chasm_room = [r for r in room_type if room_type[r] == CHASM][0] if any(room_type[r] == CHASM for r in room_type) else None
if chasm_room:
    solver.add(item_location['Grapple'] != Str(chasm_room))

# Constraint 3: YellowKey must be in the CHASM room
if chasm_room:
    solver.add(item_location['YellowKey'] == Str(chasm_room))

# Constraint 4: Connections count
# Total connections: 10-15 bidirectional + 2 one-way = 12-17 total connections
solver.add(Sum(connection_vars) >= 12)
solver.add(Sum(connection_vars) <= 20)  # Upper bound to keep it bounded

# Exactly 2 one-way connections
solver.add(Sum(one_way_flags) == 2)

# For each connection that is active, if it's one-way, it's a one-way edge
# If it's bidirectional, then the reverse connection must also be active
for idx, (f,t) in enumerate(possible_connections):
    # Find reverse index
    rev_idx = next((i for i, (rf, rt) in enumerate(possible_connections) if rf == t and rt == f), None)
    if rev_idx is None:
        continue
    
    # If this connection is one-way, the reverse must not be active as a bidirectional connection
    solver.add(Implies(And(connection_vars[idx], one_way_flags[idx]), Not(connection_vars[rev_idx])))
    
    # If this connection is bidirectional (not one-way), then reverse must also be active
    solver.add(Implies(And(connection_vars[idx], Not(one_way_flags[idx])), connection_vars[rev_idx]))

# Constraint 5: For bidirectional connections, if one direction requires a key, the other must be keyless
for idx, (f,t) in enumerate(possible_connections):
    rev_idx = next((i for i, (rf, rt) in enumerate(possible_connections) if rf == t and rt == f), None)
    if rev_idx is None:
        continue
    
    # If both directions are active (bidirectional)
    solver.add(Implies(And(connection_vars[idx], connection_vars[rev_idx]),
                      Or(
                          conn_req[idx] == NONE,
                          conn_req[rev_idx] == NONE,
                          # Or both require the same key (but this is still invalid per problem statement)
                          # Actually, the problem says: if one requires a key, the return must be keyless
                          # So we need: NOT(requires key in one direction AND requires key in other direction)
                          Not(And(
                              Or(conn_req[idx] == RedKey, conn_req[idx] == BlueKey, conn_req[idx] == GreenKey, conn_req[idx] == YellowKey),
                              Or(conn_req[rev_idx] == RedKey, conn_req[rev_idx] == BlueKey, conn_req[rev_idx] == GreenKey, conn_req[rev_idx] == YellowKey)
                          ))
                      )))

# Constraint 6: Goal room constraints
# Goal must have exactly one incoming connection and no outgoing connections
# We'll enforce this by counting active connections to/from Goal
incoming_to_goal = [
    And(connection_vars[idx], possible_connections[idx][1] == 'Goal')
    for idx in range(len(possible_connections))
]
outgoing_from_goal = [
    And(connection_vars[idx], possible_connections[idx][0] == 'Goal')
    for idx in range(len(possible_connections))
]

solver.add(Sum(incoming_to_goal) == 1)
solver.add(Sum(outgoing_from_goal) == 0)

# Constraint 7: Equipment items Boots and Grapple must be placed somewhere
solver.add(Or([item_location['Boots'] == Str(r) for r in ['R1','R2','R3','R4','R5','R6','R7','R8','R9','R10']]))
solver.add(Or([item_location['Grapple'] == Str(r) for r in ['R1','R2','R3','R4','R5','R6','R7','R8','R9','R10']]))

# All keys must be placed
for key in ['RedKey', 'BlueKey', 'GreenKey', 'YellowKey']:
    solver.add(Or([item_location[key] == Str(r) for r in ['R1','R2','R3','R4','R5','R6','R7','R8','R9','R10']]))

# ----------------------------------------------------------------------------
# 4. Check for a solution
# ----------------------------------------------------------------------------

result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract and print the solution
    print("\n=== SOLUTION ===")
    
    # Room types
    print("\nSpecial Room Types:")
    for r in ['R1','R2','R3','R4','R5','R6','R7','R8','R9','R10']:
        rt = model[room_type[r]]
        if rt == FLOODED:
            print(f"{r}: Flooded")
        elif rt == CHASM:
            print(f"{r}: Chasm")
        else:
            print(f"{r}: Normal")
    
    # Item locations
    print("\nItem Locations:")
    for it in items:
        loc = model[item_location[it]]
        print(f"{it}: {loc}")
    
    # Connections
    print("\nConnections:")
    conn_list = []
    for idx, (f,t) in enumerate(possible_connections):
        if is_true(model[connection_vars[idx]]):
            req = model[conn_req[idx]]
            req_str = str(req).split('.')[-1]  # Extract enum name
            if req_str == 'NONE':
                req_str = "null"
            
            one_way = is_true(model[one_way_flags[idx]])
            conn_list.append((f, t, req_str, one_way))
    
    # Print connections grouped by bidirectional pairs
    printed = set()
    for (f,t,req,ow) in conn_list:
        if (f,t) in printed or (t,f) in printed:
            continue
        rev_req = next((r for (rf,rt,r,ow2) in conn_list if rf == t and rt == f), None)
        if rev_req is not None:
            print(f"  {f} <-> {t} (req: {req} / {rev_req})")
            printed.add((f,t))
            printed.add((t,f))
        else:
            print(f"  {f} -> {t} (one-way, req: {req})")
            printed.add((f,t))
    
    # Print one-way connections separately
    print("\nOne-way connections:")
    for (f,t,req,ow) in conn_list:
        if ow:
            print(f"  {f} -> {t} (req: {req})")
    
    print("\n=== VALIDITY CHECKS ===")
    
    # Check: YellowKey is in Chasm room
    yellow_loc = model[item_location['YellowKey']]
    chasm_room = [r for r in room_type if model[room_type[r]] == CHASM][0] if any(model[room_type[r]] == CHASM for r in room_type) else None
    if chasm_room:
        print(f"YellowKey in Chasm room: {str(yellow_loc) == str(Str(chasm_room))}")
    
    # Check: Boots not in Flooded room
    boots_loc = model[item_location['Boots']]
    flooded_room = [r for r in room_type if model[room_type[r]] == FLOODED][0] if any(model[room_type[r]] == FLOODED for r in room_type) else None
    if flooded_room:
        print(f"Boots not in Flooded room: {str(boots_loc) != str(Str(flooded_room))}")
    
    # Check: Grapple not in Chasm room
    grapple_loc = model[item_location['Grapple']]
    if chasm_room:
        print(f"Grapple not in Chasm room: {str(grapple_loc) != str(Str(chasm_room))}")
    
    # Check: Goal has exactly one incoming connection
    incoming_count = sum(1 for (f,t,req,ow) in conn_list if t == 'Goal')
    print(f"Goal has exactly one incoming connection: {incoming_count == 1}")
    
    # Check: Goal has no outgoing connections
    outgoing_count = sum(1 for (f,t,req,ow) in conn_list if f == 'Goal')
    print(f"Goal has no outgoing connections: {outgoing_count == 0}")
    
    # Check: Exactly 2 one-way connections
    one_way_count = sum(1 for (f,t,req,ow) in conn_list if ow)
    print(f"Exactly 2 one-way connections: {one_way_count == 2}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")