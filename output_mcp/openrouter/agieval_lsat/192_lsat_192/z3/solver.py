from z3 import *

# Define years and student IDs
years = [1921, 1922, 1923, 1924]
# Student IDs: 0=Louis,1=Mollie,2=Onyx,3=Ryan,4=Tiffany,5=Yoshio
students = list(range(6))

# Variables: student assigned to each year
assign = {y: Int(f'assign_{y}') for y in years}
solver = Solver()

# Domain constraints: each assign variable must be one of the six students
for y in years:
    solver.add(Or([assign[y] == s for s in students]))

# All four assigned students must be distinct (since each year gets a different student)
solver.add(Distinct([assign[y] for y in years]))

# Base constraints
# Only Louis (0) or Tiffany (4) can be assigned to 1923
solver.add(Or(assign[1923] == 0, assign[1923] == 4))

# If Mollie (1) is assigned, she must be in 1921 or 1922
for y in years:
    solver.add(Implies(assign[y] == 1, Or(y == 1921, y == 1922)))

# If Tiffany (4) is assigned, Ryan (3) must be assigned somewhere
tiffany_assigned = Or([assign[y] == 4 for y in years])
ryan_assigned = Or([assign[y] == 3 for y in years])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# If Ryan is assigned, Onyx (2) must be assigned to the year immediately prior to Ryan's
# For each possible Ryan year, enforce existence of Onyx at year-1
for ry in years:
    # condition: Ryan at ry
    cond_ry = assign[ry] == 3
    # possible Onyx placements that satisfy prior-year relation
    prior_options = []
    for oy in years:
        if oy == ry - 1:
            prior_options.append(assign[oy] == 2)
    # If there is a valid prior year (i.e., ry not 1921), enforce it; otherwise Ryan cannot be at that year
    if prior_options:
        solver.add(Implies(cond_ry, Or(prior_options)))
    else:
        # No prior year exists, so Ryan cannot be at this year
        solver.add(assign[ry] != 3)

# Premise: both Ryan and Yoshio are assigned to the project
solver.add(ryan_assigned)
solver.add(Or([assign[y] == 5 for y in years]))

# Define option constraints
opt_constraints = {
    "A": assign[1923] == 0,          # Louis assigned to 1923
    "B": assign[1921] == 1,          # Mollie assigned to 1921
    "C": assign[1922] == 2,          # Onyx assigned to 1922
    "D": assign[1924] == 4,          # Tiffany assigned to 1924
    "E": assign[1922] == 5           # Yoshio assigned to 1922
}

found_options = []
for letter, constr in opt_constraints.items():
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