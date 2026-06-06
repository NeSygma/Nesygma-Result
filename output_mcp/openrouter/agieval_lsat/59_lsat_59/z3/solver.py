from z3 import *

# Candidates indices
J, K, L, N, O = 0, 1, 2, 3, 4
candidates = [J, K, L, N, O]

# Helper to get assigned predicate for a candidate

def assigned(solver, var, cand):
    return Or(var[0] == cand, var[1] == cand, var[2] == cand)

# Base constraints function returning solver with base (excluding J->K)
def base_solver():
    s = Solver()
    # Variables for countries: V, Y, Z
    V = Int('V')
    Y = Int('Y')
    Z = Int('Z')
    vars = [V, Y, Z]
    # Domain constraints
    for v in vars:
        s.add(v >= 0, v <= 4)
    # All different (one ambassador per country, no repeats)
    s.add(Distinct(V, Y, Z))
    # Helper lambdas for assigned
    def is_assigned(c):
        return Or(V == c, Y == c, Z == c)
    # Constraint 1: Exactly one of Kayne or Novetzke assigned, not both
    s.add(If(is_assigned(K), Not(is_assigned(N)), is_assigned(N)))  # XOR
    # Constraint 3: If Ong assigned to Venezuela, Kayne not assigned to Yemen
    s.add(Implies(V == O, Not(Y == K)))
    # Constraint 4: If Landon assigned, it is to Zambia (Z)
    # So Landon cannot be V or Y, and if assigned then Z == L
    s.add(Not(V == L))
    s.add(Not(Y == L))
    s.add(Implies(is_assigned(L), Z == L))
    return s, vars, is_assigned

# Original constraint J -> K
def original_constraint(is_assigned):
    return Implies(is_assigned(J), is_assigned(K))

# Option constraints definitions

def opt_A(is_assigned):
    return Implies(is_assigned(K), is_assigned(J))

def opt_B(is_assigned):
    return Implies(And(is_assigned(L), is_assigned(O)), is_assigned(N))

def opt_C(is_assigned):
    return Implies(Not(is_assigned(O)), is_assigned(K))

def opt_D(is_assigned):
    return Not(And(is_assigned(J), is_assigned(N)))

def opt_E(is_assigned):
    return Not(And(is_assigned(N), is_assigned(O)))

options = {
    "A": opt_A,
    "B": opt_B,
    "C": opt_C,
    "D": opt_D,
    "E": opt_E,
}

# Function to collect all models (as tuples) for given extra constraint
def collect_models(extra_constr_func):
    s, vars, is_assigned = base_solver()
    # add extra constraint (could be original or option)
    s.add(extra_constr_func(is_assigned))
    models = set()
    while s.check() == sat:
        m = s.model()
        tup = (m[vars[0]].as_long(), m[vars[1]].as_long(), m[vars[2]].as_long())
        models.add(tup)
        # block this model
        s.add(Or([vars[i] != m[vars[i]] for i in range(3)]))
    return models

# Collect models for original constraint
orig_models = collect_models(original_constraint)

found_options = []
for letter, opt_func in options.items():
    opt_models = collect_models(opt_func)
    if opt_models == orig_models:
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