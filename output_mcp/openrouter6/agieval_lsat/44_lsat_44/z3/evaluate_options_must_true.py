from z3 import *

# Define students and plays
students = ["Jiang", "Kramer", "Lopez", "Megregian", "O'Neill"]
plays = ["Sunset", "Tamerlane", "Undulation"]
num_students = len(students)
num_plays = len(plays)

review = [[Bool(f"review_{i}_{j}") for j in range(num_plays)] for i in range(num_students)]

solver = Solver()

# Base constraints
# Constraint 1: Each student reviews at least one play
for i in range(num_students):
    solver.add(Sum(review[i]) >= 1)

# Constraint 2: Kramer and Lopez each review fewer plays than Megregian
kramer_sum = Sum(review[1])
lopez_sum = Sum(review[2])
megregian_sum = Sum(review[3])
solver.add(kramer_sum < megregian_sum)
solver.add(lopez_sum < megregian_sum)

# Constraint 3: Neither Lopez nor Megregian reviews any play Jiang reviews
for j in range(num_plays):
    solver.add(Implies(review[0][j], Not(review[2][j])))
    solver.add(Implies(review[0][j], Not(review[3][j])))

# Constraint 4: Kramer and O'Neill both review Tamerlane (play index 1)
solver.add(review[1][1] == True)
solver.add(review[4][1] == True)

# Constraint 5: Exactly two students have identical review sets
eq = {}
for i in range(num_students):
    for j in range(i+1, num_students):
        eq[(i,j)] = Bool(f"eq_{i}_{j}")
        solver.add(eq[(i,j)] == And(
            review[i][0] == review[j][0],
            review[i][1] == review[j][1],
            review[i][2] == review[j][2]
        ))
solver.add(Sum([eq[(i,j)] for i in range(num_students) for j in range(i+1, num_students)]) == 1)

# Define option constraints (positive)
opt_a_constr = Sum(review[0]) > Sum(review[2])  # Jiang > Lopez
opt_b_constr = Sum(review[3]) > Sum(review[0])  # Megregian > Jiang
opt_c_constr = Sum(review[3]) > Sum(review[4])  # Megregian > O'Neill
opt_d_constr = Sum(review[4]) > Sum(review[0])  # O'Neill > Jiang
opt_e_constr = Sum(review[4]) > Sum(review[1])  # O'Neill > Kramer

# For "must be true", we check if the negation is unsatisfiable
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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