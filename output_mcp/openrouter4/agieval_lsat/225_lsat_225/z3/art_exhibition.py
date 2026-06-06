from z3 import *

solver = Solver()

# Constants
F, G, H, I = 0, 1, 2, 3
OIL, WATER = 0, 1
UPPER, LOWER = 0, 1
walls_count = 4

# student[wall][pos] = which student's painting is at this wall and position
# medium[wall][pos] = which type (oil or watercolor)
student = [[Int(f'student_{w}_{p}') for p in [UPPER, LOWER]] for w in range(walls_count)]
medium = [[Int(f'medium_{w}_{p}') for p in [UPPER, LOWER]] for w in range(walls_count)]

# Domain constraints
for w in range(walls_count):
    for p in [UPPER, LOWER]:
        solver.add(student[w][p] >= F, student[w][p] <= I)
        solver.add(medium[w][p] >= OIL, medium[w][p] <= WATER)

# Each student has exactly one oil and one watercolor
for s in [F, G, H, I]:
    oil_count = Sum([If(And(student[w][p] == s, medium[w][p] == OIL), 1, 0) for w in range(walls_count) for p in [UPPER, LOWER]])
    solver.add(oil_count == 1)
    
    water_count = Sum([If(And(student[w][p] == s, medium[w][p] == WATER), 1, 0) for w in range(walls_count) for p in [UPPER, LOWER]])
    solver.add(water_count == 1)

# Constraint 1: No wall has only watercolors (each wall has at least one oil)
for w in range(walls_count):
    solver.add(Or(medium[w][UPPER] == OIL, medium[w][LOWER] == OIL))

# Constraint 2: No wall has the work of only one student (two different students per wall)
for w in range(walls_count):
    solver.add(student[w][UPPER] != student[w][LOWER])

# Constraint 3: No wall has both Franz and Isaacs
for w in range(walls_count):
    solver.add(Not(Or(
        And(student[w][UPPER] == F, student[w][LOWER] == I),
        And(student[w][UPPER] == I, student[w][LOWER] == F)
    )))

# Constraint 4: Greene's watercolor is in the upper position of the wall on which Franz's oil is displayed.
wall_for_franz_oil = Or([
    And(student[w][UPPER] == G, medium[w][UPPER] == WATER, 
        student[w][LOWER] == F, medium[w][LOWER] == OIL)
    for w in range(walls_count)
])
solver.add(wall_for_franz_oil)

# Constraint 5: Isaacs's oil is displayed in the lower position of wall 4.
solver.add(student[3][LOWER] == I)
solver.add(medium[3][LOWER] == OIL)

# Check base consistency
print("Base constraints check:", solver.check())
if solver.check() == sat:
    m = solver.model()
    print("Base model:")
    for w in range(walls_count):
        for p in [UPPER, LOWER]:
            s_val = m.eval(student[w][p]).as_long()
            t_val = m.eval(medium[w][p]).as_long()
            s_name = ["F","G","H","I"][s_val]
            t_name = ["OIL","WATER"][t_val]
            p_name = ["UPPER","LOWER"][p]
            print(f"  Wall {w+1} {p_name}: {s_name} - {t_name}")

# Now evaluate each option: which one CANNOT be true (is UNSAT)?

# Option A: Franz's watercolor on the same wall as Greene's oil.
opt_a = Or([
    Or(And(student[w][UPPER] == F, medium[w][UPPER] == WATER, student[w][LOWER] == G, medium[w][LOWER] == OIL),
       And(student[w][UPPER] == G, medium[w][UPPER] == OIL, student[w][LOWER] == F, medium[w][LOWER] == WATER))
    for w in range(walls_count)
])

# Option B: Franz's watercolor on the same wall as Hidalgo's oil.
opt_b = Or([
    Or(And(student[w][UPPER] == F, medium[w][UPPER] == WATER, student[w][LOWER] == H, medium[w][LOWER] == OIL),
       And(student[w][UPPER] == H, medium[w][UPPER] == OIL, student[w][LOWER] == F, medium[w][LOWER] == WATER))
    for w in range(walls_count)
])

# Option C: Greene's oil is displayed in an upper position.
opt_c = Or([And(student[w][UPPER] == G, medium[w][UPPER] == OIL) for w in range(walls_count)])

# Option D: Hidalgo's watercolor is displayed in a lower position.
opt_d = Or([And(student[w][LOWER] == H, medium[w][LOWER] == WATER) for w in range(walls_count)])

# Option E: Isaacs's watercolor on the same wall as Hidalgo's oil.
opt_e = Or([
    Or(And(student[w][UPPER] == I, medium[w][UPPER] == WATER, student[w][LOWER] == H, medium[w][LOWER] == OIL),
       And(student[w][UPPER] == H, medium[w][UPPER] == OIL, student[w][LOWER] == I, medium[w][LOWER] == WATER))
    for w in range(walls_count)
])

# Find which options are IMPOSSIBLE (unsat)
impossible_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    res = solver.check()
    print(f"Option {letter}: {res}")
    if res == unsat:
        impossible_options.append(letter)
    solver.pop()

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found - all options are possible")