from z3 import *

# Witnesses: Franco, Garcia, Hong, Iturbe, Jackson
# Days: Monday=0, Tuesday=1, Wednesday=2

solver = Solver()

# Create variables: day for each witness (0=Mon, 1=Tue, 2=Wed)
F, G, H, I, J = Ints('F G H I J')
witnesses = [F, G, H, I, J]

# Domain: each witness testifies on exactly one of the three days
for w in witnesses:
    solver.add(And(w >= 0, w <= 2))

# Condition 1: Franco does not testify on the same day as Garcia
solver.add(F != G)

# Condition 2: Iturbe testifies on Wednesday (day 2)
solver.add(I == 2)

# Condition 3: Exactly two witnesses testify on Tuesday (day 1)
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)

# Condition 4: Hong does not testify on Monday (day 0)
solver.add(H != 0)

# Condition 5: At least one witness testifies on Monday (day 0)
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Additional condition from the question: Jackson is the ONLY witness on Monday
solver.add(J == 0)  # Jackson on Monday
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) == 1)  # exactly one on Monday

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
result = solver.check()
if result == sat:
    m = solver.model()
    print("Base model found:")
    print(f"  Franco (F) = {m[F]}")
    print(f"  Garcia (G) = {m[G]}")
    print(f"  Hong (H) = {m[H]}")
    print(f"  Iturbe (I) = {m[I]}")
    print(f"  Jackson (J) = {m[J]}")
else:
    print("Base constraints are UNSAT!")
    exit()

# Now evaluate each option as "must be true" - meaning it holds in ALL models
# So we check if the negation of the option is satisfiable.
# If Not(option) is UNSAT, then the option MUST be true.

print("\nChecking which options MUST be true (negation unsatisfiable):")
found_must = []
for letter, constr in [("A", F == 2), ("B", H == 1), ("C", G == 1), ("D", F == H), ("E", G == H)]:
    solver.push()
    solver.add(Not(constr))
    res = solver.check()
    if res == unsat:
        found_must.append(letter)
        print(f"  Option {letter}: MUST be true (negation is UNSAT)")
    else:
        print(f"  Option {letter}: NOT necessarily true (negation is SAT)")
    solver.pop()

if len(found_must) == 1:
    print("\nSTATUS: sat")
    print(f"answer:{found_must[0]}")
elif len(found_must) > 1:
    print(f"\nSTATUS: unsat")
    print(f"Refine: Multiple options must be true {found_must}")
else:
    print(f"\nSTATUS: unsat")
    print("Refine: No options must be true")