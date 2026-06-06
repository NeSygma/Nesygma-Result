from z3 import *

# Witnesses: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
# Days: Monday=0, Tuesday=1, Wednesday=2

def build_base_constraints(solver):
    day = [Int(f'day_{w}') for w in range(5)]
    for i in range(5):
        solver.add(day[i] >= 0, day[i] <= 2)

    # Constraint 1: Franco and Garcia not on same day
    solver.add(day[0] != day[1])

    # Constraint 2: Iturbe on Wednesday
    solver.add(day[3] == 2)

    # Constraint 3: Exactly two witnesses on Tuesday
    solver.add(Sum([If(day[i] == 1, 1, 0) for i in range(5)]) == 2)

    # Constraint 4: Hong not on Monday
    solver.add(day[2] != 0)

    # Constraint 5: At least one witness on Monday
    solver.add(Sum([If(day[i] == 0, 1, 0) for i in range(5)]) >= 1)

    # Additional condition: Franco on same day as Hong
    solver.add(day[0] == day[2])
    
    return day

# Define answer choice constraints
# (A) Franco is on Wednesday
opt_a = lambda day: (day[0] == 2)
# (B) Garcia is on Monday
opt_b = lambda day: (day[1] == 0)
# (C) Garcia is on Wednesday
opt_c = lambda day: (day[1] == 2)
# (D) Hong is on Tuesday
opt_d = lambda day: (day[2] == 1)
# (E) Iturbe is the only witness on Wednesday
opt_e = lambda day: And(day[3] == 2, And([day[i] != 2 for i in range(5) if i != 3]))

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

must_be_true = []

for letter, opt_fn in options:
    # Check if NOT(option) is unsatisfiable given base constraints
    # If so, the option must be true
    s = Solver()
    day = build_base_constraints(s)
    s.add(Not(opt_fn(day)))
    result = s.check()
    if result == unsat:
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is unsat)")
    else:
        print(f"Option {letter}: NOT necessarily true (negation is sat)")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")