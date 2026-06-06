from z3 import *

# Define photographers
photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# Create assignment variables: assigned_to_silva[p] and assigned_to_thorne[p]
assigned_to_silva = {p: Bool(f'assigned_to_silva_{p}') for p in photographers}
assigned_to_thorne = {p: Bool(f'assigned_to_thorne_{p}') for p in photographers}

# Base constraints
solver = Solver()

# 1. At least two photographers assigned to each university
solver.add(Sum([assigned_to_silva[p] for p in photographers]) >= 2)
solver.add(Sum([assigned_to_thorne[p] for p in photographers]) >= 2)

# 2. No photographer assigned to both universities
for p in photographers:
    solver.add(Not(And(assigned_to_silva[p], assigned_to_thorne[p])))

# 3. Frost must be assigned together with Heideck to one university
solver.add(Or(
    And(assigned_to_silva['Frost'], assigned_to_silva['Heideck']),
    And(assigned_to_thorne['Frost'], assigned_to_thorne['Heideck'])
))

# 4. If Lai and Mays are both assigned, they must be assigned to different universities
solver.add(Implies(
    And(Or(assigned_to_silva['Lai'], assigned_to_thorne['Lai']),
         Or(assigned_to_silva['Mays'], assigned_to_thorne['Mays'])),
    Xor(assigned_to_silva['Lai'], assigned_to_silva['Mays'])
))

# 5. If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(assigned_to_silva['Gonzalez'], assigned_to_thorne['Lai']))

# 6. If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
solver.add(Implies(Not(assigned_to_thorne['Knutson']),
                   And(assigned_to_thorne['Heideck'], assigned_to_thorne['Mays'])))

# Define the options as constraints
def option_A():
    # Silva: Gonzalez, Lai
    # Thorne: Frost, Heideck, Mays
    # All other photographers are unassigned
    return And(
        assigned_to_silva['Gonzalez'],
        assigned_to_silva['Lai'],
        assigned_to_thorne['Frost'],
        assigned_to_thorne['Heideck'],
        assigned_to_thorne['Mays'],
        # Ensure no other assignments
        Not(assigned_to_silva['Frost']),
        Not(assigned_to_silva['Heideck']),
        Not(assigned_to_silva['Knutson']),
        Not(assigned_to_silva['Mays']),
        Not(assigned_to_thorne['Gonzalez']),
        Not(assigned_to_thorne['Knutson']),
        Not(assigned_to_thorne['Lai'])
    )

def option_B():
    # Silva: Gonzalez, Mays
    # Thorne: Knutson, Lai
    # All other photographers are unassigned
    return And(
        assigned_to_silva['Gonzalez'],
        assigned_to_silva['Mays'],
        assigned_to_thorne['Knutson'],
        assigned_to_thorne['Lai'],
        # Ensure no other assignments
        Not(assigned_to_silva['Frost']),
        Not(assigned_to_silva['Heideck']),
        Not(assigned_to_silva['Knutson']),
        Not(assigned_to_silva['Lai']),
        Not(assigned_to_thorne['Frost']),
        Not(assigned_to_thorne['Gonzalez']),
        Not(assigned_to_thorne['Heideck']),
        Not(assigned_to_thorne['Mays'])
    )

def option_C():
    # Silva: Frost, Gonzalez, Heideck
    # Thorne: Knutson, Lai, Mays
    # All other photographers are unassigned
    return And(
        assigned_to_silva['Frost'],
        assigned_to_silva['Gonzalez'],
        assigned_to_silva['Heideck'],
        assigned_to_thorne['Knutson'],
        assigned_to_thorne['Lai'],
        assigned_to_thorne['Mays'],
        # Ensure no other assignments
        Not(assigned_to_silva['Knutson']),
        Not(assigned_to_silva['Lai']),
        Not(assigned_to_silva['Mays']),
        Not(assigned_to_thorne['Frost']),
        Not(assigned_to_thorne['Gonzalez']),
        Not(assigned_to_thorne['Heideck'])
    )

def option_D():
    # Silva: Frost, Heideck, Mays
    # Thorne: Gonzalez, Lai
    # All other photographers are unassigned
    return And(
        assigned_to_silva['Frost'],
        assigned_to_silva['Heideck'],
        assigned_to_silva['Mays'],
        assigned_to_thorne['Gonzalez'],
        assigned_to_thorne['Lai'],
        # Ensure no other assignments
        Not(assigned_to_silva['Gonzalez']),
        Not(assigned_to_silva['Knutson']),
        Not(assigned_to_silva['Lai']),
        Not(assigned_to_thorne['Frost']),
        Not(assigned_to_thorne['Heideck']),
        Not(assigned_to_thorne['Knutson']),
        Not(assigned_to_thorne['Mays'])
    )

def option_E():
    # Silva: Frost, Heideck, Mays
    # Thorne: Gonzalez, Knutson, Lai
    # All other photographers are unassigned
    return And(
        assigned_to_silva['Frost'],
        assigned_to_silva['Heideck'],
        assigned_to_silva['Mays'],
        assigned_to_thorne['Gonzalez'],
        assigned_to_thorne['Knutson'],
        assigned_to_thorne['Lai'],
        # Ensure no other assignments
        Not(assigned_to_silva['Gonzalez']),
        Not(assigned_to_silva['Knutson']),
        Not(assigned_to_silva['Lai']),
        Not(assigned_to_thorne['Frost']),
        Not(assigned_to_thorne['Heideck']),
        Not(assigned_to_thorne['Mays'])
    )

# Evaluate each option
found_options = []
for letter, constr in [("A", option_A()), ("B", option_B()), ("C", option_C()), ("D", option_D()), ("E", option_E())]:
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