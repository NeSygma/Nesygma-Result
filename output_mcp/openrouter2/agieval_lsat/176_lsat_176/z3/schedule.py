from z3 import *

solver = Solver()
# Map students to indices
G, H, J, K, L = 0, 1, 2, 3, 4
# Create shift variables: shift[day][shift]
shift = [[Int(f'shift_{d}_{s}') for s in range(2)] for d in range(5)]
# Domain constraints: each shift assigned to a student 0..4
for d in range(5):
    for s in range(2):
        solver.add(shift[d][s] >= 0, shift[d][s] <= 4)
# No student works both shifts of any day
for d in range(5):
    solver.add(shift[d][0] != shift[d][1])
# Each student works exactly two shifts total
for student in [G, H, J, K, L]:
    solver.add(Sum([If(shift[d][s] == student, 1, 0) for d in range(5) for s in range(2)]) == 2)
# Katya works on Tuesday (day 1) and Friday (day 4)
solver.add(Or(shift[1][0] == K, shift[1][1] == K))
solver.add(Or(shift[4][0] == K, shift[4][1] == K))
# Hakeem and Joe work on the same day as each other at least once
solver.add(Or([And(Or(shift[d][0] == H, shift[d][1] == H),
                   Or(shift[d][0] == J, shift[d][1] == J)) for d in range(5)]))
# Grecia and Louise never work on the same day as each other
for d in range(5):
    solver.add(Not(And(Or(shift[d][0] == G, shift[d][1] == G),
                       Or(shift[d][0] == L, shift[d][1] == L))))
# Louise works the second shift on two consecutive days
solver.add(Or([And(shift[d][1] == L, shift[d+1][1] == L) for d in range(4)]))
# Grecia works the first shift on two nonconsecutive days
# Exactly two first shifts for G
solver.add(Sum([If(shift[d][0] == G, 1, 0) for d in range(5)]) == 2)
# No consecutive first shifts for G
solver.add(Not(Or([And(shift[d][0] == G, shift[d+1][0] == G) for d in range(4)])))

# Option constraints
opt_a_constr = And(shift[1][0] != G, shift[1][1] != G)  # G not on Tuesday
opt_b_constr = And(shift[2][0] != H, shift[2][1] != H)  # H not on Wednesday
opt_c_constr = And(shift[1][0] != J, shift[1][1] != J)  # J not on Tuesday
opt_d_constr = And(shift[3][0] != J, shift[3][1] != J)  # J not on Thursday
opt_e_constr = And(shift[1][0] != L, shift[1][1] != L)  # L not on Tuesday

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