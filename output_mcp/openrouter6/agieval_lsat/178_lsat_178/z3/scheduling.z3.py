from z3 import *

BENCHMARK_MODE = True

# Student indices
G, H, J, K, L = 0, 1, 2, 3, 4
students = [G, H, J, K, L]
student_names = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]

# Days: 0=Mon,1=Tue,2=Wed,3=Thu,4=Fri
days = 5
shifts = 2  # 0=first, 1=second

# Declare work[s][d][shift] as Bool
work = [[[Bool(f"work_{s}_{d}_{shift}") for shift in range(shifts)] for d in range(days)] for s in students]

solver = Solver()

# Constraint 1: Each shift has exactly one student
for d in range(days):
    for shift in range(shifts):
        solver.add(Sum([work[s][d][shift] for s in students]) == 1)

# Constraint 2: Each student works exactly two shifts
for s in students:
    solver.add(Sum([work[s][d][shift] for d in range(days) for shift in range(shifts)]) == 2)

# Constraint 3: No student works both shifts on the same day
for s in students:
    for d in range(days):
        solver.add(work[s][d][0] + work[s][d][1] <= 1)

# Constraint 4: Louise works exactly two second shifts on consecutive days
# Louise never works first shift
for d in range(days):
    solver.add(Not(work[L][d][0]))
# She works exactly two second shifts
solver.add(Sum([work[L][d][1] for d in range(days)]) == 2)
# They are consecutive
consecutive_L = Or([And(work[L][d][1], work[L][d+1][1]) for d in range(4)])
solver.add(consecutive_L)

# Constraint 5: Grecia works exactly two first shifts on nonconsecutive days
# Grecia never works second shift
for d in range(days):
    solver.add(Not(work[G][d][1]))
# She works exactly two first shifts
solver.add(Sum([work[G][d][0] for d in range(days)]) == 2)
# They are nonconsecutive
nonconsecutive_G = Not(Or([And(work[G][d][0], work[G][d+1][0]) for d in range(4)]))
solver.add(nonconsecutive_G)

# Constraint 6: Katya works on Tuesday and Friday (one shift each)
# She works exactly two shifts total
solver.add(Sum([work[K][d][shift] for d in range(days) for shift in range(shifts)]) == 2)
# On Tuesday (day 1) she works exactly one shift
solver.add(Sum([work[K][1][shift] for shift in range(shifts)]) == 1)
# On Friday (day 4) she works exactly one shift
solver.add(Sum([work[K][4][shift] for shift in range(shifts)]) == 1)

# Constraint 7: Hakeem and Joe work on the same day at least once
# Define work_day for each student and day
work_day = [[Or(work[s][d][0], work[s][d][1]) for d in range(days)] for s in students]
solver.add(Or([And(work_day[H][d], work_day[J][d]) for d in range(days)]))

# Constraint 8: Grecia and Louise never work on the same day
for d in range(days):
    solver.add(work[G][d][0] + work[L][d][1] <= 1)

# Additional condition: There is at least one day on which Grecia and Joe both work
solver.add(Or([And(work[G][d][0], work_day[J][d]) for d in range(days)]))

# Now test each answer choice
options = [
    ("A", work[G][1][0]),  # Grecia works first shift on Tuesday
    ("B", work[H][0][1]),  # Hakeem works second shift on Monday
    ("C", work[H][2][1]),  # Hakeem works second shift on Wednesday
    ("D", work[J][2][0]),  # Joe works first shift on Wednesday
    ("E", work[J][3][0]),  # Joe works first shift on Thursday
]

found_options = []
for letter, constr in options:
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