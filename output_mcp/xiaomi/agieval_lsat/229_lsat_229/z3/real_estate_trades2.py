from z3 import *

# Let me think about this more carefully.
# 
# Initial state:
# RealProp (R): Garza(1), Yates(3), Zimmer(3)  -> 1 class-1, 0 class-2, 2 class-3
# Southco (S):  Flores(1), Lynch(2)             -> 1 class-1, 1 class-2, 0 class-3
# Trustcorp (T): King(2), Meyer(2), Ortiz(2)    -> 0 class-1, 3 class-2, 0 class-3
#
# Trade types:
# 1) Swap: 1 building for 1 building of same class
# 2) 1-for-2x2: 1 class-1 for 2 class-2
# 3) 2-for-2x3: 1 class-2 for 2 class-3
#
# Goal: Trustcorp has 0 class-2 buildings after trades.
#
# Let me track the COUNT of buildings by class for each company.
# This is simpler than tracking individual buildings.

# State: (c1_R, c2_R, c3_R, c1_S, c2_S, c3_S, c1_T, c2_T, c3_T)
# Initial: R=(1,0,2), S=(1,1,0), T=(0,3,0)
# Total: c1=2, c2=4, c3=2 (conserved per class)

# But we also need to track WHICH specific buildings each company has
# to answer questions about specific buildings (D and E).

# Let me use a hybrid approach: track counts AND specific building ownership.

# Actually, let me think about what trades are possible and what states are reachable.

# Key insight: Trustcorp starts with 3 class-2 buildings and must end with 0.
# Ways to lose class-2 buildings:
# - Trade class-2 for class-2 (same class swap) - net 0 change
# - Trade class-2 for two class-3s (type 3) - lose 1 class-2, gain 2 class-3
# - Receive class-2 from others then trade them away

# To go from 3 class-2 to 0 class-2, Trustcorp must do at least 3 type-3 trades
# (each removes 1 class-2), OR receive class-2 and trade more.

# Let me enumerate possible sequences more carefully.
# Actually, let me just model it with bounded model checking.

MAX_TRADES = 8

# Track building ownership
# Buildings: 0=Garza(1), 1=Yates(3), 2=Zimmer(3), 3=Flores(1), 4=Lynch(2), 5=King(2), 6=Meyer(2), 7=Ortiz(2)
# Companies: 0=R, 1=S, 2=T

solver = Solver()

# owner[b][t] = company owning building b at time t
owner = {}
for b in range(8):
    for t in range(MAX_TRADES+1):
        owner[(b,t)] = Int(f'o_{b}_{t}')
        solver.add(owner[(b,t)] >= 0, owner[(b,t)] <= 2)

# Initial ownership
init = [0, 0, 0, 1, 1, 2, 2, 2]
for b in range(8):
    solver.add(owner[(b,0)] == init[b])

# For each trade step, model what happens
# A trade involves two companies exchanging buildings according to one of the 3 types

for t in range(MAX_TRADES):
    # Trade type: 0=none, 1=same-class swap, 2=1-for-2x2, 3=2-for-2x3
    tt = Int(f'tt_{t}')
    solver.add(tt >= 0, tt <= 3)
    
    # Which buildings change hands
    changed = [Bool(f'ch_{b}_{t}') for b in range(8)]
    
    # If not changed, owner stays same
    for b in range(8):
        solver.add(Implies(Not(changed[b]), owner[(b,t+1)] == owner[(b,t)]))
        solver.add(Implies(changed[b], owner[(b,t+1)] != owner[(b,t)]))
    
    # Count changed by class
    ch_c1 = Sum([If(And(changed[b], building_classes[b] == 1), 1, 0) for b in range(8)])
    ch_c2 = Sum([If(And(changed[b], building_classes[b] == 2), 1, 0) for b in range(8)])
    ch_c3 = Sum([If(And(changed[b], building_classes[b] == 3), 1, 0) for b in range(8)])
    num_ch = Sum([If(changed[b], 1, 0) for b in range(8)])
    
    # Type constraints
    solver.add(Implies(tt == 0, num_ch == 0))
    solver.add(Implies(tt == 1, And(num_ch == 2, Or(
        And(ch_c1 == 2, ch_c2 == 0, ch_c3 == 0),
        And(ch_c1 == 0, ch_c2 == 2, ch_c3 == 0),
        And(ch_c1 == 0, ch_c2 == 0, ch_c3 == 2)))))
    solver.add(Implies(tt == 2, And(ch_c1 == 1, ch_c2 == 2, ch_c3 == 0)))
    solver.add(Implies(tt == 3, And(ch_c1 == 0, ch_c2 == 1, ch_c3 == 2)))
    
    # Exchange constraint: changed buildings form a valid exchange between 2 companies
    # All changed buildings must be owned by exactly 2 companies before trade
    # Buildings from company A go to B, buildings from B go to A
    
    # For each pair of companies
    for ca in range(3):
        for cb in range(ca+1, 3):
            # Check if this is the trading pair
            all_from_ca_or_cb = And([Implies(changed[b], Or(owner[(b,t)] == ca, owner[(b,t)] == cb)) for b in range(8)])
            ca_goes_to_cb = And([Implies(And(changed[b], owner[(b,t)] == ca), owner[(b,t+1)] == cb) for b in range(8)])
            cb_goes_to_ca = And([Implies(And(changed[b], owner[(b,t)] == cb), owner[(b,t+1)] == ca) for b in range(8)])
            
            pair_valid = And(all_from_ca_or_cb, ca_goes_to_cb, cb_goes_to_ca)
            
            # Store for later use
            if ca == 0 and cb == 1:
                p01 = pair_valid
            elif ca == 0 and cb == 2:
                p02 = pair_valid
            elif ca == 1 and cb == 2:
                p12 = pair_valid
    
    # If trade happens, exactly one pair is valid
    solver.add(Implies(tt != 0, Or(p01, p02, p12)))
    # Also need: both companies give at least one building
    # (This is implicit in the trade type definitions)
    
    # For type 1: each company gives 1 building
    # For type 2: one company gives 1 class-1, other gives 2 class-2
    # For type 3: one company gives 1 class-2, other gives 2 class-3
    
    # Ensure both sides of trade have buildings to give
    # For type 2: the company giving class-1 must own a class-1, the other must own 2 class-2
    # For type 3: the company giving class-2 must own a class-2, the other must own 2 class-3
    
    # This is implicitly handled by the ownership constraints, but let's be explicit
    # about which company gives what for each trade type
    
    # For type 2 (1-for-2x2): either ca gives 1 class-1 and gets 2 class-2, or vice versa
    # For type 3 (2-for-2x3): either ca gives 1 class-2 and gets 2 class-3, or vice versa
    
    # The exchange constraints above already handle this correctly since
    # buildings change ownership between the two companies.

# Constraint: Trustcorp owns no class-2 buildings at the end
for b in [4, 5, 6, 7]:  # Lynch, King, Meyer, Ortiz are class-2
    solver.add(owner[(b, MAX_TRADES)] != 2)

# Now test each answer choice
# (A) RealProp owns a class 1 building at the end
opt_a = Or(owner[(0, MAX_TRADES)] == 0, owner[(3, MAX_TRADES)] == 0)

# (B) Southco owns only class 2 buildings at the end
# All buildings Southco owns must be class 2, and Southco must own at least one
southco_owns_any = Or([owner[(b, MAX_TRADES)] == 1 for b in range(8)])
southco_all_class2 = And([Implies(owner[(b, MAX_TRADES)] == 1, building_classes[b] == 2) for b in range(8)])
opt_b = And(southco_owns_any, southco_all_class2)

# (C) Southco has made at least one trade with Trustcorp
# At some trade step, the pair (1,2) was active
opt_c = Or([Bool(f'pair_12_active_{t}') for t in range(MAX_TRADES)])

# Hmm, I need to track which pair is active. Let me add that.
# Actually, let me restructure. Let me add pair tracking variables.

# Let me restart with cleaner pair tracking
solver = Solver()

# Re-declare everything
owner = {}
for b in range(8):
    for t in range(MAX_TRADES+1):
        owner[(b,t)] = Int(f'o_{b}_{t}')
        solver.add(owner[(b,t)] >= 0, owner[(b,t)] <= 2)

for b in range(8):
    solver.add(owner[(b,0)] == init[b])

building_classes = [1, 3, 3, 1, 2, 2, 2, 2]

# Pair active flags
pair_01 = [Bool(f'p01_{t}') for t in range(MAX_TRADES)]
pair_02 = [Bool(f'p02_{t}') for t in range(MAX_TRADES)]
pair_12 = [Bool(f'p12_{t}') for t in range(MAX_TRADES)]

for t in range(MAX_TRADES):
    tt = Int(f'tt_{t}')
    solver.add(tt >= 0, tt <= 3)
    
    changed = [Bool(f'ch_{b}_{t}') for b in range(8)]
    
    for b in range(8):
        solver.add(Implies(Not(changed[b]), owner[(b,t+1)] == owner[(b,t)]))
        solver.add(Implies(changed[b], owner[(b,t+1)] != owner[(b,t)]))
    
    ch_c1 = Sum([If(And(changed[b], building_classes[b] == 1), 1, 0) for b in range(8)])
    ch_c2 = Sum([If(And(changed[b], building_classes[b] == 2), 1, 0) for b in range(8)])
    ch_c3 = Sum([If(And(changed[b], building_classes[b] == 3), 1, 0) for b in range(8)])
    num_ch = Sum([If(changed[b], 1, 0) for b in range(8)])
    
    solver.add(Implies(tt == 0, num_ch == 0))
    solver.add(Implies(tt == 1, And(num_ch == 2, Or(
        And(ch_c1 == 2, ch_c2 == 0, ch_c3 == 0),
        And(ch_c1 == 0, ch_c2 == 2, ch_c3 == 0),
        And(ch_c1 == 0, ch_c2 == 0, ch_c3 == 2)))))
    solver.add(Implies(tt == 2, And(ch_c1 == 1, ch_c2 == 2, ch_c3 == 0)))
    solver.add(Implies(tt == 3, And(ch_c1 == 0, ch_c2 == 1, ch_c3 == 2)))
    
    # Pair constraints
    # If pair_01 active: all changed buildings owned by 0 or 1, swap between them
    solver.add(Implies(pair_01[t], And(
        And([Implies(changed[b], Or(owner[(b,t)] == 0, owner[(b,t)] == 1)) for b in range(8)]),
        And([Implies(And(changed[b], owner[(b,t)] == 0), owner[(b,t+1)] == 1) for b in range(8)]),
        And([Implies(And(changed[b], owner[(b,t)] == 1), owner[(b,t+1)] == 0) for b in range(8)])
    )))
    
    solver.add(Implies(pair_02[t], And(
        And([Implies(changed[b], Or(owner[(b,t)] == 0, owner[(b,t)] == 2)) for b in range(8)]),
        And([Implies(And(changed[b], owner[(b,t)] == 0), owner[(b,t+1)] == 2) for b in range(8)]),
        And([Implies(And(changed[b], owner[(b,t)] == 2), owner[(b,t+1)] == 0) for b in range(8)])
    )))
    
    solver.add(Implies(pair_12[t], And(
        And([Implies(changed[b], Or(owner[(b,t)] == 1, owner[(b,t)] == 2)) for b in range(8)]),
        And([Implies(And(changed[b], owner[(b,t)] == 1), owner[(b,t+1)] == 2) for b in range(8)]),
        And([Implies(And(changed[b], owner[(b,t)] == 2), owner[(b,t+1)] == 1) for b in range(8)])
    )))
    
    # Exactly one pair active if trade happens
    solver.add(Implies(tt != 0, 
        Or(And(pair_01[t], Not(pair_02[t]), Not(pair_12[t])),
           And(Not(pair_01[t]), pair_02[t], Not(pair_12[t])),
           And(Not(pair_01[t]), Not(pair_02[t]), pair_12[t]))))
    solver.add(Implies(tt == 0, And(Not(pair_01[t]), Not(pair_02[t]), Not(pair_12[t]))))

# Trustcorp ends with 0 class-2 buildings
for b in [4, 5, 6, 7]:
    solver.add(owner[(b, MAX_TRADES)] != 2)

# Answer choices
opt_a = Or(owner[(0, MAX_TRADES)] == 0, owner[(3, MAX_TRADES)] == 0)

southco_owns_any = Or([owner[(b, MAX_TRADES)] == 1 for b in range(8)])
southco_all_class2 = And([Implies(owner[(b, MAX_TRADES)] == 1, building_classes[b] == 2) for b in range(8)])
opt_b = And(southco_owns_any, southco_all_class2)

opt_c = Or([pair_12[t] for t in range(MAX_TRADES)])

opt_d = (owner[(0, MAX_TRADES)] == 2)

opt_e = (owner[(2, MAX_TRADES)] == 2)

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e),
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

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")