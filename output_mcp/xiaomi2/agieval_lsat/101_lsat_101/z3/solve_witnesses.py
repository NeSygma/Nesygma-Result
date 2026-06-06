from z3 import *

solver = Solver()

# Witnesses: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
# Days: Monday=0, Tuesday=1, Wednesday=2
days = [Int(f'day_{i}') for i in range(5)]
F, G, H, I, J = 0, 1, 2, 3, 4

# Each witness testifies on exactly one day (0=Mon, 1=Tue, 2=Wed)
for d in days:
    solver.add(Or(d == 0, d == 1, d == 2))

# Constraint 1: Franco and Garcia on different days
solver.add(days[F] != days[G])

# Constraint 2: Iturbe on Wednesday
solver.add(days[I] == 2)

# Constraint 3: Exactly 2 witnesses on Tuesday
solver.add(Sum([If(days[i] == 1, 1, 0) for i in range(5)]) == 2)

# Constraint 4: Hong not on Monday
solver.add(days[H] != 0)

# Constraint 5: At least 1 witness on Monday
solver.add(Sum([If(days[i] == 0, 1, 0) for i in range(5)]) >= 1)

# Additional condition: Jackson is the ONLY witness on Monday
solver.add(days[J] == 0)
solver.add(Sum([If(days[i] == 0, 1, 0) for i in range(5)]) == 1)

# Define option constraints
# (A) Franco is scheduled to testify on Wednesday
opt_a = (days[F] == 2)
# (B) Hong is scheduled to testify on Tuesday
opt_b = (days[H] == 1)
# (C) Garcia is scheduled to testify on Tuesday
opt_c = (days[G] == 1)
# (D) Franco is scheduled to testify on the same day as Hong
opt_d = (days[F] == days[H])
# (E) Garcia is scheduled to testify on the same day as Hong
opt_e = (days[G] == days[H])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
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