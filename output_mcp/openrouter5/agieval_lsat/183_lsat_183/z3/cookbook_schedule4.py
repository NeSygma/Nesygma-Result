from z3 import *

# Variables: each cookbook's season (True = fall, False = spring)
K, L, M, N, O, P = Bools('K L M N O P')

# Base constraints
base_constraints = [
    M != P,           # M and P cannot be in same season
    K == N,           # K and N must be in same season
    Implies(K, O),    # If K is fall, O must be fall
    Implies(M, Not(N)) # If M is fall, N must be spring
]

# Let's examine options A and B more carefully.
# The question asks: "The schedule for the publication of the cookbooks is fully determined if which one of the following is true?"
# This means: if we know the given fact, the entire schedule (all 6 books) is uniquely determined.

# Let's print the full schedule for each option to see what's happening.

options = [
    ("A", And(K, Not(L))),  # K is fall, L is spring
    ("B", And(O, Not(P))),  # O is fall, P is spring
]

for letter, constr in options:
    s = Solver()
    s.add(base_constraints)
    s.add(constr)
    
    print(f"\n=== Option {letter} ===")
    count = 0
    vars_list = [K, L, M, N, O, P]
    names = ['K', 'L', 'M', 'N', 'O', 'P']
    while s.check() == sat:
        count += 1
        m = s.model()
        vals = {names[i]: 'fall' if m.eval(v) else 'spring' for i, v in enumerate(vars_list)}
        print(f"  Solution {count}: {vals}")
        s.add(Or([v != m.eval(v) for v in vars_list]))
    print(f"  Total: {count} solutions")

# Now let's check: Option A says K is fall and L is spring.
# If K is fall, then N is fall (K==N), and O is fall (Implies(K,O)).
# M != P, and if M is fall then N must be spring - but N is fall, so M cannot be fall. So M is spring.
# Since M != P, P must be fall.
# So: K=fall, N=fall, O=fall, M=spring, P=fall, L=spring.
# That's fully determined! Let's verify.

print("\n\n=== Verification of Option A ===")
s = Solver()
s.add(base_constraints)
s.add(And(K, Not(L)))  # K fall, L spring
print(f"Check: {s.check()}")
m = s.model()
for name, var in zip(names, vars_list):
    print(f"  {name}: {'fall' if m.eval(var) else 'spring'}")

# Now Option B: O is fall and P is spring.
# Let's trace: O=fall, P=spring.
# M != P, so M != spring, so M = fall.
# If M is fall, N must be spring.
# K == N, so K = spring.
# Implies(K, O): K is spring, so the implication is vacuously true. O can be anything - but we already know O=fall.
# L is unconstrained.
# So: O=fall, P=spring, M=fall, N=spring, K=spring, L=??? (could be fall or spring)
# That's 2 solutions for L. So not fully determined.

print("\n\n=== Verification of Option B ===")
s = Solver()
s.add(base_constraints)
s.add(And(O, Not(P)))  # O fall, P spring
count = 0
while s.check() == sat:
    count += 1
    m = s.model()
    vals = {names[i]: 'fall' if m.eval(v) else 'spring' for i, v in enumerate(vars_list)}
    print(f"  Solution {count}: {vals}")
    s.add(Or([v != m.eval(v) for v in vars_list]))
print(f"  Total: {count} solutions")

# So Option A is the correct answer.
found_options = ["A"]
print("\nSTATUS: sat")
print("answer:A")