from z3 import *

solver = Solver()

# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
# Shifts: 0=First, 1=Second
# Students: 0=Grecia, 1=Hakeem, 2=Joe, 3=Katya, 4=Louise

days = 5
shifts = 2
students = 5

# assign[d][s] = student working shift s on day d
assign = [[Int(f"assign_{d}_{s}") for s in range(shifts)] for d in range(days)]

# Each assignment is a valid student (0-4)
for d in range(days):
    for s in range(shifts):
        solver.add(assign[d][s] >= 0, assign[d][s] < students)

# Each student works exactly 2 shifts
for stu in range(students):
    solver.add(Sum([If(assign[d][s] == stu, 1, 0) for d in range(days) for s in range(shifts)]) == 2)

# No student works both shifts of any day
for d in range(days):
    solver.add(assign[d][0] != assign[d][1])

# Constraint 2: On two consecutive days, Louise (4) works the second shift
consecutive_louise = []
for d in range(4):
    consecutive_louise.append(And(assign[d][1] == 4, assign[d+1][1] == 4))
solver.add(Or(consecutive_louise))

# Constraint 3: On two nonconsecutive days, Grecia (0) works the first shift
nonconsecutive_grecia = []
for d1 in range(days):
    for d2 in range(d1+2, days):
        nonconsecutive_grecia.append(And(assign[d1][0] == 0, assign[d2][0] == 0))
solver.add(Or(nonconsecutive_grecia))

# Constraint 4: Katya (3) works on Tuesday (1) and Friday (4)
solver.add(Or(assign[1][0] == 3, assign[1][1] == 3))
solver.add(Or(assign[4][0] == 3, assign[4][1] == 3))

# Constraint 5: Hakeem (1) and Joe (2) work on the same day at least once
same_day_hj = []
for d in range(days):
    h_on_d = Or(assign[d][0] == 1, assign[d][1] == 1)
    j_on_d = Or(assign[d][0] == 2, assign[d][1] == 2)
    same_day_hj.append(And(h_on_d, j_on_d))
solver.add(Or(same_day_hj))

# Constraint 6: Grecia (0) and Louise (4) never work on the same day
for d in range(days):
    g_on_d = Or(assign[d][0] == 0, assign[d][1] == 0)
    l_on_d = Or(assign[d][0] == 4, assign[d][1] == 4)
    solver.add(Not(And(g_on_d, l_on_d)))

# Additional: Hakeem works on Wednesday (day 2)
solver.add(Or(assign[2][0] == 1, assign[2][1] == 1))

# Answer options: which pair of days must Joe work on?
# Joe works exactly 2 shifts on 2 different days (from constraints)
# For each option, check if there's a valid assignment where Joe works on exactly those 2 days
options = {
    "A": (0, 2),  # Monday and Wednesday
    "B": (0, 3),  # Monday and Thursday
    "C": (1, 2),  # Tuesday and Wednesday
    "D": (1, 3),  # Tuesday and Thursday
    "E": (2, 3),  # Wednesday and Thursday
}

found_options = []
for letter, (d1, d2) in options.items():
    solver.push()
    # Joe works at least one shift on d1
    solver.add(Or(assign[d1][0] == 2, assign[d1][1] == 2))
    # Joe works at least one shift on d2
    solver.add(Or(assign[d2][0] == 2, assign[d2][1] == 2))
    # Joe does NOT work on other days
    for d in range(days):
        if d != d1 and d != d2:
            solver.add(assign[d][0] != 2)
            solver.add(assign[d][1] != 2)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} ({d1},{d2}) is SAT:")
        for d in range(days):
            for s in range(shifts):
                print(f"  Day {d} Shift {s}: Student {m[assign[d][s]]}")
    else:
        print(f"Option {letter} ({d1},{d2}) is {result}")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")