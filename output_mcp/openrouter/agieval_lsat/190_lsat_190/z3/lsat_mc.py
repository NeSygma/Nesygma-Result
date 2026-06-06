from z3 import *

# Mapping student names to integers
students = {
    'Louis': 0,
    'Mollie': 1,
    'Onyx': 2,
    'Ryan': 3,
    'Tiffany': 4,
    'Yoshio': 5,
}

# Options: list of (letter, list of names for years 1921..1924)
options = [
    ("A", ["Louis", "Onyx", "Ryan", "Yoshio"]),
    ("B", ["Mollie", "Yoshio", "Tiffany", "Onyx"]),
    ("C", ["Onyx", "Ryan", "Louis", "Tiffany"]),
    ("D", ["Tiffany", "Onyx", "Louis", "Ryan"]),
    ("E", ["Yoshio", "Onyx", "Louis", "Mollie"]),
]

solver = Solver()
# Base variables for the four years
y1 = Int('y1')  # 1921
y2 = Int('y2')  # 1922
y3 = Int('y3')  # 1923
y4 = Int('y4')  # 1924

# Base constraints (domain and distinctness)
solver.add(And(y1 >= 0, y1 <= 5))
solver.add(And(y2 >= 0, y2 <= 5))
solver.add(And(y3 >= 0, y3 <= 5))
solver.add(And(y4 >= 0, y4 <= 5))
solver.add(Distinct(y1, y2, y3, y4))

# Additional problem constraints (as formulas over y1..y4)
# Only Louis or Tiffany can be assigned to 1923 (y3)
only_louis_or_tiffany_1923 = Or(y3 == students['Louis'], y3 == students['Tiffany'])
# If Mollie is assigned, she must be in 1921 or 1922
mollie_assigned = Or(y1 == students['Mollie'], y2 == students['Mollie'], y3 == students['Mollie'], y4 == students['Mollie'])
# then she must be in 1921 or 1922
mollie_constraint = Implies(mollie_assigned, Or(y1 == students['Mollie'], y2 == students['Mollie']))
# If Tiffany is assigned, Ryan must be assigned
tiffany_assigned = Or(y1 == students['Tiffany'], y2 == students['Tiffany'], y3 == students['Tiffany'], y4 == students['Tiffany'])
ryan_assigned = Or(y1 == students['Ryan'], y2 == students['Ryan'], y3 == students['Ryan'], y4 == students['Ryan'])
if_tiffany_then_ryan = Implies(tiffany_assigned, ryan_assigned)
# If Ryan is assigned, Onyx must be assigned to the year immediately prior to Ryan's
# Find Ryan's year index variable
# We'll encode as a disjunction of possibilities
ryan_year = Int('ryan_year')
onyx_year = Int('onyx_year')
# Link ryan_year to actual position
solver.add(ryan_year == If(y1 == students['Ryan'], 1,
                         If(y2 == students['Ryan'], 2,
                         If(y3 == students['Ryan'], 3,
                         If(y4 == students['Ryan'], 4, 0))))
# Similarly for onyx_year
solver.add(onyx_year == If(y1 == students['Onyx'], 1,
                         If(y2 == students['Onyx'], 2,
                         If(y3 == students['Onyx'], 3,
                         If(y4 == students['Onyx'], 4, 0))))
# If Ryan is assigned (ryan_year != 0) then onyx_year == ryan_year - 1
ryan_onyx_constraint = Implies(ryan_year != 0, And(onyx_year == ryan_year - 1))
# Also Ryan assigned implies Onyx assigned (implicitly via above because onyx_year must be valid)
# Add all problem constraints to base solver
solver.add(only_louis_or_tiffany_1923)
solver.add(mollie_constraint)
solver.add(if_tiffany_then_ryan)
solver.add(ryan_onyx_constraint)

found_options = []
for letter, names in options:
    # Build equality constraints for this option
    eqs = []
    eqs.append(y1 == students[names[0]])
    eqs.append(y2 == students[names[1]])
    eqs.append(y3 == students[names[2]])
    eqs.append(y4 == students[names[3]])
    # Also need to ensure ryan_year and onyx_year are correctly linked; they are already defined via y vars.
    solver.push()
    solver.add(*eqs)
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