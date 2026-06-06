from z3 import *

# We have 6 photographers: Frost, Gonzalez, Heideck, Knutson, Lai, Mays
# Two ceremonies: Silva (S) and Thorne (T)
# Each photographer is either unassigned (0), assigned to Silva (1), or assigned to Thorne (2)

# Use integer variables: 0 = unassigned, 1 = Silva, 2 = Thorne
F, G, H, K, L, M = Ints('F G H K L M')
photographers = [F, G, H, K, L, M]
names = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']

solver = Solver()

# Domain: each photographer is 0, 1, or 2
for p in photographers:
    solver.add(Or(p == 0, p == 1, p == 2))

# At least two photographers assigned to each ceremony
# Count assigned to Silva (value == 1)
solver.add(Sum([If(p == 1, 1, 0) for p in photographers]) >= 2)
# Count assigned to Thorne (value == 2)
solver.add(Sum([If(p == 2, 1, 0) for p in photographers]) >= 2)

# Constraint 1: Frost must be assigned together with Heideck to one of the ceremonies.
# They must be assigned to the same ceremony (both 1 or both 2), and neither can be 0.
solver.add(F != 0)
solver.add(H != 0)
solver.add(F == H)

# Constraint 2: If Lai and Mays are both assigned, it must be to different ceremonies.
# "Both assigned" means neither is 0. If both assigned, then L != M.
solver.add(Implies(And(L != 0, M != 0), L != M))

# Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne.
solver.add(Implies(G == 1, L == 2))

# Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it.
# "Knutson is not assigned to Thorne" means K != 2 (could be 0 or 1)
# "both Heideck and Mays must be assigned to it" means H == 2 and M == 2
solver.add(Implies(K != 2, And(H == 2, M == 2)))

# Now we need to find which photographers MUST be assigned (i.e., appear in ALL valid solutions).
# We'll enumerate all solutions and find the intersection.

# First, let's find all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {p: m.eval(p, model_completion=True).as_long() for p in photographers}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([p != sol[p] for p in photographers]))

print(f"Total solutions found: {len(solutions)}")

if len(solutions) == 0:
    print("STATUS: unsat")
    print("Refine: No solutions found")
else:
    # Find photographers who are assigned (value != 0) in ALL solutions
    must_be_assigned = []
    for i, p in enumerate(photographers):
        assigned_in_all = all(sol[p] != 0 for sol in solutions)
        if assigned_in_all:
            must_be_assigned.append(names[i])
    
    print(f"Photographers who must be assigned: {must_be_assigned}")
    
    # Now evaluate each answer choice
    # Each choice claims a list of photographers who must be assigned.
    # We need to check: is the choice's list exactly the set of must-be-assigned photographers?
    # The question asks: "Which one of the following is a complete and accurate list of all of the photographers who must be assigned?"
    # So we need to check if the choice's set equals the must_be_assigned set.
    
    opt_a = {"Frost", "Heideck"}
    opt_b = {"Frost", "Heideck", "Knutson"}
    opt_c = {"Frost", "Heideck", "Knutson", "Lai"}
    opt_d = {"Frost", "Gonzalez", "Heideck"}
    opt_e = {"Frost", "Gonzalez", "Heideck", "Mays"}
    
    must_set = set(must_be_assigned)
    
    found_options = []
    for letter, constr_set in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
        if constr_set == must_set:
            found_options.append(letter)
    
    if len(found_options) == 1:
        print("STATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")