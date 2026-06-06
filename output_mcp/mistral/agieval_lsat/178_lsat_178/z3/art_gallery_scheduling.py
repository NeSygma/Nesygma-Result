from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare students and their indices
students = [0, 1, 2, 3, 4]  # 0: Grecia, 1: Hakeem, 2: Joe, 3: Katya, 4: Louise
student_names = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]

# Declare days and their indices
days = [0, 1, 2, 3, 4]  # 0: Monday, 1: Tuesday, 2: Wednesday, 3: Thursday, 4: Friday

# Declare shifts and their indices
shifts = [0, 1]  # 0: first shift, 1: second shift

# Create a 2D array for the schedule: schedule[day][shift] = student
schedule = [[Int(f"schedule_{d}_{s}") for s in shifts] for d in days]

# Create solver
solver = Solver()

# Constraint 1: Each student works exactly 2 shifts
for student in students:
    total_shifts = Sum([If(schedule[d][sh] == student, 1, 0) for d in days for sh in shifts])
    solver.add(total_shifts == 2)

# Constraint 2: Each shift is worked by exactly one student (implicit in the function definition)
# We'll ensure all schedule entries are valid student indices
for d in days:
    for sh in shifts:
        solver.add(Or([schedule[d][sh] == s for s in students]))

# Constraint 3: No student works both shifts of any day
for d in days:
    solver.add(schedule[d][0] != schedule[d][1])

# Constraint 4: On two consecutive days, Louise works the second shift
# This means there exists at least one pair of consecutive days where Louise works second shift on both
consecutive_louise = []
for d in range(len(days) - 1):
    consecutive_louise.append(And(schedule[d][1] == 4, schedule[d+1][1] == 4))
solver.add(Or(consecutive_louise))

# Constraint 5: On two non-consecutive days, Grecia works the first shift
# This means there exists at least one pair of non-consecutive days where Grecia works first shift on both
non_consecutive_grecia = []
for d1 in days:
    for d2 in days:
        if d2 > d1 and not (d2 == d1 + 1 or d1 == d2 + 1):  # non-consecutive
            non_consecutive_grecia.append(And(schedule[d1][0] == 0, schedule[d2][0] == 0))
solver.add(Or(non_consecutive_grecia))

# Constraint 6: Katya works on Tuesday and Friday
# Katya (3) must work at least one shift on Tuesday (day 1) and at least one shift on Friday (day 4)
solver.add(Or([schedule[1][sh] == 3 for sh in shifts]))  # Tuesday
solver.add(Or([schedule[4][sh] == 3 for sh in shifts]))  # Friday

# Constraint 7: Hakeem and Joe work on the same day as each other at least once
same_day_hj = []
for d in days:
    same_day_hj.append(And(
        Or([schedule[d][sh] == 1 for sh in shifts]),  # Hakeem works on day d
        Or([schedule[d][sh] == 2 for sh in shifts])   # Joe works on day d
    ))
solver.add(Or(same_day_hj))

# Constraint 8: Grecia and Louise never work on the same day as each other
for d in days:
    # If Grecia works on day d, Louise cannot work on day d
    solver.add(Implies(
        Or([schedule[d][sh] == 0 for sh in shifts]),  # Grecia works on day d
        And([schedule[d][sh] != 4 for sh in shifts])  # Louise does not work on day d
    ))
    # If Louise works on day d, Grecia cannot work on day d
    solver.add(Implies(
        Or([schedule[d][sh] == 4 for sh in shifts]),  # Louise works on day d
        And([schedule[d][sh] != 0 for sh in shifts])  # Grecia does not work on day d
    ))

# Constraint 9: There is at least one day on which Grecia and Joe both work
at_least_one_grecia_joint = []
for d in days:
    at_least_one_grecia_joint.append(And(
        Or([schedule[d][sh] == 0 for sh in shifts]),  # Grecia works on day d
        Or([schedule[d][sh] == 2 for sh in shifts])   # Joe works on day d
    ))
solver.add(Or(at_least_one_grecia_joint))

# Now test each multiple-choice option to see which could be true
# We need to check each option independently

# Option A: Grecia works the first shift on Tuesday
# Tuesday is day 1, first shift is shift 0
opt_a_constr = (schedule[1][0] == 0)

# Option B: Hakeem works the second shift on Monday
# Monday is day 0, second shift is shift 1
opt_b_constr = (schedule[0][1] == 1)

# Option C: Hakeem works the second shift on Wednesday
# Wednesday is day 2, second shift is shift 1
opt_c_constr = (schedule[2][1] == 1)

# Option D: Joe works the first shift on Wednesday
# Wednesday is day 2, first shift is shift 0
opt_d_constr = (schedule[2][0] == 2)

# Option E: Joe works the first shift on Thursday
# Thursday is day 3, first shift is shift 0
opt_e_constr = (schedule[3][0] == 2)

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