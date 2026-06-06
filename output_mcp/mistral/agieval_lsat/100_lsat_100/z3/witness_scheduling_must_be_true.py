from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each witness's testimony day
# 0 = Monday, 1 = Tuesday, 2 = Wednesday
Franco = Int('Franco')
Garcia = Int('Garcia')
Hong = Int('Hong')
Iturbe = Int('Iturbe')
Jackson = Int('Jackson')

# Create solver
solver = Solver()

# Helper: day is 0 (Mon), 1 (Tue), 2 (Wed)
Monday = 0
Tuesday = 1
Wednesday = 2

# Each witness testifies on exactly one day
solver.add(Franco >= Monday, Franco <= Wednesday)
solver.add(Garcia >= Monday, Garcia <= Wednesday)
solver.add(Hong >= Monday, Hong <= Wednesday)
solver.add(Iturbe >= Monday, Iturbe <= Wednesday)
solver.add(Jackson >= Monday, Jackson <= Wednesday)

# Franco does not testify on the same day that Garcia testifies
solver.add(Franco != Garcia)

# Iturbe testifies on Wednesday
solver.add(Iturbe == Wednesday)

# Exactly two witnesses testify on Tuesday
# Count how many witnesses have day == Tuesday
solver.add(Sum([If(Franco == Tuesday, 1, 0),
                If(Garcia == Tuesday, 1, 0),
                If(Hong == Tuesday, 1, 0),
                If(Iturbe == Tuesday, 1, 0),
                If(Jackson == Tuesday, 1, 0)]) == 2)

# Hong does not testify on Monday
solver.add(Hong != Monday)

# At least one witness testifies on Monday (relaxed from exactly one)
solver.add(Sum([If(Franco == Monday, 1, 0),
                If(Garcia == Monday, 1, 0),
                If(Hong == Monday, 1, 0),
                If(Iturbe == Monday, 1, 0),
                If(Jackson == Monday, 1, 0)]) >= 1)

# Jackson is scheduled to testify on Wednesday (given condition)
solver.add(Jackson == Wednesday)

# Now evaluate each multiple-choice option for "must be true"
# We will check if the negation of the option is unsatisfiable under the base constraints + given condition

# Option A: Franco is scheduled to testify on Monday
# Must be true: Not(Franco == Monday) is unsat
opt_a_must = (Franco == Monday)
opt_a_neg = (Franco != Monday)

# Option B: Garcia is scheduled to testify on Monday
# Must be true: Not(Garcia == Monday) is unsat
opt_b_must = (Garcia == Monday)
opt_b_neg = (Garcia != Monday)

# Option C: Exactly one witness is scheduled to testify on Monday
# Must be true: Not(Sum(...) == 1) is unsat
opt_c_must = (Sum([If(Franco == Monday, 1, 0),
                   If(Garcia == Monday, 1, 0),
                   If(Hong == Monday, 1, 0),
                   If(Iturbe == Monday, 1, 0),
                   If(Jackson == Monday, 1, 0)]) == 1)
opt_c_neg = (Sum([If(Franco == Monday, 1, 0),
                   If(Garcia == Monday, 1, 0),
                   If(Hong == Monday, 1, 0),
                   If(Iturbe == Monday, 1, 0),
                   If(Jackson == Monday, 1, 0)]) != 1)

# Option D: Exactly two witnesses are scheduled to testify on Monday
# Must be true: Not(Sum(...) == 2) is unsat
opt_d_must = (Sum([If(Franco == Monday, 1, 0),
                   If(Garcia == Monday, 1, 0),
                   If(Hong == Monday, 1, 0),
                   If(Iturbe == Monday, 1, 0),
                   If(Jackson == Monday, 1, 0)]) == 2)
opt_d_neg = (Sum([If(Franco == Monday, 1, 0),
                   If(Garcia == Monday, 1, 0),
                   If(Hong == Monday, 1, 0),
                   If(Iturbe == Monday, 1, 0),
                   If(Jackson == Monday, 1, 0)]) != 2)

# Option E: Garcia is scheduled to testify on the same day as Hong
# Must be true: Not(Garcia == Hong) is unsat
opt_e_must = (Garcia == Hong)
opt_e_neg = (Garcia != Hong)

# List of options and their must-be-true checks
options = [
    ("A", opt_a_must, opt_a_neg),
    ("B", opt_b_must, opt_b_neg),
    ("C", opt_c_must, opt_c_neg),
    ("D", opt_d_must, opt_d_neg),
    ("E", opt_e_must, opt_e_neg),
]

must_be_true = []
for letter, must_constr, neg_constr in options:
    # Check if the negation is unsatisfiable (i.e., must be true)
    solver.push()
    solver.add(neg_constr)
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

# Determine result
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")