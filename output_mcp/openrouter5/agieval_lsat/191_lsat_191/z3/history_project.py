from z3 import *

solver = Solver()

# Students: Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio
# Years: 1921, 1922, 1923, 1924
# Exactly 4 students are assigned (one per year), 2 are not assigned.
# We'll model assignment as: for each student, which year they are assigned (0 = not assigned, 1..4 for 1921..1924)
# Or we can model: for each year, which student is assigned.

# Let's use: for each year, an integer representing the student assigned.
# Map: 0=Louis, 1=Mollie, 2=Onyx, 3=Ryan, 4=Tiffany, 5=Yoshio
# Years: 1921=0, 1922=1, 1923=2, 1924=3

year = [Int(f'year_{i}') for i in range(4)]  # year[0]=1921, year[1]=1922, year[2]=1923, year[3]=1924

# Each year gets a student from 0..5
for i in range(4):
    solver.add(year[i] >= 0, year[i] <= 5)

# All assigned students must be distinct (each student at most one year)
solver.add(Distinct(year))

# Exactly 4 students assigned, 2 not assigned. Since we have 4 years and 6 students,
# Distinct ensures 4 distinct students are assigned, and 2 are not assigned. That's fine.

# Condition 1: Only Louis (0) or Tiffany (4) can be assigned to 1923 (year[2]).
solver.add(Or(year[2] == 0, year[2] == 4))

# Condition 2: If Mollie (1) is assigned to the project, then she must be assigned to either 1921 or 1922.
# Mollie is assigned iff she appears in one of the years.
mollie_assigned = Or([year[i] == 1 for i in range(4)])
solver.add(Implies(mollie_assigned, Or(year[0] == 1, year[1] == 1)))

# Condition 3: If Tiffany (4) is assigned to the project, then Ryan (3) must be assigned.
tiffany_assigned = Or([year[i] == 4 for i in range(4)])
ryan_assigned = Or([year[i] == 3 for i in range(4)])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Condition 4: If Ryan (3) is assigned to the project, then Onyx (2) must be assigned to the year immediately prior to Ryan's.
# "immediately prior" means if Ryan is in year[i], Onyx must be in year[i-1].
for i in range(4):
    solver.add(Implies(year[i] == 3, 
                       And(i > 0, year[i-1] == 2)))

# Now we need to find which option, when added, forces Mollie to be assigned to 1922.
# The question: "Mollie must be assigned to 1922 if which one of the following is true?"
# This means: under the given conditions, if we add the option as a constraint,
# does it force Mollie to be in 1922? We need to check: does the option + base constraints
# entail that Mollie is in 1922?

# For each option, we check: with the option added, is Mollie necessarily in 1922?
# We can check this by: add option, then check if Mollie NOT in 1922 is unsatisfiable.
# If so, then Mollie MUST be in 1922.

# Option A: Louis is assigned to 1924. (year[3] == 0)
# Option B: Onyx is assigned to 1921. (year[0] == 2)
# Option C: Onyx is assigned to 1924. (year[3] == 2)
# Option D: Tiffany is assigned to 1923. (year[2] == 4)
# Option E: Yoshio is assigned to 1921. (year[0] == 5)

options = {
    "A": year[3] == 0,
    "B": year[0] == 2,
    "C": year[3] == 2,
    "D": year[2] == 4,
    "E": year[0] == 5
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    # Now check if Mollie must be in 1922: try to find a model where Mollie is NOT in 1922
    # If unsat, then Mollie must be in 1922.
    solver.push()
    solver.add(Not(year[1] == 1))  # Mollie not in 1922
    result = solver.check()
    if result == unsat:
        # Mollie must be in 1922 under this option
        found_options.append(letter)
    solver.pop()
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