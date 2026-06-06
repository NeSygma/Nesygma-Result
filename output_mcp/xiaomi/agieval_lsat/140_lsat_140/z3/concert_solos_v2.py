from z3 import *

solver = Solver()

# Variables: position (1-6) for each band member
G = Int('G')  # Guitarist
K = Int('K')  # Keyboard player
P = Int('P')  # Percussionist
S = Int('S')  # Saxophonist
T = Int('T')  # Trumpeter
V = Int('V')  # Violinist

members = [G, K, P, S, T, V]

# Each performs exactly one solo, positions 1-6, all distinct
for m in members:
    solver.add(m >= 1, m <= 6)
solver.add(Distinct(members))

# Constraint 1: The guitarist does not perform the fourth solo.
solver.add(G != 4)

# Constraint 2: The percussionist performs a solo at some time before the keyboard player does.
solver.add(P < K)

# Constraint 3: The keyboard player performs a solo at some time after the violinist does
# and at some time before the guitarist does.
solver.add(V < K)
solver.add(K < G)

# Constraint 4: The saxophonist performs a solo at some time after either the percussionist
# does or the trumpeter does, but not both.
# "after P or after T, but not both" means exactly one of (P < S, T < S) is true
solver.add(Xor(P < S, T < S))

# Additional premise: If the percussionist performs a solo at some time before the saxophonist does
solver.add(P < S)

# Check satisfiability first
result = solver.check()
print(f"Base constraints check: {result}")

if result == sat:
    m = solver.model()
    print(f"G={m[G]}, K={m[K]}, P={m[P]}, S={m[S]}, T={m[T]}, V={m[V]}")

# Now evaluate each answer choice
# (A) The percussionist performs the first solo.
opt_a = (P == 1)

# (B) The percussionist performs the second solo.
opt_b = (P == 2)

# (C) The violinist performs a solo at some time before the saxophonist does.
opt_c = (V < S)

# (D) The percussionist performs a solo at some time before the trumpeter does.
opt_d = (P < T)

# (E) The saxophonist performs a solo at some time before the keyboard player does.
opt_e = (S < K)

# For "must be true", we need to check if the negation is UNSAT
# i.e., the option is entailed by the premises
must_be_true = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s_test = Solver()
    # Add all base constraints
    for c in solver.assertions():
        s_test.add(c)
    # Try to find a model where the option is FALSE
    s_test.add(Not(constr))
    neg_result = s_test.check()
    if neg_result == unsat:
        # The negation is unsatisfiable, so the option MUST be true
        must_be_true.append(letter)
        print(f"Option {letter}: MUST BE TRUE (negation is UNSAT)")
    else:
        print(f"Option {letter}: NOT necessarily true (counterexample exists)")

print(f"\nOptions that must be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")