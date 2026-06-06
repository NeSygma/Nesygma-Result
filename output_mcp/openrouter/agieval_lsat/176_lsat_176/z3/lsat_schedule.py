from z3 import *

# Students indices
GRE = 0
HAK = 1
JOE = 2
KAT = 3
LOU = 4
students = [GRE, HAK, JOE, KAT, LOU]

# Days 0..4 (Mon..Fri), shifts 0 first,1 second
shifts = [[Int(f's_{d}_{s}') for s in range(2)] for d in range(5)]
solver = Solver()

# Domain constraints: each shift assigned a student 0-4
for d in range(5):
    for s in range(2):
        solver.add(And(shifts[d][s] >= 0, shifts[d][s] <= 4))

# No student works both shifts of any day
for d in range(5):
    solver.add(shifts[d][0] != shifts[d][1])

# Each student works exactly two shifts total
for stu in students:
    count = Sum([If(shifts[d][s] == stu, 1, 0) for d in range(5) for s in range(2)])
    solver.add(count == 2)

# Louise works second shift on two consecutive days, and only those two shifts
lou_consec = []
for d in range(4):
    cond = And(shifts[d][1] == LOU, shifts[d+1][1] == LOU)
    others = []
    for dd in range(5):
        for ss in range(2):
            if not (dd == d and ss == 1) and not (dd == d+1 and ss == 1):
                others.append(shifts[dd][ss] != LOU)
    lou_consec.append(And(cond, *others))
solver.add(Or(*lou_consec))

# Grecia works first shift on two nonconsecutive days, exactly two first shifts, not consecutive.
gre_choices = []
for i in range(5):
    for j in range(i+1,5):
        if j == i+1:
            continue  # consecutive not allowed
        cond = And(shifts[i][0] == GRE, shifts[j][0] == GRE)
        others = []
        for dd in range(5):
            for ss in range(2):
                if not (dd == i and ss == 0) and not (dd == j and ss == 0):
                    others.append(shifts[dd][ss] != GRE)
        gre_choices.append(And(cond, *others))
solver.add(Or(*gre_choices))

# Katya works on Tuesday (day1) and Friday (day4), exactly one shift each day.
kat_constraints = []
for ss1 in range(2):
    for ss2 in range(2):
        cond = And(shifts[1][ss1] == KAT, shifts[4][ss2] == KAT)
        others = []
        for dd in range(5):
            for ss in range(2):
                if not (dd == 1 and ss == ss1) and not (dd == 4 and ss == ss2):
                    others.append(shifts[dd][ss] != KAT)
        kat_constraints.append(And(cond, *others))
solver.add(Or(*kat_constraints))

# Hakeem and Joe work on the same day at least once (one shift each on same day)
same_day_hj = []
for d in range(5):
    cond = Or(And(shifts[d][0] == HAK, shifts[d][1] == JOE),
              And(shifts[d][0] == JOE, shifts[d][1] == HAK))
    same_day_hj.append(cond)
solver.add(Or(*same_day_hj))

# Grecia and Louise never work on the same day
for d in range(5):
    gre_present = Or(shifts[d][0] == GRE, shifts[d][1] == GRE)
    lou_present = Or(shifts[d][0] == LOU, shifts[d][1] == LOU)
    solver.add(Not(And(gre_present, lou_present)))

# Option constraints definitions
# A: Grecia does not work on Tuesday (day1)
opt_a = And(shifts[1][0] != GRE, shifts[1][1] != GRE)
# B: Hakeem does not work on Wednesday (day2)
opt_b = And(shifts[2][0] != HAK, shifts[2][1] != HAK)
# C: Joe does not work on Tuesday
opt_c = And(shifts[1][0] != JOE, shifts[1][1] != JOE)
# D: Joe does not work on Thursday (day3)
opt_d = And(shifts[3][0] != JOE, shifts[3][1] != JOE)
# E: Louise does not work on Tuesday
opt_e = And(shifts[1][0] != LOU, shifts[1][1] != LOU)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

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