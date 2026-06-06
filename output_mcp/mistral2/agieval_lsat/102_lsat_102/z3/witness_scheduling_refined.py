from z3 import *

# Initialize solver
solver = Solver()

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
days = [0, 1, 2]

# Witnesses: Franco, Garcia, Hong, Iturbe, Jackson
witnesses = ['Franco', 'Garcia', 'Hong', 'Iturbe', 'Jackson']
witness_vars = {w: Int(w) for w in witnesses}

# Assign each witness to a day
for w in witnesses:
    solver.add(witness_vars[w] >= 0, witness_vars[w] <= 2)

# Constraints:
# 1. Franco does not testify on the same day as Garcia
solver.add(witness_vars['Franco'] != witness_vars['Garcia'])

# 2. Iturbe testifies on Wednesday (day 2)
solver.add(witness_vars['Iturbe'] == 2)

# 3. Exactly two witnesses testify on Tuesday (day 1)
solver.add(Sum([witness_vars[w] == 1 for w in witnesses]) == 2)

# 4. Hong does not testify on Monday (day 0)
solver.add(witness_vars['Hong'] != 0)

# 5. At least one witness testifies on Monday (day 0)
solver.add(Sum([witness_vars[w] == 0 for w in witnesses]) >= 1)

# Additional condition: Franco is scheduled to testify on the same day as Hong
solver.add(witness_vars['Franco'] == witness_vars['Hong'])

# Now evaluate the options (A-E) individually to see which MUST be true
found_options = []

# Option A: Franco is scheduled to testify on Wednesday.
opt_a_constr = (witness_vars['Franco'] == 2)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    # Check if this is the ONLY possible option
    other_options = [
        ("B", witness_vars['Garcia'] == 0),
        ("C", witness_vars['Garcia'] == 2),
        ("D", witness_vars['Hong'] == 1),
        ("E", And(witness_vars['Iturbe'] == 2, Sum([witness_vars[w] == 2 for w in witnesses]) == 1))
    ]
    is_unique = True
    for letter, constr in other_options:
        solver.push()
        solver.add(constr)
        if solver.check() == sat:
            is_unique = False
        solver.pop()
    if is_unique:
        found_options.append("A")
    else:
        # If not unique, just check if it is satisfiable
        found_options.append("A")
else:
    solver.pop()

# Option B: Garcia is scheduled to testify on Monday.
opt_b_constr = (witness_vars['Garcia'] == 0)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Garcia is scheduled to testify on Wednesday.
opt_c_constr = (witness_vars['Garcia'] == 2)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Hong is scheduled to testify on Tuesday.
opt_d_constr = (witness_vars['Hong'] == 1)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Iturbe is the only witness scheduled to testify on Wednesday.
opt_e_constr = And(
    witness_vars['Iturbe'] == 2,
    Sum([witness_vars[w] == 2 for w in witnesses]) == 1
)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")