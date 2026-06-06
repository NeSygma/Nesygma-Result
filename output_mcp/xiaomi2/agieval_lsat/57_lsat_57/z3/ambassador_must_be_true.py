from z3 import *

# Base constraints setup
def create_base_solver():
    solver = Solver()
    J, K, L, N, O = Ints('J K L N O')
    candidates = [J, K, L, N, O]
    
    for c in candidates:
        solver.add(And(c >= 0, c <= 3))
    
    solver.add(Sum([If(c != 0, 1, 0) for c in candidates]) == 3)
    
    for country in [1, 2, 3]:
        solver.add(Sum([If(c == country, 1, 0) for c in candidates]) == 1)
    
    for i in range(len(candidates)):
        for j in range(i+1, len(candidates)):
            solver.add(Implies(And(candidates[i] != 0, candidates[j] != 0), candidates[i] != candidates[j]))
    
    # Constraint 1: Exactly one of Kayne or Novetzke is assigned
    solver.add(Xor(K != 0, N != 0))
    
    # Constraint 2: If Jaramillo assigned, then Kayne assigned
    solver.add(Implies(J != 0, K != 0))
    
    # Constraint 3: If Ong assigned to Venezuela, Kayne not assigned to Yemen
    solver.add(Implies(O == 1, K != 2))
    
    # Constraint 4: If Landon assigned, it is to Zambia
    solver.add(Implies(L != 0, L == 3))
    
    # Premise: Kayne assigned to Yemen
    solver.add(K == 2)
    
    return solver, J, K, L, N, O

# Define answer options
options = [
    ("A", lambda J,K,L,N,O: J == 1),   # Jaramillo -> Venezuela
    ("B", lambda J,K,L,N,O: L == 3),   # Landon -> Zambia
    ("C", lambda J,K,L,N,O: O == 3),   # Ong -> Zambia
    ("D", lambda J,K,L,N,O: J == 0),   # Jaramillo not assigned
    ("E", lambda J,K,L,N,O: O == 0),   # Ong not assigned
]

must_be_true = []

for letter, opt_fn in options:
    # Check if negation of option is unsatisfiable (i.e., option must be true)
    s = Solver()
    J, K, L, N, O = Ints('J K L N O')
    candidates = [J, K, L, N, O]
    
    for c in candidates:
        s.add(And(c >= 0, c <= 3))
    
    s.add(Sum([If(c != 0, 1, 0) for c in candidates]) == 3)
    
    for country in [1, 2, 3]:
        s.add(Sum([If(c == country, 1, 0) for c in candidates]) == 1)
    
    for i in range(len(candidates)):
        for j in range(i+1, len(candidates)):
            s.add(Implies(And(candidates[i] != 0, candidates[j] != 0), candidates[i] != candidates[j]))
    
    s.add(Xor(K != 0, N != 0))
    s.add(Implies(J != 0, K != 0))
    s.add(Implies(O == 1, K != 2))
    s.add(Implies(L != 0, L == 3))
    s.add(K == 2)
    
    # Add NEGATION of the option
    s.add(Not(opt_fn(J, K, L, N, O)))
    
    result = s.check()
    if result == unsat:
        must_be_true.append(letter)
        print(f"Option {letter}: MUST BE TRUE (negation is unsat)")
    else:
        print(f"Option {letter}: NOT necessarily true (negation is sat)")
        if result == sat:
            m = s.model()
            country_map = {0: "unassigned", 1: "Venezuela", 2: "Yemen", 3: "Zambia"}
            for c, name in [(J, "Jaramillo"), (K, "Kayne"), (L, "Landon"), (N, "Novetzke"), (O, "Ong")]:
                print(f"    {name} -> {country_map[m[c].as_long()]}")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")