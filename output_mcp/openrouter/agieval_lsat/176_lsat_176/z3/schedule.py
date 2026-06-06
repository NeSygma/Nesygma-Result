from z3 import *

# Students indices
GRE = 0
HAK = 1
JOE = 2
KAT = 3
LOU = 4
students = [GRE, HAK, JOE, KAT, LOU]

# Days 0..4 (Mon..Fri), shifts 0(first),1(second)
shifts = [[Int(f's_{d}_{s}') for s in range(2)] for d in range(5)]
solver = Solver()

# Domain constraints: each shift assigned a student 0..4
for d in range(5):
    for s in range(2):
        solver.add(And(shifts[d][s] >= 0, shifts[d][s] <= 4))

# No student works both shifts of any day
for d in range(5):
    solver.add(shifts[d][0] != shifts[d][1])

# Each student works exactly two shifts total
for stu in students:
    cnt = Sum([If(shifts[d][s] == stu, 1, 0) for d in range(5) for s in range(2)])
    solver.add(cnt == 2)

# Louise works second shift on two consecutive days, and only those two shifts
# Ensure Louise never appears in first shift
for d in range(5):
    solver.add(shifts[d][0] != LOU)
# Count of Louise in second shift is 2
cnt_lou_sec = Sum([If(shifts[d][1] == LOU, 1, 0) for d in range(5)])
solver.add(cnt_lou_sec == 2)
# Consecutive days condition: there exists d such that both d and d+1 have Louise in second shift
consec = []
for d in range(4):
    consec.append(And(shifts[d][1] == LOU, shifts[d+1][1] == LOU))
solver.add(Or(consec))
# Also ensure no other day has Louise in second shift (already count=2 ensures that)

# Grecia works first shift on two nonconsecutive days, and only those two shifts
# Ensure Grecia never appears in second shift
for d in range(5):
    solver.add(shifts[d][1] != GRE)
cnt_gre_first = Sum([If(shifts[d][0] == GRE, 1, 0) for d in range(5)])
solver.add(cnt_gre_first == 2)
# Nonconsecutive: the two days where Grecia appears first are not consecutive
# Let day variables for Grecia first shift
gre_days = [If(shifts[d][0] == GRE, 1, 0) for d in range(5)]
# We need to enforce that there is no pair of consecutive days both with Grecia first.
for d in range(4):
    solver.add(Not(And(shifts[d][0] == GRE, shifts[d+1][0] == GRE)))

# Katya works on Tuesday (day1) and Friday (day4) exactly (one shift each)
# Ensure Katya appears exactly twice (already from count), and those days are 1 and 4.
# Enforce Katya appears on day1 and day4 (at least one shift each)
solver.add(Or(shifts[1][0] == KAT, shifts[1][1] == KAT))
solver.add(Or(shifts[4][0] == KAT, shifts[4][1] == KAT))
# Ensure Katya does NOT appear on other days
for d in [0,2,3]:
    solver.add(shifts[d][0] != KAT, shifts[d][1] != KAT)

# Hakeem and Joe work on the same day at least once (one shift each on same day)
same_day = []
for d in range(5):
    same_day.append(Or(And(shifts[d][0] == HAK, shifts[d][1] == JOE), And(shifts[d][0] == JOE, shifts[d][1] == HAK)))
solver.add(Or(same_day))

# Grecia and Louise never work on the same day
for d in range(5):
    # not both present in any order
    solver.add(Not(And(Or(shifts[d][0] == GRE, shifts[d][1] == GRE), Or(shifts[d][0] == LOU, shifts[d][1] == LOU)))

# Define option constraints
opt_a = And(shifts[1][0] != GRE, shifts[1][1] != GRE)  # Grecia not on Tuesday
opt_b = And(shifts[2][0] != HAK, shifts[2][1] != HAK)  # Hakeem not on Wednesday
opt_c = And(shifts[1][0] != JOE, shifts[1][1] != JOE)  # Joe not on Tuesday
opt_d = And(shifts[3][0] != JOE, shifts[3][1] != JOE)  # Joe not on Thursday
opt_e = And(shifts[1][0] != LOU, shifts[1][1] != LOU)  # Louise not on Tuesday

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