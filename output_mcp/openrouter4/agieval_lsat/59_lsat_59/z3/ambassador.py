from z3 import *

def is_assigned(person_idx, assign_vars):
    """Return a Bool indicating whether person_idx is assigned to any country."""
    return Or([assign_vars[person_idx][c] for c in range(3)])

def exactly_one_of(p1, p2, assign_vars):
    """Exactly one of two persons is assigned."""
    a1 = is_assigned(p1, assign_vars)
    a2 = is_assigned(p2, assign_vars)
    return And(Or(a1, a2), Not(And(a1, a2)))

def get_all_solutions(constraints_list, assign_vars):
    """Get all solutions for a given set of constraints."""
    solver = Solver()
    
    # Base constraints: each country gets exactly one ambassador
    for c in range(3):
        solver.add(Sum([If(assign_vars[p][c], 1, 0) for p in range(5)]) == 1)
    
    # Each person gets at most one assignment
    for p in range(5):
        solver.add(Sum([If(assign_vars[p][c], 1, 0) for c in range(3)]) <= 1)
    
    # Exactly 3 people assigned
    solver.add(Sum([If(is_assigned(p, assign_vars), 1, 0) for p in range(5)]) == 3)
    
    # Add the additional constraints
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
        
        # Block this solution
        solver.add(Or([assign_vars[p][c] != m.eval(assign_vars[p][c], model_completion=True) for p in range(5) for c in range(3)]))
    
    return solutions

# People: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong
# Countries: 0=Venezuela, 1=Yemen, 2=Zambia

assign = [[Bool(f'assign_{p}_{c}') for c in range(3)] for p in range(5)]

# Original constraints
# Constraint 1: Either Kayne or Novetzke, but not both
c1 = exactly_one_of(1, 3, assign)

# Constraint 2: If Jaramillo is assigned, then Kayne is assigned
c2 = Implies(is_assigned(0, assign), is_assigned(1, assign))

# Constraint 3: If Ong is Venezuela, Kayne is not Yemen
c3 = Implies(assign[4][0], Not(assign[1][1]))

# Constraint 4: If Landon is assigned, it's to Zambia
c4 = Implies(is_assigned(2, assign), assign[2][2])

original_constraints = [c1, c2, c3, c4]
original_solutions = get_all_solutions(original_constraints, assign)
print(f"Original solutions count: {len(original_solutions)}")
for i, sol in enumerate(original_solutions):
    print(f"  Solution {i+1}:")
    for p in range(5):
        assigned_to = None
        for c in range(3):
            if sol[(p, c)]:
                assigned_to = c
                break
        person_names = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]
        country_names = ["Venezuela", "Yemen", "Zambia"]
        if assigned_to is not None:
            print(f"    {person_names[p]} -> {country_names[assigned_to]}")
        else:
            print(f"    {person_names[p]} -> unassigned")

print()

# Now test each option
options = {
    "A": Implies(is_assigned(1, assign), is_assigned(0, assign)),  # Kayne -> Jaramillo
    "B": Implies(And(is_assigned(2, assign), is_assigned(4, assign)), is_assigned(3, assign)),  # (Landon AND Ong) -> Novetzke
    "C": Implies(Not(is_assigned(4, assign)), is_assigned(1, assign)),  # Not Ong -> Kayne
    "D": Not(And(is_assigned(0, assign), is_assigned(3, assign))),  # Not (Jaramillo AND Novetzke)
    "E": Not(And(is_assigned(3, assign), is_assigned(4, assign)))  # Not (Novetzke AND Ong)
}

for letter, constr in options.items():
    modified_constraints = [c1, constr, c3, c4]  # Replace c2 with the option
    solutions = get_all_solutions(modified_constraints, assign)
    print(f"Option {letter} solutions count: {len(solutions)}")
    # Check if solution sets are identical
    if len(solutions) != len(original_solutions):
        print(f"  -> Different count, so NOT equivalent")
    else:
        # Compare solution sets (they should be identical sets)
        # Convert to sets of tuples for comparison
        orig_set = set()
        for sol in original_solutions:
            orig_set.add(tuple(sorted([(p, c, bool(sol[(p, c)])) for p in range(5) for c in range(3)])))
        
        opt_set = set()
        for sol in solutions:
            opt_set.add(tuple(sorted([(p, c, bool(sol[(p, c)])) for p in range(5) for c in range(3)])))
        
        if orig_set == opt_set:
            print(f"  -> EXACTLY EQUIVALENT (same solution set)!")
        else:
            print(f"  -> Different solutions, so NOT equivalent")
            # Show differences
            only_in_orig = orig_set - opt_set
            only_in_opt = opt_set - orig_set
            if only_in_orig:
                print(f"  -> Only in original: {len(only_in_orig)} solutions")
            if only_in_opt:
                print(f"  -> Only in option: {len(only_in_opt)} solutions")
    print()