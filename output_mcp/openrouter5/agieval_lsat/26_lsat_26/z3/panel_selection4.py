from z3 import *

# Let me re-read the problem more carefully.
# 
# Conditions:
# 1. At least one of each type (botanist, chemist, zoologist)
# 2. If more than one botanist is selected, then at most one zoologist is selected.
# 3. F and K cannot both be selected.
# 4. K and M cannot both be selected.
# 5. If M is selected, both P and R must be selected.
#
# Question: If M is the only chemist selected for the panel, which one of the following MUST be true?
#
# M is the only chemist => M is selected, K and L are NOT selected.
# Since M is selected, P and R must be selected (condition 5).
#
# So we have: M, P, R are selected. K, L are not selected.
# Need at least one botanist (F, G, or H).
# Need at least one zoologist - already have P, R. Q is optional.
#
# Condition 2: If more than one botanist, then at most one zoologist.
# We already have P and R selected (2 zoologists). So if we have more than one botanist,
# we'd violate "at most one zoologist" since we have 2 zoologists.
# Therefore: we CANNOT have more than one botanist. So at most one botanist.
# But we need at least one botanist. So exactly one botanist.
#
# So exactly one of {F, G, H} is selected.
# P and R are selected. Q may or may not be selected.
# Condition 3: F and K cannot both be selected. K is not selected, so F is fine.
# Condition 4: K and M cannot both be selected. K is not selected, fine.
#
# Let's enumerate all valid models.

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
    solver.add(Or([s != is_true(m.eval(s)) for s in [F, G, H, K, L, M, P, Q, R]]))

print(f"Total valid models: {len(all_models)}")
for i, model in enumerate(all_models):
    print(f"Model {i+1}: {sorted([str(s) for s in model])}")

print()

# Now check each option: does it hold in ALL models?
# Option A: F and G are both selected
# Option B: G and H are both selected
# Option C: H and P are both selected
# Option D: F, G, and H are all selected
# Option E: P, Q, and R are all selected

# Let's check each option using the LSAT skeleton
found_options = []

# Option A: F and G both selected
solver.push()
solver.add(And(F, G))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: G and H both selected
solver.push()
solver.add(And(G, H))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: H and P both selected
solver.push()
solver.add(And(H, P))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: F, G, and H all selected
solver.push()
solver.add(And(F, G, H))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: P, Q, and R all selected
solver.push()
solver.add(And(P, Q, R))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

print(f"Options that are possible: {found_options}")

# But the question asks "MUST be true" - meaning it's true in ALL valid models.
# Let me check which options are true in ALL models.

print()
print("Checking which options MUST be true (true in ALL models):")
must_options = []
for letter, constr in [("A", And(F, G)), ("B", And(G, H)), ("C", And(H, P)), ("D", And(F, G, H)), ("E", And(P, Q, R))]:
    # Check if NOT(constr) is unsat (meaning constr is always true)
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        must_options.append(letter)
    solver.pop()
    print(f"Option {letter}: {'MUST BE TRUE' if letter in must_options else 'not necessarily true'}")

print(f"\nMust-be-true options: {must_options}")

# Now use the LSAT skeleton properly
# The question asks "which MUST be true" - we need the option that is true in ALL valid models.
# So we check: is there exactly one option that is entailed (its negation is unsat)?

if len(must_options) == 1:
    print("STATUS: sat")
    print(f"answer:{must_options[0]}")
elif len(must_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {must_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")