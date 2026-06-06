from z3 import *

# Houses: J, K, L, M, N, O, P
# Positions 1-7 (1,2=morning; 3,4,5=afternoon; 6,7=evening)

houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# Base constraints (shared across all option checks)
def add_base_constraints(solver):
    for h in houses:
        solver.add(pos[h] >= 1, pos[h] <= 7)
    solver.add(Distinct([pos[h] for h in houses]))
    # J must be shown in the evening (position 6 or 7)
    solver.add(Or(pos['J'] == 6, pos['J'] == 7))
    # K cannot be shown in the morning (not position 1 or 2)
    solver.add(pos['K'] >= 3)
    # L must be shown after K and before M: K < L < M
    solver.add(pos['K'] < pos['L'])
    solver.add(pos['L'] < pos['M'])

# The question asks which pair CANNOT be shown consecutively.
# For each option, check if the pair CAN be shown consecutively.
# The correct answer is the one that CANNOT (returns UNSAT).

options = {
    "A": ('J', 'K'),
    "B": ('J', 'M'),
    "C": ('J', 'O'),
    "D": ('J', 'P'),
    "E": ('M', 'P'),
}

cannot_be_consecutive = []

for letter, (h1, h2) in options.items():
    s = Solver()
    add_base_constraints(s)
    # Constraint: h1 and h2 are consecutive (in either order)
    s.add(Or(pos[h1] - pos[h2] == 1, pos[h2] - pos[h1] == 1))
    result = s.check()
    if result == unsat:
        cannot_be_consecutive.append(letter)
        print(f"Option {letter} ({h1},{h2}): CANNOT be consecutive")
    elif result == sat:
        m = s.model()
        arrangement = sorted([(m.eval(pos[h]).as_long(), h) for h in houses])
        print(f"Option {letter} ({h1},{h2}): CAN be consecutive. Example: {arrangement}")
    else:
        print(f"Option {letter} ({h1},{h2}): unknown")

print()
if len(cannot_be_consecutive) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be_consecutive[0]}")
elif len(cannot_be_consecutive) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be consecutive {cannot_be_consecutive}")
else:
    print("STATUS: unsat")
    print("Refine: No options found that cannot be consecutive")