from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Shifts: 0=first, 1=second
# Students: 0=Grecia, 1=Hakeem, 2=Joe, 3=Katya, 4=Louise

solver = Solver()

# schedule[day][shift] = student working that shift
schedule = [[Int(f"schedule_{d}_{s}") for s in range(2)] for d in range(5)]

# Each shift is worked by exactly one student (0-4)
for d in range(5):
    for s in range(2):
        solver.add(schedule[d][s] >= 0, schedule[d][s] <= 4)

# Each student works exactly two shifts total
for student in range(5):
    solver.add(Sum([If(schedule[d][s] == student, 1, 0) for d in range(5) for s in range(2)]) == 2)

# No student works both shifts of any day
for d in range(5):
    solver.add(schedule[d][0] != schedule[d][1])

# On two consecutive days, Louise (4) works the second shift
# Find two consecutive days where Louise works second shift
louise_second = [Bool(f"louise_second_{d}") for d in range(5)]
for d in range(5):
    solver.add(louise_second[d] == (schedule[d][1] == 4))

# At least one pair of consecutive days where Louise works second shift
solver.add(Or(
    And(louise_second[0], louise_second[1]),
    And(louise_second[1], louise_second[2]),
    And(louise_second[2], louise_second[3]),
    And(louise_second[3], louise_second[4])
))

# On two nonconsecutive days, Grecia (0) works the first shift
grecia_first = [Bool(f"grecia_first_{d}") for d in range(5)]
for d in range(5):
    solver.add(grecia_first[d] == (schedule[d][0] == 0))

# At least two nonconsecutive days where Grecia works first shift
# Nonconsecutive pairs: (0,2), (0,3), (0,4), (1,3), (1,4), (2,4)
solver.add(Or(
    And(grecia_first[0], grecia_first[2]),
    And(grecia_first[0], grecia_first[3]),
    And(grecia_first[0], grecia_first[4]),
    And(grecia_first[1], grecia_first[3]),
    And(grecia_first[1], grecia_first[4]),
    And(grecia_first[2], grecia_first[4])
))

# Katya (3) works on Tuesday (1) and Friday (4)
# Katya works at least one shift on Tuesday
solver.add(Or(schedule[1][0] == 3, schedule[1][1] == 3))
# Katya works at least one shift on Friday
solver.add(Or(schedule[4][0] == 3, schedule[4][1] == 3))

# Hakeem (1) and Joe (2) work on the same day at least once
solver.add(Or([
    Or(And(schedule[d][0] == 1, schedule[d][1] == 2),
       And(schedule[d][0] == 2, schedule[d][1] == 1),
       And(schedule[d][0] == 1, Or(schedule[d][0] == 2, schedule[d][1] == 2)),
       And(schedule[d][1] == 1, Or(schedule[d][0] == 2, schedule[d][1] == 2)))
    for d in range(5)
]))
# Simpler: on some day, both Hakeem and Joe appear (in either shift)
solver.add(Or([
    And(Or(schedule[d][0] == 1, schedule[d][1] == 1),
        Or(schedule[d][0] == 2, schedule[d][1] == 2))
    for d in range(5)
]))

# Grecia (0) and Louise (4) never work on the same day
for d in range(5):
    solver.add(Not(And(
        Or(schedule[d][0] == 0, schedule[d][1] == 0),
        Or(schedule[d][0] == 4, schedule[d][1] == 4)
    )))

# Additional constraint: Hakeem works on Wednesday (day 2)
solver.add(Or(schedule[2][0] == 1, schedule[2][1] == 1))

# Now test each answer option for Joe (2)
# Option A: Joe works Monday (0) and Wednesday (2)
opt_a = And(Or(schedule[0][0] == 2, schedule[0][1] == 2),
            Or(schedule[2][0] == 2, schedule[2][1] == 2))

# Option B: Joe works Monday (0) and Thursday (3)
opt_b = And(Or(schedule[0][0] == 2, schedule[0][1] == 2),
            Or(schedule[3][0] == 2, schedule[3][1] == 2))

# Option C: Joe works Tuesday (1) and Wednesday (2)
opt_c = And(Or(schedule[1][0] == 2, schedule[1][1] == 2),
            Or(schedule[2][0] == 2, schedule[2][1] == 2))

# Option D: Joe works Tuesday (1) and Thursday (3)
opt_d = And(Or(schedule[1][0] == 2, schedule[1][1] == 2),
            Or(schedule[3][0] == 2, schedule[3][1] == 2))

# Option E: Joe works Wednesday (2) and Thursday (3)
opt_e = And(Or(schedule[2][0] == 2, schedule[2][1] == 2),
            Or(schedule[3][0] == 2, schedule[3][1] == 2))

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