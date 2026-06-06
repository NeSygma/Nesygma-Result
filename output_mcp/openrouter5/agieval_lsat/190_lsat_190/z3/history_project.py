from z3 import *

# We have 4 positions (years): 1921, 1922, 1923, 1924
# We have 6 students: Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio
# Each year gets exactly one student assigned.
# Not all students must be assigned; exactly 4 are assigned.

# Let's model: assign[i] = student assigned to year i (0=1921, 1=1922, 2=1923, 3=1924)
# We'll use integers 0..5 for students: 0=Louis, 1=Mollie, 2=Onyx, 3=Ryan, 4=Tiffany, 5=Yoshio

solver = Solver()

# Decision variables: assign[0..3] are the students for years 1921..1924
assign = [Int(f'assign_{i}') for i in range(4)]

# Domain: each assign[i] is one of the 6 students (0..5)
for i in range(4):
    solver.add(assign[i] >= 0, assign[i] <= 5)

# All assigned students must be distinct (each student can be assigned to at most one year)
solver.add(Distinct(assign))

# Condition 1: Only Louis (0) or Tiffany (4) can be assigned to 1923 (index 2)
solver.add(Or(assign[2] == 0, assign[2] == 4))

# Condition 2: If Mollie (1) is assigned to the project, then she must be assigned to either 1921 (0) or 1922 (1)
# "If Mollie is assigned" means Mollie appears in one of the 4 positions
mollie_assigned = Or([assign[i] == 1 for i in range(4)])
mollie_in_21_or_22 = Or(assign[0] == 1, assign[1] == 1)
solver.add(Implies(mollie_assigned, mollie_in_21_or_22))

# Condition 3: If Tiffany (4) is assigned to the project, then Ryan (3) must be assigned to the project.
tiffany_assigned = Or([assign[i] == 4 for i in range(4)])
ryan_assigned = Or([assign[i] == 3 for i in range(4)])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Condition 4: If Ryan (3) is assigned to the project, then Onyx (2) must be assigned to the year immediately prior to Ryan's.
# "Immediately prior" means if Ryan is at position p, Onyx is at position p-1.
# We need to encode: for each possible position p where Ryan could be, Onyx is at p-1.
# Ryan can be at positions 1, 2, or 3 (since position 0 has no prior year).
ryan_prior_constraints = []
for p in range(1, 4):  # Ryan can be at positions 1, 2, or 3
    ryan_prior_constraints.append(Implies(assign[p] == 3, assign[p-1] == 2))
solver.add(Implies(ryan_assigned, And(ryan_prior_constraints)))

# Also: if Ryan is assigned, he cannot be at position 0 (no prior year for Onyx)
solver.add(Implies(ryan_assigned, assign[0] != 3))

# Now evaluate each option
# Each option gives a list of 4 students in order 1921, 1922, 1923, 1924

# Map student names to integers
name_to_int = {"Louis": 0, "Mollie": 1, "Onyx": 2, "Ryan": 3, "Tiffany": 4, "Yoshio": 5}

options = {
    "A": ["Louis", "Onyx", "Ryan", "Yoshio"],
    "B": ["Mollie", "Yoshio", "Tiffany", "Onyx"],
    "C": ["Onyx", "Ryan", "Louis", "Tiffany"],
    "D": ["Tiffany", "Onyx", "Louis", "Ryan"],
    "E": ["Yoshio", "Onyx", "Louis", "Mollie"]
}

found_options = []
for letter, names in options.items():
    constr = And([assign[i] == name_to_int[names[i]] for i in range(4)])
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