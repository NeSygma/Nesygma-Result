from z3 import *

MAX_TRADES = 6

# Buildings: 0=Garza(1), 1=Yates(3), 2=Zimmer(3), 3=Flores(1), 4=Lynch(2), 5=King(2), 6=Meyer(2), 7=Ortiz(2)
# Companies: 0=R, 1=S, 2=T
building_classes = [1, 3, 3, 1, 2, 2, 2, 2]
init = [0, 0, 0, 1, 1, 2, 2, 2]

solver = Solver()

# owner[b][t] = company owning building b at time t
owner = {}
for b in range(8):
    for t in range(MAX_TRADES+1):
        owner[(b,t)] = Int(f'o_{b}_{t}')
        solver.add(owner[(b,t)] >= 0, owner[(b,t)] <= 2)

for b in range(8):
    solver.add(owner[(b,0)] == init[b])

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