from z3 import *

# Colors: 0=forest, 1=olive, 2=peach, 3=turquoise, 4=white, 5=yellow
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]

# Variables: which rug each color belongs to (0=unused, 1,2,3=rug numbers)
rug_of_color = [Int(f"rug_{c}") for c in range(6)]

solver = Solver()

# Constraint 1: Exactly 5 colors are used (one rug_of_color is 0)
solver.add(Sum([If(rug_of_color[c] == 0, 1, 0) for c in range(6)]) == 1)

# Constraint 2: Each used color belongs to exactly one rug (1,2,3)
for c in range(6):
    solver.add(Or(rug_of_color[c] == 0, 
                  rug_of_color[c] == 1, 
                  rug_of_color[c] == 2, 
                  rug_of_color[c] == 3))

# Constraint 3: For each rug, count how many colors it has
rug_size = [Int(f"size_{r}") for r in range(1, 4)]
for r in range(1, 4):
    solver.add(rug_size[r-1] == Sum([If(rug_of_color[c] == r, 1, 0) for c in range(6)]))

# Constraint 4: If white (color 4) is used in a rug, that rug must have exactly 3 colors
# Use Or-loop pattern to avoid indexing with Z3 variable
white_rug_constraints = []
for r in range(1, 4):
    white_rug_constraints.append(And(rug_of_color[4] == r, rug_size[r-1] == 3))
solver.add(Implies(rug_of_color[4] != 0, Or(white_rug_constraints)))

# Constraint 5: If olive (color 1) is used, peach (color 2) must be in same rug
solver.add(Implies(rug_of_color[1] != 0, rug_of_color[1] == rug_of_color[2]))

# Constraint 6: Forest (0) and turquoise (3) not together
solver.add(Implies(And(rug_of_color[0] != 0, rug_of_color[3] != 0),
                   rug_of_color[0] != rug_of_color[3]))

# Constraint 7: Peach (2) and turquoise (3) not together
solver.add(Implies(And(rug_of_color[2] != 0, rug_of_color[3] != 0),
                   rug_of_color[2] != rug_of_color[3]))

# Constraint 8: Peach (2) and yellow (5) not together
solver.add(Implies(And(rug_of_color[2] != 0, rug_of_color[5] != 0),
                   rug_of_color[2] != rug_of_color[5]))

# Now test each option
found_options = []

# Option A: "There are no multicolored rugs in which forest is used"
# This means: If forest is used, it's in a solid rug (size 1)
# We need to express: rug_of_color[0] != 0 => rug_size[rug_of_color[0]-1] == 1
# Use Or-loop pattern
opt_a = Or([And(rug_of_color[0] == r, rug_size[r-1] == 1) for r in range(1, 4)])

# Option B: "There are no multicolored rugs in which turquoise is used"
# This means: If turquoise is used, it's in a solid rug (size 1)
opt_b = Or([And(rug_of_color[3] == r, rug_size[r-1] == 1) for r in range(1, 4)])

# Option C: "Peach is used in one of the rugs"
opt_c = rug_of_color[2] != 0

# Option D: "Turquoise is used in one of the rugs"
opt_d = rug_of_color[3] != 0

# Option E: "Yellow is used in one of the rugs"
opt_e = rug_of_color[5] != 0

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