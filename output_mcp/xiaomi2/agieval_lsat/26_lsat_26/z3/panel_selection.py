from z3 import *

solver = Solver()

# Boolean variables: True if selected for the panel
F, G, H = Bools('F G H')  # Botanists
K, L, M_var = Bools('K L M')  # Chemists
P, Q, R = Bools('P Q R')  # Zoologists

all_scientists = [F, G, H, K, L, M_var, P, Q, R]

# Panel must have exactly 5 members
solver.add(Sum([If(s, 1, 0) for s in all_scientists]) == 5)

# At least one of each type
solver.add(Or(F, G, H))  # at least one botanist
solver.add(Or(K, L, M_var))  # at least one chemist
solver.add(Or(P, Q, R))  # at least one zoologist

# Condition 2: If more than one botanist → at most one zoologist
botanist_count = Sum([If(s, 1, 0) for s in [F, G, H]])
zoologist_count = Sum([If(s, 1, 0) for s in [P, Q, R]])
solver.add(Implies(botanist_count > 1, zoologist_count <= 1))

# Condition 3: F and K cannot both be selected
solver.add(Not(And(F, K)))

# Condition 4: K and M cannot both be selected
solver.add(Not(And(K, M_var)))

# Condition 5: If M is selected → both P and R must be selected
solver.add(Implies(M_var, And(P, R)))

# QUESTION: M is the only chemist selected
solver.add(M_var == True)
solver.add(K == False)
solver.add(L == False)

# Now check each answer choice
# (A) F and G are both selected
opt_a = And(F, G)
# (B) G and H are both selected
opt_b = And(G, H)
# (C) H and P are both selected
opt_c = And(H, P)
# (D) F, G, and H are all selected
opt_d = And(F, G, H)
# (E) P, Q, and R are all selected
opt_e = And(P, Q, R)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# For "must be true", we check: is the negation unsatisfiable given the constraints?
# i.e., can we find a valid panel where the option is FALSE?
must_be_true = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    result = solver.check()
    if result == unsat:
        # Cannot falsify → must be true
        must_be_true.append(letter)
    solver.pop()

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")

# Also print a sample valid model for verification
solver.push()
if solver.check() == sat:
    m = solver.model()
    print("\nSample valid panel:")
    for s in all_scientists:
        if is_true(m.evaluate(s)):
            print(f"  {s} = selected")
solver.pop()