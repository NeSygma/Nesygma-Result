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

# Special types
special_types = ["Flooded", "Chasm"]

# ========== DECISION VARIABLES ==========

# Item locations: each item placed in one of R1-R10 (indices 1-10)
item_loc = [Int(f"item_loc_{it}") for it in items]
for it_idx in range(n_items):
    solver.add(item_loc[it_idx] >= 1)  # R1
    solver.add(item_loc[it_idx] <= 10) # R10

# Special room types: which room (R1-R10) gets which special type
flooded_room = Int("flooded_room")
chasm_room = Int("chasm_room")
solver.add(flooded_room >= 1, flooded_room <= 10)
solver.add(chasm_room >= 1, chasm_room <= 10)
solver.add(flooded_room != chasm_room)

# Connections: We'll model all possible directed edges between rooms.
# For each ordered pair (i, j) with i != j, we have:
#   - exists[i][j]: Bool, whether this directed edge exists
#   - requires[i][j]: Int, 0=null, 1=RedKey, 2=BlueKey, 3=GreenKey, 4=YellowKey, 5=Boots, 6=Grapple
# But keys and equipment are different: keys are for doors, equipment for traversal.
# Actually the "requires" field can be: null, or a key name (RedKey, BlueKey, GreenKey, YellowKey).
# Equipment (Boots, Grapple) are not used as door requirements; they enable entering special rooms.
# So requires is either null or one of the 4 keys.

# Let's use a simpler approach: we'll model connections as a set of directed edges.
# We'll use Bool variables for existence and Int variables for requirement (0=null, 1-4=keys).

MAX_EDGES = 15  # max total directed edges (bidirectional counts as 2)

# For each ordered pair (i, j) with i != j
exists = [[Bool(f"exists_{i}_{j}") for j in range(n_rooms)] for i in range(n_rooms)]
req = [[Int(f"req_{i}_{j}") for j in range(n_rooms)] for i in range(n_rooms)]

for i in range(n_rooms):
    for j in range(n_rooms):
        if i == j:
            solver.add(exists[i][j] == False)
            solver.add(req[i][j] == 0)
        else:
            # req is 0 (null) or 1-4 (keys)
            solver.add(req[i][j] >= 0, req[i][j] <= 4)
            # If edge doesn't exist, req must be 0
            solver.add(Implies(Not(exists[i][j]), req[i][j] == 0))
            # If edge exists, req can be 0-4
            # (no constraint needed beyond the range)

# Constraint 2: Goal room has exactly one incoming connection and no outgoing connections
solver.add(Sum([If(exists[i][room_indices["Goal"]], 1, 0) for i in range(n_rooms)]) == 1)
solver.add(Sum([If(exists[room_indices["Goal"]][j], 1, 0) for j in range(n_rooms)]) == 0)

# Constraint 2: Total connections (bidirectional counts as 2 directed edges)
# 10-15 bidirectional connections = 20-30 directed edges, plus one one-way = 21-31 directed edges
# Wait, re-reading: "10-15 bidirectional connections and exactly one one-way connection"
# So total directed edges = 2*(bidirectional count) + 1 (one-way) + 1 (mandatory one-way to Goal)
# Actually: "exactly one one-way connection (this is in addition to the mandatory one-way path to the Goal room, for a total of two one-way edges in the final graph)"
# So: bidirectional connections: 10-15 (each counts as 2 directed edges)
#     one-way connections: 2 (one extra + one to Goal)
# Total directed edges: 2*bidir_count + 2
# bidir_count between 10 and 15, so total directed between 22 and 32

# Let's count total directed edges
total_directed = Sum([If(exists[i][j], 1, 0) for i in range(n_rooms) for j in range(n_rooms) if i != j])

# Count bidirectional pairs
bidir_count = Sum([If(And(exists[i][j], exists[j][i]), 1, 0) for i in range(n_rooms) for j in range(n_rooms) if i < j])

# Count one-way pairs (exactly one direction exists)
oneway_count = Sum([If(And(exists[i][j], Not(exists[j][i])), 1, 0) for i in range(n_rooms) for j in range(n_rooms) if i < j])

# Total directed = 2*bidir_count + oneway_count
solver.add(total_directed == 2 * bidir_count + oneway_count)

# bidir_count between 10 and 15
solver.add(bidir_count >= 10, bidir_count <= 15)

# oneway_count == 2 (one extra one-way + one mandatory to Goal)
solver.add(oneway_count == 2)

# Constraint 2: For each bidirectional pair, if any connection in one direction requires a key,
# there must exist at least one connection in the return direction that is keyless.
for i in range(n_rooms):
    for j in range(n_rooms):
        if i < j:
            # If both directions exist and one requires a key (req > 0)
            # then the other direction must have at least one keyless path
            # Since there's only one edge per direction, this means:
            # If exists[i][j] and exists[j][i] and req[i][j] > 0, then req[j][i] == 0
            # AND If exists[i][j] and exists[j][i] and req[j][i] > 0, then req[i][j] == 0
            solver.add(Implies(And(exists[i][j], exists[j][i], req[i][j] > 0), req[j][i] == 0))
            solver.add(Implies(And(exists[i][j], exists[j][i], req[j][i] > 0), req[i][j] == 0))

# Constraint 3: Equipment cannot be placed in the room of the type it enables
# Boots cannot be in Flooded room
solver.add(item_loc[item_indices["Boots"]] != flooded_room)
# Grapple cannot be in Chasm room
solver.add(item_loc[item_indices["Grapple"]] != chasm_room)

# Constraint 4: YellowKey must be located in the Chasm room
solver.add(item_loc[item_indices["YellowKey"]] == chasm_room)

# ========== REACHABILITY ANALYSIS ==========
# We need to model reachability with item-based traversal.
# This is complex: we need to track which items the player has at each point.
# 
# Approach: Model the game as a state graph where a state is (room, items_collected).
# Items are collected when first entering a room that contains them.
# 
# Items: 4 keys + 2 equipment = 6 items
# Rooms: 12
# States: 12 * 2^6 = 12 * 64 = 768 states - manageable for Z3 with quantifiers?
# 
# Alternative: Use a simpler approach - define reachability predicates.
# 
# Let's use a fixed-point approach: define reachable_with_items[room][items_bitmask]
# But that's 12*64=768 booleans. Let's try.

# Bitmask: bit 0=RedKey, 1=BlueKey, 2=GreenKey, 3=YellowKey, 4=Boots, 5=Grapple
# We'll use Int variables for bitmasks (0-63)

# reachable[r][mask] = Bool - whether room r is reachable with exactly item set mask
# Actually, we want: can we reach room r with at least items in mask?
# Let's define: can_reach[r][mask] = can reach room r having collected items superset of mask

# For simplicity, let's define a function: reachable(room, mask)
# We'll use Z3 Function or just encode the constraints.

# Actually, let's use a simpler approach: 
# Define a predicate path_exists(from_room, to_room, items_mask) meaning
# you can traverse from from_room to to_room with the given items.
# Then define reachability inductively.

# Let's use a bounded approach: the player can visit at most N rooms.
# Since there are 12 rooms, the player visits at most 12 rooms (no repeats needed for items).
# Actually, the player might need to revisit rooms after getting new items.
# So the path length could be longer.

# Let's use a different approach: define a graph of (room, mask) states and check connectivity.

# Number of states: 12 * 64 = 768
# We'll create a Bool variable for each state: state_reachable[r][mask]
# But that's a lot of variables. Let's use a more efficient encoding.

# Actually, let's use Z3's uninterpreted functions or just encode the constraints
# using quantifiers. But quantifiers can be slow.

# Alternative: Use a simpler model where we just check if there exists a path
# using the items. We can model this as: there exists an ordering of room visits
# such that each step is valid given items collected so far.

# Let's use a path-based approach: the player visits rooms in some order.
# At step 0, player is at Start with no items.
# At each step, player moves to an adjacent room (via a connection).
# When entering a room, the player collects any items there.
# The player can traverse connections that require keys only if they have the key.

# Since there are 12 rooms, the player might need to visit some rooms multiple times.
# Let's bound the path length to, say, 30 steps (should be enough).

MAX_STEPS = 30

# Variables for path
path_room = [Int(f"path_room_{t}") for t in range(MAX_STEPS + 1)]
path_items = [Int(f"path_items_{t}") for t in range(MAX_STEPS + 1)]  # bitmask

# Start state
solver.add(path_room[0] == room_indices["Start"])
solver.add(path_items[0] == 0)  # no items at start

# At each step, either stay (if we've reached all rooms) or move
for t in range(MAX_STEPS):
    # Room must be valid
    solver.add(path_room[t] >= 0, path_room[t] < n_rooms)
    solver.add(path_items[t] >= 0, path_items[t] <= 63)
    
    # Items collected are cumulative (monotonic)
    # At step t+1, items are a superset of items at step t
    # Actually, items can only increase when entering a room with items
    # For simplicity, we'll say items at t+1 >= items at t (bitwise)
    # But we need to model exactly which items are collected.
    
    # Let's model: when at room r at step t, if room r has items not yet collected,
    # the player collects them. So items at step t include items from rooms visited up to step t.
    
    # This is getting complex. Let's simplify.

# Actually, let's take a different approach entirely.
# Let's model the problem as a constraint satisfaction problem where we
# define the graph structure and item placements, and then verify reachability
# using a separate algorithm (not in Z3).

# We can use Z3 to find a candidate solution, then verify it with Python code.
# But the instructions say to use Z3 for everything.

# Let's try a simpler encoding: define reachability as a transitive closure.

# Define: can_reach_without_items[r] = reachable from Start using only keyless paths
# Then: can_reach_with_items[r][items_set] = reachable with given items

# Actually, let's use a different approach. Let's define:
# - A room is "accessible" if there exists a path from Start to that room
#   where each edge's requirements are satisfied by items collected along the way.
# - Items are collected when first entering a room that contains them.

# We can model this with a fixed-point computation using Z3.

# Let's define variables:
# visited[r] = Bool - whether room r is visited at some point
# collected[i] = Bool - whether item i is collected

# But the order matters: you need items to traverse some edges, and you get items
# by visiting rooms. This is circular.

# Let's use a simpler model: define a partial order of item acquisition.
# The player starts with no items. They can traverse keyless edges freely.
# When they reach a room with an item, they collect it.
# With new items, they can traverse more edges.

# This is essentially a graph reachability problem with progressive unlocking.
# We can model it as: there exists an ordering of item acquisitions.

# Let's define:
# - For each item i, step[i] = the step at which item i is collected (0 = never collected, or 1-12)
# - Items are collected when visiting their room.
# - The player can traverse an edge requiring key k only if step[k] < current step.

# This is still complex. Let's try a simpler encoding.

# ===== SIMPLER APPROACH =====
# Let's just define the graph and item placements, and use Z3 to check
# if there exists a valid traversal order.

# We'll define a sequence of room visits (up to 30 steps).
# At each step, the player is in a room and has a set of items.
# The player can move to an adjacent room if the edge's requirement is satisfied.

# Let's use a cleaner encoding.

# First, let's define what items are needed for each edge.
# For an edge from i to j with req = k (1-4 = key), the player needs key k.
# For entering a Flooded room, the player needs Boots.
# For entering a Chasm room, the player needs Grapple.

# Let's define: can_traverse(i, j, items_mask) = True if the player can go from i to j
# with the given items.

# We'll encode this as a constraint.

# Let's use a simpler bounded model.

# Path variables
path_len = Int("path_len")  # number of steps (edges traversed)
solver.add(path_len >= 0, path_len <= MAX_STEPS)

# path_room[t] = room at step t
# path_items[t] = items collected up to step t (bitmask)
path_room = [Int(f"pr_{t}") for t in range(MAX_STEPS + 1)]
path_items = [Int(f"pi_{t}") for t in range(MAX_STEPS + 1)]

for t in range(MAX_STEPS + 1):
    solver.add(path_room[t] >= 0, path_room[t] < n_rooms)
    solver.add(path_items[t] >= 0, path_items[t] <= 63)

solver.add(path_room[0] == room_indices["Start"])
solver.add(path_items[0] == 0)

# For each step t (0 to MAX_STEPS-1):
# Either we've finished (t >= path_len) and stay in place with same items,
# or we move to a new room.
for t in range(MAX_STEPS):
    # If we're still moving (t < path_len)
    moving = (t < path_len)
    
    # The edge from path_room[t] to path_room[t+1] must exist
    # and its requirement must be satisfied by path_items[t]
    
    # We need to express: there exists an edge from path_room[t] to path_room[t+1]
    # such that the requirement is satisfied.
    
    # This is complex because path_room[t] is a Z3 variable.
    # We need to use the Or-loop pattern.
    
    # For each possible pair (i, j):
    # If path_room[t] == i and path_room[t+1] == j and exists[i][j] == True
    # and requirement is satisfied, then the move is valid.
    
    # Requirement satisfied means:
    # - If req[i][j] == 0 (null), always satisfied
    # - If req[i][j] == k (1-4), then bit (k-1) of path_items[t] must be 1
    
    # Also, entering a Flooded room requires Boots (bit 4)
    # Entering a Chasm room requires Grapple (bit 5)
    
    # Let's build the condition for each pair (i, j)
    move_valid_conditions = []
    for i in range(n_rooms):
        for j in range(n_rooms):
            if i == j:
                continue
            # Condition: path_room[t] == i and path_room[t+1] == j and exists[i][j]
            # and requirement satisfied
            
            # Requirement satisfied:
            req_satisfied = Or(
                req[i][j] == 0,  # null requirement
                # req[i][j] is a key (1-4), check if bit (req[i][j]-1) is set
                And(req[i][j] >= 1, req[i][j] <= 4,
                    (path_items[t] & (1 << (req[i][j] - 1))) != 0)
            )
            
            # Also need to check special room entry requirements
            # If j is Flooded room, need Boots (bit 4)
            # If j is Chasm room, need Grapple (bit 5)
            entry_requirements = True
            # We'll handle this separately
            
            cond = And(
                path_room[t] == i,
                path_room[t+1] == j,
                exists[i][j],
                req_satisfied
            )
            move_valid_conditions.append(cond)
    
    # At least one valid move (or we're done moving)
    solver.add(Implies(moving, Or(move_valid_conditions)))
    
    # If not moving, stay in place
    solver.add(Implies(Not(moving), And(
        path_room[t+1] == path_room[t],
        path_items[t+1] == path_items[t]
    )))
    
    # Update items: when entering a room, collect items there
    # Items in room j: for each item k, if item_loc[k] == j, then bit k is set
    # Actually, items are collected when first entering the room.
    # So path_items[t+1] should include items from path_room[t+1] if not already collected.
    
    # This is complex. Let's simplify: items are collected when visiting a room.
    # path_items[t+1] = path_items[t] | items_in_room(path_room[t+1])
    
    # items_in_room(r) = bitmask of items located in room r
    # We need to express this as a constraint.
    
    # For each room r, items_in_room[r] = sum over items of (1<<item_idx) if item_loc[item_idx] == r
    # This is a sum of conditional expressions.
    
    # Let's define items_in_room as a function of room index.
    items_in_room = [Int(f"items_in_room_{r}") for r in range(n_rooms)]
    for r in range(n_rooms):
        solver.add(items_in_room[r] >= 0, items_in_room[r] <= 63)
        # items_in_room[r] = sum of (1 << item_idx) for items where item_loc[item_idx] == r
        solver.add(items_in_room[r] == Sum([
            If(item_loc[it_idx] == r, 1 << it_idx, 0) for it_idx in range(n_items)
        ]))
    
    # Now, path_items[t+1] = path_items[t] | items_in_room[path_room[t+1]]
    # But path_room[t+1] is a Z3 variable, so we can't index a Python list with it.
    # We need the Or-loop pattern.
    
    # For each room r:
    # If path_room[t+1] == r, then path_items[t+1] = path_items[t] | items_in_room[r]
    item_update_conditions = []
    for r in range(n_rooms):
        cond = And(
            path_room[t+1] == r,
            path_items[t+1] == (path_items[t] | items_in_room[r])
        )
        item_update_conditions.append(cond)
    
    solver.add(Implies(moving, Or(item_update_conditions)))

# Now, we need to ensure all rooms are visited
# For each room r, there exists some step t where path_room[t] == r
for r in range(n_rooms):
    solver.add(Or([path_room[t] == r for t in range(MAX_STEPS + 1)]))

# Goal must be the last new room visited
# This means: for all rooms r != Goal, there exists a step before the first time we reach Goal
# where r is visited.
# Let's define: first_goal_step = the first t where path_room[t] == Goal
# Then for all r != Goal, there exists t < first_goal_step where path_room[t] == r

# We can encode this as: there exists an ordering where Goal is last.
# Let's use a simpler encoding: 
# For each room r != Goal, there exists a step t such that path_room[t] == r
# AND for all steps t' where path_room[t'] == Goal, there exists some step t'' < t'
# where path_room[t''] == r.

# This is getting very complex. Let's try a different approach.

# ===== SIMPLER APPROACH: Use Python to verify after Z3 finds candidate =====
# Let's use Z3 to find a candidate solution (graph + item placements + special rooms),
# then verify reachability with Python code.

# Actually, let's just encode the constraints more simply and use Z3's solver.
# We'll define the graph structure and item placements, and then use a
# separate reachability check.

# Let's simplify: we'll find a solution where:
# 1. Graph structure satisfies constraints
# 2. Item placements satisfy constraints
# 3. Special room assignments satisfy constraints
# 4. Reachability is checked separately

# For reachability, we can use a simple algorithm:
# - Start with items = {}
# - Repeatedly: find all rooms reachable with current items, collect new items, repeat
# - This is a fixed-point computation.

# We can encode this fixed-point in Z3 using iterative deepening.

# Let's define:
# reachable_at_iter[k][r] = Bool - room r is reachable by iteration k
# items_at_iter[k] = Int - bitmask of items collected by iteration k

# Iteration 0: reachable from Start using only keyless edges, no special room entry
# Iteration k+1: reachable using items from iteration k, collect new items

# Let's implement this.

# Maximum iterations (should be at most number of items + 1 = 7)
MAX_ITER = 10

reachable = [[Bool(f"reach_{k}_{r}") for r in range(n_rooms)] for k in range(MAX_ITER + 1)]
items_at_iter = [Int(f"items_{k}") for k in range(MAX_ITER + 1)]

for k in range(MAX_ITER + 1):
    solver.add(items_at_iter[k] >= 0, items_at_iter[k] <= 63)

# Iteration 0: Start is reachable with no items
solver.add(reachable[0][room_indices["Start"]] == True)
solver.add(items_at_iter[0] == 0)

# For other rooms at iteration 0: reachable if there's a path from Start
# using only edges with req == 0, and no special room entry requirements.
# Actually, let's define reachability more carefully.

# A room is reachable at iteration k if:
# - It's reachable at iteration k-1, OR
# - There exists a room r' reachable at iteration k-1, and an edge from r' to r
#   such that the edge's requirement is satisfied by items_at_iter[k-1],
#   AND if r is Flooded, items_at_iter[k-1] has Boots,
#   AND if r is Chasm, items_at_iter[k-1] has Grapple.

# Items at iteration k = items_at_iter[k-1] OR items in rooms reachable at iteration k
# (but not at iteration k-1)

# This is still complex. Let's use a simpler encoding.

# Actually, let's just use the path-based approach but with a simpler encoding.
# We'll bound the path length and use Z3 to find a valid path.

# Let's restart with a cleaner approach.

print("Starting solver...")

# Let's try a different strategy: use Z3 to find the graph structure and item placements,
# then verify reachability with a simple Python function.

# We'll use Z3's model to get a candidate, then check it.

# Actually, let's just encode everything in Z3 using a simpler model.

# ===== NEW APPROACH: Direct encoding with reachability as constraints =====

# We'll define:
# - For each room r, a variable order[r] = the step at which room r is first visited (0 = Start, 1-11 for others)
# - The player visits rooms in order of increasing order[r]
# - When visiting a room, the player collects items there
# - The player can only move from room r to room s if there's a connection and requirements are met

# This is a Hamiltonian path-like problem but with revisits allowed.
# Actually, the player might need to revisit rooms. But for the purpose of
# "first visit", we only care about the first time each room is visited.

# Let's define:
# first_visit[r] = Int - the step at which room r is first visited (0 for Start, 1-11 for others)
# All first_visit values are distinct (each room is first visited exactly once)
# Start is visited at step 0

first_visit = [Int(f"first_visit_{r}") for r in range(n_rooms)]
solver.add(first_visit[room_indices["Start"]] == 0)
for r in range(n_rooms):
    if r != room_indices["Start"]:
        solver.add(first_visit[r] >= 1, first_visit[r] <= 11)
solver.add(Distinct(first_visit))

# Goal must be last: first_visit[Goal] == 11
solver.add(first_visit[room_indices["Goal"]] == 11)

# Items collected up to step k
# items_up_to[k] = bitmask of items in rooms with first_visit <= k
items_up_to = [Int(f"items_up_to_{k}") for k in range(12)]  # steps 0-11
for k in range(12):
    solver.add(items_up_to[k] >= 0, items_up_to[k] <= 63)
    # items_up_to[k] = sum of (1<<it_idx) for items where first_visit[item_loc[it_idx]] <= k
    solver.add(items_up_to[k] == Sum([
        If(first_visit[item_loc[it_idx]] <= k, 1 << it_idx, 0) for it_idx in range(n_items)
    ]))

# For each room r (except Start), there must exist a connection from some room s
# that is visited earlier (first_visit[s] < first_visit[r]) to r,
# such that the connection's requirement is satisfied by items available at that time.

# The connection from s to r must exist, and:
# - If req[s][r] == 0, no key needed
# - If req[s][r] == k (1-4), then items_up_to[first_visit[s]] must have bit (k-1)
# - If r is Flooded, items_up_to[first_visit[s]] must have Boots (bit 4)
# - If r is Chasm, items_up_to[first_visit[s]] must have Grapple (bit 5)

# For each room r (not Start):
for r in range(n_rooms):
    if r == room_indices["Start"]:
        continue
    
    # There exists some s such that:
    # first_visit[s] < first_visit[r] AND exists[s][r] AND requirements met
    conditions = []
    for s in range(n_rooms):
        if s == r:
            continue
        
        # Requirement satisfied:
        req_cond = Or(
            req[s][r] == 0,
            And(req[s][r] >= 1, req[s][r] <= 4,
                (items_up_to[first_visit[s]] & (1 << (req[s][r] - 1))) != 0)
        )
        
        # Special room entry requirements
        # We need to check if r is Flooded or Chasm
        # But flooded_room and chasm_room are variables, so we need Or-loop
        
        # If r == flooded_room, need Boots (bit 4)
        # If r == chasm_room, need Grapple (bit 5)
        # Otherwise, no special requirement
        
        special_cond = True
        # Actually, we need to handle this differently.
        # Let's define: entry_requires_boots[r] = (r == flooded_room)
        # entry_requires_grapple[r] = (r == chasm_room)
        
        # We'll handle this with Or conditions.
        
        cond = And(
            first_visit[s] < first_visit[r],
            exists[s][r],
            req_cond
        )
        conditions.append(cond)
    
    solver.add(Or(conditions))

# Now add special room entry requirements separately
# For each room r, if r is Flooded, then the player must have Boots when first entering
# If r is Chasm, the player must have Grapple when first entering

# For the Flooded room:
# There must exist some s such that first_visit[s] < first_visit[flooded_room]
# and exists[s][flooded_room] and req satisfied and Boots owned
# We already have the general constraint above. We just need to add the Boots requirement.

# Let's add: for the room that is Flooded, the items at the step before entering must include Boots
# The step before entering is first_visit[flooded_room] - 1 (or 0 if first visit is 0, but flooded can't be Start)
# Actually, items_up_to[first_visit[s]] where s is the predecessor.

# Let's add a constraint: if r is Flooded, then for the predecessor s that provides the first entry,
# items_up_to[first_visit[s]] must have Boots.

# We can express this as: for all s, if first_visit[s] < first_visit[r] and exists[s][r] and
# the edge requirement is met, then items_up_to[first_visit[s]] must have Boots.
# But this is too strong - we only need one such s.

# Better: There exists s such that first_visit[s] < first_visit[r] and exists[s][r] and
# req satisfied and (r is not Flooded or Boots owned) and (r is not Chasm or Grapple owned).

# Let's redo the main constraint with special room requirements included.

# For each room r (not Start):
for r in range(n_rooms):
    if r == room_indices["Start"]:
        continue
    
    conditions = []
    for s in range(n_rooms):
        if s == r:
            continue
        
        req_cond = Or(
            req[s][r] == 0,
            And(req[s][r] >= 1, req[s][r] <= 4,
                (items_up_to[first_visit[s]] & (1 << (req[s][r] - 1))) != 0)
        )
        
        # Special room entry: if r is Flooded, need Boots (bit 4)
        # If r is Chasm, need Grapple (bit 5)
        boots_cond = Or(flooded_room != r, (items_up_to[first_visit[s]] & (1 << 4)) != 0)
        grapple_cond = Or(chasm_room != r, (items_up_to[first_visit[s]] & (1 << 5)) != 0)
        
        cond = And(
            first_visit[s] < first_visit[r],
            exists[s][r],
            req_cond,
            boots_cond,
            grapple_cond
        )
        conditions.append(cond)
    
    solver.add(Or(conditions))

# Now let's also ensure that the items_up_to values are consistent with first_visit ordering.
# This is already handled by the Sum constraint above.

# Let's also add: items_up_to[k] is monotonic (non-decreasing in terms of set inclusion)
# This should follow from the definition.

# Let's solve this!

print("Checking satisfiability...")
result = solver.check()
print(f"Result: {result}")

if result == sat:
    m = solver.model()
    
    # Extract solution
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
    for r in range(n_rooms):
        fv = m[first_visit[r]].as_long()
        print(f"  {rooms[r]}: step {fv}")
    print()
    
    # Items up to each step
    print(f"items_up_to:")
    for k in range(12):
        iu = m[items_up_to[k]].as_long()
        collected = [items[idx] for idx in range(n_items) if (iu >> idx) & 1]
        print(f"  step {k}: {collected}")
    print()
    
    # Verify reachability manually
    print("Verifying solution...")
    
    # Build graph
    edges = {}
    for i in range(n_rooms):
        for j in range(n_rooms):
            if i == j:
                continue
            if is_true(m[exists[i][j]]):
                req_val = m[req[i][j]].as_long()
                edges[(i, j)] = req_val  # 0 = null, 1-4 = keys
    
    # Item locations
    item_rooms = {}
    for it_idx, it_name in enumerate(items):
        loc = m[item_loc[it_idx]].as_long()
        item_rooms[it_name] = loc
    
    # Special rooms
    special_rooms = {
        "Flooded": flooded,
        "Chasm": chasm
    }
    
    # Reachability check
    def check_reachability():
        # Fixed-point computation
        items_owned = 0  # bitmask
        reachable_rooms = {room_indices["Start"]}
        prev_reachable = set()
        
        while reachable_rooms != prev_reachable:
            prev_reachable = set(reachable_rooms)
            
            # Find all rooms reachable with current items
            new_reachable = set(reachable_rooms)
            changed = True
            while changed:
                changed = False
                for (i, j), req_val in edges.items():
                    if i in new_reachable and j not in new_reachable:
                        # Check if we can traverse
                        can_traverse = True
                        
                        # Check key requirement
                        if req_val >= 1 and req_val <= 4:
                            if not ((items_owned >> (req_val - 1)) & 1):
                                can_traverse = False
                        
                        # Check special room entry
                        if j == special_rooms["Flooded"]:
                            if not ((items_owned >> 4) & 1):  # Boots
                                can_traverse = False
                        if j == special_rooms["Chasm"]:
                            if not ((items_owned >> 5) & 1):  # Grapple
                                can_traverse = False
                        
                        if can_traverse:
                            new_reachable.add(j)
                            changed = True
            
            # Collect items in newly reachable rooms
            new_items = 0
            for it_name, room_idx in item_rooms.items():
                if room_idx in new_reachable:
                    it_idx = item_indices[it_name]
                    new_items |= (1 << it_idx)
            
            items_owned |= new_items
            reachable_rooms = set(new_reachable)
        
        return reachable_rooms, items_owned
    
    reachable_rooms, items_owned = check_reachability()
    
    print(f"All rooms reachable: {len(reachable_rooms) == n_rooms}")
    print(f"Reachable rooms: {[rooms[r] for r in sorted(reachable_rooms)]}")
    print(f"Items owned: {[items[i] for i in range(n_items) if (items_owned >> i) & 1]}")
    
    # Check if Goal is last new room
    # We need to verify that all other rooms are reachable before Goal
    # Let's simulate the order of first visits
    
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
            for (i, j), req_val in edges.items():
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
        
        # Visit new rooms (in any order, but for simulation, add all at once)
        for r in newly_visited:
            first_visit_order.append(r)
        
        visited = set(new_reachable)
        
        # Collect items in newly visited rooms
        for it_name, room_idx in item_rooms.items():
            if room_idx in visited:
                it_idx = item_indices[it_name]
                items_owned |= (1 << it_idx)
    
    print(f"\nFirst visit order: {[rooms[r] for r in first_visit_order]}")
    
    goal_idx = room_indices["Goal"]
    if goal_idx in first_visit_order:
        goal_pos = first_visit_order.index(goal_idx)
        print(f"Goal is at position {goal_pos} (0-indexed)")
        print(f"Goal is last: {goal_pos == len(first_visit_order) - 1}")
        
        if goal_pos == len(first_visit_order) - 1:
            print("\nCONCLUSION: Valid solution found!")
            print("solution_validity:")
            print("  all_rooms_reachable: true")
            print("  goal_is_last: true")
        else:
            print("\nCONCLUSION: Goal is not last - need to refine")
    else:
        print("\nCONCLUSION: Goal not reachable - need to refine")
else:
    print("STATUS: unsat")
    print("No solution found with current encoding")