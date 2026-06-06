from z3 import *

# Photographers
photographers = ['F', 'G', 'H', 'K', 'L', 'M']
# Ceremonies: 0=Silva, 1=Thorne, 2=None
S, T, N = 0, 1, 2

def get_base_constraints(assign):
    constraints = []
    # Each photographer assigned to S, T, or N
    for p in photographers:
        constraints.append(Or(assign[p] == S, assign[p] == T, assign[p] == N))
    
    # At least two photographers at S and T
    count_s = Sum([If(assign[p] == S, 1, 0) for p in photographers])
    count_t = Sum([If(assign[p] == T, 1, 0) for p in photographers])
    constraints.append(count_s >= 2)
    constraints.append(count_t >= 2)
    
    # Frost and Heideck assigned together to one of the ceremonies
    constraints.append(assign['F'] == assign['H'])
    constraints.append(Or(assign['F'] == S, assign['F'] == T))
    
    # If Lai and Mays are both assigned, they must be to different ceremonies
    constraints.append(Implies(And(assign['L'] != N, assign['M'] != N), assign['L'] != assign['M']))
    
    # If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
    constraints.append(Implies(assign['G'] == S, assign['L'] == T))
    
    return constraints

def get_orig_constraint(assign):
    # If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to it
    return Implies(assign['K'] != T, And(assign['H'] == T, assign['M'] == T))

# Options
def get_opt_a(assign):
    # If Knutson is assigned to Silva, then Heideck and Mays cannot both be assigned to that ceremony
    return Implies(assign['K'] == S, Not(And(assign['H'] == S, assign['M'] == S)))

def get_opt_b(assign):
    # If Knutson is assigned to Silva, then Lai must also be assigned to that ceremony
    return Implies(assign['K'] == S, assign['L'] == S)

def get_opt_c(assign):
    # Unless Knutson is assigned to Thorne, both Frost and Mays must be assigned to that ceremony
    # "Unless P, Q" is equivalent to "If not P, then Q"
    # "Unless K == T, F == T and M == T" -> "If K != T, then F == T and M == T"
    return Implies(assign['K'] != T, And(assign['F'] == T, assign['M'] == T))

def get_opt_d(assign):
    # Unless Knutson is assigned to Thorne, Heideck cannot be assigned to the same ceremony as Lai
    # "If K != T, then H != L"
    return Implies(assign['K'] != T, assign['H'] != assign['L'])

def get_opt_e(assign):
    # Unless either Heideck or Mays is assigned to Thorne, Knutson must be assigned to that ceremony
    # "If not (H == T or M == T), then K == T"
    # "If H != T and M != T, then K == T"
    return Implies(And(assign['H'] != T, assign['M'] != T), assign['K'] == T)

# We need to check if the original constraint and the option constraint are logically equivalent
# Two constraints C1 and C2 are equivalent if (C1 <-> C2) is a tautology,
# which means (C1 != C2) is unsatisfiable.
# Or, more simply, for all possible assignments, C1 is true iff C2 is true.
# We can check this by finding if there exists an assignment that satisfies the base constraints
# AND (C1 != C2). If no such assignment exists, they are equivalent.

def check_equivalence(opt_func):
    solver = Solver()
    assign = {p: Int(p) for p in photographers}
    solver.add(get_base_constraints(assign))
    
    c1 = get_orig_constraint(assign)
    c2 = opt_func(assign)
    
    # Check if there exists an assignment satisfying base constraints where c1 != c2
    solver.add(c1 != c2)
    
    return solver.check() == unsat

options = [
    ("A", get_opt_a),
    ("B", get_opt_b),
    ("C", get_opt_c),
    ("D", get_opt_d),
    ("E", get_opt_e)
]

found_options = []
for letter, opt_func in options:
    if check_equivalence(opt_func):
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