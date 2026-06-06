from z3 import *

solver = Solver()

# Constants for students
F, G, H, I = 0, 1, 2, 3
# Constants for medium
OIL, WC = 0, 1  # watercolor

# For each wall (0..3) and each position (0=upper, 1=lower)
# student[w][p] = which student's painting
# medium[w][p] = type of painting
student = [[Int(f"student_{w}_{p}") for p in range(2)] for w in range(4)]
medium = [[Int(f"medium_{w}_{p}") for p in range(2)] for w in range(4)]

for w in range(4):
    for p in range(2):
        solver.add(student[w][p] >= 0, student[w][p] <= 3)
        solver.add(medium[w][p] >= 0, medium[w][p] <= 1)

# Each student has exactly one oil painting
for s in [F, G, H, I]:
    solver.add(Sum([If(And(student[w][p] == s, medium[w][p] == OIL), 1, 0)
                    for w in range(4) for p in range(2)]) == 1)

# Each student has exactly one watercolor
for s in [F, G, H, I]:
    solver.add(Sum([If(And(student[w][p] == s, medium[w][p] == WC), 1, 0)
                    for w in range(4) for p in range(2)]) == 1)

# 1. No wall has only watercolors (each wall has at least one oil)
for w in range(4):
    solver.add(Not(And(medium[w][0] == WC, medium[w][1] == WC)))

# 2. No wall has the work of only one student (two different students per wall)
for w in range(4):
    solver.add(student[w][0] != student[w][1])

# 3. No wall has both Franz and Isaacs
for w in range(4):
    solver.add(Not(Or(
        And(student[w][0] == F, student[w][1] == I),
        And(student[w][0] == I, student[w][1] == F)
    )))

# 4. Greene's watercolor is upper on the wall where Franz's oil is displayed
# There exists a wall w such that:
# (upper: Greene's watercolor) AND (lower: Franz's oil)
# OR... wait, "Greene's watercolor is displayed in the upper position of the wall on which Franz's oil is displayed"
# This means: there's a wall, and on that wall, upper = Greene's watercolor, and Franz's oil is also on that wall.
# Since Greene's watercolor occupies the upper position, Franz's oil must be lower.
wall_with_franz_oil = Bool('wall_with_franz_oil')
solver.add(Or([
    And(student[w][0] == G, medium[w][0] == WC,
        student[w][1] == F, medium[w][1] == OIL)
    for w in range(4)
]))

# 5. Isaacs's oil is displayed in the lower position of wall 4
solver.add(student[3][1] == I)
solver.add(medium[3][1] == OIL)

# Now evaluate each option
# Each option specifies lower position (p=1) of walls 1 through 4 (w=0,1,2,3)

def make_lower_constraint(opt_list):
    """opt_list is a list of 4 pairs (student, medium) for walls 0,1,2,3 lower position"""
    constr = True
    for w, (s_val, m_val) in enumerate(opt_list):
        constr = And(constr, student[w][1] == s_val, medium[w][1] == m_val)
    return constr

# Option A: Franz's oil, Franz's watercolor, Greene's oil, Isaacs's oil
opt_a = make_lower_constraint([
    (F, OIL), (F, WC), (G, OIL), (I, OIL)
])

# Option B: Franz's oil, Hidalgo's watercolor, Isaacs's watercolor, Isaacs's oil
opt_b = make_lower_constraint([
    (F, OIL), (H, WC), (I, WC), (I, OIL)
])

# Option C: Greene's oil, Franz's oil, Isaacs's oil, Hidalgo's oil
opt_c = make_lower_constraint([
    (G, OIL), (F, OIL), (I, OIL), (H, OIL)
])

# Option D: Hidalgo's oil, Greene's oil, Greene's watercolor, Isaacs's oil
opt_d = make_lower_constraint([
    (H, OIL), (G, OIL), (G, WC), (I, OIL)
])

# Option E: Hidalgo's watercolor, Franz's oil, Greene's oil, Isaacs's oil
opt_e = make_lower_constraint([
    (H, WC), (F, OIL), (G, OIL), (I, OIL)
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