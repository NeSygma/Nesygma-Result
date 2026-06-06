from z3 import *

# Let's re-examine the problem more carefully.
# The question: "If M is the only chemist selected for the panel, which one of the following MUST be true?"
# 
# We need to find what is necessarily true in ALL valid selections.
# Let's enumerate all valid models and check each option.

solver = Solver()

F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

# At least one of each type
solver.add(Or(F, G, H))
solver.add(Or(K, L, M))
solver.add(Or(P, Q, R))

# If more than one botanist, then at most one zoologist
more_than_one_botanist = Sum([If(b, 1, 0) for b in [F, G, H]]) >= 2
at_most_one_zoologist = Sum([If(z, 1, 0) for z in [P, Q, R]]) <= 1
solver.add(Implies(more_than_one_botanist, at_most_one_zoologist))

# F and K cannot both be selected
solver.add(Not(And(F, K)))

# K and M cannot both be selected
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# M is the ONLY chemist selected
solver.add(M)
solver.add(Not(K))
solver.add(Not(L))

# Enumerate all solutions
all_models = []
while solver.check() == sat:
    m = solver.model()
    selected = frozenset([s for s in [F, G, H, K, L, M, P, Q, R] if is_true(m.eval(s))])
    all_models.append(selected)
    # Block this exact combination
    solver.add(Or([s != is_true(m.eval(s)) for s in [F, G, H, K, L, M, P, Q, R]]))

print(f"Total valid models: {len(all_models)}")
for i, model in enumerate(all_models):
    print(f"Model {i+1}: {sorted([str(s) for s in model])}")

print()

# Now check each option: does it hold in ALL models?
options = {
    "A": And(F, G),
    "B": And(G, H),
    "C": And(H, P),
    "D": And(F, G, H),
    "E": And(P, Q, R)
}

for letter, constr in options.items():
    # Check if constr is true in all models
    holds_in_all = True
    for model_set in all_models:
        # Evaluate the constraint in this model
        # We need to check if the constraint is satisfied
        s_check = Solver()
        for var in [F, G, H, K, L, M, P, Q, R]:
            s_check.add(var == (var in model_set))
        s_check.add(Not(constr))
        if s_check.check() == sat:
            holds_in_all = False
            break
    
    if holds_in_all:
        print(f"Option {letter}: MUST BE TRUE (holds in all {len(all_models)} models)")
    else:
        print(f"Option {letter}: NOT necessarily true")