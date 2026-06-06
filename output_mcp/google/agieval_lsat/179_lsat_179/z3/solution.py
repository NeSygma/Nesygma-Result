from z3 import *

solver = Solver()

# Students: 0:G, 1:H, 2:J, 3:K, 4:L
G, H, J, K, L = 0, 1, 2, 3, 4
students = [G, H, J, K, L]

# shift[day][shift_idx]
shift = [[Int(f"shift_{d}_{s}") for s in range(2)] for d in range(5)]

# Each shift is worked by exactly one student
for d in range(5):
    for s in range(2):
        solver.add(shift[d][s] >= 0, shift[d][s] <= 4)

# Each student works exactly two shifts
for s_id in students:
    solver.add(Sum([If(shift[d][s] == s_id, 1, 0) for d in range(5) for s in range(2)]) == 2)

# No student works both shifts of any day
for d in range(5):
    solver.add(shift[d][0] != shift[d][1])

# Louise (L) works the 2nd shift on two consecutive days
l_2nd_days = [If(shift[d][1] == L, 1, 0) for d in range(5)]
solver.add(Sum(l_2nd_days) == 2)
# Consecutive: (d=0,1), (1,2), (2,3), (3,4)
solver.add(Or(
    And(shift[0][1] == L, shift[1][1] == L),
    And(shift[1][1] == L, shift[2][1] == L),
    And(shift[2][1] == L, shift[3][1] == L),
    And(shift[3][1] == L, shift[4][1] == L)
))

# Grecia (G) works the 1st shift on two nonconsecutive days
g_1st_days = [If(shift[d][0] == G, 1, 0) for d in range(5)]
solver.add(Sum(g_1st_days) == 2)
# Nonconsecutive: (0,2), (0,3), (0,4), (1,3), (1,4), (2,4)
solver.add(Or(
    And(shift[0][0] == G, shift[2][0] == G),
    And(shift[0][0] == G, shift[3][0] == G),
    And(shift[0][0] == G, shift[4][0] == G),
    And(shift[1][0] == G, shift[3][0] == G),
    And(shift[1][0] == G, shift[4][0] == G),
    And(shift[2][0] == G, shift[4][0] == G)
))

# Katya (K) works on Tuesday (day 1) and Friday (day 4)
# K works exactly 2 shifts, so these must be the only days K works
for d in range(5):
    if d != 1 and d != 4:
        solver.add(shift[d][0] != K, shift[d][1] != K)
# K works on day 1 and day 4
solver.add(Or(shift[1][0] == K, shift[1][1] == K))
solver.add(Or(shift[4][0] == K, shift[4][1] == K))

# Hakeem (H) and Joe (J) work on the same day at least once
solver.add(Or([
    Or(And(shift[d][0] == H, shift[d][1] == J), And(shift[d][0] == J, shift[d][1] == H))
    for d in range(5)
]))

# Grecia (G) and Louise (L) never work on the same day
for d in range(5):
    solver.add(Not(And(
        Or(shift[d][0] == G, shift[d][1] == G),
        Or(shift[d][0] == L, shift[d][1] == L)
    )))

# Condition: Katya (K) works the 2nd shift on Tuesday (day 1)
solver.add(shift[1][1] == K)

# Options
opt_a_constr = (shift[0][0] == G)
opt_b_constr = (shift[0][0] == H)
opt_c_constr = (shift[2][1] == H)
opt_d_constr = (shift[3][1] == J)
opt_e_constr = (shift[0][1] == L)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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