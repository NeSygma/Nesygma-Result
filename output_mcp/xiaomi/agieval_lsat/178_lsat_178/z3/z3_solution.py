from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Shifts: 1=first, 2=second
# Students: G=0, H=1, J=2, K=3, L=4

N_DAYS = 5
N_STUDENTS = 5

# shift[d][s] = student working day d, shift s (0-indexed)
shift = [[Int(f"shift_{d}_{s}") for s in range(2)] for d in range(N_DAYS)]

solver = Solver()

# Each shift is assigned exactly one student (0-4)
for d in range(N_DAYS):
    for s in range(2):
        solver.add(shift[d][s] >= 0, shift[d][s] < N_STUDENTS)

# No student works both shifts of any day
for d in range(N_DAYS):
    solver.add(shift[d][0] != shift[d][1])

# Each student works exactly two shifts total
for student in range(N_STUDENTS):
    solver.add(Sum([If(shift[d][s] == student, 1, 0) for d in range(N_DAYS) for s in range(2)]) == 2)

# On two consecutive days, Louise (4) works the second shift
# Possible pairs: (Mon,Tue), (Tue,Wed), (Wed,Thu), (Thu,Fri)
solver.add(Or(
    And(shift[0][1] == 4, shift[1][1] == 4),
    And(shift[1][1] == 4, shift[2][1] == 4),
    And(shift[2][1] == 4, shift[3][1] == 4),
    And(shift[3][1] == 4, shift[4][1] == 4)
))

# On two nonconsecutive days, Grecia (0) works the first shift
# Possible nonconsecutive pairs from {Mon,Tue,Wed,Thu,Fri}:
# (Mon,Wed), (Mon,Thu), (Mon,Fri), (Tue,Thu), (Tue,Fri), (Wed,Fri)
solver.add(Or(
    And(shift[0][0] == 0, shift[2][0] == 0),
    And(shift[0][0] == 0, shift[3][0] == 0),
    And(shift[0][0] == 0, shift[4][0] == 0),
    And(shift[1][0] == 0, shift[3][0] == 0),
    And(shift[1][0] == 0, shift[4][0] == 0),
    And(shift[2][0] == 0, shift[4][0] == 0)
))

# Katya (3) works on Tuesday (1) and Friday (4)
# Katya works at least one shift on Tuesday and at least one shift on Friday
solver.add(Or(shift[1][0] == 3, shift[1][1] == 3))
solver.add(Or(shift[4][0] == 3, shift[4][1] == 3))

# Hakeem (1) and Joe (2) work on the same day at least once
solver.add(Or([And(
    Or(shift[d][0] == 1, shift[d][1] == 1),
    Or(shift[d][0] == 2, shift[d][1] == 2)
) for d in range(N_DAYS)]))

# Grecia (0) and Louise (4) never work on the same day
for d in range(N_DAYS):
    solver.add(Not(And(
        Or(shift[d][0] == 0, shift[d][1] == 0),
        Or(shift[d][0] == 4, shift[d][1] == 4)
    )))

# Additional constraint: There is at least one day where Grecia and Joe both work
solver.add(Or([And(
    Or(shift[d][0] == 0, shift[d][1] == 0),
    Or(shift[d][0] == 2, shift[d][1] == 2)
) for d in range(N_DAYS)]))

# Now test each answer option
# (A) Grecia works the first shift on Tuesday
opt_a = (shift[1][0] == 0)

# (B) Hakeem works the second shift on Monday
opt_b = (shift[0][1] == 1)

# (C) Hakeem works the second shift on Wednesday
opt_c = (shift[2][1] == 1)

# (D) Joe works the first shift on Wednesday
opt_d = (shift[2][0] == 2)

# (E) Joe works the first shift on Thursday
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