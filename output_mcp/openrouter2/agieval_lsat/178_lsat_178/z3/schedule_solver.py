from z3 import *

solver = Solver()
# Student indices: 0=Grecia, 1=Hakeem, 2=Joe, 3=Katya, 4=Louise
# Create shift variables: shift[day][shift]
shift = [[Int(f'shift_{d}_{s}') for s in range(2)] for d in range(5)]

# Domain constraints
for d in range(5):
    for s in range(2):
        solver.add(shift[d][s] >= 0, shift[d][s] <= 4)

# No student works both shifts of any day
for d in range(5):
    solver.add(shift[d][0] != shift[d][1])

# Each student works exactly two shifts
for i in range(5):
    solver.add(Sum([If(shift[d][s] == i, 1, 0) for d in range(5) for s in range(2)]) == 2)

# Louise works the second shift on exactly two consecutive days
# Exactly two days
solver.add(Sum([If(shift[d][1] == 4, 1, 0) for d in range(5)]) == 2)
# Consecutive pair exists
solver.add(Or([And(shift[d][1] == 4, shift[d+1][1] == 4) for d in range(4)]))

# Grecia works the first shift on exactly two nonconsecutive days
solver.add(Sum([If(shift[d][0] == 0, 1, 0) for d in range(5)]) == 2)
# No consecutive days for Grecia first shift
for d in range(4):
    solver.add(Not(And(shift[d][0] == 0, shift[d+1][0] == 0)))

# Katya works on Tuesday (day 1) and Friday (day 4), one shift each day
# Tuesday
solver.add(Or(shift[1][0] == 3, shift[1][1] == 3))
solver.add(Not(And(shift[1][0] == 3, shift[1][1] == 3)))
# Friday
solver.add(Or(shift[4][0] == 3, shift[4][1] == 3))
solver.add(Not(And(shift[4][0] == 3, shift[4][1] == 3)))

# Hakeem and Joe work on the same day at least once
solver.add(Or([And(Or(shift[d][0] == 1, shift[d][1] == 1),
                    Or(shift[d][0] == 2, shift[d][1] == 2)) for d in range(5)]))

# Grecia and Louise never work on the same day
for d in range(5):
    solver.add(Not(And(Or(shift[d][0] == 0, shift[d][1] == 0),
                        Or(shift[d][0] == 4, shift[d][1] == 4))))

# Additional condition: at least one day where Grecia and Joe both work
solver.add(Or([And(Or(shift[d][0] == 0, shift[d][1] == 0),
                    Or(shift[d][0] == 2, shift[d][1] == 2)) for d in range(5)]))

# Option constraints
opt_a_constr = shift[1][0] == 0  # Grecia works first shift on Tuesday
opt_b_constr = shift[0][1] == 1  # Hakeem works second shift on Monday
opt_c_constr = shift[2][1] == 1  # Hakeem works second shift on Wednesday
opt_d_constr = shift[2][0] == 2  # Joe works first shift on Wednesday
opt_e_constr = shift[3][0] == 2  # Joe works first shift on Thursday

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