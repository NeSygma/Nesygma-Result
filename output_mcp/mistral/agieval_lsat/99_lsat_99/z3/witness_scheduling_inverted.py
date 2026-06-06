from z3 import *

# Base constraints
solver = Solver()

# Witnesses: Franco, Garcia, Hong, Iturbe, Jackson
# Days: Monday=0, Tuesday=1, Wednesday=2
witnesses = [
    Int('Franco'),
    Int('Garcia'),
    Int('Hong'),
    Int('Iturbe'),
    Int('Jackson')
]

# Each witness testifies on exactly one day
for w in witnesses:
    solver.add(Or(w == 0, w == 1, w == 2))

# Franco does not testify on the same day that Garcia testifies
solver.add(witnesses[0] != witnesses[1])

# Iturbe testifies on Wednesday (2)
solver.add(witnesses[3] == 2)

# Exactly two witnesses testify on Tuesday (1)
solver.add(Sum([w == 1 for w in witnesses]) == 2)

# Hong does not testify on Monday (0)
solver.add(witnesses[2] != 0)

# At least one witness testifies on Monday (0)
solver.add(Sum([w == 0 for w in witnesses]) >= 1)

# Base constraints complete

# Define options as constraints
# Option A: Franco is the only witness scheduled to testify on Monday.
# This means:
# - Franco is on Monday (0)
# - All others are not on Monday
# - Exactly one witness on Monday (Franco)
opt_a_constr = And(
    witnesses[0] == 0,
    witnesses[1] != 0,
    witnesses[2] != 0,
    witnesses[3] != 0,
    witnesses[4] != 0,
    Sum([w == 0 for w in witnesses]) == 1
)

# Option B: Franco is scheduled to testify on the same day as Iturbe.
# Iturbe is on Wednesday (2), so Franco must also be on Wednesday.
opt_b_constr = (witnesses[0] == witnesses[3])

# Option C: Garcia and Hong are both scheduled to testify on Tuesday.
opt_c_constr = And(
    witnesses[1] == 1,
    witnesses[2] == 1
)

# Option D: Garcia is the only witness scheduled to testify on Monday and Hong is one of two witnesses scheduled to testify on Wednesday.
# - Garcia is on Monday (0) and only witness on Monday
# - Hong is on Wednesday (2)
# - Iturbe is also on Wednesday (2), so Wednesday has two witnesses (Hong and Iturbe)
opt_d_constr = And(
    witnesses[1] == 0,
    Sum([w == 0 for w in witnesses]) == 1,
    witnesses[2] == 2,
    Sum([w == 2 for w in witnesses]) == 2
)

# Option E: Jackson is scheduled to testify on Tuesday and two witnesses are scheduled to testify on Monday.
# - Jackson is on Tuesday (1)
# - Exactly two witnesses on Monday (0)
opt_e_constr = And(
    witnesses[4] == 1,
    Sum([w == 0 for w in witnesses]) == 2
)

# Evaluate options: check if each option is UNSATISFIABLE (i.e., cannot be true)
unsat_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        unsat_options.append(letter)
    solver.pop()

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options cannot be true {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options cannot be true (all are possible)")