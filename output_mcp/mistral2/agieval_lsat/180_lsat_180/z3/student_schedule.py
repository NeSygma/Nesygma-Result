from z3 import *

# Days: Monday (0), Tuesday (1), Wednesday (2), Thursday (3), Friday (4)
days = range(5)
shifts = [0, 1]  # 0: first shift, 1: second shift
students = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]

# Create a 3D array: schedule[day][shift] = student
schedule = [[String(f"schedule_{d}_{s}") for s in shifts] for d in days]

# Create a solver
solver = Solver()

# Helper: student works on a given day
works_on_day = {s: [Bool(f"works_{s}_{d}") for d in days] for s in students}

# Helper: student works a given shift
works_shift = {s: [Bool(f"works_{s}_{d}_{sft}") for d in days for sft in shifts] for s in students}

# Helper: student works a specific shift on a specific day
for s in students:
    for d in days:
        for sft in shifts:
            solver.add(works_shift[s][d*2 + sft] == (schedule[d][sft] == s))

# 1. Each student works exactly two shifts
for s in students:
    solver.add(Sum([works_shift[s][d*2 + sft] for d in days for sft in shifts]) == 2)

# 2. No student works both shifts of any day
for d in days:
    for s in students:
        solver.add(Not(And(schedule[d][0] == s, schedule[d][1] == s)))

# 3. On two consecutive days, Louise works the second shift
# Find two consecutive days where Louise works the second shift
consecutive_days = [(0,1), (1,2), (2,3), (3,4)]
for d1, d2 in consecutive_days:
    solver.add(Or(
        And(schedule[d1][1] == "Louise", schedule[d2][1] == "Louise"),
        And(schedule[d1][1] != "Louise", schedule[d2][1] != "Louise")
    ))
# Ensure exactly two consecutive days where Louise works the second shift
consecutive_louise = []
for d1, d2 in consecutive_days:
    consecutive_louise.append(And(schedule[d1][1] == "Louise", schedule[d2][1] == "Louise"))
solver.add(Sum(consecutive_louise) == 1)

# 4. On two nonconsecutive days, Grecia works the first shift
# Find two nonconsecutive days where Grecia works the first shift
nonconsecutive_days = [(0,2), (0,3), (0,4), (1,3), (1,4), (2,4)]
for d1, d2 in nonconsecutive_days:
    solver.add(Or(
        And(schedule[d1][0] == "Grecia", schedule[d2][0] == "Grecia"),
        And(schedule[d1][0] != "Grecia", schedule[d2][0] != "Grecia")
    ))
# Ensure exactly two nonconsecutive days where Grecia works the first shift
nonconsecutive_grecia = []
for d1, d2 in nonconsecutive_days:
    nonconsecutive_grecia.append(And(schedule[d1][0] == "Grecia", schedule[d2][0] == "Grecia"))
solver.add(Sum(nonconsecutive_grecia) == 1)

# 5. Katya works on Tuesday and Friday (at least one shift each day)
solver.add(Or(schedule[1][0] == "Katya", schedule[1][1] == "Katya"))
solver.add(Or(schedule[4][0] == "Katya", schedule[4][1] == "Katya"))

# 6. Hakeem and Joe work on the same day at least once
same_day_hj = []
for d in days:
    same_day_hj.append(And(Or(schedule[d][0] == "Hakeem", schedule[d][1] == "Hakeem"),
                           Or(schedule[d][0] == "Joe", schedule[d][1] == "Joe")))
solver.add(Or(same_day_hj))

# 7. Grecia and Louise never work on the same day
for d in days:
    solver.add(Not(And(Or(schedule[d][0] == "Grecia", schedule[d][1] == "Grecia"),
                       Or(schedule[d][0] == "Louise", schedule[d][1] == "Louise"))))

# Check for a solution
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    for d in days:
        for s in shifts:
            student = model[schedule[d][s]]
            print(f"Day {d} {s}: {student}")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")