from z3 import *

# Define students
Grecia, Hakeem, Joe, Katya, Louise = 0, 1, 2, 3, 4
students = [Grecia, Hakeem, Joe, Katya, Louise]
student_names = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Shifts: 0=first, 1=second
shifts = ["first", "second"]

# Create a 5x2 array of integer variables for assignments
assign = [[Int(f"assign_{d}_{s}") for s in range(2)] for d in range(5)]

solver = Solver()

# Each shift must be assigned to a student (0-4)
for d in range(5):
    for s in range(2):
        solver.add(assign[d][s] >= 0)
        solver.add(assign[d][s] <= 4)

# Each student works exactly two shifts
for stu in students:
    solver.add(Sum([If(assign[d][s] == stu, 1, 0) for d in range(5) for s in range(2)]) == 2)

# No student works both shifts of any day
for d in range(5):
    solver.add(assign[d][0] != assign[d][1])

# Louise works second shift on two consecutive days (and only those two shifts)
louise_consecutive = False
for d in range(4):  # consecutive pairs: (0,1), (1,2), (2,3), (3,4)
    # Louise works second on both days
    solver.add(Or(
        And(assign[d][1] == Louise, assign[d+1][1] == Louise),
        # We'll ensure she works only these two shifts by counting later
    ))
# Actually, we need to enforce that Louise works exactly two shifts, both second, on consecutive days.
# We'll do this by adding constraints that she works second on exactly two consecutive days.
# We'll use a helper: for each possible consecutive pair, we can choose one.
# But to simplify, we'll add constraints that she works second on exactly two days that are consecutive.
# We'll use a boolean for each day indicating if she works second.
louise_second = [Bool(f"louise_second_{d}") for d in range(5)]
for d in range(5):
    solver.add(louise_second[d] == (assign[d][1] == Louise))
# She must work exactly two second shifts
solver.add(Sum([If(louise_second[d], 1, 0) for d in range(5)]) == 2)
# They must be consecutive
solver.add(Or(
    And(louise_second[0], louise_second[1]),
    And(louise_second[1], louise_second[2]),
    And(louise_second[2], louise_second[3]),
    And(louise_second[3], louise_second[4])
))
# She cannot work any first shift
for d in range(5):
    solver.add(assign[d][0] != Louise)

# Grecia works first shift on two nonconsecutive days (and only those two shifts)
grecia_first = [Bool(f"grecia_first_{d}") for d in range(5)]
for d in range(5):
    solver.add(grecia_first[d] == (assign[d][0] == Grecia))
# She must work exactly two first shifts
solver.add(Sum([If(grecia_first[d], 1, 0) for d in range(5)]) == 2)
# They must be nonconsecutive
solver.add(Or(
    And(grecia_first[0], grecia_first[2]),
    And(grecia_first[0], grecia_first[3]),
    And(grecia_first[0], grecia_first[4]),
    And(grecia_first[1], grecia_first[3]),
    And(grecia_first[1], grecia_first[4]),
    And(grecia_first[2], grecia_first[4])
))
# She cannot work any second shift
for d in range(5):
    solver.add(assign[d][1] != Grecia)

# Katya works on Tuesday and Friday (exactly one shift each day)
# Tuesday is day 1, Friday is day 4
solver.add(Or(assign[1][0] == Katya, assign[1][1] == Katya))
solver.add(Or(assign[4][0] == Katya, assign[4][1] == Katya))
# Since she works exactly two shifts, she works exactly one on each of these days
solver.add(Sum([If(assign[1][s] == Katya, 1, 0) for s in range(2)]) == 1)
solver.add(Sum([If(assign[4][s] == Katya, 1, 0) for s in range(2)]) == 1)

# Hakeem and Joe work on the same day at least once
same_day = Bool("same_day")
solver.add(Or([
    And(assign[d][0] == Hakeem, assign[d][1] == Joe) for d in range(5)
] + [
    And(assign[d][0] == Joe, assign[d][1] == Hakeem) for d in range(5)
]))

# Grecia and Louise never work on the same day
for d in range(5):
    solver.add(Not(And(assign[d][0] == Grecia, assign[d][1] == Louise)))
    solver.add(Not(And(assign[d][0] == Louise, assign[d][1] == Grecia)))
    # Also, they cannot both work on the same day in any shift combination
    solver.add(Or(
        assign[d][0] != Grecia,
        assign[d][1] != Louise
    ))
    solver.add(Or(
        assign[d][0] != Louise,
        assign[d][1] != Grecia
    ))

# Now, evaluate each answer choice by checking if its negation is unsatisfiable
# We'll use the skeleton but with a twist: we'll check for unsat of the negation
found_options = []

# Option A: Grecia does not work on Tuesday
# Negation: Grecia works on Tuesday (i.e., on Tuesday, she works either first or second)
opt_a_neg = Or(assign[1][0] == Grecia, assign[1][1] == Grecia)
solver.push()
solver.add(opt_a_neg)
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: Hakeem does not work on Wednesday
# Negation: Hakeem works on Wednesday
opt_b_neg = Or(assign[2][0] == Hakeem, assign[2][1] == Hakeem)
solver.push()
solver.add(opt_b_neg)
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: Joe does not work on Tuesday
# Negation: Joe works on Tuesday
opt_c_neg = Or(assign[1][0] == Joe, assign[1][1] == Joe)
solver.push()
solver.add(opt_c_neg)
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: Joe does not work on Thursday
# Negation: Joe works on Thursday
opt_d_neg = Or(assign[3][0] == Joe, assign[3][1] == Joe)
solver.push()
solver.add(opt_d_neg)
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: Louise does not work on Tuesday
# Negation: Louise works on Tuesday
opt_e_neg = Or(assign[1][0] == Louise, assign[1][1] == Louise)
solver.push()
solver.add(opt_e_neg)
if solver.check() == unsat:
    found_options.append("E")
solver.pop()

# Now, based on found_options, print the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")