from z3 import *

# Initialize solver
solver = Solver()

# Photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# Assignments: assigned_S[ph] = True if assigned to Silva, False if assigned to Thorne or not assigned
# We will use two Booleans per photographer: assigned_S[ph] and assigned_T[ph]
# with the constraint that assigned_S[ph] and assigned_T[ph] cannot both be True.

# Declare variables
assigned_S = {ph: Bool(f'assigned_S_{ph}') for ph in photographers}
assigned_T = {ph: Bool(f'assigned_T_{ph}') for ph in photographers}

# Constraint: No photographer is assigned to both ceremonies
for ph in photographers:
    solver.add(Not(And(assigned_S[ph], assigned_T[ph])))

# Constraint: At least two photographers assigned to each ceremony
solver.add(Sum([assigned_S[ph] for ph in photographers]) >= 2)
solver.add(Sum([assigned_T[ph] for ph in photographers]) >= 2)

# Constraint 3: Frost must be assigned together with Heideck to one of the ceremonies
# This means Frost and Heideck must be assigned to the same ceremony (both S or both T)
solver.add(Or(
    And(assigned_S['Frost'], assigned_S['Heideck']),
    And(assigned_T['Frost'], assigned_T['Heideck'])
))

# Constraint 4: If Lai and Mays are both assigned, they must be assigned to different ceremonies
# This is equivalent to: Not (Lai and Mays are both assigned to S) and Not (Lai and Mays are both assigned to T)
solver.add(Not(And(assigned_S['Lai'], assigned_S['Mays'])))
solver.add(Not(And(assigned_T['Lai'], assigned_T['Mays'])))

# Constraint 5: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
# Equivalent to: Not assigned_S['Gonzalez'] or assigned_T['Lai']
solver.add(Implies(assigned_S['Gonzalez'], assigned_T['Lai']))

# Constraint 6: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
# Equivalent to: Not assigned_T['Knutson'] implies (assigned_T['Heideck'] and assigned_T['Mays'])
solver.add(Implies(Not(assigned_T['Knutson']), And(assigned_T['Heideck'], assigned_T['Mays'])))

# Now, evaluate each option for Thorne University assignment
# We will check if the Thorne assignment matches the option and the constraints are satisfied.
# Additionally, we enforce that no other photographers are assigned to Thorne.

# Option A: Frost, Gonzalez, Heideck, Mays assigned to Thorne
# No other photographers assigned to Thorne
opt_a_constr = And(
    assigned_T['Frost'],
    assigned_T['Gonzalez'],
    assigned_T['Heideck'],
    assigned_T['Mays'],
    Not(assigned_T['Knutson']),
    Not(assigned_T['Lai']),
    # Ensure no other photographers are assigned to Thorne
    And([Not(assigned_T[ph]) for ph in photographers if ph not in ['Frost', 'Gonzalez', 'Heideck', 'Mays']])
)

# Option B: Frost, Heideck, Knutson, Mays assigned to Thorne
opt_b_constr = And(
    assigned_T['Frost'],
    assigned_T['Heideck'],
    assigned_T['Knutson'],
    assigned_T['Mays'],
    Not(assigned_T['Gonzalez']),
    Not(assigned_T['Lai']),
    # Ensure no other photographers are assigned to Thorne
    And([Not(assigned_T[ph]) for ph in photographers if ph not in ['Frost', 'Heideck', 'Knutson', 'Mays']])
)

# Option C: Gonzalez, Knutson, Lai assigned to Thorne
opt_c_constr = And(
    assigned_T['Gonzalez'],
    assigned_T['Knutson'],
    assigned_T['Lai'],
    Not(assigned_T['Frost']),
    Not(assigned_T['Heideck']),
    Not(assigned_T['Mays']),
    # Ensure no other photographers are assigned to Thorne
    And([Not(assigned_T[ph]) for ph in photographers if ph not in ['Gonzalez', 'Knutson', 'Lai']])
)

# Option D: Gonzalez, Knutson, Mays assigned to Thorne
opt_d_constr = And(
    assigned_T['Gonzalez'],
    assigned_T['Knutson'],
    assigned_T['Mays'],
    Not(assigned_T['Frost']),
    Not(assigned_T['Heideck']),
    Not(assigned_T['Lai']),
    # Ensure no other photographers are assigned to Thorne
    And([Not(assigned_T[ph]) for ph in photographers if ph not in ['Gonzalez', 'Knutson', 'Mays']])
)

# Option E: Knutson, Mays assigned to Thorne
opt_e_constr = And(
    assigned_T['Knutson'],
    assigned_T['Mays'],
    Not(assigned_T['Frost']),
    Not(assigned_T['Gonzalez']),
    Not(assigned_T['Heideck']),
    Not(assigned_T['Lai']),
    # Ensure no other photographers are assigned to Thorne
    And([Not(assigned_T[ph]) for ph in photographers if ph not in ['Knutson', 'Mays']])
)

# Check each option
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