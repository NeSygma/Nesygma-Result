from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Shifts: 0=first, 1=second
# Students: 0=Grecia, 1=Hakeem, 2=Joe, 3=Katya, 4=Louise

days = 5
shifts = 2
students = 5

# schedule[d][s] = student working day d, shift s
schedule = [[Int(f"schedule_{d}_{s}") for s in range(shifts)] for d in range(days)]

solver = Solver()

# Each schedule entry is a valid student (0-4)
for d in range(days):
    for s in range(shifts):
        solver.add(schedule[d][s] >= 0, schedule[d][s] < students)

# Each student works exactly 2 shifts total
for st in range(students):
    solver.add(Sum([If(schedule[d][s] == st, 1, 0) for d in range(days) for s in range(shifts)]) == 2)

# No student works both shifts of any day
for d in range(days):
    solver.add(schedule[d][0] != schedule[d][1])

# Each shift is worked by exactly one student (already ensured by Int domain + no student works both shifts of same day)
# Actually we need each (day, shift) slot to have exactly one student - already done by Int assignment

# Constraint: On two consecutive days, Louise (4) works the second shift
# Louise works second shift on exactly two consecutive days
# Find which consecutive pair
louise_second = [Bool(f"louise_second_{d}") for d in range(days)]
for d in range(days):
    solver.add(louise_second[d] == (schedule[d][1] == 4))

# Exactly two consecutive days where Louise works second shift
# Possible consecutive pairs: (0,1), (1,2), (2,3), (3,4)
consecutive_pairs = [(0,1), (1,2), (2,3), (3,4)]
pair_active = [Bool(f"pair_{i}") for i in range(4)]

for i, (d1, d2) in enumerate(consecutive_pairs):
    solver.add(pair_active[i] == And(louise_second[d1], louise_second[d2]))

# Exactly one pair is active
solver.add(Sum([If(pair_active[i], 1, 0) for i in range(4)]) == 1)

# Constraint: On two nonconsecutive days, Grecia (0) works the first shift
# Grecia works first shift on exactly two nonconsecutive days
grecia_first = [Bool(f"grecia_first_{d}") for d in range(days)]
for d in range(days):
    solver.add(grecia_first[d] == (schedule[d][0] == 0))

# Exactly two days where Grecia works first shift, and they are nonconsecutive
solver.add(Sum([If(grecia_first[d], 1, 0) for d in range(days)]) == 2)

# Nonconsecutive: no two selected days are adjacent
for d in range(days - 1):
    solver.add(Not(And(grecia_first[d], grecia_first[d+1])))

# Constraint: Katya (3) works on Tuesday (1) and Friday (4)
# Katya works at least one shift on Tuesday and at least one shift on Friday
solver.add(Or(schedule[1][0] == 3, schedule[1][1] == 3))
solver.add(Or(schedule[4][0] == 3, schedule[4][1] == 3))

# Constraint: Hakeem (1) and Joe (2) work on the same day at least once
solver.add(Or([And(Or(schedule[d][0] == 1, schedule[d][1] == 1),
                   Or(schedule[d][0] == 2, schedule[d][1] == 2)) for d in range(days)]))

# Constraint: Grecia (0) and Louise (4) never work on the same day
for d in range(days):
    solver.add(Not(And(Or(schedule[d][0] == 0, schedule[d][1] == 0),
                       Or(schedule[d][0] == 4, schedule[d][1] == 4))))

# Additional constraint: Katya works second shift on Tuesday
solver.add(schedule[1][1] == 3)

# Now evaluate each option
# (A) Grecia works the first shift on Monday
opt_a = (schedule[0][0] == 0)

# (B) Hakeem works the first shift on Monday
opt_b = (schedule[0][0] == 1)

# (C) Hakeem works the second shift on Wednesday
opt_c = (schedule[2][1] == 1)

# (D) Joe works the second shift on Thursday
opt_d = (schedule[3][1] == 2)

# (E) Louise works the second shift on Monday
opt_e = (schedule[0][1] == 4)

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