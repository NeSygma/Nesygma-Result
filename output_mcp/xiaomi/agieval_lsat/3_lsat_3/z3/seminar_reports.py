from z3 import *

solver = Solver()

# Students: George(0), Helen(1), Irving(2), Kyle(3), Lenore(4), Nina(5), Olivia(6), Robert(7)
students = ['George', 'Helen', 'Irving', 'Kyle', 'Lenore', 'Nina', 'Olivia', 'Robert']
n_students = 8

# Days: Monday(0), Tuesday(1), Wednesday(2)
days = ['Monday', 'Tuesday', 'Wednesday']
n_days = 3

# For each student, which day they report (0=Mon, 1=Tue, 2=Wed), or -1 if not reporting
report_day = [Int(f'report_day_{i}') for i in range(n_students)]

# For each student, whether they report in morning (0) or afternoon (1), or -1 if not reporting
report_slot = [Int(f'report_slot_{i}') for i in range(n_students)]

# Whether each student gives a report
gives_report = [Bool(f'gives_report_{i}') for i in range(n_students)]

# Exactly 6 students give reports
solver.add(Sum([If(gives_report[i], 1, 0) for i in range(n_students)]) == 6)

# Domain constraints
for i in range(n_students):
    # If gives report, day is 0-2 and slot is 0-1
    solver.add(Implies(gives_report[i], And(report_day[i] >= 0, report_day[i] <= 2)))
    solver.add(Implies(gives_report[i], And(report_slot[i] >= 0, report_slot[i] <= 1)))
    # If not giving report, set to -1
    solver.add(Implies(Not(gives_report[i]), And(report_day[i] == -1, report_slot[i] == -1)))

# Exactly 2 reports per day (one morning, one afternoon)
for d in range(n_days):
    # Exactly 2 students report on day d
    solver.add(Sum([If(And(gives_report[i], report_day[i] == d), 1, 0) for i in range(n_students)]) == 2)
    # Exactly 1 morning and 1 afternoon on day d
    solver.add(Sum([If(And(gives_report[i], report_day[i] == d, report_slot[i] == 0), 1, 0) for i in range(n_students)]) == 1)
    solver.add(Sum([If(And(gives_report[i], report_day[i] == d, report_slot[i] == 1), 1, 0) for i in range(n_students)]) == 1)

# Constraint 1: George can only give a report on Tuesday
solver.add(Implies(gives_report[0], report_day[0] == 1))

# Constraint 2: Olivia(6) and Robert(7) cannot give afternoon reports
solver.add(Implies(gives_report[6], report_slot[6] == 0))
solver.add(Implies(gives_report[7], report_slot[7] == 0))

# Constraint 3: If Nina(5) gives a report, then on the next day Helen(1) and Irving(2) must both give reports, unless Nina's report is on Wednesday
for d in range(n_days):
    # If Nina reports on day d and d is not Wednesday (d < 2)
    solver.add(Implies(And(gives_report[5], report_day[5] == d, d < 2),
                       And(gives_report[1], report_day[1] == d + 1,
                           gives_report[2], report_day[2] == d + 1)))

# Now test each answer choice
# The question: which pair, if they give reports on the same day, MUST give reports on Wednesday?

# Option A: George and Lenore
opt_a_constr = And(gives_report[0], gives_report[4], report_day[0] == report_day[4])

# Option B: Helen and Nina
opt_b_constr = And(gives_report[1], gives_report[5], report_day[1] == report_day[5])

# Option C: Irving and Robert
opt_c_constr = And(gives_report[2], gives_report[7], report_day[2] == report_day[7])

# Option D: Kyle and Nina
opt_d_constr = And(gives_report[3], gives_report[5], report_day[3] == report_day[5])

# Option E: Olivia and Kyle
opt_e_constr = And(gives_report[6], gives_report[3], report_day[6] == report_day[3])

# For each option, check if the pair being on the same day forces that day to be Wednesday
# We need: if they're on the same day, that day MUST be Wednesday
# i.e., it's impossible for them to be on the same day on Monday or Tuesday

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    # Check if they can be on the same day but NOT on Wednesday
    solver.push()
    solver.add(constr)
    # Try to make them on the same day but not Wednesday (i.e., Monday or Tuesday)
    solver.add(report_day[0 if letter == "A" else (1 if letter == "B" else (2 if letter == "C" else (3 if letter == "D" else 6)))] != 2)
    result = solver.check()
    if result == unsat:
        # They cannot be on the same day unless it's Wednesday
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