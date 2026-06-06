from z3 import *

# Houses: J, K, L, M, N, O, P
# Positions 1-7 (1,2=morning; 3,4,5=afternoon; 6,7=evening)

houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# Base constraints (shared across all option checks)
def add_base_constraints(solver):
    # Each house has a position from 1 to 7
    for h in houses:
        solver.add(pos[h] >= 1, pos[h] <= 7)
    # All positions are distinct
    solver.add(Distinct([pos[h] for h in houses]))
    # J must be shown in the evening (position 6 or 7)
    solver.add(Or(pos['J'] == 6, pos['J'] == 7))
    # K cannot be shown in the morning (not position 1 or 2)
    solver.add(pos['K'] >= 3)
    # L must be shown after K and before M: K < L < M
    solver.add(pos['K'] < pos['L'])
    solver.add(pos['L'] < pos['M'])

# For each option, check if the pair CAN be shown consecutively
# The correct answer is the pair that CANNOT be consecutive (returns UNSAT)

options = {
    "A": ('J', 'K'),
    "B": ('J', 'M'),
    "C": ('J', 'O'),
    "D": ('J', 'P'),
    "E": ('M', 'P'),
}

found_options = []

for letter, (h1, h2) in options.items():
    s = Solver()
    add_base_constraints(s)
    # Constraint: h1 and h2 are consecutive (in either order)
    s.add(Or(pos[h1] - pos[h2] == 1, pos[h2] - pos[h1] == 1))
    result = s.check()
    if result == sat:
        found_options.append(letter)
        m = s.model()
        arrangement = sorted([(m[pos[h]], h) for h in houses])
        print(f"Option {letter} ({h1},{h2}): CAN be consecutive. Example: {[(p, h) for p, h in arrangement]}")
    else:
        print(f"Option {letter} ({h1},{h2}): CANNOT be consecutive (result={result})")

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")