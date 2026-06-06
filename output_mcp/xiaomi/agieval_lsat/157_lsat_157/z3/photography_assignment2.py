from z3 import *

solver = Solver()

photographers = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

# assigned[p] = True if photographer p is assigned to some ceremony
assigned = {p: Bool(f'assigned_{p}') for p in photographers}

# at_silva[p] = True if photographer p is at Silva, False if at Thorne
at_silva = {p: Bool(f'at_silva_{p}') for p in photographers}

# Constraint: At least 2 photographers at Silva
silva_count = Sum([If(And(assigned[p], at_silva[p]), 1, 0) for p in photographers])
solver.add(silva_count >= 2)

# Constraint: At least 2 photographers at Thorne
thorne_count = Sum([If(And(assigned[p], Not(at_silva[p])), 1, 0) for p in photographers])
solver.add(thorne_count >= 2)

# Constraint: Frost must be assigned together with Heideck to one ceremony
solver.add(Implies(assigned['Frost'], And(assigned['Heideck'], at_silva['Frost'] == at_silva['Heideck'])))
solver.add(Implies(assigned['Heideck'], And(assigned['Frost'], at_silva['Frost'] == at_silva['Heideck'])))

# Constraint: If Lai and Mays are both assigned, they must be at different ceremonies
solver.add(Implies(And(assigned['Lai'], assigned['Mays']), at_silva['Lai'] != at_silva['Mays']))

# Constraint: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(And(assigned['Gonzalez'], at_silva['Gonzalez']), And(assigned['Lai'], Not(at_silva['Lai']))))

# Constraint: If Knutson is NOT assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
solver.add(Implies(Or(Not(assigned['Knutson']), at_silva['Knutson']), 
                   And(assigned['Heideck'], Not(at_silva['Heideck']), assigned['Mays'], Not(at_silva['Mays']))))

# Now test each option for the COMPLETE assignment to Silva University
# The option specifies EXACTLY who is at Silva. Others may be at Thorne or unassigned.

# Option A: Frost, Gonzalez, Heideck, Knutson at Silva (these 4 at Silva, others not at Silva)
opt_a_constr = And(
    assigned['Frost'], at_silva['Frost'],
    assigned['Gonzalez'], at_silva['Gonzalez'],
    assigned['Heideck'], at_silva['Heideck'],
    assigned['Knutson'], at_silva['Knutson'],
    # Lai and Mays NOT at Silva (could be at Thorne or unassigned)
    Not(And(assigned['Lai'], at_silva['Lai'])),
    Not(And(assigned['Mays'], at_silva['Mays']))
)

# Option B: Frost, Gonzalez, Heideck at Silva
opt_b_constr = And(
    assigned['Frost'], at_silva['Frost'],
    assigned['Gonzalez'], at_silva['Gonzalez'],
    assigned['Heideck'], at_silva['Heideck'],
    Not(And(assigned['Knutson'], at_silva['Knutson'])),
    Not(And(assigned['Lai'], at_silva['Lai'])),
    Not(And(assigned['Mays'], at_silva['Mays']))
)

# Option C: Gonzalez, Knutson at Silva
opt_c_constr = And(
    Not(And(assigned['Frost'], at_silva['Frost'])),
    assigned['Gonzalez'], at_silva['Gonzalez'],
    Not(And(assigned['Heideck'], at_silva['Heideck'])),
    assigned['Knutson'], at_silva['Knutson'],
    Not(And(assigned['Lai'], at_silva['Lai'])),
    Not(And(assigned['Mays'], at_silva['Mays']))
)

# Option D: Heideck, Lai at Silva
opt_d_constr = And(
    Not(And(assigned['Frost'], at_silva['Frost'])),
    Not(And(assigned['Gonzalez'], at_silva['Gonzalez'])),
    assigned['Heideck'], at_silva['Heideck'],
    Not(And(assigned['Knutson'], at_silva['Knutson'])),
    assigned['Lai'], at_silva['Lai'],
    Not(And(assigned['Mays'], at_silva['Mays']))
)

# Option E: Knutson, Mays at Silva
opt_e_constr = And(
    Not(And(assigned['Frost'], at_silva['Frost'])),
    Not(And(assigned['Gonzalez'], at_silva['Gonzalez'])),
    Not(And(assigned['Heideck'], at_silva['Heideck'])),
    assigned['Knutson'], at_silva['Knutson'],
    Not(And(assigned['Lai'], at_silva['Lai'])),
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
    else:
        print(f"Option {letter} is UNSAT")
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