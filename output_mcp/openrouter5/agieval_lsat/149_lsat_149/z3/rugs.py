from z3 import *

# Six colors: forest, olive, peach, turquoise, white, yellow
# Exactly five of the six colors are used.
# Each used color is used in only one rug.
# Three rugs. Each rug is either solid (one color) or multicolored.
# Rules:
# 1. In any rug in which white is used, two other colors are also used. (So white rug has exactly 3 colors total)
# 2. In any rug in which olive is used, peach is also used.
# 3. Forest and turquoise are not used together in a rug.
# 4. Peach and turquoise are not used together in a rug.
# 5. Peach and yellow are not used together in a rug.

colors = ['forest', 'olive', 'peach', 'turquoise', 'white', 'yellow']
c_idx = {c: i for i, c in enumerate(colors)}

solver = Solver()

# Each color gets a rug assignment: 0, 1, 2 for the three rugs, or -1 for unused
assign = [Int(f'assign_{c}') for c in colors]
for a in assign:
    solver.add(Or(a == -1, a == 0, a == 1, a == 2))

# Exactly 5 colors are used (one is -1)
solver.add(Sum([If(a != -1, 1, 0) for a in assign]) == 5)

# --- Rules ---

# Rule 1: In any rug in which white is used, two other colors are also used.
# So if white is used, the rug containing white has exactly 3 colors total.
for r in range(3):
    white_in_r = (assign[c_idx['white']] == r)
    count_in_r = Sum([If(assign[i] == r, 1, 0) for i in range(6)])
    solver.add(Implies(white_in_r, count_in_r == 3))

# Rule 2: In any rug in which olive is used, peach is also used.
for r in range(3):
    olive_in_r = (assign[c_idx['olive']] == r)
    peach_in_r = (assign[c_idx['peach']] == r)
    solver.add(Implies(olive_in_r, peach_in_r))

# Rule 3: Forest and turquoise are not used together in a rug.
for r in range(3):
    forest_in_r = (assign[c_idx['forest']] == r)
    turquoise_in_r = (assign[c_idx['turquoise']] == r)
    solver.add(Not(And(forest_in_r, turquoise_in_r)))

# Rule 4: Peach and turquoise are not used together in a rug.
for r in range(3):
    peach_in_r = (assign[c_idx['peach']] == r)
    turquoise_in_r = (assign[c_idx['turquoise']] == r)
    solver.add(Not(And(peach_in_r, turquoise_in_r)))

# Rule 5: Peach and yellow are not used together in a rug.
for r in range(3):
    peach_in_r = (assign[c_idx['peach']] == r)
    yellow_in_r = (assign[c_idx['yellow']] == r)
    solver.add(Not(And(peach_in_r, yellow_in_r)))

# --- Now evaluate each option ---
# Each option describes the three rugs. We need to check if the option is consistent with the rules.

def parse_rug(rug_desc):
    """Parse a rug description like 'forest only' or 'olive, peach, and white' into a list of colors."""
    # Remove 'only' if present
    desc = rug_desc.replace(' only', '')
    # Replace ' and ' with ', '
    desc = desc.replace(' and ', ', ')
    # Split by comma
    parts = [c.strip() for c in desc.split(',')]
    # Filter empty
    return [p for p in parts if p]

def make_option_constraint(rugs_list):
    """rugs_list is a list of 3 strings, each describing a rug's colors."""
    constrs = []
    for r_idx, rug_desc in enumerate(rugs_list):
        rug_colors = parse_rug(rug_desc)
        # Each listed color must be in this rug
        for col in rug_colors:
            constrs.append(assign[c_idx[col]] == r_idx)
        # Colors not listed must NOT be in this rug
        for col in colors:
            if col not in rug_colors:
                constrs.append(assign[c_idx[col]] != r_idx)
    return And(constrs)

# Option A: forest only; turquoise only; olive, peach, and white
opt_a = make_option_constraint([
    'forest only',
    'turquoise only',
    'olive, peach, and white'
])

# Option B: forest only; turquoise only; olive, peach, and yellow
opt_b = make_option_constraint([
    'forest only',
    'turquoise only',
    'olive, peach, and yellow'
])

# Option C: peach only; turquoise only; forest, olive, and white
opt_c = make_option_constraint([
    'peach only',
    'turquoise only',
    'forest, olive, and white'
])

# Option D: yellow only; forest and turquoise; olive and peach
opt_d = make_option_constraint([
    'yellow only',
    'forest and turquoise',
    'olive and peach'
])

# Option E: yellow only; olive and peach; turquoise and white
opt_e = make_option_constraint([
    'yellow only',
    'olive and peach',
    'turquoise and white'
])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
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