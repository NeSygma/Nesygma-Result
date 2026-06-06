from z3 import *

# Declare variables for positions (1-6)
pos = {name: Int(f'pos_{name}') for name in ['K', 'L', 'T', 'W', 'Y', 'Z']}

# Base constraints
base = []
for name, p in pos.items():
    base.append(p >= 1)
    base.append(p <= 6)
base.append(Distinct(list(pos.values())))
base.append(pos['K'] != 4)
base.append(pos['L'] != 4)
base.append(Or(pos['K'] == 5, pos['L'] == 5))
base.append(pos['K'] < pos['T'])
base.append(pos['Z'] < pos['Y'])

# Original constraint
original = And(pos['W'] < pos['K'], pos['W'] < pos['L'])

# Option constraints
opt_a = And(pos['Z'] < pos['W'], *[pos[X] > pos['W'] for X in ['K', 'L', 'T', 'Y']])
opt_b = Or(pos['W'] == pos['Z'] - 1, pos['W'] == pos['Z'] + 1)
opt_c = pos['W'] < pos['L']
opt_d = Or(pos['W'] == 1, pos['W'] == 2)
opt_e = And(pos['K'] != 1, pos['L'] != 1)

options = [('A', opt_a), ('B', opt_b), ('C', opt_c), ('D', opt_d), ('E', opt_e)]

for letter, opt in options:
    print(f"\nChecking option {letter}:")
    
    # Check 1: base + original => opt
    s1 = Solver()
    s1.add(base)
    s1.add(original)
    s1.add(Not(opt))
    res1 = s1.check()
    if res1 == unsat:
        print("  base + original => opt: TRUE")
    else:
        print("  base + original => opt: FALSE")
        # Show a counterexample
        m = s1.model()
        print("  Counterexample:", {name: m.evaluate(pos[name]) for name in pos})
    
    # Check 2: base + opt => original
    s2 = Solver()
    s2.add(base)
    s2.add(opt)
    s2.add(Not(original))
    res2 = s2.check()
    if res2 == unsat:
        print("  base + opt => original: TRUE")
    else:
        print("  base + opt => original: FALSE")
        # Show a counterexample
        m = s2.model()
        print("  Counterexample:", {name: m.evaluate(pos[name]) for name in pos})
    
    if res1 == unsat and res2 == unsat:
        print(f"  => Option {letter} is equivalent to original constraint.")
    else:
        print(f"  => Option {letter} is NOT equivalent.")