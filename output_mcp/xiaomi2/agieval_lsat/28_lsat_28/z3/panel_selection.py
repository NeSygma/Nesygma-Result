from z3 import *

solver = Solver()

# Boolean variables for each scientist
F, G, H = Bools('F G H')  # Botanists
K, L, M = Bools('K L M')  # Chemists
P, Q, R = Bools('P Q R')  # Zoologists

all_scientists = [F, G, H, K, L, M, P, Q, R]
botanists = [F, G, H]
chemists = [K, L, M]
zoologists = [P, Q, R]

# Exactly 5 panelists selected
solver.add(Sum([If(s, 1, 0) for s in all_scientists]) == 5)

# At least one of each type
solver.add(Or(F, G, H))
solver.add(Or(K, L, M))
solver.add(Or(P, Q, R))

# If more than one botanist, then at most one zoologist
more_than_one_bot = Or(
    And(F, G), And(F, H), And(G, H)
)
at_most_one_zoo = Not(Or(
    And(P, Q), And(P, R), And(Q, R)
))
solver.add(Implies(more_than_one_bot, at_most_one_zoo))

# F and K cannot both be selected
solver.add(Not(And(F, K)))

# K and M cannot both be selected
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Additional condition: P is the ONLY zoologist selected
solver.add(P == True)
solver.add(Q == False)
solver.add(R == False)

# Now test each option: an option "must be true" iff its negation is UNSAT
# We use the theorem-proving pattern

options = {
    "A": Implies(K, Not(G)),
    "B": Implies(L, Not(F)),
    "C": Implies(Sum([If(s, 1, 0) for s in chemists]) == 1, K),
    "D": Implies(Sum([If(s, 1, 0) for s in chemists]) == 2, Not(F)),
    "E": Implies(Sum([If(s, 1, 0) for s in chemists]) == 2, Not(G)),
}

must_be_true = []
for letter, claim in options.items():
    # Check if negation of claim is satisfiable
    s_neg = Solver()
    # Add all base constraints
    s_neg.add(solver.assertions())
    # Add negation of the claim
    s_neg.add(Not(claim))
    neg_result = s_neg.check()
    
    if neg_result == unsat:
        # Negation is unsat => claim MUST be true
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is unsat)")
    elif neg_result == sat:
        m = s_neg.model()
        print(f"Option {letter}: NOT necessarily true (counterexample exists)")
        # Print the counterexample
        selected = [str(s) for s in all_scientists if is_true(m.evaluate(s))]
        print(f"  Counterexample - Selected: {', '.join(selected)}")
    else:
        print(f"Option {letter}: unknown")

print()
print(f"Options that must be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")