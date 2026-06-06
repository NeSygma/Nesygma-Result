from z3 import *

solver = Solver()

# Students: 0:G, 1:H, 2:J, 3:K, 4:L
# Days: 0:Mon, 1:Tue, 2:Wed, 3:Thu, 4:Fri
# Shifts: 0:1st, 1:2nd

S = [[Int(f"S_{d}_{s}") for s in range(2)] for d in range(5)]

# Domain constraints
for d in range(5):
    for s in range(2):
        solver.add(S[d][s] >= 0, S[d][s] <= 4)

# Each student works exactly 2 shifts
for student in range(5):
    solver.add(Sum([If(S[d][s] == student, 1, 0) for d in range(5) for s in range(2)]) == 2)

# No student works both shifts of any day
for d in range(5):
    solver.add(S[d][0] != S[d][1])

# Helper: WorksOn(student, day)
def WorksOn(student, day):
    return Or(S[day][0] == student, S[day][1] == student)

# Louise (4) works the 2nd shift on two consecutive days
solver.add(Or(
    And(S[0][1] == 4, S[1][1] == 4),
    And(S[1][1] == 4, S[2][1] == 4),
    And(S[2][1] == 4, S[3][1] == 4),
    And(S[3][1] == 4, S[4][1] == 4)
))

# Grecia (0) works the 1st shift on two nonconsecutive days
# Exactly two 1st shifts for Grecia
solver.add(Sum([If(S[d][0] == 0, 1, 0) for d in range(5)]) == 2)
# Nonconsecutive
g_first_days = [d for d in range(5)]
solver.add(Not(Or(
    And(S[0][0] == 0, S[1][0] == 0),
    And(S[1][0] == 0, S[2][0] == 0),
    And(S[2][0] == 0, S[3][0] == 0),
    And(S[3][0] == 0, S[4][0] == 0)
)))

# Katya (3) works on Tuesday (1) and Friday (4)
solver.add(WorksOn(3, 1))
solver.add(WorksOn(3, 4))

# Hakeem (1) and Joe (2) work on the same day at least once
solver.add(Or([And(WorksOn(1, d), WorksOn(2, d)) for d in range(5)]))

# Grecia (0) and Louise (4) never work on the same day
for d in range(5):
    solver.add(Not(And(WorksOn(0, d), WorksOn(4, d))))

# Condition: At least one day on which Grecia (0) and Joe (2) both work
solver.add(Or([And(WorksOn(0, d), WorksOn(2, d)) for d in range(5)]))

# Answer Choices
opt_a_constr = (S[1][0] == 0)
opt_b_constr = (S[0][1] == 1)
opt_c_constr = (S[2][1] == 1)
opt_d_constr = (S[2][0] == 2)
opt_e_constr = (S[3][0] == 2)

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