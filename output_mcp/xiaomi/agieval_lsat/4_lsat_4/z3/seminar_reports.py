from z3 import *

# Students: George(0), Helen(1), Irving(2), Kyle(3), Lenore(4), Nina(5), Olivia(6), Robert(7)
# Days: Monday(0), Tuesday(1), Wednesday(2)
# Slots: Morning(0), Afternoon(1)

N_STUDENTS = 8
N_DAYS = 3
N_SLOTS = 2

students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
days = ["Monday", "Tuesday", "Wednesday"]
slots = ["Morning", "Afternoon"]

# report[s][d][sl] = True if student s gives a report on day d in slot sl
report = [[[Bool(f"report_{s}_{d}_{sl}") for sl in range(N_SLOTS)] for d in range(N_DAYS)] for s in range(N_STUDENTS)]

solver = Solver()

# Exactly 6 students give reports (2 don't)
# Each student either gives a report or doesn't
for s in range(N_STUDENTS):
    gives = Or([report[s][d][sl] for d in range(N_DAYS) for sl in range(N_SLOTS)])
    # Each student gives at most one report total
    for i in range(N_DAYS * N_SLOTS):
        for j in range(i+1, N_DAYS * N_SLOTS):
            d1, sl1 = divmod(i, N_SLOTS)
            d2, sl2 = divmod(j, N_SLOTS)
            solver.add(Not(And(report[s][d1][sl1], report[s][d2][sl2])))

# Exactly 6 students give reports
solver.add(Sum([If(Or([report[s][d][sl] for d in range(N_DAYS) for sl in range(N_SLOTS)]), 1, 0) for s in range(N_STUDENTS)]) == 6)

# Exactly 2 reports per day (one morning, one afternoon)
for d in range(N_DAYS):
    for sl in range(N_SLOTS):
        solver.add(Sum([If(report[s][d][sl], 1, 0) for s in range(N_STUDENTS)]) == 1)

# Tuesday is the only day George can give a report
for d in range(N_DAYS):
    if d != 1:  # Not Tuesday
        for sl in range(N_SLOTS):
            solver.add(Not(report[0][d][sl]))

# Neither Olivia nor Robert can give an afternoon report
for d in range(N_DAYS):
    solver.add(Not(report[6][d][1]))  # Olivia
    solver.add(Not(report[7][d][1]))  # Robert

# If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday.
# Nina is index 5
for d in range(N_DAYS):
    for sl in range(N_SLOTS):
        if d < 2:  # Monday or Tuesday (next day exists)
            # If Nina reports on day d, then on day d+1 both Helen and Irving must report
            solver.add(Implies(report[5][d][sl], 
                              And(Or([report[1][d+1][sl2] for sl2 in range(N_SLOTS)]),
                                  Or([report[2][d+1][sl2] for sl2 in range(N_SLOTS)]))))

# Additional constraints from the question:
# George, Nina, and Robert give reports
solver.add(Or([report[0][d][sl] for d in range(N_DAYS) for sl in range(N_SLOTS)]))  # George
solver.add(Or([report[5][d][sl] for d in range(N_DAYS) for sl in range(N_SLOTS)]))  # Nina
solver.add(Or([report[7][d][sl] for d in range(N_DAYS) for sl in range(N_SLOTS)]))  # Robert

# They do so on different days from one another
# George can only be on Tuesday (day 1)
# So Nina and Robert must be on Monday and Wednesday (in some order)
# Nina not on Tuesday, Robert not on Tuesday
for sl in range(N_SLOTS):
    solver.add(Not(report[5][1][sl]))  # Nina not on Tuesday
    solver.add(Not(report[7][1][sl]))  # Robert not on Tuesday

# Define option constraints
# (A) Helen gives a report on Wednesday
opt_a = Or([report[1][2][sl] for sl in range(N_SLOTS)])

# (B) Nina gives a report on Monday
opt_b = Or([report[5][0][sl] for sl in range(N_SLOTS)])

# (C) Nina gives a report on Tuesday
opt_c = Or([report[5][1][sl] for sl in range(N_SLOTS)])

# (D) Olivia gives a report on Monday
opt_d = Or([report[6][0][sl] for sl in range(N_SLOTS)])

# (E) Robert gives a report on Wednesday
opt_e = Or([report[7][2][sl] for sl in range(N_SLOTS)])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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