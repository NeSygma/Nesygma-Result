from z3 import *

# Students: 0:G, 1:H, 2:J, 3:K, 4:L
# Days: 0:Mon, 1:Tue, 2:Wed, 3:Thu, 4:Fri
# Shifts: 0:First, 1:Second

solver = Solver()

# Work[day][shift][student]
work = [[[Bool(f"work_{d}_{s}_{st}") for st in range(5)] for s in range(2)] for d in range(5)]

# Each shift is worked by exactly one student
for d in range(5):
    for s in range(2):
        solver.add(Sum([If(work[d][s][st], 1, 0) for st in range(5)]) == 1)

# Each student works exactly two shifts
for st in range(5):
    solver.add(Sum([If(work[d][s][st], 1, 0) for d in range(5) for s in range(2)]) == 2)

# No student works both shifts of any day
for d in range(5):
    for st in range(5):
        solver.add(Sum([If(work[d][s][st], 1, 0) for s in range(2)]) <= 1)

# Louise (L=4) works the second shift on two consecutive days
l_second_consecutive = Or([And(work[d][1][4], work[d+1][1][4]) for d in range(4)])
solver.add(l_second_consecutive)

# Grecia (G=0) works the first shift on two nonconsecutive days
g_first_nonconsecutive = Or([And(work[d1][0][0], work[d2][0][0]) for d1 in range(5) for d2 in range(d1 + 2, 5)])
solver.add(g_first_nonconsecutive)

# Katya (K=3) works on Tuesday (1) and Friday (4)
solver.add(Sum([If(work[1][s][3], 1, 0) for s in range(2)]) == 1)
solver.add(Sum([If(work[4][s][3], 1, 0) for s in range(2)]) == 1)

# Hakeem (H=1) and Joe (J=2) work on the same day at least once
h_works_day = [Or([work[d][s][1] for s in range(2)]) for d in range(5)]
j_works_day = [Or([work[d][s][2] for s in range(2)]) for d in range(5)]
h_j_same_day = Or([And(h_works_day[d], j_works_day[d]) for d in range(5)])
solver.add(h_j_same_day)

# Grecia (G=0) and Louise (L=4) never work on the same day
for d in range(5):
    g_works_day = Or([work[d][s][0] for s in range(2)])
    l_works_day = Or([work[d][s][4] for s in range(2)])
    solver.add(Not(And(g_works_day, l_works_day)))

# Check if the constraints are satisfiable at all
result = solver.check()
print(f"Result: {result}")
if result == sat:
    m = solver.model()
    for d in range(5):
        for s in range(2):
            for st in range(5):
                if m.is_true(work[d][s][st]):
                    print(f"Day {d}, Shift {s}: Student {st}")