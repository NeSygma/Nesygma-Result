from z3 import *

# Define solver for base constraints (without T not in chapter 1)
solver_base = Solver()
# Variables for each clue position 1..7
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
# Domain constraints
for v in [R,S,T,U,W,X,Z]:
    solver_base.add(v >= 1, v <= 7)
# All distinct
solver_base.add(Distinct([R,S,T,U,W,X,Z]))
# Constraints
solver_base.add(T < W)  # T before W
solver_base.add(W == T + 3)  # exactly two chapters between
solver_base.add(Abs(S - Z) > 1)  # S and Z not adjacent
solver_base.add(Abs(W - X) > 1)  # W and X not adjacent
solver_base.add(Abs(U - X) == 1)  # U and X adjacent
# Note: T not in chapter 1 is omitted here

# Define T not in chapter 1 constraint for later use
T_not_1 = T != 1

# Option constraints
opt_a = U != 2
opt_b = W != 4
opt_c = X != 6
opt_d = U < T
opt_e = X < W

# Negations of options
neg_opt_a = U == 2
neg_opt_b = W == 4
neg_opt_c = X == 6
neg_opt_d = U >= T
neg_opt_e = X >= W

options = [
    ('A', opt_a, neg_opt_a),
    ('B', opt_b, neg_opt_b),
    ('C', opt_c, neg_opt_c),
    ('D', opt_d, neg_opt_d),
    ('E', opt_e, neg_opt_e),
]

found_options = []
for letter, opt_constr, neg_opt_constr in options:
    # Solver for base + option
    solver_opt = Solver()
    solver_opt.add(solver_base.assertions())
    solver_opt.add(opt_constr)
    if solver_opt.check() != sat:
        continue  # no solutions, skip
    # Check if option allows T in chapter 1
    solver_opt_T1 = Solver()
    solver_opt_T1.add(solver_base.assertions())
    solver_opt_T1.add(opt_constr)
    solver_opt_T1.add(T == 1)
    if solver_opt_T1.check() == sat:
        continue  # option does not forbid T in chapter 1
    # Check if option forbids any solution allowed by T not in chapter 1
    solver_base_not_opt = Solver()
    solver_base_not_opt.add(solver_base.assertions())
    solver_base_not_opt.add(T_not_1)
    solver_base_not_opt.add(neg_opt_constr)
    if solver_base_not_opt.check() == sat:
        continue  # option is stronger
    # If passed all checks, option is equivalent
    found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")