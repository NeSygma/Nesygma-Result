from z3 import *

solver = Solver()

# Define student IDs
G, H, J, K, L = 0, 1, 2, 3, 4

# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
# Shifts: 0=first, 1=second
assign = [[Int(f"assign_{d}_{s}") for s in range(2)] for d in range(5)]

# Domain constraints for each assignment
for d in range(5):
    for s in range(2):
        solver.add(assign[d][s] >= 0, assign[d][s] <= 4)

# 1. Each student works exactly two shifts
for student in [G, H, J, K, L]:
    solver.add(Sum([If(assign[d][s] == student, 1, 0) for d in range(5) for s in range(2)]) == 2)

# 2. No student works both shifts of any day
for d in range(5):
    solver.add(assign[d][0] != assign[d][1])

# 3. Louise works second shift on two consecutive days
solver.add(Or([And(assign[d][1] == L, assign[d+1][1] == L) for d in range(4)]))

# 4. Grecia works first shift on two nonconsecutive days
solver.add(Or([And(assign[d1][0] == G, assign[d2][0] == G) for d1 in range(5) for d2 in range(d1+2, 5)]))

# 5. Katya works on Tuesday and Friday
solver.add(Or(assign[1][0] == K, assign[1][1] == K))
solver.add(Or(assign[4][0] == K, assign[4][1] == K))

# 6. Hakeem and Joe work on the same day at least once
solver.add(Or([And(Or(assign[d][0] == H, assign[d][1] == H), Or(assign[d][0] == J, assign[d][1] == J)) for d in range(5)]))

# 7. Grecia and Louise never work on the same day
for d in range(5):
    solver.add(Not(And(Or(assign[d][0] == G, assign[d][1] == G), Or(assign[d][0] == L, assign[d][1] == L))))

# 8. Extra condition: Hakeem works on Wednesday
solver.add(Or(assign[2][0] == H, assign[2][1] == H))

# Now evaluate multiple choice options
found_options = []

# Option A: Monday and Wednesday
opt_a = And(Or(assign[0][0] == J, assign[0][1] == J), Or(assign[2][0] == J, assign[2][1] == J))
# Option B: Monday and Thursday
opt_b = And(Or(assign[0][0] == J, assign[0][1] == J), Or(assign[3][0] == J, assign[3][1] == J))
# Option C: Tuesday and Wednesday
opt_c = And(Or(assign[1][0] == J, assign[1][1] == J), Or(assign[2][0] == J, assign[2][1] == J))
# Option D: Tuesday and Thursday
opt_d = And(Or(assign[1][0] == J, assign[1][1] == J), Or(assign[3][0] == J, assign[3][1] == J))
# Option E: Wednesday and Thursday
opt_e = And(Or(assign[2][0] == J, assign[2][1] == J), Or(assign[3][0] == J, assign[3][1] == J))

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

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