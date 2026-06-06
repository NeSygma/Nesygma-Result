from z3 import *

# We have 3 kinds: Oatmeal (O), Peanut Butter (P), Sugar (S)
# Each kind has 3 batches (1st, 2nd, 3rd)
# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4

solver = Solver()

# Variables: day each batch is made
# O[i], P[i], S[i] for i=0,1,2 (0=first batch, 1=second batch, 2=third batch)
O = [Int(f'O_{i}') for i in range(3)]
P = [Int(f'P_{i}') for i in range(3)]
S = [Int(f'S_{i}') for i in range(3)]

all_batches = O + P + S

# Domain: each batch on Monday(0) through Friday(4)
for b in all_batches:
    solver.add(b >= 0, b <= 4)

# No two batches of the same kind on the same day
solver.add(Distinct(O))
solver.add(Distinct(P))
solver.add(Distinct(S))

# At least one batch on Monday
solver.add(Or([b == 0 for b in all_batches]))

# The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies
solver.add(O[1] == P[0])

# The second batch of sugar cookies is made on Thursday (day 3)
solver.add(S[1] == 3)

# Additional condition from the question:
# "If one kind of cookie's first batch is made on the same day as another kind of cookie's third batch"
first_batch = [O[0], P[0], S[0]]
third_batch = [O[2], P[2], S[2]]

condition = Or([
    And(i != j, first_batch[i] == third_batch[j])
    for i in range(3) for j in range(3)
])
solver.add(condition)

# Let's first see what models exist to understand the space
print("=== Checking all models (first 5) ===")
solver_copy = Solver()
for c in solver.assertions():
    solver_copy.add(c)

count = 0
while solver_copy.check() == sat and count < 5:
    m = solver_copy.model()
    print(f"Model {count}:")
    print(f"  O: {m[O[0]]}, {m[O[1]]}, {m[O[2]]}")
    print(f"  P: {m[P[0]]}, {m[P[1]]}, {m[P[2]]}")
    print(f"  S: {m[S[0]]}, {m[S[1]]}, {m[S[2]]}")
    
    # Check each option
    all_b = O + P + S
    vals = [m.eval(b) for b in all_b]
    
    # A: at least one on each day
    a_holds = all(any(v == d for v in vals) for d in range(5))
    # B: at least two on Wednesday (day 2)
    b_holds = sum(1 for v in vals if v == 2) >= 2
    # C: exactly one on Monday (day 0)
    c_holds = sum(1 for v in vals if v == 0) == 1
    # D: exactly two on Tuesday (day 1)
    d_holds = sum(1 for v in vals if v == 1) == 2
    # E: exactly one on Friday (day 4)
    e_holds = sum(1 for v in vals if v == 4) == 1
    
    print(f"  A={a_holds}, B={b_holds}, C={c_holds}, D={d_holds}, E={e_holds}")
    
    # Block this model
    solver_copy.add(Or([b != m.eval(b) for b in all_b]))
    count += 1

print()

# Now let's think about the question differently.
# "If condition X holds, which could be false?"
# This means: among A-E, which one is NOT necessarily true when X holds?
# So we need to find an option that CAN be false (i.e., its negation is satisfiable with X).

# Let's test each option's negation more carefully.
# The issue might be that ALL options can be false, meaning the condition is too weak.
# Let's re-read: "If one kind of cookie's first batch is made on the same day as another kind of cookie's third batch"
# This means: there exist two DIFFERENT kinds where first of one = third of another.

# Let's test each option's negation individually
print("=== Testing each option's negation ===")
for letter, name in [("A", "At least one batch on each day"), 
                      ("B", "At least two batches on Wednesday"),
                      ("C", "Exactly one batch on Monday"),
                      ("D", "Exactly two batches on Tuesday"),
                      ("E", "Exactly one batch on Friday")]:
    s = Solver()
    for c in solver.assertions():
        s.add(c)
    
    if letter == "A":
        s.add(Not(And([Or([b == d for b in all_batches]) for d in range(5)])))
    elif letter == "B":
        s.add(Not(Sum([If(b == 2, 1, 0) for b in all_batches]) >= 2))
    elif letter == "C":
        s.add(Not(Sum([If(b == 0, 1, 0) for b in all_batches]) == 1))
    elif letter == "D":
        s.add(Not(Sum([If(b == 1, 1, 0) for b in all_batches]) == 2))
    elif letter == "E":
        s.add(Not(Sum([If(b == 4, 1, 0) for b in all_batches]) == 1))
    
    res = s.check()
    print(f"Option {letter} ({name}) negation: {res}")
    if res == sat:
        m = s.model()
        print(f"  O: {m[O[0]]}, {m[O[1]]}, {m[O[2]]}")
        print(f"  P: {m[P[0]]}, {m[P[1]]}, {m[P[2]]}")
        print(f"  S: {m[S[0]]}, {m[S[1]]}, {m[S[2]]}")