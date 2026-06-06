from z3 import *

# Let's think about this differently.
# We track: for each company, how many class 1, 2, 3 buildings they own.
# Initial: R: (1,0,2), S: (1,1,0), T: (0,3,0)
# Trade types (between two companies A and B):
#   Type 1: A gives 1 class-c, B gives 1 class-c (same class)
#   Type 2: A gives 1 class-1, B gives 2 class-2
#   Type 3: A gives 1 class-2, B gives 2 class-3
# (or reverse direction for types 2 and 3)

# We need to find sequences of trades such that T ends with 0 class-2.
# Then check which answer must be true.

# Let's enumerate possible final states by tracking counts.
# R_c1, R_c2, R_c3 = class counts for RealProp
# S_c1, S_c2, S_c3 = class counts for Southco
# T_c1, T_c2, T_c3 = class counts for Trustcorp

# Total buildings: class1=2, class2=4, class3=2
# So R_c1+S_c1+T_c1=2, R_c2+S_c2+T_c2=4, R_c3+S_c3+T_c3=2

# Each trade changes counts. Let's model trades abstractly.
# A trade between companies X and Y of type t changes their counts.

# Trade types (X gives to Y):
# T1: X gives 1c1, Y gives 1c1 -> net: no change (just swap)
# T1: X gives 1c2, Y gives 1c2 -> net: no change
# T1: X gives 1c3, Y gives 1c3 -> net: no change
# T2: X gives 1c1, Y gives 2c2 -> X: c1-1, c2+2; Y: c1+1, c2-2
# T2 reverse: X gives 2c2, Y gives 1c1 -> X: c1+1, c2-2; Y: c1-1, c2+2
# T3: X gives 1c2, Y gives 2c3 -> X: c2-1, c3+2; Y: c2+1, c3-2
# T3 reverse: X gives 2c3, Y gives 1c2 -> X: c2+1, c3-2; Y: c2-1, c3+2

# Let's use a different approach: just try all possible final states
# and check if they're reachable.

# We'll use Z3 to find reachable states.
# Let's model with a bounded number of trades.

MAX_TRADES = 8

solver = Solver()

# State at each time step: (R_c1, R_c2, R_c3, S_c1, S_c2, S_c3, T_c1, T_c2, T_c3)
R_c1 = [Int(f'R_c1_{t}') for t in range(MAX_TRADES+1)]
R_c2 = [Int(f'R_c2_{t}') for t in range(MAX_TRADES+1)]
R_c3 = [Int(f'R_c3_{t}') for t in range(MAX_TRADES+1)]
S_c1 = [Int(f'S_c1_{t}') for t in range(MAX_TRADES+1)]
S_c2 = [Int(f'S_c2_{t}') for t in range(MAX_TRADES+1)]
S_c3 = [Int(f'S_c3_{t}') for t in range(MAX_TRADES+1)]
T_c1 = [Int(f'T_c1_{t}') for t in range(MAX_TRADES+1)]
T_c2 = [Int(f'T_c2_{t}') for t in range(MAX_TRADES+1)]
T_c3 = [Int(f'T_c3_{t}') for t in range(MAX_TRADES+1)]

# Initial state
solver.add(R_c1[0] == 1, R_c2[0] == 0, R_c3[0] == 2)
solver.add(S_c1[0] == 1, S_c2[0] == 1, S_c3[0] == 0)
solver.add(T_c1[0] == 0, T_c2[0] == 3, T_c3[0] == 0)

# Conservation constraints at all times
for t in range(MAX_TRADES+1):
    solver.add(R_c1[t] + S_c1[t] + T_c1[t] == 2)
    solver.add(R_c2[t] + S_c2[t] + T_c2[t] == 4)
    solver.add(R_c3[t] + S_c3[t] + T_c3[t] == 2)
    solver.add(R_c1[t] >= 0, R_c2[t] >= 0, R_c3[t] >= 0)
    solver.add(S_c1[t] >= 0, S_c2[t] >= 0, S_c3[t] >= 0)
    solver.add(T_c1[t] >= 0, T_c2[t] >= 0, T_c3[t] >= 0)

# Trade types: each trade is between two companies
# We encode each trade as a choice of type and direction
# trade_type[t] = 0 (no trade), 1 (same-class swap), 2 (c1<->2c2), 3 (c2<->2c3)
# pair[t] = which pair trades: 0 (R-S), 1 (R-T), 2 (S-T)
# direction[t] = 0 or 1 (which company gives the "1" side)

trade_type = [Int(f'tt_{t}') for t in range(MAX_TRADES)]
pair = [Int(f'pr_{t}') for t in range(MAX_TRADES)]
direction = [Int(f'dr_{t}') for t in range(MAX_TRADES)]

for t in range(MAX_TRADES):
    solver.add(trade_type[t] >= 0, trade_type[t] <= 3)
    solver.add(pair[t] >= 0, pair[t] <= 2)
    solver.add(direction[t] >= 0, direction[t] <= 1)
    
    # No trade
    solver.add(Implies(trade_type[t] == 0, And(
        R_c1[t+1] == R_c1[t], R_c2[t+1] == R_c2[t], R_c3[t+1] == R_c3[t],
        S_c1[t+1] == S_c1[t], S_c2[t+1] == S_c2[t], S_c3[t+1] == S_c3[t],
        T_c1[t+1] == T_c1[t], T_c2[t+1] == T_c2[t], T_c3[t+1] == T_c3[t]
    )))
    
    # Type 1: same-class swap (no net change in counts)
    solver.add(Implies(trade_type[t] == 1, And(
        R_c1[t+1] == R_c1[t], R_c2[t+1] == R_c2[t], R_c3[t+1] == R_c3[t],
        S_c1[t+1] == S_c1[t], S_c2[t+1] == S_c2[t], S_c3[t+1] == S_c3[t],
        T_c1[t+1] == T_c1[t], T_c2[t+1] == T_c2[t], T_c3[t+1] == T_c3[t]
    )))
    
    # Type 2: 1c1 <-> 2c2
    # If pair=0 (R-S), dir=0: R gives 1c1, S gives 2c2
    #   R: c1-1, c2+2; S: c1+1, c2-2
    # If pair=0, dir=1: S gives 1c1, R gives 2c2
    #   R: c1+1, c2-2; S: c1-1, c2+2
    # Similarly for other pairs
    
    # R-S, dir=0
    solver.add(Implies(And(trade_type[t] == 2, pair[t] == 0, direction[t] == 0), And(
        R_c1[t+1] == R_c1[t] - 1, R_c2[t+1] == R_c2[t] + 2, R_c3[t+1] == R_c3[t],
        S_c1[t+1] == S_c1[t] + 1, S_c2[t+1] == S_c2[t] - 2, S_c3[t+1] == S_c3[t],
        T_c1[t+1] == T_c1[t], T_c2[t+1] == T_c2[t], T_c3[t+1] == T_c3[t]
    )))
    # R-S, dir=1
    solver.add(Implies(And(trade_type[t] == 2, pair[t] == 0, direction[t] == 1), And(
        R_c1[t+1] == R_c1[t] + 1, R_c2[t+1] == R_c2[t] - 2, R_c3[t+1] == R_c3[t],
        S_c1[t+1] == S_c1[t] - 1, S_c2[t+1] == S_c2[t] + 2, S_c3[t+1] == S_c3[t],
        T_c1[t+1] == T_c1[t], T_c2[t+1] == T_c2[t], T_c3[t+1] == T_c3[t]
    )))
    # R-T, dir=0
    solver.add(Implies(And(trade_type[t] == 2, pair[t] == 1, direction[t] == 0), And(
        R_c1[t+1] == R_c1[t] - 1, R_c2[t+1] == R_c2[t] + 2, R_c3[t+1] == R_c3[t],
        S_c1[t+1] == S_c1[t], S_c2[t+1] == S_c2[t], S_c3[t+1] == S_c3[t],
        T_c1[t+1] == T_c1[t] + 1, T_c2[t+1] == T_c2[t] - 2, T_c3[t+1] == T_c3[t]
    )))
    # R-T, dir=1
    solver.add(Implies(And(trade_type[t] == 2, pair[t] == 1, direction[t] == 1), And(
        R_c1[t+1] == R_c1[t] + 1, R_c2[t+1] == R_c2[t] - 2, R_c3[t+1] == R_c3[t],
        S_c1[t+1] == S_c1[t], S_c2[t+1] == S_c2[t], S_c3[t+1] == S_c3[t],
        T_c1[t+1] == T_c1[t] - 1, T_c2[t+1] == T_c2[t] + 2, T_c3[t+1] == T_c3[t]
    )))
    # S-T, dir=0
    solver.add(Implies(And(trade_type[t] == 2, pair[t] == 2, direction[t] == 0), And(
        R_c1[t+1] == R_c1[t], R_c2[t+1] == R_c2[t], R_c3[t+1] == R_c3[t],
        S_c1[t+1] == S_c1[t] - 1, S_c2[t+1] == S_c2[t] + 2, S_c3[t+1] == S_c3[t],
        T_c1[t+1] == T_c1[t] + 1, T_c2[t+1] == T_c2[t] - 2, T_c3[t+1] == T_c3[t]
    )))
    # S-T, dir=1
    solver.add(Implies(And(trade_type[t] == 2, pair[t] == 2, direction[t] == 1), And(
        R_c1[t+1] == R_c1[t], R_c2[t+1] == R_c2[t], R_c3[t+1] == R_c3[t],
        S_c1[t+1] == S_c1[t] + 1, S_c2[t+1] == S_c2[t] - 2, S_c3[t+1] == S_c3[t],
        T_c1[t+1] == T_c1[t] - 1, T_c2[t+1] == T_c2[t] + 2, T_c3[t+1] == T_c3[t]
    )))
    
    # Type 3: 1c2 <-> 2c3
    # R-S, dir=0: R gives 1c2, S gives 2c3
    solver.add(Implies(And(trade_type[t] == 3, pair[t] == 0, direction[t] == 0), And(
        R_c1[t+1] == R_c1[t], R_c2[t+1] == R_c2[t] - 1, R_c3[t+1] == R_c3[t] + 2,
        S_c1[t+1] == S_c1[t], S_c2[t+1] == S_c2[t] + 1, S_c3[t+1] == S_c3[t] - 2,
        T_c1[t+1] == T_c1[t], T_c2[t+1] == T_c2[t], T_c3[t+1] == T_c3[t]
    )))
    # R-S, dir=1
    solver.add(Implies(And(trade_type[t] == 3, pair[t] == 0, direction[t] == 1), And(
        R_c1[t+1] == R_c1[t], R_c2[t+1] == R_c2[t] + 1, R_c3[t+1] == R_c3[t] - 2,
        S_c1[t+1] == S_c1[t], S_c2[t+1] == S_c2[t] - 1, S_c3[t+1] == S_c3[t] + 2,
        T_c1[t+1] == T_c1[t], T_c2[t+1] == T_c2[t], T_c3[t+1] == T_c3[t]
    )))
    # R-T, dir=0
    solver.add(Implies(And(trade_type[t] == 3, pair[t] == 1, direction[t] == 0), And(
        R_c1[t+1] == R_c1[t], R_c2[t+1] == R_c2[t] - 1, R_c3[t+1] == R_c3[t] + 2,
        S_c1[t+1] == S_c1[t], S_c2[t+1] == S_c2[t], S_c3[t+1] == S_c3[t],
        T_c1[t+1] == T_c1[t], T_c2[t+1] == T_c2[t] + 1, T_c3[t+1] == T_c3[t] - 2
    )))
    # R-T, dir=1
    solver.add(Implies(And(trade_type[t] == 3, pair[t] == 1, direction[t] == 1), And(
        R_c1[t+1] == R_c1[t], R_c2[t+1] == R_c2[t] + 1, R_c3[t+1] == R_c3[t] - 2,
        S_c1[t+1] == S_c1[t], S_c2[t+1] == S_c2[t], S_c3[t+1] == S_c3[t],
        T_c1[t+1] == T_c1[t], T_c2[t+1] == T_c2[t] - 1, T_c3[t+1] == T_c3[t] + 2
    )))
    # S-T, dir=0
    solver.add(Implies(And(trade_type[t] == 3, pair[t] == 2, direction[t] == 0), And(
        R_c1[t+1] == R_c1[t], R_c2[t+1] == R_c2[t], R_c3[t+1] == R_c3[t],
        S_c1[t+1] == S_c1[t], S_c2[t+1] == S_c2[t] - 1, S_c3[t+1] == S_c3[t] + 2,
        T_c1[t+1] == T_c1[t], T_c2[t+1] == T_c2[t] + 1, T_c3[t+1] == T_c3[t] - 2
    )))
    # S-T, dir=1
    solver.add(Implies(And(trade_type[t] == 3, pair[t] == 2, direction[t] == 1), And(
        R_c1[t+1] == R_c1[t], R_c2[t+1] == R_c2[t], R_c3[t+1] == R_c3[t],
        S_c1[t+1] == S_c1[t], S_c2[t+1] == S_c2[t] + 1, S_c3[t+1] == S_c3[t] - 2,
        T_c1[t+1] == T_c1[t], T_c2[t+1] == T_c2[t] - 1, T_c3[t+1] == T_c3[t] + 2
    )))

# Goal: Trustcorp has 0 class-2 buildings at end
solver.add(T_c2[MAX_TRADES] == 0)

# Answer choices
# (A) RealProp owns a class 1 building
opt_a = Or(R_c1[MAX_TRADES] >= 1)

# (B) Southco owns only class 2 buildings
opt_b = And(S_c1[MAX_TRADES] == 0, S_c3[MAX_TRADES] == 0, S_c2[MAX_TRADES] >= 1)

# (C) Southco has made at least one trade with Trustcorp
# This means at some time t, pair[t] == 2 and trade_type[t] != 0
opt_c = Or([And(pair[t] == 2, trade_type[t] != 0) for t in range(MAX_TRADES)])

# (D) Trustcorp owns the Garza Tower
# Garza is class 1. T_c1 >= 1 means T owns at least one class-1 building.
# But there are 2 class-1 buildings. We need to track which specific building.
# Actually, we can't distinguish which class-1 building T owns with just counts.
# Let me think... Garza is one of two class-1 buildings. If T has at least 1 class-1,
# it could be Garza or Flores. We need to track individual buildings.
# For now, let's approximate: if T has >= 1 class-1, it MIGHT own Garza.
# But we need to be more precise. Let me add building-level tracking.

# Actually, let me reconsider. With just counts, we can't determine (D) and (E) precisely.
# Let me add building-level tracking for the specific buildings mentioned.

# Let me track: does Trustcorp own Garza (building 0), Zimmer (building 2)?
# These are specific buildings. We need to track them individually.

# Let me add variables for specific buildings
garza_owner = [Int(f'garza_{t}') for t in range(MAX_TRADES+1)]
zimmer_owner = [Int(f'zimmer_{t}') for t in range(MAX_TRADES+1)]

solver.add(garza_owner[0] == 0)  # RealProp
solver.add(zimmer_owner[0] == 0)  # RealProp

for t in range(MAX_TRADES+1):
    solver.add(garza_owner[t] >= 0, garza_owner[t] <= 2)
    solver.add(zimmer_owner[t] >= 0, zimmer_owner[t] <= 2)

# When a trade happens, specific buildings can change owner
# For type 1 (same class), we need to track which specific buildings swap
# This gets complex. Let me simplify: just check if it's possible for T to own Garza/Zimmer

# Actually, let me just check the count-based options first and see if we get a unique answer.

opt_d_approx = (T_c1[MAX_TRADES] >= 1)  # T owns at least one class-1 building
opt_e_approx = (T_c3[MAX_TRADES] >= 1)  # T owns at least one class-3 building

# But wait - Zimmer is class 3. T_c3 >= 1 means T owns at least one class-3 building.
# There are only 2 class-3 buildings (Yates and Zimmer). So T_c3 >= 1 means T owns one of them.

# For (D): Garza is class 1. T_c1 >= 1 means T owns at least one class-1 building.
# There are 2 class-1 buildings (Garza and Flores). So T_c1 >= 1 means T owns one of them,
# but not necessarily Garza.

# Hmm, this is tricky. Let me think about whether the answer can be determined from counts alone.

# Let me first check options A, B, C with the count model.
# For D and E, I'll need building-level tracking.

# Let me try a different approach: track building-level ownership for all buildings.
# This is more complex but necessary for D and E.

# Actually, let me just run with the count model for A, B, C first and see what happens.
# Then I'll refine for D and E if needed.

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    result = solver.check()
    if result == sat:
        pass  # Can be false
    elif result == unsat:
        found_options.append(letter)
    solver.pop()

print(f"Options that must be true (count-based): {found_options}")

# Now let's check D and E with building-level tracking
# We need to track individual building ownership through trades
# This is complex with the count model. Let me try a different approach.

# For D: Can T end up owning Garza?
# Garza starts with R. For T to own Garza, there must be a trade where Garza moves to T.
# This can happen via:
# - R-T trade of type 1 (same class, Garza is class 1)
# - R-S trade then S-T trade
# etc.

# Let me check if it's possible for T to own Garza (D) and Zimmer (E)
# by adding building-level tracking.

# Actually, let me just check: with the count model, can T have c1 >= 1?
# If yes, then D is possible (but not guaranteed).
# If T must have c1 >= 1, then D is possible.

# Let me check if T_c1 >= 1 is forced
solver.push()
solver.add(T_c1[MAX_TRADES] == 0)
result_c1 = solver.check()
solver.pop()

solver.push()
solver.add(T_c3[MAX_TRADES] == 0)
result_c3 = solver.check()
solver.pop()

print(f"T_c1 == 0 possible: {result_c1}")
print(f"T_c3 == 0 possible: {result_c3}")

# Check if T can own Garza specifically
# For this, I need building-level tracking. Let me add it.

# Let me track: for each building, who owns it at each time
# Building 0 (Garza, c1), 1 (Yates, c3), 2 (Zimmer, c3), 3 (Flores, c1),
# 4 (Lynch, c2), 5 (King, c2), 6 (Meyer, c2), 7 (Ortiz, c2)

bld_owner = {}
for b in range(8):
    for t in range(MAX_TRADES+1):
        bld_owner[(b,t)] = Int(f'bo_{b}_{t}')
        solver.add(bld_owner[(b,t)] >= 0, bld_owner[(b,t)] <= 2)

solver.add(bld_owner[(0,0)] == 0)  # Garza: R
solver.add(bld_owner[(1,0)] == 0)  # Yates: R
solver.add(bld_owner[(2,0)] == 0)  # Zimmer: R
solver.add(bld_owner[(3,0)] == 1)  # Flores: S
solver.add(bld_owner[(4,0)] == 1)  # Lynch: S
solver.add(bld_owner[(5,0)] == 2)  # King: T
solver.add(bld_owner[(6,0)] == 2)  # Meyer: T
solver.add(bld_owner[(7,0)] == 2)  # Ortiz: T

# Consistency: counts must match
for t in range(MAX_TRADES+1):
    solver.add(R_c1[t] == Sum([If(bld_owner[(b,t)] == 0, 1, 0) for b in [0,3]]))
    solver.add(R_c2[t] == Sum([If(bld_owner[(b,t)] == 0, 1, 0) for b in [4,5,6,7]]))
    solver.add(R_c3[t] == Sum([If(bld_owner[(b,t)] == 0, 1, 0) for b in [1,2]]))
    solver.add(S_c1[t] == Sum([If(bld_owner[(b,t)] == 1, 1, 0) for b in [0,3]]))
    solver.add(S_c2[t] == Sum([If(bld_owner[(b,t)] == 1, 1, 0) for b in [4,5,6,7]]))
    solver.add(S_c3[t] == Sum([If(bld_owner[(b,t)] == 1, 1, 0) for b in [1,2]]))
    solver.add(T_c1[t] == Sum([If(bld_owner[(b,t)] == 2, 1, 0) for b in [0,3]]))
    solver.add(T_c2[t] == Sum([If(bld_owner[(b,t)] == 2, 1, 0) for b in [4,5,6,7]]))
    solver.add(T_c3[t] == Sum([If(bld_owner[(b,t)] == 2, 1, 0) for b in [1,2]]))

# Now check D and E
opt_d = (bld_owner[(0, MAX_TRADES)] == 2)  # T owns Garza
opt_e = (bld_owner[(2, MAX_TRADES)] == 2)  # T owns Zimmer

options2 = [
    ("D", opt_d),
    ("E", opt_e),
]

for letter, constr in options2:
    solver.push()
    solver.add(Not(constr))
    result = solver.check()
    if result == sat:
        pass  # Can be false
    elif result == unsat:
        found_options.append(letter)
    solver.pop()

print(f"All options that must be true: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")