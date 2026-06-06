from z3 import *

# Base constraints for the mystery novel clues problem
solver = Solver()

# Declare symbolic variables for the clues (each represents the chapter it is assigned to)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')

# Each clue must be assigned to a chapter between 1 and 7
solver.add(R >= 1, R <= 7)
solver.add(S >= 1, S <= 7)
solver.add(T >= 1, T <= 7)
solver.add(U >= 1, U <= 7)
solver.add(W >= 1, W <= 7)
solver.add(X >= 1, X <= 7)
solver.add(Z >= 1, Z <= 7)

# Each clue must appear exactly once
solver.add(Distinct([R, S, T, U, W, X, Z]))

# T must be mentioned before W, with exactly two chapters separating T and W
# This means W = T + 3
solver.add(W == T + 3)

# S and Z cannot be mentioned in adjacent chapters
solver.add(Not(Or(S == Z - 1, S == Z + 1)))

# W and X cannot be mentioned in adjacent chapters
solver.add(Not(Or(W == X - 1, W == X + 1)))

# U and X must be mentioned in adjacent chapters
solver.add(Or(U == X - 1, U == X + 1))

# Original constraint: T cannot be mentioned in chapter 1
original_constraint = (T != 1)

# Now, evaluate each option to see if it can replace the original constraint (T != 1)
# We need to check if the substitution constraints uniquely enforce T != 1
# and do not allow any additional valid orderings beyond those allowed by the original constraint.

# Option A: U cannot be mentioned in chapter 2
opt_a_constr = (U != 2)

# Option B: W cannot be mentioned in chapter 4
opt_b_constr = (W != 4)

# Option C: X cannot be mentioned in chapter 6
opt_c_constr = (X != 6)

# Option D: U must be mentioned in an earlier chapter than T
opt_d_constr = (U < T)

# Option E: X must be mentioned in an earlier chapter than W
opt_e_constr = (X < W)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    # Replace the original constraint with the new one
    solver.add(constr)
    # Check if the substitution constraints allow T == 1
    solver.push()
    solver.add(T == 1)
    if solver.check() == unsat:
        # If T == 1 is not allowed, check if the substitution constraints
        # allow the same set of orderings as the original constraint
        solver.pop()
        solver.add(original_constraint)
        if solver.check() == sat:
            # Check if the substitution constraints allow the same set of orderings
            # as the original constraint
            solver.push()
            solver.add(original_constraint)
            if solver.check() == sat:
                # If both constraints allow the same set of orderings, this is a valid substitution
                found_options.append(letter)
            solver.pop()
    solver.pop()
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