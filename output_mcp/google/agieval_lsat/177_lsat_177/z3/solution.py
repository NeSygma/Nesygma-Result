from z3 import *

# Students: 0:Grecia, 1:Hakeem, 2:Joe, 3:Katya, 4:Louise
G, H, J, K, L = 0, 1, 2, 3, 4
students = [G, H, J, K, L]

# Days: 0:Mon, 1:Tue, 2:Wed, 3:Thu, 4:Fri
# Shifts: 0:First, 1:Second
# work[day][shift] = student
work = [[Int(f'work_{d}_{s}') for s in range(2)] for d in range(5)]

solver = Solver()

# Each shift is worked by exactly one student
for d in range(5):
    for s in range(2):
        solver.add(work[d][s] >= 0, work[d][s] <= 4)

# Each student works exactly two shifts
for s_idx in students:
    solver.add(Sum([If(work[d][s] == s_idx, 1, 0) for d in range(5) for s in range(2)]) == 2)

# No student works both shifts of any day
for d in range(5):
    solver.add(work[d][0] != work[d][1])

# On two consecutive days, Louise works the second shift
solver.add(Or([And(work[d][1] == L, work[d+1][1] == L) for d in range(4)]))

# On two nonconsecutive days, Grecia works the first shift
solver.add(Or([And(work[d1][0] == G, work[d2][0] == G, abs(d1 - d2) > 1) for d1 in range(5) for d2 in range(d1+1, 5)]))

# Katya works on Tuesday and Friday
# She works exactly 2 shifts, so she must work one shift on Tuesday and one on Friday
solver.add(Or(work[1][0] == K, work[1][1] == K))
solver.add(Or(work[4][0] == K, work[4][1] == K))

# Helper: student works on day d
def works_on_day(student, d):
    return Or(work[d][0] == student, work[d][1] == student)

# Hakeem and Joe work on the same day as each other at least once
solver.add(Or([And(works_on_day(H, d), works_on_day(J, d)) for d in range(5)]))

# Grecia and Louise never work on the same day as each other
for d in range(5):
    solver.add(Not(And(works_on_day(G, d), works_on_day(L, d))))

# Condition: Hakeem works on Wednesday
solver.add(works_on_day(H, 2))

# Joe works on which pair of days?
# Joe works exactly 2 shifts, and since he can't work both shifts on the same day,
# he works on exactly two distinct days.
# Let Joe_days be the set of days Joe works.
joe_days = [Bool(f'joe_day_{d}') for d in range(5)]
for d in range(5):
    solver.add(joe_days[d] == works_on_day(J, d))

# The question asks for a pair of days {d1, d2} such that Joe works on those days.
# Since Joe works exactly 2 shifts on 2 different days, he works on exactly 2 days.
# Let's check which pair of days {d1, d2} is forced.
# Days: 0:Mon, 1:Tue, 2:Wed, 3:Thu, 4:Fri
# Pairs:
# A: Mon(0) and Wed(2)
# B: Mon(0) and Thu(3)
# C: Tue(1) and Wed(2)
# D: Tue(1) and Thu(3)
# E: Wed(2) and Thu(3)

def get_joe_days_constraint(d1, d2):
    return And(joe_days[d1], joe_days[d2], Sum([If(joe_days[d], 1, 0) for d in range(5)]) == 2)

options = [
    ("A", get_joe_days_constraint(0, 2)),
    ("B", get_joe_days_constraint(0, 3)),
    ("C", get_joe_days_constraint(1, 2)),
    ("D", get_joe_days_constraint(1, 3)),
    ("E", get_joe_days_constraint(2, 3))
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