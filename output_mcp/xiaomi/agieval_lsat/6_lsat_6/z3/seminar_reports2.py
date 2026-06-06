from z3 import *

# Students: 0=George, 1=Helen, 2=Irving, 3=Kyle, 4=Lenore, 5=Nina, 6=Olivia, 7=Robert
students = ['George', 'Helen', 'Irving', 'Kyle', 'Lenore', 'Nina', 'Olivia', 'Robert']
n_students = 8

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
days = ['Monday', 'Tuesday', 'Wednesday']
n_days = 3

# Slots: 0=morning, 1=afternoon
slots = ['morning', 'afternoon']

def build_base_constraints():
    solver = Solver()
    
    reports = [[Int(f'reports_{d}_{s}') for s in range(2)] for d in range(3)]
    
    for d in range(3):
        for s in range(2):
            solver.add(reports[d][s] >= 0, reports[d][s] < n_students)
    
    all_reports = [reports[d][s] for d in range(3) for s in range(2)]
    solver.add(Distinct(all_reports))
    
    # George can only give a report on Tuesday (day 1)
    for d in range(3):
        for s in range(2):
            if d != 1:
                solver.add(reports[d][s] != 0)
    
    # Olivia (6) and Robert (7) cannot give afternoon reports
    for d in range(3):
        solver.add(reports[d][1] != 6)
        solver.add(reports[d][1] != 7)
    
    # Nina constraint
    for d in range(3):
        nina_on_day_d = Or([reports[d][s] == 5 for s in range(2)])
        if d < 2:
            helen_next = Or([reports[d+1][s] == 1 for s in range(2)])
            irving_next = Or([reports[d+1][s] == 2 for s in range(2)])
            solver.add(Implies(nina_on_day_d, And(helen_next, irving_next)))
    
    # Helen, Kyle, Lenore give morning reports
    morning_reports = [reports[d][0] for d in range(3)]
    solver.add(Or([And(morning_reports[0] == 1, morning_reports[1] == 3, morning_reports[2] == 4),
                  And(morning_reports[0] == 1, morning_reports[1] == 4, morning_reports[2] == 3),
                  And(morning_reports[0] == 3, morning_reports[1] == 1, morning_reports[2] == 4),
                  And(morning_reports[0] == 3, morning_reports[1] == 4, morning_reports[2] == 1),
                  And(morning_reports[0] == 4, morning_reports[1] == 1, morning_reports[2] == 3),
                  And(morning_reports[0] == 4, morning_reports[1] == 3, morning_reports[2] == 1)]))
    
    return solver, reports

# Check which options MUST be true (negation is unsat)
options = {
    "A": lambda r: Or(r[0][0] == 1, r[0][1] == 1),  # Helen on Monday
    "B": lambda r: Or(r[0][0] == 2, r[0][1] == 2),  # Irving on Monday
    "C": lambda r: Or(r[2][0] == 2, r[2][1] == 2),  # Irving on Wednesday
    "D": lambda r: Or(r[1][0] == 3, r[1][1] == 3),  # Kyle on Tuesday
    "E": lambda r: Or(r[2][0] == 3, r[2][1] == 3),  # Kyle on Wednesday
}

must_be_true = []
for letter, opt_fn in options.items():
    # Check if negation is unsatisfiable (meaning option must be true)
    s = Solver()
    reports = [[Int(f'reports_{d}_{s2}') for s2 in range(2)] for d in range(3)]
    
    for d in range(3):
        for s2 in range(2):
            s.add(reports[d][s2] >= 0, reports[d][s2] < n_students)
    
    all_reports = [reports[d][s2] for d in range(3) for s2 in range(2)]
    s.add(Distinct(all_reports))
    
    for d in range(3):
        for s2 in range(2):
            if d != 1:
                s.add(reports[d][s2] != 0)
    
    for d in range(3):
        s.add(reports[d][1] != 6)
        s.add(reports[d][1] != 7)
    
    for d in range(3):
        nina_on_day_d = Or([reports[d][s2] == 5 for s2 in range(2)])
        if d < 2:
            helen_next = Or([reports[d+1][s2] == 1 for s2 in range(2)])
            irving_next = Or([reports[d+1][s2] == 2 for s2 in range(2)])
            s.add(Implies(nina_on_day_d, And(helen_next, irving_next)))
    
    morning_reports = [reports[d][0] for d in range(3)]
    s.add(Or([And(morning_reports[0] == 1, morning_reports[1] == 3, morning_reports[2] == 4),
              And(morning_reports[0] == 1, morning_reports[1] == 4, morning_reports[2] == 3),
              And(morning_reports[0] == 3, morning_reports[1] == 1, morning_reports[2] == 4),
              And(morning_reports[0] == 3, morning_reports[1] == 4, morning_reports[2] == 1),
              And(morning_reports[0] == 4, morning_reports[1] == 1, morning_reports[2] == 3),
              And(morning_reports[0] == 4, morning_reports[1] == 3, morning_reports[2] == 1)]))
    
    # Add negation of the option
    s.add(Not(opt_fn(reports)))
    
    result = s.check()
    if result == unsat:
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is unsat)")
    else:
        print(f"Option {letter}: NOT necessarily true (counterexample exists)")
        if result == sat:
            m = s.model()
            for d in range(3):
                for s2 in range(2):
                    student_idx = m.evaluate(reports[d][s2]).as_long()
                    print(f"  {days[d]} {slots[s2]}: {students[student_idx]}")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")