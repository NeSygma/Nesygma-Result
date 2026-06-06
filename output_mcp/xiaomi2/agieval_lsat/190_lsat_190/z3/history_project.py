from z3 import *

solver = Solver()

# Students: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Years: 1921=0, 1922=1, 1923=2, 1924=3
# year[i] = student assigned to year i
year = [Int(f'year_{y}') for y in range(4)]

# Each year gets exactly one student from {0..5}
for y in range(4):
    solver.add(year[y] >= 0, year[y] <= 5)

# All four assigned students must be distinct
solver.add(Distinct(year))

# Constants
Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio = 0, 1, 2, 3, 4, 5

# Condition 1: Only Louis or Tiffany can be assigned to 1923 (index 2)
solver.add(Or(year[2] == Louis, year[2] == Tiffany))

# Condition 2: If Mollie is assigned, she must be in 1921 or 1922
for y in range(4):
    solver.add(Implies(year[y] == Mollie, Or(y == 0, y == 1)))

# Condition 3: If Tiffany is assigned, then Ryan must be assigned
tiffany_assigned = Or([year[y] == Tiffany for y in range(4)])
ryan_assigned = Or([year[y] == Ryan for y in range(4)])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Condition 4: If Ryan is assigned, then Onyx must be in the year immediately prior
# Ryan at year y => Onyx at year y-1 (for y in 1..3)
for y in range(1, 4):
    solver.add(Implies(year[y] == Ryan, year[y-1] == Onyx))
# Ryan cannot be at year 0 (no prior year for Onyx)
solver.add(year[0] != Ryan)

# Now evaluate each option
# Option A: 1921=Louis, 1922=Onyx, 1923=Ryan, 1924=Yoshio
opt_a = And(year[0] == Louis, year[1] == Onyx, year[2] == Ryan, year[3] == Yoshio)
# Option B: 1921=Mollie, 1922=Yoshio, 1923=Tiffany, 1924=Onyx
opt_b = And(year[0] == Mollie, year[1] == Yoshio, year[2] == Tiffany, year[3] == Onyx)
# Option C: 1921=Onyx, 1922=Ryan, 1923=Louis, 1924=Tiffany
opt_c = And(year[0] == Onyx, year[1] == Ryan, year[2] == Louis, year[3] == Tiffany)
# Option D: 1921=Tiffany, 1922=Onyx, 1923=Louis, 1924=Ryan
opt_d = And(year[0] == Tiffany, year[1] == Onyx, year[2] == Louis, year[3] == Ryan)
# Option E: 1921=Yoshio, 1922=Onyx, 1923=Louis, 1924=Mollie
opt_e = And(year[0] == Yoshio, year[1] == Onyx, year[2] == Louis, year[3] == Mollie)

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