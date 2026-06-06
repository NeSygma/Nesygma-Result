from z3 import *

# Create solver
solver = Solver()

# Define positions for each composition
compositions = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']
pos = {c: Int(f'pos_{c}') for c in compositions}

# Domain constraints: each position is between 1 and 8
for c in compositions:
    solver.add(pos[c] >= 1, pos[c] <= 8)

# All positions must be distinct (exactly one composition per position)
solver.add(Distinct([pos[c] for c in compositions]))

# Additional constraints from the problem
# 1. T is performed either immediately before F or immediately after R
solver.add(Or(pos['T'] + 1 == pos['F'], pos['R'] + 1 == pos['T']))

# 2. At least two compositions between F and R
solver.add(Abs(pos['F'] - pos['R']) >= 3)

# 3. O is first or fifth
solver.add(Or(pos['O'] == 1, pos['O'] == 5))

# 4. Eighth composition is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))

# 5. P before S
solver.add(pos['P'] < pos['S'])

# 6. At least one composition between O and S
solver.add(Abs(pos['O'] - pos['S']) >= 2)

# Question-specific constraints
solver.add(pos['T'] == 5)  # T is fifth
solver.add(pos['F'] == 6)  # F is sixth

# Find all possible positions for S
possible_S_positions = set()
while solver.check() == sat:
    model = solver.model()
    s_pos = model[pos['S']].as_long()
    possible_S_positions.add(s_pos)
    # Block this specific S position to find next solution
    solver.add(pos['S'] != s_pos)

print(f"Possible positions for S: {sorted(possible_S_positions)}")

# Now check which answer choice matches exactly these positions
opt_a = {4, 7}
opt_b = {3, 6}
opt_c = {3, 4}
opt_d = {2, 7}
opt_e = {1, 4}

found_options = []
if possible_S_positions == opt_a:
    found_options.append("A")
if possible_S_positions == opt_b:
    found_options.append("B")
if possible_S_positions == opt_c:
    found_options.append("C")
if possible_S_positions == opt_d:
    found_options.append("D")
if possible_S_positions == opt_e:
    found_options.append("E")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")