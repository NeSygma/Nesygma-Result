from z3 import *

clues = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']

def get_all_solutions(extra_constr_fn=None):
    solver = Solver()
    chap = {c: Int(f'chap_{c}') for c in clues}
    
    for c in clues:
        solver.add(chap[c] >= 1, chap[c] <= 7)
    solver.add(Distinct([chap[c] for c in clues]))
    
    if extra_constr_fn is None:
        solver.add(chap['T'] != 1)
    else:
        solver.add(extra_constr_fn(chap))
    
    solver.add(chap['T'] < chap['W'])
    solver.add(chap['W'] - chap['T'] == 3)
    solver.add(Abs(chap['S'] - chap['Z']) != 1)
    solver.add(Abs(chap['W'] - chap['X']) != 1)
    solver.add(Abs(chap['U'] - chap['X']) == 1)
    
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = tuple(m.eval(chap[c], model_completion=True).as_long() for c in clues)
        solutions.append(sol)
        solver.add(Or([chap[c] != m.eval(chap[c], model_completion=True).as_long() for c in clues]))
    
    return sorted(solutions)

# Get baseline
baseline = get_all_solutions()
print("Baseline solutions (T != 1):")
print("(R,S,T,U,W,X,Z)")
for s in baseline:
    print(s)
print(f"Total: {len(baseline)}")

# Test Option B
sols_b = get_all_solutions(extra_constr_fn=lambda ch: ch['W'] != 4)
print("\n\nOption B solutions (W != 4):")
for s in sols_b:
    print(s)
print(f"Total: {len(sols_b)}")

# Verify exact equality
if set(baseline) == set(sols_b):
    print("\n✅ EXACT MATCH: Option B has the same effect!")
else:
    print("\n❌ NOT an exact match")