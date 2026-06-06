from z3 import *

# Six colors: forest, olive, peach, turquoise, white, yellow
# Exactly five of the six colors are used.
# Each used color is used in only one rug.
# Three rugs: rug0, rug1, rug2
# Each rug is either solid (one color) or multicolored (multiple colors).
# Rules:
# 1. In any rug in which white is used, two other colors are also used. So white rug has exactly 3 colors total.
# 2. In any rug in which olive is used, peach is also used.
# 3. Forest and turquoise are not used together in a rug.
# 4. Peach and turquoise are not used together in a rug.
# 5. Peach and yellow are not used together in a rug.

# We need to determine which of A-E must be true.

# Let's model: each color is either used or not (exactly 5 used).
# For each used color, assign it to one of the 3 rugs (0,1,2).
# Each rug has a set of colors assigned to it.

colors = ['forest', 'olive', 'peach', 'turquoise', 'white', 'yellow']
color_idx = {c: i for i, c in enumerate(colors)}
N = 6

# Boolean: is color i used?
used = [Bool(f'used_{colors[i]}') for i in range(N)]

# Integer: which rug (0,1,2) is color i assigned to? Only meaningful if used.
# We'll use Int variables, domain 0..2
rug_of = [Int(f'rug_of_{colors[i]}') for i in range(N)]

solver = Solver()

# Exactly 5 colors are used
solver.add(Sum([If(used[i], 1, 0) for i in range(N)]) == 5)

# If a color is used, its rug assignment is 0,1,2; if not used, rug assignment is irrelevant but we can set to -1 or something.
# Let's constrain: if used, rug_of in {0,1,2}; if not used, rug_of = -1 (sentinel)
for i in range(N):
    solver.add(Implies(used[i], And(rug_of[i] >= 0, rug_of[i] <= 2)))
    solver.add(Implies(Not(used[i]), rug_of[i] == -1))

# Each used color is used in only one rug (already enforced by rug_of being a single value per color)

# Now encode the rules about rugs.

# For each rug r (0,1,2), we need to know which colors are in it.
# We'll define: in_rug[r][i] = True if color i is in rug r
in_rug = [[Bool(f'in_rug_{r}_{colors[i]}') for i in range(N)] for r in range(3)]

# Link in_rug to used and rug_of
for r in range(3):
    for i in range(N):
        # color i is in rug r iff used[i] and rug_of[i] == r
        solver.add(in_rug[r][i] == And(used[i], rug_of[i] == r))

# Rule 1: In any rug in which white is used, two other colors are also used.
# So if white is in rug r, then exactly 3 colors total in that rug (white + 2 others).
white_idx = color_idx['white']
for r in range(3):
    # count colors in rug r
    count_in_rug = Sum([If(in_rug[r][i], 1, 0) for i in range(N)])
    solver.add(Implies(in_rug[r][white_idx], count_in_rug == 3))

# Rule 2: In any rug in which olive is used, peach is also used.
olive_idx = color_idx['olive']
peach_idx = color_idx['peach']
for r in range(3):
    solver.add(Implies(in_rug[r][olive_idx], in_rug[r][peach_idx]))

# Rule 3: Forest and turquoise are not used together in a rug.
forest_idx = color_idx['forest']
turquoise_idx = color_idx['turquoise']
for r in range(3):
    solver.add(Not(And(in_rug[r][forest_idx], in_rug[r][turquoise_idx])))

# Rule 4: Peach and turquoise are not used together in a rug.
for r in range(3):
    solver.add(Not(And(in_rug[r][peach_idx], in_rug[r][turquoise_idx])))

# Rule 5: Peach and yellow are not used together in a rug.
yellow_idx = color_idx['yellow']
for r in range(3):
    solver.add(Not(And(in_rug[r][peach_idx], in_rug[r][yellow_idx])))

# Now evaluate each option.

# Option A: "There are no multicolored rugs in which forest is used."
# Means: For every rug r, if forest is in rug r, then that rug is solid (only 1 color).
# i.e., if forest is in rug r, then count_in_rug[r] == 1.
opt_a_constr = True
for r in range(3):
    opt_a_constr = And(opt_a_constr, Implies(in_rug[r][forest_idx], Sum([If(in_rug[r][i], 1, 0) for i in range(N)]) == 1))

# Option B: "There are no multicolored rugs in which turquoise is used."
# Means: For every rug r, if turquoise is in rug r, then that rug is solid.
opt_b_constr = True
for r in range(3):
    opt_b_constr = And(opt_b_constr, Implies(in_rug[r][turquoise_idx], Sum([If(in_rug[r][i], 1, 0) for i in range(N)]) == 1))

# Option C: "Peach is used in one of the rugs."
opt_c_constr = used[peach_idx]

# Option D: "Turquoise is used in one of the rugs."
opt_d_constr = used[turquoise_idx]

# Option E: "Yellow is used in one of the rugs."
opt_e_constr = used[yellow_idx]

# Now test each option: is it necessarily true? We need to check if the negation is possible.
# For "must be true", we check if there exists a model where the option is FALSE.
# If no model exists where option is false, then it must be true.

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        # The negation is unsatisfiable, so the option must be true
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