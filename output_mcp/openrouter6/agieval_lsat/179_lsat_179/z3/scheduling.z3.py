from z3 import *

# Student IDs
GRECIA = 0
HAKEEM = 1
JOE = 2
KATYA = 3
LOUISE = 4

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Shifts: 0=first, 1=second

# Create assignment variables
assign = [[Int(f"assign_{d}_{s}") for s in range(2)] for d in range(5)]

solver = Solver()

# Domain constraints for all assignments
for d in range(5):
    for s in range(2):
        solver.add(assign[d][s] >= 0)
        solver.add(assign[d][s] <= 4)

# 1. Each student works exactly 2 shifts
for student in [GRECIA, HAKEEM, JOE, KATYA, LOUISE]:
    solver.add(Sum([If(assign[d][s] == student, 1, 0) for d in range(5) for s in range(2)]) == 2)

# 2. No student works both shifts on the same day
for d in range(5):
    solver.add(assign[d][0] != assign[d][1])

# 3. Louise works second shift on two consecutive days (and only those two shifts)
# Louise cannot work first shift
for d in range(5):
    solver.add(assign[d][0] != LOUISE)
# Exactly two days with Louise on second shift
solver.add(Sum([If(assign[d][1] == LOUISE, 1, 0) for d in range(5)]) == 2)
# They must be consecutive
solver.add(Or([And(assign[i][1] == LOUISE, assign[i+1][1] == LOUISE) for i in range(4)]))

# 4. Grecia works first shift on two nonconsecutive days (and only those two shifts)
# Grecia cannot work second shift
for d in range(5):
    solver.add(assign[d][1] != GRECIA)
# Exactly two days with Grecia on first shift
solver.add(Sum([If(assign[d][0] == GRECIA, 1, 0) for d in range(5)]) == 2)
# No two consecutive days with Grecia on first shift
for i in range(4):
    solver.add(Not(And(assign[i][0] == GRECIA, assign[i+1][0] == GRECIA)))

# 5. Katya works on Tuesday and Friday, with second shift on Tuesday
solver.add(assign[1][1] == KATYA)  # Tuesday second shift
# Katya works exactly one shift on Friday (since total is 2 and Tuesday uses one)
solver.add(Or(assign[4][0] == KATYA, assign[4][1] == KATYA))

# 6. Hakeem and Joe work on the same day at least once
solver.add(Or([
    Or(
        And(assign[d][0] == HAKEEM, assign[d][1] == JOE),
        And(assign[d][0] == JOE, assign[d][1] == HAKEEM)
    )
    for d in range(5)
]))

# 7. Grecia and Louise never work on the same day
for d in range(5):
    solver.add(Not(Or(
        And(assign[d][0] == GRECIA, assign[d][1] == LOUISE),
        And(assign[d][0] == LOUISE, assign[d][1] == GRECIA)
    )))

# Answer choices as constraints
opt_a_constr = assign[0][0] == GRECIA  # Grecia works first shift on Monday
opt_b_constr = assign[0][0] == HAKEEM  # Hakeem works first shift on Monday
opt_c_constr = assign[2][1] == HAKEEM  # Hakeem works second shift on Wednesday
opt_d_constr = assign[3][1] == JOE     # Joe works second shift on Thursday
opt_e_constr = assign[0][1] == LOUISE  # Louise works second shift on Monday

# Evaluate each option using the required skeleton
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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