from z3 import *

# Define constants for students
GRE = 0
HAK = 1
JOE = 2
KAT = 3
LOU = 4
students = [GRE, HAK, JOE, KAT, LOU]

# Days 0..4 (Mon..Fri), shifts 0:first,1:second
shifts = [[Int(f'shift_{d}_{s}') for s in range(2)] for d in range(5)]
solver = Solver()

# Domain constraints
for d in range(5):
    for s in range(2):
        solver.add(And(shifts[d][s] >= 0, shifts[d][s] <= 4))
    # No student works both shifts of same day
    solver.add(shifts[d][0] != shifts[d][1])

# Each student works exactly two shifts total
for stu in students:
    cnt = Sum([If(shifts[d][s] == stu, 1, 0) for d in range(5) for s in range(2)])
    solver.add(cnt == 2)

# Katya works Tuesday second shift and works on Friday (some shift)
solver.add(shifts[1][1] == KAT)  # Tuesday second
# Friday (day 4) at least one shift is Katya
solver.add(Or(shifts[4][0] == KAT, shifts[4][1] == KAT))

# Louise works second shift on two consecutive days, only second shifts, exactly two occurrences
louise_second = [Bool(f'louise_second_{d}') for d in range(5)]
for d in range(5):
    solver.add(louise_second[d] == (shifts[d][1] == LOU))
    # Louise never works first shift
    solver.add(shifts[d][0] != LOU)
# Exactly two second shifts for Louise
solver.add(Sum([If(louise_second[d], 1, 0) for d in range(5)]) == 2)
# They must be consecutive
consec_pairs = []
for d in range(4):
    consec_pairs.append(And(louise_second[d], louise_second[d+1]))
solver.add(Or(consec_pairs))

# Grecia works first shift on two nonconsecutive days, never second shift
grecia_first = [Bool(f'grecia_first_{d}') for d in range(5)]
for d in range(5):
    solver.add(grecia_first[d] == (shifts[d][0] == GRE))
    # Grecia never second shift
    solver.add(shifts[d][1] != GRE)
# Exactly two first shifts for Grecia
solver.add(Sum([If(grecia_first[d], 1, 0) for d in range(5)]) == 2)
# Nonconsecutive: no adjacent true
for d in range(4):
    solver.add(Not(And(grecia_first[d], grecia_first[d+1])))

# Hakeem and Joe work on the same day at least once (different shifts)
same_day_hj = []
for d in range(5):
    same_day_hj.append(Or(And(shifts[d][0] == HAK, shifts[d][1] == JOE),
                         And(shifts[d][0] == JOE, shifts[d][1] == HAK)))
solver.add(Or(same_day_hj))

# Grecia and Louise never work on same day
for d in range(5):
    # If Grecia appears (first shift) then Louise cannot appear either shift, and vice versa
    solver.add(Not(Or(shifts[d][0] == GRE, shifts[d][1] == GRE) & Or(shifts[d][0] == LOU, shifts[d][1] == LOU)))

# Prepare option constraints
option_constraints = []
# A: Grecia first shift Monday (day 0)
opt_a = shifts[0][0] == GRE
option_constraints.append(("A", opt_a))
# B: Hakeem first shift Monday
opt_b = shifts[0][0] == HAK
option_constraints.append(("B", opt_b))
# C: Hakeem second shift Wednesday (day 2)
opt_c = shifts[2][1] == HAK
option_constraints.append(("C", opt_c))
# D: Joe second shift Thursday (day 3)
opt_d = shifts[3][1] == JOE
option_constraints.append(("D", opt_d))
# E: Louise second shift Monday
opt_e = shifts[0][1] == LOU
option_constraints.append(("E", opt_e))

found_options = []
for letter, constr in option_constraints:
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