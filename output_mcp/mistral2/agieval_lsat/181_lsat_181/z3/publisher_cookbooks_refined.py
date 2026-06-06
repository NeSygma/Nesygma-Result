from z3 import *

solver = Solver()

# Declare season variables: True = fall, False = spring
K, L, M, N, O, P = Bools('K L M N O P')

# Base constraints
solver.add(Not(M == P))  # M and P cannot be in the same season
solver.add(K == N)       # K and N must be in the same season
solver.add(Implies(K, O)) # If K is in fall, O must be in fall

# Given condition: M is in fall
solver.add(M == True)

# Define the options as constraints
# Option A: K and O are in fall
opt_a = And(K == True, O == True)
# Option B: L and N are in fall
opt_b = And(L == True, N == True)
# Option C: L and O are in fall
opt_c = And(L == True, O == True)
# Option D: N and P are in fall
opt_d = And(N == True, P == True)
# Option E: O and P are in fall
opt_e = And(O == True, P == True)

# Evaluate each option while ensuring others are not satisfied
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    # Ensure only the current option is satisfied
    solver.add(constr)
    # Ensure other options are not satisfied
    if letter != "A":
        solver.add(Not(opt_a))
    if letter != "B":
        solver.add(Not(opt_b))
    if letter != "C":
        solver.add(Not(opt_c))
    if letter != "D":
        solver.add(Not(opt_d))
    if letter != "E":
        solver.add(Not(opt_e))
    
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