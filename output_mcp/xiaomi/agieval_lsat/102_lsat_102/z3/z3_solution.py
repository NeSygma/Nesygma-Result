from z3 import *

solver = Solver()

# Witnesses: Franco=0, Garcia=1, Hong=2, Iturbe=3, Jackson=4
# Days: Monday=0, Tuesday=1, Wednesday=2
witnesses = [Int(f'w_{i}') for i in range(5)]
# witnesses[0]=Franco, [1]=Garcia, [2]=Hong, [3]=Iturbe, [4]=Jackson

# Each witness testifies on exactly one day (0=Mon, 1=Tue, 2=Wed)
for w in witnesses:
    solver.add(Or(w == 0, w == 1, w == 2))

# Franco does not testify on the same day as Garcia
solver.add(witnesses[0] != witnesses[1])

# Iturbe testifies on Wednesday
solver.add(witnesses[3] == 2)

# Exactly two witnesses testify on Tuesday
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)

# Hong does not testify on Monday
solver.add(witnesses[2] != 0)

# At least one witness testifies on Monday
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Franco is scheduled to testify on the same day as Hong
solver.add(witnesses[0] == witnesses[2])

# Define option constraints
# (A) Franco is scheduled to testify on Wednesday.
opt_a = (witnesses[0] == 2)

# (B) Garcia is scheduled to testify on Monday.
opt_b = (witnesses[1] == 0)

# (C) Garcia is scheduled to testify on Wednesday.
opt_c = (witnesses[1] == 2)

# (D) Hong is scheduled to testify on Tuesday.
opt_d = (witnesses[2] == 1)

# (E) Iturbe is the only witness scheduled to testify on Wednesday.
opt_e = And(witnesses[3] == 2, 
            witnesses[0] != 2, witnesses[1] != 2, witnesses[2] != 2, witnesses[4] != 2)

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