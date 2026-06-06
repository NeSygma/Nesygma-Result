from z3 import *

def base_solver():
    s = Solver()
    # Students list
    students = ['Louis','Mollie','Onyx','Ryan','Tiffany','Yoshio']
    years = [1921,1922,1923,1924]
    # Create variables: assign year -> student (function) or student -> year.
    # We'll use a mapping student -> year (Int) with -1 meaning not assigned.
    assign = {stu: Int(f'year_{stu}') for stu in students}
    # Domain: either -1 (not assigned) or one of the years
    for stu in students:
        s.add(Or(assign[stu] == -1, Or([assign[stu] == y for y in years]))
    # Exactly four students assigned (year != -1)
    assigned_vars = [If(assign[stu] != -1, 1, 0) for stu in students]
    s.add(Sum(assigned_vars) == 4)
    # Each year assigned to exactly one student
    for y in years:
        s.add(Sum([If(assign[stu] == y, 1, 0) for stu in students]) == 1)
    # Constraint: Only Louis or Tiffany can be assigned to 1923.
    # Means the student assigned to 1923 must be Louis or Tiffany.
    # So for each other student, they cannot have year 1923.
    for stu in students:
        if stu not in ['Louis','Tiffany']:
            s.add(assign[stu] != 1923)
    # If Mollie assigned, year must be 1921 or 1922.
    s.add(Implies(assign['Mollie'] != -1, Or(assign['Mollie'] == 1921, assign['Mollie'] == 1922)))
    # If Tiffany assigned, Ryan assigned.
    s.add(Implies(assign['Tiffany'] != -1, assign['Ryan'] != -1))
    # If Ryan assigned, Onyx assigned to year immediately prior.
    # Ryan cannot be 1921.
    s.add(Implies(assign['Ryan'] != -1, And(assign['Ryan'] != 1921, assign['Onyx'] == assign['Ryan'] - 1)))
    return s, assign

def check_option(option):
    s, assign = base_solver()
    # add option constraint
    if option == 'A':
        s.add(assign['Louis'] == 1924)
    elif option == 'B':
        s.add(assign['Onyx'] == 1921)
    elif option == 'C':
        s.add(assign['Onyx'] == 1924)
    elif option == 'D':
        s.add(assign['Tiffany'] == 1923)
    elif option == 'E':
        s.add(assign['Yoshio'] == 1921)
    else:
        raise ValueError('bad')
    res = s.check()
    print('Option', option, 'result', res)
    if res == sat:
        m = s.model()
        print({stu: m[assign[stu]] for stu in assign})

for opt in ['A','B','C','D','E']:
    check_option(opt)