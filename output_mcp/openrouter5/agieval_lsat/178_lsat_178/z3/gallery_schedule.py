from z3 import *

# Students: Grecia=0, Hakeem=1, Joe=2, Katya=3, Louise=4
# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
# Shifts: first=0, second=1

# Decision variables: shift[d][s] = student working day d, shift s
# We'll use Int variables with domain 0..4
shift = [[Int(f"shift_{d}_{s}") for s in range(2)] for d in range(5)]

solver = Solver()

# Domain: each shift is worked by exactly one student (0..4)
for d in range(5):
    for s in range(2):
        solver.add(shift[d][s] >= 0, shift[d][s] <= 4)

# Each student works exactly two shifts total
for student in range(5):
    solver.add(Sum([If(shift[d][s] == student, 1, 0) for d in range(5) for s in range(2)]) == 2)

# No student works both shifts of any day
for d in range(5):
    solver.add(shift[d][0] != shift[d][1])

# On two consecutive days, Louise works the second shift.
# Louise = 4, second shift = 1
# Two consecutive days: (Mon,Tue), (Tue,Wed), (Wed,Thu), (Thu,Fri)
consec_pairs = [(0,1), (1,2), (2,3), (3,4)]
solver.add(Or([And(shift[d1][1] == 4, shift[d2][1] == 4) for (d1,d2) in consec_pairs]))

# On two nonconsecutive days, Grecia works the first shift.
# Grecia = 0, first shift = 0
# Nonconsecutive means days that are not adjacent.
# We need exactly two days where Grecia works first shift, and those two days are not consecutive.
# First, count how many days Grecia works first shift:
gracia_first_days = [If(shift[d][0] == 0, 1, 0) for d in range(5)]
solver.add(Sum(gracia_first_days) == 2)

# Now ensure those two days are not consecutive.
# We can encode: for each pair of consecutive days, not both have Grecia first shift.
for (d1, d2) in consec_pairs:
    solver.add(Not(And(shift[d1][0] == 0, shift[d2][0] == 0)))

# Katya works on Tuesday and Friday.
# Katya = 3
# Katya works on Tuesday (day 1) - could be either shift
solver.add(Or(shift[1][0] == 3, shift[1][1] == 3))
# Katya works on Friday (day 4)
solver.add(Or(shift[4][0] == 3, shift[4][1] == 3))

# Hakeem and Joe work on the same day as each other at least once.
# Hakeem = 1, Joe = 2
solver.add(Or([Or(And(shift[d][0] == 1, shift[d][1] == 2), And(shift[d][0] == 2, shift[d][1] == 1)) for d in range(5)]))

# Grecia and Louise never work on the same day as each other.
# Grecia = 0, Louise = 4
for d in range(5):
    solver.add(Not(And(Or(shift[d][0] == 0, shift[d][1] == 0), Or(shift[d][0] == 4, shift[d][1] == 4))))

# Additional condition: There is at least one day on which Grecia and Joe both work.
# Grecia = 0, Joe = 2
solver.add(Or([Or(And(shift[d][0] == 0, shift[d][1] == 2), And(shift[d][0] == 2, shift[d][1] == 0)) for d in range(5)]))

# Now evaluate each option
# Option A: Grecia works the first shift on Tuesday.
# Tuesday = day 1, first shift = 0, Grecia = 0
opt_a = (shift[1][0] == 0)

# Option B: Hakeem works the second shift on Monday.
# Monday = day 0, second shift = 1, Hakeem = 1
opt_b = (shift[0][1] == 1)

# Option C: Hakeem works the second shift on Wednesday.
# Wednesday = day 2, second shift = 1, Hakeem = 1
opt_c = (shift[2][1] == 1)

# Option D: Joe works the first shift on Wednesday.
# Wednesday = day 2, first shift = 0, Joe = 2
opt_d = (shift[2][0] == 2)

# Option E: Joe works the first shift on Thursday.
# Thursday = day 3, first shift = 0, Joe = 2
opt_e = (shift[3][0] == 2)

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