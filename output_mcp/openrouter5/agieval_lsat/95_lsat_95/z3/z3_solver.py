from z3 import *

solver = Solver()

# Houses: J, K, L, M, N, O, P
# Positions: 1-7 (1=morning1, 2=morning2, 3=afternoon1, 4=afternoon2, 5=afternoon3, 6=evening1, 7=evening2)
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# Domain: each position is 1..7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)

# All positions distinct
solver.add(Distinct([pos[h] for h in houses]))

# Rule 1: J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Rule 2: K cannot be shown in the morning (positions 1 or 2)
solver.add(Not(Or(pos['K'] == 1, pos['K'] == 2)))

# Rule 3: L must be shown at some time after K and before M
solver.add(pos['L'] > pos['K'])
solver.add(pos['L'] < pos['M'])

# The question asks "which one MUST be true" - meaning we need to find which option
# is entailed by the premises. An option MUST be true if it holds in ALL valid models.
# So we need to check if the negation of each option is UNSAT (i.e., no counterexample exists).

# For each option, check if NOT(option) is unsat with the premises.
# If so, the option MUST be true.

found_options = []
for letter, constr in [("A", Or(pos['K'] == 6, pos['K'] == 7)),
                        ("B", Or(pos['L'] == 3, pos['L'] == 4, pos['L'] == 5)),
                        ("C", Or(pos['L'] == 6, pos['L'] == 7)),
                        ("D", Or(pos['M'] == 1, pos['M'] == 2)),
                        ("E", Or(pos['M'] == 3, pos['M'] == 4, pos['M'] == 5))]:
    solver.push()
    solver.add(Not(constr))  # Try to find a counterexample where the option is false
    if solver.check() == unsat:
        # No counterexample exists -> option MUST be true
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