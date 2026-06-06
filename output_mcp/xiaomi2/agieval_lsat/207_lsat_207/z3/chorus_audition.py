from z3 import *

def get_orderings(extra_constraints_fn):
    solver = Solver()
    pos_K = Int('pos_K')
    pos_L = Int('pos_L')
    pos_T = Int('pos_T')
    pos_W = Int('pos_W')
    pos_Y = Int('pos_Y')
    pos_Z = Int('pos_Z')
    
    pos = [pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z]
    names = ['K', 'L', 'T', 'W', 'Y', 'Z']
    
    for p in pos:
        solver.add(p >= 1, p <= 6)
    solver.add(Distinct(pos))
    
    # Base constraints (conditions 1, 2, 4, 5)
    solver.add(pos_K != 4)  # Position 4 cannot be recorded
    solver.add(pos_L != 4)  # Position 4 cannot be recorded
    solver.add(Or(pos_K == 5, pos_L == 5))  # Position 5 must be recorded
    solver.add(pos_K < pos_T)  # Kammer before Trillo
    solver.add(pos_Z < pos_Y)  # Zinn before Yoshida
    
    # Add extra constraints (replacing condition 3)
    extra_constraints_fn(solver, pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z)
    
    orderings = []
    while solver.check() == sat:
        m = solver.model()
        vals = {}
        for i, p in enumerate(pos):
            vals[names[i]] = m[p].as_long()
        order = [None] * 6
        for name, p_val in vals.items():
            order[p_val - 1] = name
        orderings.append(tuple(order))
        solver.add(Or([p != m[p] for p in pos]))
    
    return set(orderings)

def original_constraints(solver, pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z):
    # Condition 3: Waite before both recorded auditions (K and L)
    solver.add(pos_W < pos_K)
    solver.add(pos_W < pos_L)

def opt_a(solver, pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z):
    # Zinn's audition is the only one that can take place earlier than Waite's
    solver.add(pos_Z < pos_W)
    solver.add(pos_K > pos_W)
    solver.add(pos_L > pos_W)
    solver.add(pos_T > pos_W)
    solver.add(pos_Y > pos_W)

def opt_b(solver, pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z):
    # Waite immediately before or after Zinn
    solver.add(Or(pos_W == pos_Z + 1, pos_W == pos_Z - 1))

def opt_c(solver, pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z):
    # Waite before Lugo
    solver.add(pos_W < pos_L)

def opt_d(solver, pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z):
    # Waite first or second
    solver.add(Or(pos_W == 1, pos_W == 2))

def opt_e(solver, pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z):
    # First audition cannot be recorded
    solver.add(pos_K != 1)
    solver.add(pos_L != 1)

original_set = get_orderings(original_constraints)
print(f"Original (condition 3): {len(original_set)} orderings")
for o in sorted(original_set):
    print(f"  {' '.join(o)}")

results = {}
for name, fn in [('A', opt_a), ('B', opt_b), ('C', opt_c), ('D', opt_d), ('E', opt_e)]:
    s = get_orderings(fn)
    results[name] = s
    match = (s == original_set)
    print(f"\nOption {name}: {len(s)} orderings, MATCH={match}")
    for o in sorted(s):
        print(f"  {' '.join(o)}")
    if not match:
        only_in_original = original_set - s
        only_in_option = s - original_set
        if only_in_original:
            print(f"  Missing from option (in original only): {len(only_in_original)}")
            for o in sorted(only_in_original):
                print(f"    {' '.join(o)}")
        if only_in_option:
            print(f"  Extra in option (not in original): {len(only_in_option)}")
            for o in sorted(only_in_option):
                print(f"    {' '.join(o)}")

# Summary
print("\n=== SUMMARY ===")
matching = [name for name in results if results[name] == original_set]
if len(matching) == 1:
    print(f"STATUS: sat")
    print(f"answer:{matching[0]}")
elif len(matching) > 1:
    print(f"STATUS: unsat")
    print(f"Refine: Multiple options match: {matching}")
else:
    print(f"STATUS: unsat")
    print(f"Refine: No options match")