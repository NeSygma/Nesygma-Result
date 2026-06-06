from z3 import *

solver = Solver()

# Students: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Years: 1921=0, 1922=1, 1923=2, 1924=3
# We need to assign 4 out of 6 students to the 4 years.

students = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']
years = [1921, 1922, 1923, 1924]

# year[i] = which student is assigned to year i (0-5), or -1 if none
# But each year has exactly one student, so we use 4 variables
y0 = Int('y0')  # student assigned to 1921
y1 = Int('y1')  # student assigned to 1922
y2 = Int('y2')  # student assigned to 1923
y3 = Int('y3')  # student assigned to 1924

assignment = [y0, y1, y2, y3]

# Each assignment is a valid student (0-5)
for y in assignment:
    solver.add(y >= 0, y <= 5)

# All four assigned students must be distinct
solver.add(Distinct(assignment))

# Condition 1: Only Louis (0) or Tiffany (4) can be assigned to 1923
solver.add(Or(y2 == 0, y2 == 4))

# Condition 2: If Mollie (1) is assigned, she must be assigned to 1921 or 1922
# Mollie is assigned iff y0==1 or y1==1 or y2==1 or y3==1
mollie_assigned = Or(y0 == 1, y1 == 1, y2 == 1, y3 == 1)
solver.add(Implies(mollie_assigned, Or(y0 == 1, y1 == 1)))

# Condition 3: If Tiffany (4) is assigned, then Ryan (3) must be assigned
tiffany_assigned = Or(y0 == 4, y1 == 4, y2 == 4, y3 == 4)
ryan_assigned = Or(y0 == 3, y1 == 3, y2 == 3, y3 == 3)
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Condition 4: If Ryan (3) is assigned, then Onyx (2) must be assigned to the year immediately prior to Ryan's
# "immediately prior" means if Ryan is in year i, Onyx must be in year i-1
# Ryan in 1921 (y0==3): no prior year, so this would be impossible if condition is strict
# Ryan in 1922 (y1==3): Onyx in 1921 (y0==2)
# Ryan in 1923 (y2==3): Onyx in 1922 (y1==2)
# Ryan in 1924 (y3==3): Onyx in 1923 (y2==2)
solver.add(Implies(y1 == 3, y0 == 2))
solver.add(Implies(y2 == 3, y1 == 2))
solver.add(Implies(y3 == 3, y2 == 2))
# If Ryan is in 1921, there's no prior year, so Ryan can't be in 1921
solver.add(y0 != 3)

# Now evaluate each option
# Option A: Louis, Onyx, Ryan, Yoshio -> 1921=Louis(0), 1922=Onyx(2), 1923=Ryan(3), 1924=Yoshio(5)
opt_a = And(y0 == 0, y1 == 2, y2 == 3, y3 == 5)

# Option B: Mollie, Yoshio, Tiffany, Onyx -> 1921=Mollie(1), 1922=Yoshio(5), 1923=Tiffany(4), 1924=Onyx(2)
opt_b = And(y0 == 1, y1 == 5, y2 == 4, y3 == 2)

# Option C: Onyx, Ryan, Louis, Tiffany -> 1921=Onyx(2), 1922=Ryan(3), 1923=Louis(0), 1924=Tiffany(4)
opt_c = And(y0 == 2, y1 == 3, y2 == 0, y3 == 4)

# Option D: Tiffany, Onyx, Louis, Ryan -> 1921=Tiffany(4), 1922=Onyx(2), 1923=Louis(0), 1924=Ryan(3)
opt_d = And(y0 == 4, y1 == 2, y2 == 0, y3 == 3)

# Option E: Yoshio, Onyx, Louis, Mollie -> 1921=Yoshio(5), 1922=Onyx(2), 1923=Louis(0), 1924=Mollie(1)
opt_e = And(y0 == 5, y1 == 2, y2 == 0, y3 == 1)

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