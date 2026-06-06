from z3 import *

# Students: 0:G, 1:H, 2:J, 3:K, 4:L
G, H, J, K, L = 0, 1, 2, 3, 4
students = [G, H, J, K, L]

# Days: 0:Mon, 1:Tue, 2:Wed, 3:Thu, 4:Fri
days = range(5)
shifts = range(2)

solver = Solver()

# W[d][s] is the student working on day d, shift s
W = [[Int(f"W_{d}_{s}") for s in shifts] for d in days]

# Each shift is worked by exactly one student
for d in days:
    for s in shifts:
        solver.add(W[d][s] >= 0, W[d][s] <= 4)

# Each student works exactly two shifts
for p in students:
    solver.add(Sum([If(W[d][s] == p, 1, 0) for d in days for s in shifts]) == 2)

# No student works both shifts of any day
for d in days:
    solver.add(W[d][0] != W[d][1])

# On two consecutive days, Louise works the second shift
# L works shift 1 on two consecutive days
# L works shift 1 on day d and day d+1.
# L works no other shifts (since L works exactly 2 shifts total)
solver.add(Or([And(W[d][1] == L, W[d+1][1] == L) for d in range(4)]))
solver.add(Sum([If(W[d][0] == L, 1, 0) for d in days]) == 0)

# On two nonconsecutive days, Grecia works the first shift
# G works shift 0 on two days d1, d2 such that |d1 - d2| > 1
# G works no other shifts (since G works exactly 2 shifts total)
# Use Or-loop to represent G working shift 0 on two nonconsecutive days
g_shift0_days = [Bool(f"g_shift0_{d}") for d in days]
for d in days:
    solver.add(g_shift0_days[d] == (W[d][0] == G))
solver.add(Sum([If(g_shift0_days[d], 1, 0) for d in days]) == 2)
solver.add(Or([And(g_shift0_days[d1], g_shift0_days[d2]) for d1 in range(5) for d2 in range(d1 + 2, 5)]))
solver.add(Sum([If(W[d][1] == G, 1, 0) for d in days]) == 0)

# Katya works on Tuesday (day 1) and Friday (day 4)
# K works exactly 2 shifts.
# K works one shift on day 1 and one shift on day 4.
solver.add(Or(W[1][0] == K, W[1][1] == K))
solver.add(Or(W[4][0] == K, W[4][1] == K))
solver.add(Sum([If(W[d][s] == K, 1, 0) for d in days for s in shifts]) == 2)

# Hakeem and Joe work on the same day as each other at least once
solver.add(Or([And(W[d][0] == H, W[d][1] == J) for d in days] + [And(W[d][0] == J, W[d][1] == H) for d in days]))

# Grecia and Louise never work on the same day as each other
for d in days:
    is_G_on_day = Or(W[d][0] == G, W[d][1] == G)
    is_L_on_day = Or(W[d][0] == L, W[d][1] == L)
    solver.add(Not(And(is_G_on_day, is_L_on_day)))

# Answer Choices
# (A) Grecia does not work at the gallery on Tuesday (day 1)
# (B) Hakeem does not work at the gallery on Wednesday (day 2)
# (C) Joe does not work at the gallery on Tuesday (day 1)
# (D) Joe does not work at the gallery on Thursday (day 3)
# (E) Louise does not work at the gallery on Tuesday (day 1)

options = [
    ("A", Not(Or(W[1][0] == G, W[1][1] == G))),
    ("B", Not(Or(W[2][0] == H, W[2][1] == H))),
    ("C", Not(Or(W[1][0] == J, W[1][1] == J))),
    ("D", Not(Or(W[3][0] == J, W[3][1] == J))),
    ("E", Not(Or(W[1][0] == L, W[1][1] == L)))
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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