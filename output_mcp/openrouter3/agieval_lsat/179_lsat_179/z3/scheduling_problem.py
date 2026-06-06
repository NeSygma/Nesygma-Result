from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Shifts: 0=First, 1=Second

# Create solver
solver = Solver()

# Variables: schedule[day][shift] = student
# Students: 0=Grecia, 1=Hakeem, 2=Joe, 3=Katya, 4=Louise
schedule = [[Int(f"schedule_{d}_{s}") for s in range(2)] for d in range(5)]

# Domain constraints: each schedule entry is a student ID (0-4)
for d in range(5):
    for s in range(2):
        solver.add(schedule[d][s] >= 0)
        solver.add(schedule[d][s] <= 4)

# Constraint 1: Each student works exactly 2 shifts
for student in range(5):
    count = Sum([If(schedule[d][s] == student, 1, 0) for d in range(5) for s in range(2)])
    solver.add(count == 2)

# Constraint 2: Each shift has exactly one student (already enforced by domain)
# Constraint 3: No student works both shifts on the same day
for d in range(5):
    solver.add(schedule[d][0] != schedule[d][1])

# Constraint 4: Louise works the second shift on two consecutive days
# Louise is student 4
louise_second_days = [d for d in range(5) if schedule[d][1] == 4]
# We need exactly two consecutive days where Louise works second shift
# Let's create a variable for each day indicating if Louise works second shift
louise_second = [Bool(f"louise_second_{d}") for d in range(5)]
for d in range(5):
    solver.add(louise_second[d] == (schedule[d][1] == 4))

# Exactly two consecutive days
# Check all possible consecutive pairs
consecutive_pairs = [(0,1), (1,2), (2,3), (3,4)]
# At least one pair must be true
solver.add(Or([And(louise_second[i], louise_second[j]) for i,j in consecutive_pairs]))
# Exactly two days total
solver.add(Sum([If(louise_second[d], 1, 0) for d in range(5)]) == 2)

# Constraint 5: Grecia works the first shift on two nonconsecutive days
# Grecia is student 0
grecia_first = [Bool(f"grecia_first_{d}") for d in range(5)]
for d in range(5):
    solver.add(grecia_first[d] == (schedule[d][0] == 0))

# Exactly two days total
solver.add(Sum([If(grecia_first[d], 1, 0) for d in range(5)]) == 2)
# Nonconsecutive: not both on consecutive days
for i in range(4):
    solver.add(Not(And(grecia_first[i], grecia_first[i+1])))

# Constraint 6: Katya works on Tuesday and Friday
# Katya is student 3
# She works on Tuesday (day 1) and Friday (day 4)
solver.add(Or(schedule[1][0] == 3, schedule[1][1] == 3))
solver.add(Or(schedule[4][0] == 3, schedule[4][1] == 3))

# Constraint 7: Hakeem and Joe work on the same day at least once
# Hakeem is 1, Joe is 2
same_day = [Bool(f"same_day_{d}") for d in range(5)]
for d in range(5):
    solver.add(same_day[d] == Or(
        And(schedule[d][0] == 1, schedule[d][1] == 2),
        And(schedule[d][0] == 2, schedule[d][1] == 1),
        And(schedule[d][0] == 1, schedule[d][1] == 1),  # Both on same shift? No, impossible
        And(schedule[d][0] == 2, schedule[d][1] == 2)   # Both on same shift? No, impossible
    ))
# Actually, they can't both work the same shift, so they must be on different shifts same day
# Let's correct: they work on the same day means one works first, other works second
for d in range(5):
    solver.add(same_day[d] == Or(
        And(schedule[d][0] == 1, schedule[d][1] == 2),
        And(schedule[d][0] == 2, schedule[d][1] == 1)
    ))
solver.add(Or(same_day))

# Constraint 8: Grecia and Louise never work on the same day
for d in range(5):
    solver.add(Not(Or(
        And(schedule[d][0] == 0, schedule[d][1] == 4),
        And(schedule[d][0] == 4, schedule[d][1] == 0)
    )))

# Additional constraint from question: Katya works the second shift on Tuesday
solver.add(schedule[1][1] == 3)  # Tuesday second shift is Katya

# Now test each option
# Option A: Grecia works the first shift on Monday
opt_a = (schedule[0][0] == 0)

# Option B: Hakeem works the first shift on Monday
opt_b = (schedule[0][0] == 1)

# Option C: Hakeem works the second shift on Wednesday
opt_c = (schedule[2][1] == 1)

# Option D: Joe works the second shift on Thursday
opt_d = (schedule[3][1] == 2)

# Option E: Louise works the second shift on Monday
opt_e = (schedule[0][1] == 4)

# Evaluate each option
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