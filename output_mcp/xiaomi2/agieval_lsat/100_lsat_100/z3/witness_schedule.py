from z3 import *

solver = Solver()

# Witnesses: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
# Days: Monday=0, Tuesday=1, Wednesday=2
witnesses = ['Franco', 'Garcia', 'Hong', 'Iturbe', 'Jackson']
days = ['Monday', 'Tuesday', 'Wednesday']

# Each witness testifies on exactly one day
day = [Int(f'day_{w}') for w in range(5)]
for i in range(5):
    solver.add(Or(day[i] == 0, day[i] == 1, day[i] == 2))

# Constraint 1: Franco and Garcia not on the same day
solver.add(day[0] != day[1])

# Constraint 2: Iturbe testifies on Wednesday
solver.add(day[3] == 2)

# Constraint 3: Exactly two witnesses testify on Tuesday
solver.add(Sum([If(day[i] == 1, 1, 0) for i in range(5)]) == 2)

# Constraint 4: Hong does not testify on Monday
solver.add(day[2] != 0)

# Constraint 5: At least one witness testifies on Monday
solver.add(Sum([If(day[i] == 0, 1, 0) for i in range(5)]) >= 1)

# Given condition: Jackson testifies on Wednesday
solver.add(day[4] == 2)

# Now check each answer choice to see which MUST be true
# We check if the negation of each option is UNSAT (meaning the option must be true)

# Option A: Franco testifies on Monday
# Option B: Garcia testifies on Monday
# Option C: Exactly one witness testifies on Monday
# Option D: Exactly two witnesses testify on Monday
# Option E: Garcia testifies on the same day as Hong

options = {
    "A": day[0] == 0,  # Franco on Monday
    "B": day[1] == 0,  # Garcia on Monday
    "C": Sum([If(day[i] == 0, 1, 0) for i in range(5)]) == 1,  # Exactly one on Monday
    "D": Sum([If(day[i] == 0, 1, 0) for i in range(5)]) == 2,  # Exactly two on Monday
    "E": day[1] == day[2],  # Garcia same day as Hong
}

# For each option, check if it MUST be true (negation is unsat)
must_be_true = []
for letter, constr in options.items():
    s = Solver()
    s.add(solver.assertions())
    s.add(Not(constr))
    if s.check() == unsat:
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is unsat)")
    else:
        print(f"Option {letter}: NOT necessarily true (counterexample exists)")
        m = s.model()
        for i in range(5):
            print(f"  {witnesses[i]} -> {days[m[day[i]].as_long()]}")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")