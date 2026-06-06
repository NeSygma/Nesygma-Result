from z3 import *

def base_solver():
    s = Solver()
    students = ['Louis','Mollie','Onyx','Ryan','Tiffany','Yoshio']
    years = [1921,1922,1923,1924]
    assign = {stu: Int(f'year_{stu}') for stu in students}
    # domain: -1 (not assigned) or one of years
    for stu in students:
        s.add(Or(assign[stu] == -1, Or([assign[stu] == y for y in years])))
    # exactly four assigned
    s.add(Sum([If(assign[stu] != -1, 1, 0) for stu in students]) == 4)
    # each year assigned to exactly one student
    for y in years:
        s.add(Sum([If(assign[stu] == y, 1, 0) for stu in students]) == 1)
    # Only Louis or Tiffany can be assigned to 1923
    for stu in students:
        if stu not in ['Louis','Tiffany']:
            s.add(assign[stu] != 1923)
    # Mollie if assigned must be 1921 or 1922
    s.add(Implies(assign['Mollie'] != -1, Or(assign['Mollie'] == 1921, assign['Mollie'] == 1922)))
    # Tiffany assigned => Ryan assigned
    s.add(Implies(assign['Tiffany'] != -1, assign['Ryan'] != -1))
    # Ryan assigned => Onyx year = Ryan-1 and Ryan not 1921
    s.add(Implies(assign['Ryan'] != -1,
                  And(assign['Ryan'] != 1921,
                      assign['Onyx'] == assign['Ryan'] - 1)))
    return s, assign

option_constraints = {
    'A': lambda a: a['Louis'] == 1924,
    'B': lambda a: a['Onyx'] == 1921,
    'C': lambda a: a['Onyx'] == 1924,
    'D': lambda a: a['Tiffany'] == 1923,
    'E': lambda a: a['Yoshio'] == 1921,
}

base_s, base_assign = base_solver()
found_options = []
for letter, constr in [(l, option_constraints[l]) for l in ['A','B','C','D','E']]:
    s = Solver()
    # add base constraints
    for c in base_s.assertions():
        s.add(c)
    # add option constraint
    s.add(constr(base_assign))
    # Now test if there exists a model where Mollie is NOT 1922 (i.e., either -1 or 1921)
    s.push()
    s.add(Or(base_assign['Mollie'] == -1, base_assign['Mollie'] == 1921))
    if s.check() == unsat:
        # No model where Mollie !=1922, so Mollie must be 1922 under this option
        found_options.append(letter)
    s.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")