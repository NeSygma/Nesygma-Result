from z3 import *

# Blocks A-L (0-11), Table (12)
blocks = range(12)
TABLE = 12
weights = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12}

# Initial configuration
# Stack 1: D(table), C(D), B(C), A(B)
# Stack 2: H(table), G(H), F(G), E(F)
# Stack 3: L(table), K(L), J(K), I(J)
initial_on = {0: 1, 1: 2, 2: 3, 3: TABLE, 4: 5, 5: 6, 6: 7, 7: TABLE, 8: 9, 9: 10, 10: 11, 11: TABLE}

# Goal configuration
# Tower 1: L(table), I(L), F(I), C(F)
# Tower 2: K(table), H(K), E(H), B(E)
# Tower 3: J(table), G(J), D(G), A(D)
goal_on = {2: 5, 5: 8, 8: 11, 11: TABLE, 1: 4, 4: 7, 7: 10, 10: TABLE, 0: 3, 3: 6, 6: 9, 9: TABLE}

T = 20 # Start with a smaller horizon and increase if needed
solver = Solver()

# Variables
# on[b, t] is the block or table that block b is on at time t
on = [[Int(f"on_{b}_{t}") for t in range(T + 1)] for b in blocks]

# Constraints
for b in blocks:
    for t in range(T + 1):
        solver.add(on[b][t] >= 0, on[b][t] <= TABLE)

# Initial state
for b in blocks:
    solver.add(on[b][0] == initial_on[b])

# Goal state
for b in blocks:
    solver.add(on[b][T] == goal_on[b])

# Helper: is_clear(b, t)
def is_clear(b, t):
    return Not(Or([on[b_prime][t] == b for b_prime in blocks]))

# Helper: height(b, t)
# height(table) = 0, height(base) = 1, etc.
def get_height(b, t):
    # Recursive definition is hard in Z3, use a helper array
    h = [Int(f"h_{b}_{t}") for b in blocks]
    # This is complex, let's simplify:
    # height(b, t) = If(on[b, t] == TABLE, 1, height(on[b, t], t) + 1)
    return h[b]

# Actually, let's use a simpler approach for height and clear
# Action: move(b, from, to) at time t
# move_b[t] is the block moved at time t
move_b = [Int(f"move_b_{t}") for t in range(T)]
move_from = [Int(f"move_from_{t}") for t in range(T)]
move_to = [Int(f"move_to_{t}") for t in range(T)]

for t in range(T):
    solver.add(move_b[t] >= 0, move_b[t] < 12)
    solver.add(move_from[t] >= 0, move_from[t] <= TABLE)
    solver.add(move_to[t] >= 0, move_to[t] <= TABLE)
    
    # Only one block moves
    # Constraint: move_b[t] must be clear at t
    # Constraint: move_from[t] must be on[move_b[t]][t]
    # Constraint: move_to[t] must be clear at t (or table)
    
    # Weight constraint: if move_to[t] != TABLE, weight[move_to[t]] >= weight[move_b[t]]
    for b in blocks:
        solver.add(Implies(move_b[t] == b, And(
            on[b][t] == move_from[t],
            is_clear(b, t),
            Or(move_to[t] == TABLE, And(move_to[t] != b, is_clear(move_to[t], t))),
            move_from[t] != move_to[t]
        )))
        
        # Weight
        for target in blocks:
            solver.add(Implies(And(move_b[t] == b, move_to[t] == target), weights[target] >= weights[b]))

    # Update state
    for b in blocks:
        solver.add(If(move_b[t] == b, on[b][t+1] == move_to[t], on[b][t+1] == on[b][t]))

# Table limit: at most 6 blocks on table
for t in range(T + 1):
    solver.add(Sum([If(on[b][t] == TABLE, 1, 0) for b in blocks]) <= 6)

# Height limit: no tower > 5
# This is tricky. Let's define height(b, t)
height = [[Int(f"height_{b}_{t}") for t in range(T + 1)] for b in blocks]
for t in range(T + 1):
    for b in blocks:
        solver.add(If(on[b][t] == TABLE, height[b][t] == 1, 
                      Or([And(on[b][t] == b_prime, height[b][t] == height[b_prime][t] + 1) for b_prime in blocks])))
        solver.add(height[b][t] <= 5)

result = solver.check()
if result == sat:
    print("STATUS: sat")
    m = solver.model()
    for t in range(T):
        b = m[move_b[t]].as_long()
        f = m[move_from[t]].as_long()
        to = m[move_to[t]].as_long()
        print(f"Step {t+1}: Move {chr(ord('A')+b)} from {chr(ord('A')+f) if f < 12 else 'table'} to {chr(ord('A')+to) if to < 12 else 'table'}")
else:
    print("STATUS: unsat")