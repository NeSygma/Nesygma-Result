from z3 import *

# Base solver with constraints common to all options

def base_solver():
    s = Solver()
    students = ['Louis','Mollie','Onyx','Ryan','Tiffany','Yoshio']
    years = [1921,1922,1923,1924]
    # Mapping student -> year, -1 means not assigned
    assign = {stu: Int(f'year_{stu}') for stu in students}
    # Domain constraints
    for stu in students:
        s.add(Or(assign[stu] == -1, Or([assign[stu] == y for y in years])))
    # Exactly four students assigned
    assigned = [If(assign[stu] != -1, 1, 0) for stu in students]
    s.add(Sum(assigned) == 4)
    # Each year assigned to exactly one student
    for y in years:
        s.add(Sum([If(assign[stu] == y, 1, 0) for stu in students]) == 1)
    # Only Louis or Tiffany can be assigned to 1923
    for stu in students:
        if stu not in ['Louis','Tiffany']:
            s.add(assign[stu] != 1923)
    # If Mollie assigned, she must be 1921 or 1922
    s.add(Implies(assign['Mollie'] != -1, Or(assign['Mollie'] == 1921, assign['Mollie'] == 1922)))
    # If Tiffany assigned, Ryan must be assigned
    s.add(Implies(assign['Tiffany'] != -1, assign['Ryan'] != -1))
    # If Ryan assigned, Onyx must be assigned to the year immediately prior
    # Ryan cannot be 1921 (no prior year)
    s.add(Implies(assign['Ryan'] != -1,
                  And(assign['Ryan'] != 1921,
                      assign['Onyx'] == assign['Ryan'] - 1)))
    return s, assign

# Option specific constraints
option_constraints = {
    'A': lambda assign: assign['Louis'] == 1924,
    'B': lambda assign: assign['Onyx'] == 1921,
    'C': lambda assign: assign['Onyx'] == 1924,
    'D': lambda assign: assign['Tiffany'] == 1923,
    'E': lambda assign: assign['Yoshio'] == 1921,
}

solver = Solver()
# Add base constraints once (they will be reused via push/pop)
base_s, base_assign = base_solver()
# Transfer base constraints to main solver
for c in base_s.assertions():
    solver.add(c)

found_options = []
for letter, constr_func in [(l, option_constraints[l]) for l in ['A','B','C','D','E']]:
    solver.push()
    solver.add(constr_func(base_assign))
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