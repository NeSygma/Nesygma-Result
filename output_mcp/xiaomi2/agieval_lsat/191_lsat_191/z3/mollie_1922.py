from z3 import *

solver = Solver()

# Students: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Years: year[0]=1921, year[1]=1922, year[2]=1923, year[3]=1924

year = [Int(f'year_{y}') for y in range(4)]

# Each year has a student from {0,1,2,3,4,5}
for i in range(4):
    solver.add(year[i] >= 0, year[i] <= 5)

# All four years have different students
solver.add(Distinct(year))

# Condition 1: Only Louis or Tiffany can be assigned to 1923
solver.add(Or(year[2] == 0, year[2] == 4))

# Condition 2: If Mollie is assigned, she must be at 1921 or 1922
mollie_assigned = Or(year[0] == 1, year[1] == 1, year[2] == 1, year[3] == 1)
solver.add(Implies(mollie_assigned, Or(year[0] == 1, year[1] == 1)))

# Condition 3: If Tiffany is assigned, Ryan must be assigned
tiffany_assigned = Or(year[0] == 4, year[1] == 4, year[2] == 4, year[3] == 4)
ryan_assigned = Or(year[0] == 3, year[1] == 3, year[2] == 3, year[3] == 3)
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Condition 4: If Ryan is assigned, Onyx must be at the year immediately prior
# Ryan can't be at 1921 (no prior year)
solver.add(year[0] != 3)
solver.add(Implies(year[1] == 3, year[0] == 2))  # Ryan at 1922 -> Onyx at 1921
solver.add(Implies(year[2] == 3, year[1] == 2))  # Ryan at 1923 -> Onyx at 1922
solver.add(Implies(year[3] == 3, year[2] == 2))  # Ryan at 1924 -> Onyx at 1923

# First verify base constraints are satisfiable
base_check = solver.check()
print(f"Base constraints satisfiable: {base_check}")
if base_check == sat:
    print(f"Sample model: {[solver.model()[year[i]] for i in range(4)]}")

# Define options
options = [
    ("A", year[3] == 0),  # Louis at 1924
    ("B", year[0] == 2),  # Onyx at 1921
    ("C", year[3] == 2),  # Onyx at 1924
    ("D", year[2] == 4),  # Tiffany at 1923
    ("E", year[0] == 5),  # Yoshio at 1921
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    # Check if Mollie MUST be at 1922: try to find a model where year[1] != 1
    solver.add(year[1] != 1)
    result = solver.check()
    if result == unsat:
        # Mollie must be at 1922 under this option
        found_options.append(letter)
        print(f"Option {letter}: Mollie MUST be at 1922 (year[1]!=1 is UNSAT)")
    else:
        print(f"Option {letter}: Mollie NOT forced to 1922 (year[1]!=1 is {result})")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")