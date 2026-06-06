from z3 import *

solver = Solver()

# Declare witnesses and days
witnesses = ["Franco", "Garcia", "Hong", "Iturbe", "Jackson"]
days = ["Monday", "Tuesday", "Wednesday"]

# Assign each witness to a day (0=Monday, 1=Tuesday, 2=Wednesday)
assign = {w: Int(f"assign_{w}") for w in witnesses}
for w in witnesses:
    solver.add(assign[w] >= 0, assign[w] <= 2)

# Constraints from the problem statement
# 1. Franco does not testify on the same day as Garcia
solver.add(assign["Franco"] != assign["Garcia"])

# 2. Iturbe testifies on Wednesday
solver.add(assign["Iturbe"] == 2)

# 3. Exactly two witnesses testify on Tuesday
solver.add(Sum([If(assign[w] == 1, 1, 0) for w in witnesses]) == 2)

# 4. Hong does not testify on Monday
solver.add(assign["Hong"] != 0)

# 5. At least one witness testifies on Monday
solver.add(Sum([If(assign[w] == 0, 1, 0) for w in witnesses]) >= 1)

# Base constraints are set. Now evaluate each option.

# Define constraints for each option
# Option A: Monday: Franco, Tuesday: Hong and Iturbe, Wednesday: Garcia and Jackson
opt_a_constr = And(
    assign["Franco"] == 0,
    assign["Hong"] == 1,
    assign["Iturbe"] == 1,
    assign["Garcia"] == 2,
    assign["Jackson"] == 2
)

# Option B: Monday: Franco and Hong, Tuesday: Iturbe and Jackson, Wednesday: Garcia
opt_b_constr = And(
    assign["Franco"] == 0,
    assign["Hong"] == 0,
    assign["Iturbe"] == 1,
    assign["Jackson"] == 1,
    assign["Garcia"] == 2
)

# Option C: Monday: Garcia, Tuesday: Franco and Iturbe, Wednesday: Hong and Jackson
opt_c_constr = And(
    assign["Garcia"] == 0,
    assign["Franco"] == 1,
    assign["Iturbe"] == 1,
    assign["Hong"] == 2,
    assign["Jackson"] == 2
)

# Option D: Monday: Garcia and Jackson, Tuesday: Franco and Hong, Wednesday: Iturbe
opt_d_constr = And(
    assign["Garcia"] == 0,
    assign["Jackson"] == 0,
    assign["Franco"] == 1,
    assign["Hong"] == 1,
    assign["Iturbe"] == 2
)

# Option E: Monday: Garcia and Jackson, Tuesday: Hong, Wednesday: Franco and Iturbe
opt_e_constr = And(
    assign["Garcia"] == 0,
    assign["Jackson"] == 0,
    assign["Hong"] == 1,
    assign["Franco"] == 2,
    assign["Iturbe"] == 2
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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