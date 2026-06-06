from z3 import *

# Create a solver
solver = Solver()

# Define the compositions
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
positions = [Int(f'pos_{c}') for c in compositions]

# All positions are distinct and between 1 and 8
solver.add(Distinct(positions))
for p in positions:
    solver.add(p >= 1, p <= 8)

# Constraint: S is performed fourth
solver.add(positions[compositions.index('S')] == 4)

# Constraint: O is performed either first or fifth
o_pos = positions[compositions.index('O')]
solver.add(Or(o_pos == 1, o_pos == 5))

# Constraint: The eighth composition performed is either L or H
eighth_pos_L = positions[compositions.index('L')]
eighth_pos_H = positions[compositions.index('H')]
solver.add(Or(eighth_pos_L == 8, eighth_pos_H == 8))

# Constraint: P is performed at some time before S
p_pos = positions[compositions.index('P')]
s_pos = positions[compositions.index('S')]
solver.add(p_pos < s_pos)

# Constraint: At least one composition is performed either after O and before S, or after S and before O
# This means O and S cannot be adjacent
solver.add(Or(
    And(o_pos < s_pos, s_pos - o_pos >= 2),
    And(s_pos < o_pos, o_pos - s_pos >= 2)
))

# Constraint: T is performed either immediately before F or immediately after R
t_pos = positions[compositions.index('T')]
f_pos = positions[compositions.index('F')]
r_pos = positions[compositions.index('R')]

# T immediately before F: t_pos + 1 == f_pos
# T immediately after R: r_pos + 1 == t_pos
solver.add(Or(
    t_pos + 1 == f_pos,
    r_pos + 1 == t_pos
))

# Constraint: At least two compositions are performed either after F and before R, or after R and before F
# This means |f_pos - r_pos| >= 3
solver.add(Or(
    And(f_pos < r_pos, r_pos - f_pos >= 3),
    And(r_pos < f_pos, f_pos - r_pos >= 3)
))

# Now, evaluate each choice
found_options = []

# Choice A: F, H, P in positions 1, 2, 3
solver.push()
f_pos_A = positions[compositions.index('F')]
h_pos_A = positions[compositions.index('H')]
p_pos_A = positions[compositions.index('P')]
solver.add(f_pos_A == 1, h_pos_A == 2, p_pos_A == 3)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Choice B: H, P, L in positions 1, 2, 3
solver.push()
h_pos_B = positions[compositions.index('H')]
p_pos_B = positions[compositions.index('P')]
l_pos_B = positions[compositions.index('L')]
solver.add(h_pos_B == 1, p_pos_B == 2, l_pos_B == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Choice C: O, P, R in positions 1, 2, 3
solver.push()
o_pos_C = positions[compositions.index('O')]
p_pos_C = positions[compositions.index('P')]
r_pos_C = positions[compositions.index('R')]
solver.add(o_pos_C == 1, p_pos_C == 2, r_pos_C == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Choice D: O, P, T in positions 1, 2, 3
solver.push()
o_pos_D = positions[compositions.index('O')]
p_pos_D = positions[compositions.index('P')]
t_pos_D = positions[compositions.index('T')]
solver.add(o_pos_D == 1, p_pos_D == 2, t_pos_D == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Choice E: P, R, T in positions 1, 2, 3
solver.push()
p_pos_E = positions[compositions.index('P')]
r_pos_E = positions[compositions.index('R')]
t_pos_E = positions[compositions.index('T')]
solver.add(p_pos_E == 1, r_pos_E == 2, t_pos_E == 3)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")