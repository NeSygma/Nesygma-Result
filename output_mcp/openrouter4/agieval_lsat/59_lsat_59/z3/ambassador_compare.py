from z3 import *

def is_assigned(person_idx, assign_vars):
    return Or([assign_vars[person_idx][c] for c in range(3)])

def get_solution_set(constraints_list):
    assign = [[Bool(f'assign_{p}_{c}') for c in range(3)] for p in range(5)]
    solver = Solver()
    
    for c in range(3):
        solver.add(Sum([If(assign[p][c], 1, 0) for p in range(5)]) == 1)
    for p in range(5):
        solver.add(Sum([If(assign[p][c], 1, 0) for c in range(3)]) <= 1)
    solver.add(Sum([If(is_assigned(p, assign), 1, 0) for p in range(5)]) == 3)
    
    for c in constraints_list:
        solver.add(c)
    
    sol_set = set()
    while solver.check() == sat:
        m = solver.model()
        # Create a canonical representation
        rep = []
        for p in range(5):
            assigned_to = None
            for c in range(3):
                if m.eval(assign[p][c], model_completion=True):
                    assigned_to = c
                    break
            rep.append(assigned_to if assigned_to is not None else -1)
        sol_set.add(tuple(rep))
        
        solver.add(Or([assign[p][c] != m.eval(assign[p][c], model_completion=True) for p in range(5) for c in range(3)]))
    
    return sol_set

# Base constraints (shared)
def make_base_constraints(assign):
    return []

# Build the original solution set
assign = [[Bool(f'assign_{p}_{c}') for c in range(3)] for p in range(5)]

# Constraint 1: Either Kayne or Novetzke, but not both
c1 = lambda assign: And(Or(is_assigned(1, assign), is_assigned(3, assign)), 
                         Not(And(is_assigned(1, assign), is_assigned(3, assign))))

# Constraint 2: If Jaramillo is assigned, then Kayne is assigned  
c2 = lambda assign: Implies(is_assigned(0, assign), is_assigned(1, assign))

# Constraint 3: If Ong is Venezuela, Kayne is not Yemen
c3 = lambda assign: Implies(assign[4][0], Not(assign[1][1]))

# Constraint 4: If Landon is assigned, it's to Zambia
c4 = lambda assign: Implies(is_assigned(2, assign), assign[2][2])

# Options
opt_a = lambda assign: Implies(is_assigned(1, assign), is_assigned(0, assign))
opt_b = lambda assign: Implies(And(is_assigned(2, assign), is_assigned(4, assign)), is_assigned(3, assign))
opt_c = lambda assign: Implies(Not(is_assigned(4, assign)), is_assigned(1, assign))
opt_d = lambda assign: Not(And(is_assigned(0, assign), is_assigned(3, assign)))
opt_e = lambda assign: Not(And(is_assigned(3, assign), is_assigned(4, assign)))

# Fresh assign for each call
def get_sols_for(constraint_fns):
    assign = [[Bool(f'assign_{p}_{c}') for c in range(3)] for p in range(5)]
    solver = Solver()
    
    for c in range(3):
        solver.add(Sum([If(assign[p][c], 1, 0) for p in range(5)]) == 1)
    for p in range(5):
        solver.add(Sum([If(assign[p][c], 1, 0) for c in range(3)]) <= 1)
    solver.add(Sum([If(is_assigned(p, assign), 1, 0) for p in range(5)]) == 3)
    
    for fn in constraint_fns:
        solver.add(fn(assign))
    
    sols = set()
    while solver.check() == sat:
        m = solver.model()
        rep = tuple(m.eval(assign[p][c], model_completion=True) for p in range(5) for c in range(3))
        # Also store human-readable version
        readable = []
        person_names = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]
        country_names = ["Venezuela", "Yemen", "Zambia"]
        for p in range(5):
            assigned_to = None
            for c in range(3):
                if m.eval(assign[p][c], model_completion=True):
                    assigned_to = c
                    break
            if assigned_to is not None:
                readable.append(f"{person_names[p]}:{country_names[assigned_to]}")
            else:
                readable.append(f"{person_names[p]}:unassigned")
        sols.add(tuple(sorted(readable)))
        
        solver.add(Or([assign[p][c] != m.eval(assign[p][c], model_completion=True) for p in range(5) for c in range(3)]))
    
    return sols

original_sols = get_sols_for([c1, c2, c3, c4])
print(f"Original count: {len(original_sols)}")

option_d_sols = get_sols_for([c1, opt_d, c3, c4])
print(f"Option D count: {len(option_d_sols)}")

option_e_sols = get_sols_for([c1, opt_e, c3, c4])
print(f"Option E count: {len(option_e_sols)}")

option_a_sols = get_sols_for([c1, opt_a, c3, c4])
print(f"Option A count: {len(option_a_sols)}")

option_b_sols = get_sols_for([c1, opt_b, c3, c4])
print(f"Option B count: {len(option_b_sols)}")

option_c_sols = get_sols_for([c1, opt_c, c3, c4])
print(f"Option C count: {len(option_c_sols)}")

print(f"\nOriginal == Option D: {original_sols == option_d_sols}")
print(f"Original == Option A: {original_sols == option_a_sols}")
print(f"Original == Option B: {original_sols == option_b_sols}")
print(f"Original == Option C: {original_sols == option_c_sols}")
print(f"Original == Option E: {original_sols == option_e_sols}")

# Let's see what's different
if original_sols != option_d_sols:
    print(f"\nIn original but not D: {original_sols - option_d_sols}")
    print(f"In D but not original: {option_d_sols - original_sols}")

if original_sols != option_a_sols:
    print(f"\nIn original but not A: {original_sols - option_a_sols}")
if original_sols != option_b_sols:
    print(f"\nIn original but not B: {original_sols - option_b_sols}")
if original_sols != option_c_sols:
    print(f"\nIn original but not C: {original_sols - option_c_sols}")
if original_sols != option_e_sols:
    print(f"\nIn original but not E: {original_sols - option_e_sols}")