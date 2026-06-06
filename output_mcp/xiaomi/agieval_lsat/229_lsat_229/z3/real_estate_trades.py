from z3 import *

# We'll model the problem by tracking building ownership after trades.
# Buildings and their classes:
# RealProp: Garza Tower (1), Yates House (3), Zimmer House (3)
# Southco: Flores Tower (1), Lynch Building (2)
# Trustcorp: King Building (2), Meyer Building (2), Ortiz Building (2)

# Let's define ownership as: each building belongs to one of 3 companies
# 0=RealProp, 1=Southco, 2=Trustcorp

# We'll model trades as sequences of exchanges.
# Since we don't know how many trades, let's try with a bounded number of trades.
# Trustcorp needs to get rid of all 3 class-2 buildings.
# Possible ways: trade class-2 for two class-3s, or swap class-2 for class-2 (doesn't help),
# or receive class-2 from others then trade them away.

# Let's try modeling with up to 4 trades (should be sufficient).

MAX_TRADES = 6

# Building indices
buildings = {
    'Garza': 0,    # class 1, RealProp
    'Yates': 1,    # class 3, RealProp
    'Zimmer': 2,   # class 3, RealProp
    'Flores': 3,   # class 1, Southco
    'Lynch': 4,    # class 2, Southco
    'King': 5,     # class 2, Trustcorp
    'Meyer': 6,    # class 2, Trustcorp
    'Ortiz': 7,    # class 2, Trustcorp
}

building_classes = [1, 3, 3, 1, 2, 2, 2, 2]
building_names = ['Garza', 'Yates', 'Zimmer', 'Flores', 'Lynch', 'King', 'Meyer', 'Ortiz']

# Company: 0=RealProp, 1=Southco, 2=Trustcorp
# owner[b][t] = company owning building b after trade t
# We have MAX_TRADES trades, so states 0..MAX_TRADES

solver = Solver()

# owner[b][t] = company owning building b at time t
owner = [[Int(f'owner_{b}_{t}') for t in range(MAX_TRADES+1)] for b in range(8)]

# Initial ownership
initial = [0, 0, 0, 1, 1, 2, 2, 2]  # RealProp, Southco, Trustcorp
for b in range(8):
    solver.add(owner[b][0] == initial[b])
    # Valid company range
    for t in range(MAX_TRADES+1):
        solver.add(owner[b][t] >= 0, owner[b][t] <= 2)

# Trade modeling: each trade is one of three types
# Type A: swap one building for another of same class (both change owner)
# Type B: trade one class-1 for two class-2s
# Type C: trade one class-2 for two class-3s

# For each trade step t (0-indexed), we define what happens
# We'll use a trade_type variable and specific building variables

trade_type = [Int(f'trade_type_{t}') for t in range(MAX_TRADES)]  # 0=none, 1=same-class, 2=1-for-2x2, 3=2-for-2x3

for t in range(MAX_TRADES):
    solver.add(trade_type[t] >= 0, trade_type[t] <= 3)

# For each trade, we need to specify which buildings are involved and who trades with whom
# Let's use a more structured approach:
# For each trade t, define:
#   - company_a, company_b (the two trading companies)
#   - buildings given by A, buildings given by B

# This gets complex. Let me use a simpler approach: track ownership changes directly.

# For each trade step, at most one trade happens.
# A trade involves two companies exchanging buildings.

# Let me define: for each trade t, which buildings change ownership
# changed[b][t] = True if building b changes owner at trade t
changed = [[Bool(f'changed_{b}_{t}') for t in range(MAX_TRADES)] for b in range(8)]

# If a building changes owner, it goes to one of the other two companies
# If it doesn't change, it stays with the same owner

for t in range(MAX_TRADES):
    for b in range(8):
        # If not changed, owner stays same
        solver.add(Implies(Not(changed[b][t]), owner[b][t+1] == owner[b][t]))
        # If changed, owner must be different
        solver.add(Implies(changed[b][t], owner[b][t+1] != owner[b][t]))

# Now encode trade types
# For each trade, exactly one trade type applies (or type 0 = no trade)

# Trade type 1: same-class swap - exactly 2 buildings of same class change hands, 
#   one from company A to B, one from B to A
# Trade type 2: 1-for-2x2 - one class-1 building from A to B, two class-2 buildings from B to A
# Trade type 3: 2-for-2x3 - one class-2 building from A to B, two class-3 buildings from B to A

# Let's encode each trade type's constraints on which buildings change

for t in range(MAX_TRADES):
    # Count buildings that change hands
    num_changed = Sum([If(changed[b][t], 1, 0) for b in range(8)])
    
    # Type 0: no trade
    solver.add(Implies(trade_type[t] == 0, num_changed == 0))
    
    # Type 1: same-class swap - exactly 2 buildings change, same class, 
    # they swap between two companies
    # The two buildings must be same class, and owned by different companies before trade
    # After trade, they swap owners
    
    # Type 2: 1-for-2x2 - 3 buildings change: 1 class-1 goes one way, 2 class-2 go other way
    # Type 3: 2-for-2x3 - 3 buildings change: 1 class-2 goes one way, 2 class-3 go other way
    
    solver.add(Implies(trade_type[t] == 1, num_changed == 2))
    solver.add(Implies(trade_type[t] == 2, num_changed == 3))
    solver.add(Implies(trade_type[t] == 3, num_changed == 3))
    
    # For type 1: the two changed buildings must have same class
    # For type 2: one class-1 and two class-2 change
    # For type 3: one class-2 and two class-3 change
    
    # Count changed buildings by class
    changed_class1 = Sum([If(And(changed[b][t], building_classes[b] == 1), 1, 0) for b in range(8)])
    changed_class2 = Sum([If(And(changed[b][t], building_classes[b] == 2), 1, 0) for b in range(8)])
    changed_class3 = Sum([If(And(changed[b][t], building_classes[b] == 3), 1, 0) for b in range(8)])
    
    # Type 1: same class swap
    solver.add(Implies(trade_type[t] == 1, Or(
        And(changed_class1 == 2, changed_class2 == 0, changed_class3 == 0),
        And(changed_class1 == 0, changed_class2 == 2, changed_class3 == 0),
        And(changed_class1 == 0, changed_class2 == 0, changed_class3 == 2)
    )))
    
    # Type 2: 1-for-2x2
    solver.add(Implies(trade_type[t] == 2, And(changed_class1 == 1, changed_class2 == 2, changed_class3 == 0)))
    
    # Type 3: 2-for-2x3
    solver.add(Implies(trade_type[t] == 3, And(changed_class1 == 0, changed_class2 == 1, changed_class3 == 2)))

# For each trade, the buildings that change must form a valid exchange between exactly 2 companies
for t in range(MAX_TRADES):
    # The changed buildings must involve exactly 2 companies
    # Company A gives some buildings, Company B gives some buildings
    # All changed buildings from A go to B and vice versa
    
    # For each pair of companies, check if the trade is between them
    for ca in range(3):
        for cb in range(ca+1, 3):
            # If trade is between ca and cb:
            # All changed buildings were owned by ca or cb before trade
            # Buildings owned by ca before trade go to cb after
            # Buildings owned by cb before trade go to ca after
            
            trade_between_ca_cb = And(
                # All changed buildings were owned by ca or cb
                And([Implies(changed[b][t], Or(owner[b][t] == ca, owner[b][t] == cb)) for b in range(8)]),
                # Changed buildings from ca go to cb
                And([Implies(And(changed[b][t], owner[b][t] == ca), owner[b][t+1] == cb) for b in range(8)]),
                # Changed buildings from cb go to ca
                And([Implies(And(changed[b][t], owner[b][t] == cb), owner[b][t+1] == ca) for b in range(8)])
            )
            
            # At least one pair must be the trading pair
            if ca == 0 and cb == 1:
                pair_01 = trade_between_ca_cb
            elif ca == 0 and cb == 2:
                pair_02 = trade_between_ca_cb
            elif ca == 1 and cb == 2:
                pair_12 = trade_between_ca_cb
    
    # If there's a trade (type != 0), exactly one pair is trading
    solver.add(Implies(trade_type[t] != 0, Or(pair_01, pair_02, pair_12)))
    # If no trade, no buildings change
    solver.add(Implies(trade_type[t] == 0, Not(Or(pair_01, pair_02, pair_12))))

# Constraint: Trustcorp owns no class-2 buildings after all trades
# Class-2 buildings: Lynch(4), King(5), Meyer(6), Ortiz(7)
for b in [4, 5, 6, 7]:
    solver.add(owner[b][MAX_TRADES] != 2)

# Now test each answer choice
# We need to find which MUST be true (i.e., holds in ALL valid final states)

# (A) RealProp owns a class 1 building
# Class 1 buildings: Garza(0), Flores(3)
opt_a = Or(owner[0][MAX_TRADES] == 0, owner[3][MAX_TRADES] == 0)

# (B) Southco owns only class 2 buildings
# Southco = company 1. Check that all buildings owned by Southco are class 2,
# and Southco owns at least one class-2 building
southco_owns = [owner[b][MAX_TRADES] == 1 for b in range(8)]
southco_class2 = [And(owner[b][MAX_TRADES] == 1, building_classes[b] == 2) for b in range(8)]
southco_non_class2 = [And(owner[b][MAX_TRADES] == 1, building_classes[b] != 2) for b in range(8)]
opt_b = And(Or(southco_class2), Not(Or(southco_non_class2)))

# (C) Southco has made at least one trade with Trustcorp
# This means at some trade step, the trading pair was (1, 2)
opt_c = Or([And(trade_type[t] != 0, 
               Or([And(changed[b][t], owner[b][t] == 1) for b in range(8)]),
               Or([And(changed[b][t], owner[b][t] == 2) for b in range(8)]))
           for t in range(MAX_TRADES)])

# (D) Trustcorp owns the Garza Tower
opt_d = (owner[0][MAX_TRADES] == 2)

# (E) Trustcorp owns the Zimmer House
opt_e = (owner[2][MAX_TRADES] == 2)

# Test each option: check if it's possible for the option to be FALSE
# If it's UNSAT for the option to be false, then the option MUST be true

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
    if solver.check() == sat:
        # Option can be false, so it's not necessarily true
        pass
    else:
        # Option must be true
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