from z3 import *

solver = Solver()

# Seven houses: J, K, L, M, N, O, P
# Position 1-7 (1-indexed)
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

# Each house has a unique position 1-7
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
solver.add(Distinct([pos[h] for h in houses]))

# Time slots:
# Morning: positions 1, 2
# Afternoon: positions 3, 4, 5
# Evening: positions 6, 7

# Rule 1: J must be shown in the evening (position 6 or 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# Rule 2: K cannot be shown in the morning (not position 1 or 2)
solver.add(pos['K'] != 1, pos['K'] != 2)

# Rule 3: L must be shown at some time after K and before M
solver.add(pos['K'] < pos['L'])
solver.add(pos['L'] < pos['M'])

# Now check each option to see which MUST be true
# We check if the negation is unsatisfiable (meaning the option must be true)

# Option A: K is shown in the evening (pos 6 or 7)
opt_a_constr = Or(pos['K'] == 6, pos['K'] == 7)

# Option B: L is shown in the afternoon (pos 3, 4, or 5)
opt_b_constr = Or(pos['L'] == 3, pos['L'] == 4, pos['L'] == 5)

# Option C: L is shown in the evening (pos 6 or 7)
opt_c_constr = Or(pos['L'] == 6, pos['L'] == 7)

# Option D: M is shown in the morning (pos 1 or 2)
opt_d_constr = Or(pos['M'] == 1, pos['M'] == 2)

# Option E: M is shown in the afternoon (pos 3, 4, or 5)
opt_e_constr = Or(pos['M'] == 3, pos['M'] == 4, pos['M'] == 5)

# For "must be true" we check: is the negation unsatisfiable?
# If negation is unsat, the statement must be true.
must_be_true = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    s = Solver()
    s.add(solver.assertions())
    s.add(Not(constr))
    if s.check() == unsat:
        must_be_true.append(letter)

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")