from z3 import *

# Initialize solver
solver = Solver()

# Days: 0 (June 1) to 5 (June 6)
days = range(6)

# Antiques
antiques = ['harmonica', 'lamp', 'mirror', 'sundial', 'table', 'vase']

# Assign each antique to a day (0-5)
assignments = {a: Int(f'assign_{a}') for a in antiques}

# Constraints:
# 1. All antiques are assigned to distinct days
solver.add(Distinct(list(assignments.values())))

# 2. Sundial is not auctioned on June 1st (day 0)
solver.add(assignments['sundial'] != 0)

# 3. If harmonica is auctioned earlier than lamp, then mirror is auctioned earlier than lamp
#    This is equivalent to: harmonica < lamp => mirror < lamp
#    Which is equivalent to: harmonica >= lamp or mirror < lamp
solver.add(Implies(assignments['harmonica'] < assignments['lamp'],
                   assignments['mirror'] < assignments['lamp']))

# 4. Sundial is auctioned earlier than mirror and earlier than vase
solver.add(assignments['sundial'] < assignments['mirror'])
solver.add(assignments['sundial'] < assignments['vase'])

# 5. Table is auctioned earlier than harmonica or earlier than vase, but not both
#    This is equivalent to: (table < harmonica) XOR (table < vase)
solver.add( (assignments['table'] < assignments['harmonica']) != (assignments['table'] < assignments['vase']) )

# Base constraints for all options
base_constraints = solver.assertions()

# Define the options as constraints
def option_constraints(letter, option):
    # option is a list of antiques in order from day 0 to day 5
    constraints = []
    for day, antique in enumerate(option):
        constraints.append(assignments[antique] == day)
    return And(constraints)

# Option A: harmonica, table, sundial, lamp, vase, mirror
opt_a_constr = option_constraints("A", ['harmonica', 'table', 'sundial', 'lamp', 'vase', 'mirror'])

# Option B: lamp, harmonica, sundial, mirror, vase, table
opt_b_constr = option_constraints("B", ['lamp', 'harmonica', 'sundial', 'mirror', 'vase', 'table'])

# Option C: harmonica, sundial, table, mirror, lamp, vase
opt_c_constr = option_constraints("C", ['harmonica', 'sundial', 'table', 'mirror', 'lamp', 'vase'])

# Option D: sundial, mirror, harmonica, table, vase, lamp
opt_d_constr = option_constraints("D", ['sundial', 'mirror', 'harmonica', 'table', 'vase', 'lamp'])

# Option E: vase, sundial, lamp, harmonica, table, mirror
opt_e_constr = option_constraints("E", ['vase', 'sundial', 'lamp', 'harmonica', 'table', 'mirror'])

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    # Add base constraints
    for c in base_constraints:
        solver.add(c)
    # Add option-specific constraints
    solver.add(constr)
    # Check satisfiability
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")