from z3 import *

# Create solver
solver = Solver()

# Define positions 1-5 (using 0-indexed for programming, but conceptually 1-5)
positions = range(5)  # 0,1,2,3,4 correspond to solos 1-5

# Pianist variables: 0 = Wayne, 1 = Zara
pianist = [Int(f'pianist_{i}') for i in positions]
for i in positions:
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))

# Type variables: 0 = Modern, 1 = Traditional
typ = [Int(f'typ_{i}') for i in positions]
for i in positions:
    solver.add(Or(typ[i] == 0, typ[i] == 1))

# Constraint 1: Third solo is traditional (position 2 in 0-indexed)
solver.add(typ[2] == 1)

# Constraint 2: Exactly two traditional pieces are performed consecutively
# This means there is exactly one pair (i, i+1) where both are T (1)
pair_T = [Bool(f'pair_T_{i}') for i in range(4)]  # pairs: (0,1), (1,2), (2,3), (3,4)
for i in range(4):
    solver.add(pair_T[i] == And(typ[i] == 1, typ[i+1] == 1))

# Exactly one of these pairs is true
solver.add(Sum([If(pair_T[i], 1, 0) for i in range(4)]) == 1)

# Constraint 3: Fourth solo condition (position 3 in 0-indexed)
solver.add(Or(
    And(pianist[3] == 0, typ[3] == 1),
    And(pianist[3] == 1, typ[3] == 0)
))

# Constraint 4: Pianist of second solo ≠ pianist of fifth solo
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece.
for i in positions:
    if i > 0:
        earlier_M_W = Or([And(typ[j] == 0, pianist[j] == 0) for j in range(i)])
        solver.add(Implies(typ[i] == 1, earlier_M_W))
    else:
        solver.add(typ[0] == 0)  # First solo cannot be traditional

# Additional constraint from question: pianist[1] == pianist[2] (first and second solo same pianist)
solver.add(pianist[0] == pianist[1])

# Define option constraints
opt_a_constr = (pianist[0] == 1)  # Zara performs first solo
opt_b_constr = (pianist[2] == 0)  # Wayne performs third solo
opt_c_constr = (pianist[4] == 1)  # Zara performs fifth solo
opt_d_constr = (typ[1] == 1)      # Second solo is traditional
opt_e_constr = (typ[3] == 0)      # Fourth solo is modern

# For "must be true", we check if the negation of each option makes the solver unsatisfiable
necessary_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        necessary_options.append(letter)
    solver.pop()

# According to the problem, we need exactly one option that must be true
if len(necessary_options) == 1:
    print("STATUS: sat")
    print(f"answer:{necessary_options[0]}")
elif len(necessary_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true: {necessary_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")

# Also, let's print a model to verify
print("\n--- Example model ---")
if solver.check() == sat:
    m = solver.model()
    print("Pianists (0=W, 1=Z):", [m[pianist[i]] for i in positions])
    print("Types (0=M, 1=T):", [m[typ[i]] for i in positions])