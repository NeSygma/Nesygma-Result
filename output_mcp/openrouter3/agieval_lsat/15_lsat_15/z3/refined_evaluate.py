from z3 import *
solver = Solver()

# Define positions for each composition (1-8)
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')

# All positions must be between 1 and 8
solver.add([And(1 <= var, var <= 8) for var in [F, H, L, O, P, R, S, T]])

# All positions must be distinct
solver.add(Distinct(F, H, L, O, P, R, S, T))

# Constraint 1: T is performed either immediately before F or immediately after R
# This is an exclusive OR - exactly one of these must be true
solver.add(Or(F == T + 1, T == R + 1))
solver.add(Not(And(F == T + 1, T == R + 1)))  # Exclusive OR

# Constraint 2: At least two compositions between F and R
solver.add(Abs(F - R) >= 3)

# Constraint 3: O is first or fifth
solver.add(Or(O == 1, O == 5))

# Constraint 4: Eighth composition is L or H
solver.add(Or(L == 8, H == 8))

# Constraint 5: P before S
solver.add(P < S)

# Constraint 6: At least one composition between O and S
solver.add(Abs(O - S) >= 2)

# Additional: O is immediately after T (the condition in the question)
solver.add(O == T + 1)

# Define answer choices
opt_a_constr = Or(F == 1, F == 2)
opt_b_constr = Or(F == 2, F == 3)
opt_c_constr = Or(F == 4, F == 6)
opt_d_constr = Or(F == 4, F == 7)
opt_e_constr = Or(F == 6, F == 7)

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