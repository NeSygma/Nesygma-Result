from z3 import *

# Colors
F, O, P, T, W, Y = range(6)  # forest, olive, peach, turquoise, white, yellow
NUM_COLORS = 6
NUM_RUGS = 3

solver = Solver()

# in_rug[r][c] = True if color c is used in rug r
in_rug = [[Bool(f"in_rug_{r}_{c}") for c in range(NUM_COLORS)] for r in range(NUM_RUGS)]

# Each color can be in at most one rug
for c in range(NUM_COLORS):
    solver.add(AtMost(*[in_rug[r][c] for r in range(NUM_RUGS)], 1))

# Exactly 5 of the 6 colors are used (i.e., exist in at least one rug)
used = [Or([in_rug[r][c] for r in range(NUM_RUGS)]) for c in range(NUM_COLORS)]
solver.add(PbEq([(used[c], 1) for c in range(NUM_COLORS)], 5))

# Each rug must have at least one color (otherwise it's not a real rug)
for r in range(NUM_RUGS):
    solver.add(Or([in_rug[r][c] for c in range(NUM_COLORS)]))

# Rule 1: If white is in a rug, at least two other colors are also in that rug.
# i.e., total colors in that rug >= 3
for r in range(NUM_RUGS):
    solver.add(Implies(in_rug[r][W],
                       Sum([If(in_rug[r][c], 1, 0) for c in range(NUM_COLORS)]) >= 3))

# Rule 2: If olive is in a rug, peach is also in that rug.
for r in range(NUM_RUGS):
    solver.add(Implies(in_rug[r][O], in_rug[r][P]))

# Rule 3: Forest and turquoise are not used together in a rug.
for r in range(NUM_RUGS):
    solver.add(Not(And(in_rug[r][F], in_rug[r][T])))

# Rule 4: Peach and turquoise are not used together in a rug.
for r in range(NUM_RUGS):
    solver.add(Not(And(in_rug[r][P], in_rug[r][T])))

# Rule 5: Peach and yellow are not used together in a rug.
for r in range(NUM_RUGS):
    solver.add(Not(And(in_rug[r][P], in_rug[r][Y])))

# Now define each option's statement

# (A) There are no multicolored rugs in which forest is used.
# If forest is in a rug, that rug has exactly 1 color.
opt_a = And([Implies(in_rug[r][F], Sum([If(in_rug[r][c], 1, 0) for c in range(NUM_COLORS)]) == 1)
             for r in range(NUM_RUGS)])

# (B) There are no multicolored rugs in which turquoise is used.
opt_b = And([Implies(in_rug[r][T], Sum([If(in_rug[r][c], 1, 0) for c in range(NUM_COLORS)]) == 1)
             for r in range(NUM_RUGS)])

# (C) Peach is used in one of the rugs.
opt_c = Or([in_rug[r][P] for r in range(NUM_RUGS)])

# (D) Turquoise is used in one of the rugs.
opt_d = Or([in_rug[r][T] for r in range(NUM_RUGS)])

# (E) Yellow is used in one of the rugs.
opt_e = Or([in_rug[r][Y] for r in range(NUM_RUGS)])

# For "must be true": check if NOT(option) is unsatisfiable.
found_options = []
for letter, constr in [("A", Not(opt_a)), ("B", Not(opt_b)), ("C", Not(opt_c)),
                       ("D", Not(opt_d)), ("E", Not(opt_e))]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:  # negation unsat -> option must be true
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