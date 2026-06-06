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

# Exactly one witness testifies on Monday (refined from at least one)
solver.add(Sum([If(Franco == Monday, 1, 0),
                If(Garcia == Monday, 1, 0),
                If(Hong == Monday, 1, 0),
                If(Iturbe == Monday, 1, 0),
                If(Jackson == Monday, 1, 0)]) == 1)

# Jackson is scheduled to testify on Wednesday (given condition)
solver.add(Jackson == Wednesday)

# Now evaluate each multiple-choice option
# Option A: Franco is scheduled to testify on Monday
opt_a_constr = (Franco == Monday)

# Option B: Garcia is scheduled to testify on Monday
opt_b_constr = (Garcia == Monday)

# Option C: Exactly one witness is scheduled to testify on Monday
opt_c_constr = (Sum([If(Franco == Monday, 1, 0),
                     If(Garcia == Monday, 1, 0),
                     If(Hong == Monday, 1, 0),
                     If(Iturbe == Monday, 1, 0),
                     If(Jackson == Monday, 1, 0)]) == 1)

# Option D: Exactly two witnesses are scheduled to testify on Monday
opt_d_constr = (Sum([If(Franco == Monday, 1, 0),
                     If(Garcia == Monday, 1, 0),
                     If(Hong == Monday, 1, 0),
                     If(Iturbe == Monday, 1, 0),
                     If(Jackson == Monday, 1, 0)]) == 2)

# Option E: Garcia is scheduled to testify on the same day as Hong
opt_e_constr = (Garcia == Hong)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")