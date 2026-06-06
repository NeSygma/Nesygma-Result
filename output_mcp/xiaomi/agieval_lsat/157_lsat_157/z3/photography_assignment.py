from z3 import *

solver = Solver()

# Photographers: Frost, Gonzalez, Heideck, Knutson, Lai, Mays
# For each photographer, we define whether they are assigned to Silva (True) or Thorne (False)
# We also need to track if they are assigned at all

photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# assigned[p] = True if photographer p is assigned to some ceremony
assigned = {p: Bool(f'assigned_{p}') for p in photographers}

# at_silva[p] = True if photographer p is at Silva, False if at Thorne
# Only meaningful if assigned[p] is True
at_silva = {p: Bool(f'at_silva_{p}') for p in photographers}

# Constraint: No photographer can be assigned to both ceremonies
# (This is implicit in our encoding - each photographer is either at Silva or Thorne or unassigned)

# Constraint 1: At least 2 photographers at Silva
silva_count = Sum([If(And(assigned[p], at_silva[p]), 1, 0) for p in photographers])
solver.add(silva_count >= 2)

# Constraint 2: At least 2 photographers at Thorne
thorne_count = Sum([If(And(assigned[p], Not(at_silva[p])), 1, 0) for p in photographers])
solver.add(thorne_count >= 2)

# Constraint 3: Frost must be assigned together with Heideck to one ceremony
# Both must be assigned, and both at the same ceremony
solver.add(Implies(assigned['Frost'], And(assigned['Heideck'], at_silva['Frost'] == at_silva['Heideck'])))
solver.add(Implies(assigned['Heideck'], And(assigned['Frost'], at_silva['Frost'] == at_silva['Heideck'])))

# Constraint 4: If Lai and Mays are both assigned, they must be at different ceremonies
solver.add(Implies(And(assigned['Lai'], assigned['Mays']), at_silva['Lai'] != at_silva['Mays']))

# Constraint 5: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(And(assigned['Gonzalez'], at_silva['Gonzalez']), And(assigned['Lai'], Not(at_silva['Lai']))))

# Constraint 6: If Knutson is NOT assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
# "Not assigned to Thorne" means either unassigned or at Silva
solver.add(Implies(Or(Not(assigned['Knutson']), at_silva['Knutson']), 
                   And(assigned['Heideck'], Not(at_silva['Heideck']), assigned['Mays'], Not(at_silva['Mays']))))

# Now test each option for the COMPLETE assignment to Silva University
# Option A: Frost, Gonzalez, Heideck, Knutson at Silva
opt_a_constr = And(
    assigned['Frost'], at_silva['Frost'],
    assigned['Gonzalez'], at_silva['Gonzalez'],
    assigned['Heideck'], at_silva['Heideck'],
    assigned['Knutson'], at_silva['Knutson'],
    Not(assigned['Lai']),  # Lai not assigned
    Not(assigned['Mays'])  # Mays not assigned
)

# Option B: Frost, Gonzalez, Heideck at Silva
opt_b_constr = And(
    assigned['Frost'], at_silva['Frost'],
    assigned['Gonzalez'], at_silva['Gonzalez'],
    assigned['Heideck'], at_silva['Heideck'],
    Not(assigned['Knutson']),
    Not(assigned['Lai']),
    Not(assigned['Mays'])
)

# Option C: Gonzalez, Knutson at Silva
opt_c_constr = And(
    Not(assigned['Frost']),
    assigned['Gonzalez'], at_silva['Gonzalez'],
    Not(assigned['Heideck']),
    assigned['Knutson'], at_silva['Knutson'],
    Not(assigned['Lai']),
    Not(assigned['Mays'])
)

# Option D: Heideck, Lai at Silva
opt_d_constr = And(
    Not(assigned['Frost']),
    Not(assigned['Gonzalez']),
    assigned['Heideck'], at_silva['Heideck'],
    Not(assigned['Knutson']),
    assigned['Lai'], at_silva['Lai'],
    Not(assigned['Mays'])
)

# Option E: Knutson, Mays at Silva
opt_e_constr = And(
    Not(assigned['Frost']),
    Not(assigned['Gonzalez']),
    Not(assigned['Heideck']),
    assigned['Knutson'], at_silva['Knutson'],
    Not(assigned['Lai']),
    assigned['Mays'], at_silva['Mays']
)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for p in photographers:
            if is_true(m.evaluate(assigned[p])):
                location = "Silva" if is_true(m.evaluate(at_silva[p])) else "Thorne"
                print(f"  {p} -> {location}")
            else:
                print(f"  {p} -> Not assigned")
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