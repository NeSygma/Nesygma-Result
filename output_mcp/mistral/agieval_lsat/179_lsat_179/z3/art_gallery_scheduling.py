from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# Create solver
solver = Solver()

# Define students, days, and shifts
students = ['Grecia', 'Hakeem', 'Joe', 'Katya', 'Louise']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
shifts = ['first', 'second']

# Map names to indices
student_to_idx = {s: i for i, s in enumerate(students)}
day_to_idx = {d: i for i, d in enumerate(days)}

# Create schedule: schedule[day][shift] = student_idx
# We'll use a 2D list of Int variables
schedule = [[Int(f"schedule_{days[d]}_{shifts[sh]}") for sh in range(2)] for d in range(5)]

# Constraint 1: Each student works exactly 2 shifts
for s in range(5):
    total_shifts = Sum([If(schedule[d][sh] == s, 1, 0) for d in range(5) for sh in range(2)])
    solver.add(total_shifts == 2)

# Constraint 2: No student works both shifts of any day
for d in range(5):
    solver.add(schedule[d][0] != schedule[d][1])

# Constraint 3: Louise works the second shift on exactly two consecutive days
# Louise is student 4
consecutive_louise = [Bool(f'consec_louise_{d}') for d in range(4)]
for d in range(4):
    # If this consecutive pair has Louise on second shift both days
    solver.add(Implies(consecutive_louise[d], 
                       And(schedule[d][1] == 4, schedule[d+1][1] == 4)))
# Exactly one such consecutive pair exists
solver.add(Sum(consecutive_louise) == 1)

# Constraint 4: Grecia works the first shift on exactly two non-consecutive days
# Grecia is student 0
grecia_first = [Bool(f'grecia_first_{d}') for d in range(5)]
for d in range(5):
    solver.add(Implies(grecia_first[d], schedule[d][0] == 0))

# Exactly 2 days with Grecia on first shift
solver.add(Sum(grecia_first) == 2)

# Non-consecutive constraint for Grecia's first shifts
for i in range(5):
    for j in range(i+1, 5):
        solver.add(Implies(And(grecia_first[i], grecia_first[j]), abs(i - j) > 1))

# Constraint 5: Katya works on Tuesday and Friday
# Katya is student 3
# Tuesday is day 1, Friday is day 4
solver.add(Or(schedule[1][0] == 3, schedule[1][1] == 3))  # Tuesday
solver.add(Or(schedule[4][0] == 3, schedule[4][1] == 3))  # Friday

# Constraint 6: Hakeem and Joe work on the same day at least once
# Hakeem is 1, Joe is 2
solver.add(Or(
    Or([And(schedule[d][0] == 1, schedule[d][1] == 2) for d in range(5)]),
    Or([And(schedule[d][0] == 2, schedule[d][1] == 1) for d in range(5)])
))

# Constraint 7: Grecia and Louise never work on the same day
# Grecia is 0, Louise is 4
for d in range(5):
    solver.add(Not(Or(
        And(schedule[d][0] == 0, schedule[d][1] == 4),
        And(schedule[d][0] == 4, schedule[d][1] == 0)
    )))

# Additional constraint from the question: Katya works the second shift on Tuesday
# Tuesday is day 1, second shift is shift 1, Katya is 3
solver.add(schedule[1][1] == 3)

# Now evaluate the multiple choice options
# (A) Grecia works the first shift on Monday
opt_a_constr = (schedule[0][0] == 0)

# (B) Hakeem works the first shift on Monday
opt_b_constr = (schedule[0][0] == 1)

# (C) Hakeem works the second shift on Wednesday
opt_c_constr = (schedule[2][1] == 1)

# (D) Joe works the second shift on Thursday
opt_d_constr = (schedule[3][1] == 2)

# (E) Louise works the second shift on Monday
opt_e_constr = (schedule[0][1] == 4)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")