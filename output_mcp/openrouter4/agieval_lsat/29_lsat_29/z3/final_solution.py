from z3 import *

# Declare variables
F, G, H = Bools('F G H')  # botanists
K, L, M = Bools('K L M')  # chemists
P, Q, R = Bools('P Q R')  # zoologists

all_vars = [F, G, H, K, L, M, P, Q, R]

solver = Solver()

# The panel has exactly 5 scientists
solver.add(Sum([If(v, 1, 0) for v in all_vars]) == 5)

# G and H are selected (premise of the conditional)
solver.add(G)
solver.add(H)

# Condition 1: At least one of each type
solver.add(Or(F, G, H))  # botanist (trivially true)
solver.add(Or(K, L, M))  # chemist
solver.add(Or(P, Q, R))  # zoologist

# Condition 2: If more than one botanist, then at most one zoologist.
# G and H are selected, so more_than_one_botanist is true.
# Therefore at most one zoologist.
at_least_two_zoologists = Or(And(P, Q), And(P, R), And(Q, R))
solver.add(Not(at_least_two_zoologists))

# Condition 3: F and K cannot both be selected
solver.add(Not(And(F, K)))

# Condition 4: K and M cannot both be selected
solver.add(Not(And(K, M)))

# Condition 5: If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Evaluate each option: does the option hold in ALL valid configurations?
# We test by checking if there exists a configuration where the option FAILS
# i.e., neither X nor Y is selected.

found_options = []
for letter, (x_var, y_var) in [("A", (F, K)), ("B", (F, M)), ("C", (K, M)), ("D", (M, Q)), ("E", (P, Q))]:
    solver.push()
    # Try to find a configuration where NEITHER is selected (violating the "must include either")
    solver.add(Not(x_var))
    solver.add(Not(y_var))
    if solver.check() == unsat:
        # No configuration exists where both are absent -> the option is necessary
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