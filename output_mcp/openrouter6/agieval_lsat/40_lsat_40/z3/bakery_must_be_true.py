from z3 import *

# Define days
Mon, Tue, Wed, Thu, Fri = 0, 1, 2, 3, 4

# Variables for each batch
O1, O2, O3, P1, P2, P3, S1, S2, S3 = Ints('O1 O2 O3 P1 P2 P3 S1 S2 S3')
all_vars = [O1, O2, O3, P1, P2, P3, S1, S2, S3]

# Base solver with constraints
def base_solver():
    s = Solver()
    # Domain: days 0,1,3,4 (no Wednesday)
    for v in all_vars:
        s.add(Or(v == Mon, v == Tue, v == Thu, v == Fri))
    # No two batches of same kind on same day
    s.add(O1 != O2)
    s.add(O1 != O3)
    s.add(O2 != O3)
    s.add(P1 != P2)
    s.add(P1 != P3)
    s.add(P2 != P3)
    s.add(S1 != S2)
    s.add(S1 != S3)
    s.add(S2 != S3)
    # At least one batch on Monday
    s.add(Or([v == Mon for v in all_vars]))
    # Second batch of oatmeal same day as first batch of peanut butter
    s.add(O2 == P1)
    # Second batch of sugar on Thursday
    s.add(S2 == Thu)
    return s

# Option constraints (the statements themselves)
opt_a = Sum([If(v == Tue, 1, 0) for v in all_vars]) == 3
opt_b = Sum([If(v == Fri, 1, 0) for v in all_vars]) == 3
opt_c = Sum([If(v == Mon, 1, 0) for v in all_vars]) >= 2
opt_d = Sum([If(v == Thu, 1, 0) for v in all_vars]) >= 2
opt_e = Sum([If(v == Mon, 1, 0) for v in all_vars]) < Sum([If(v == Tue, 1, 0) for v in all_vars])

# Test necessity: for each option, check if its negation is unsatisfiable
necessary_options = []
for letter, opt in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s = base_solver()
    s.add(Not(opt))
    result = s.check()
    if result == unsat:
        necessary_options.append(letter)
        print(f"Option {letter} must be true (negation unsat)")
    else:
        print(f"Option {letter} not necessarily true (negation sat)")

print("\nNecessary options:", necessary_options)

# Now use the required skeleton for multiple choice
# We need to define opt_a_constr, etc. as the option constraints (the statements)
# But the skeleton checks if the option is satisfiable. That's for "possible".
# For "must be true", we need to check if the option is necessary.
# However, the user insists on using the skeleton. We'll adapt: we'll test each option
# by adding the option and checking if it's always true? That doesn't work.
# Instead, we'll use the skeleton but with the negation of the option? That would be wrong.
# Let's follow the skeleton literally but interpret "valid" as "necessary".
# We'll test each option by adding the option and checking if it's unsatisfiable when negated? No.

# Actually, the skeleton is for "possible". The user might have mis-specified.
# Given the instruction, I'll use the skeleton but with the correct logic for "must be true":
# We'll test each option by checking if the option is true in all models.
# That is equivalent to: the negation of the option is unsatisfiable.
# So we can define "constr" as the negation of the option, and then check if it's unsat.
# But the skeleton checks if solver.check() == sat. If we add the negation and it's unsat, then the option is necessary.
# So we can do:
found_options = []
for letter, constr in [("A", Not(opt_a)), ("B", Not(opt_b)), ("C", Not(opt_c)), ("D", Not(opt_d)), ("E", Not(opt_e))]:
    s = base_solver()
    s.push()
    s.add(constr)
    if s.check() == unsat:  # if negation is unsat, then option is necessary
        found_options.append(letter)
    s.pop()

if len(found_options) == 1:
    print("\nSTATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("\nSTATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("\nSTATUS: unsat")
    print("Refine: No options found")