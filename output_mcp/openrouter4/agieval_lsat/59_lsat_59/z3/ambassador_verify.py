from z3 import *

def is_assigned(person_idx, assign_vars):
    return Or([assign_vars[person_idx][c] for c in range(3)])

def get_all_solutions(constraints_list, assign_vars):
    solver = Solver()
    
    for c in range(3):
        solver.add(Sum([If(assign_vars[p][c], 1, 0) for p in range(5)]) == 1)
    
    for p in range(5):
        solver.add(Sum([If(assign_vars[p][c], 1, 0) for c in range(3)]) <= 1)
    
    solver.add(Sum([If(is_assigned(p, assign_vars), 1, 0) for p in range(5)]) == 3)
    
    for c in constraints_list:
        solver.add(c)
    
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = {}
        for p in range(5):
            for c in range(3):
                sol[(p, c)] = m.eval(assign_vars[p][c], model_completion=True)
        solutions.append(sol)
        
        solver.add(Or([assign_vars[p][c] != m.eval(assign_vars[p][c], model_completion=True) for p in range(5) for c in range(3)]))
    
    return solutions

assign = [[Bool(f'assign_{p}_{c}') for c in range(3)] for p in range(5)]

# Constraint 1: Either Kayne or Novetzke, but not both
c1 = And(Or(is_assigned(1, assign), is_assigned(3, assign)), Not(And(is_assigned(1, assign), is_assigned(3, assign))))

# Constraint 2: If Jaramillo is assigned, then Kayne is assigned
c2 = Implies(is_assigned(0, assign), is_assigned(1, assign))

# Constraint 3: If Ong is Venezuela, Kayne is not Yemen
c3 = Implies(assign[4][0], Not(assign[1][1]))

# Constraint 4: If Landon is assigned, it's to Zambia
c4 = Implies(is_assigned(2, assign), assign[2][2])

# Let's also check Option E more carefully
opt_e = Not(And(is_assigned(3, assign), is_assigned(4, assign)))  # Not (Novetzke AND Ong)

# Option D
opt_d = Not(And(is_assigned(0, assign), is_assigned(3, assign)))  # Not (Jaramillo AND Novetzke)

original_sols = get_all_solutions([c1, c2, c3, c4], assign)
opt_d_sols = get_all_solutions([c1, opt_d, c3, c4], assign)
opt_e_sols = get_all_solutions([c1, opt_e, c3, c4], assign)

print("Original solutions:")
for sol in original_sols:
    persons = []
    for p in range(5):
        assigned_to = None
        for c in range(3):
            if sol[(p, c)]:
                assigned_to = c
                break
        person_names = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]
        country_names = ["Venezuela", "Yemen", "Zambia"]
        if assigned_to is not None:
            persons.append(f"{person_names[p]}:{country_names[assigned_to]}")
        else:
            persons.append(f"{person_names[p]}:unassigned")
    print("  " + ", ".join(persons))

print("\nOption E solutions:")
for sol in opt_e_sols:
    persons = []
    for p in range(5):
        assigned_to = None
        for c in range(3):
            if sol[(p, c)]:
                assigned_to = c
                break
        person_names = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]
        country_names = ["Venezuela", "Yemen", "Zambia"]
        if assigned_to is not None:
            persons.append(f"{person_names[p]}:{country_names[assigned_to]}")
        else:
            persons.append(f"{person_names[p]}:unassigned")
    print("  " + ", ".join(persons))

# Now use the LSAT skeleton to confirm
print("\n\nLSAT Multiple Choice Skeleton:")
solver = Solver()
# Base constraints
for c in range(3):
    solver.add(Sum([If(assign[p][c], 1, 0) for p in range(5)]) == 1)
for p in range(5):
    solver.add(Sum([If(assign[p][c], 1, 0) for c in range(3)]) <= 1)
solver.add(Sum([If(is_assigned(p, assign), 1, 0) for p in range(5)]) == 3)
# Original constraints 1, 3, 4 (keeping c2 out since we're substituting)
solver.add(c1)
solver.add(c3)
solver.add(c4)

found_options = []
for letter, constr in [("A", Implies(is_assigned(1, assign), is_assigned(0, assign))),
                       ("B", Implies(And(is_assigned(2, assign), is_assigned(4, assign)), is_assigned(3, assign))),
                       ("C", Implies(Not(is_assigned(4, assign)), is_assigned(1, assign))),
                       ("D", Not(And(is_assigned(0, assign), is_assigned(3, assign)))),
                       ("E", Not(And(is_assigned(3, assign), is_assigned(4, assign))))]:
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