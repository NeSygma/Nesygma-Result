from z3 import *

# Boolean variables for each scientist
F, G, H = Bools('F G H')  # botanists
K, L, M = Bools('K L M')  # chemists
P, Q, R = Bools('P Q R')  # zoologists

# We'll test each option separately with a fresh solver
# Each solver gets the base constraints + G and H are selected

def get_base_solver():
    s = Solver()
    
    # G and H are selected (given in the question)
    s.add(G)
    s.add(H)
    
    # Condition 1: At least one of each type
    s.add(Or(F, G, H))  # at least one botanist (already satisfied by G,H)
    s.add(Or(K, L, M))  # at least one chemist
    s.add(Or(P, Q, R))  # at least one zoologist
    
    # Condition 2: If more than one botanist, then at most one zoologist
    # With G and H selected, we already have >1 botanist, so at most 1 zoologist
    more_than_one_botanist = Or(And(F, G), And(F, H), And(G, H))
    at_least_two_zoologists = Or(And(P, Q), And(P, R), And(Q, R))
    s.add(Implies(more_than_one_botanist, Not(at_least_two_zoologists)))
    
    # Condition 3: F and K cannot both be selected
    s.add(Not(And(F, K)))
    
    # Condition 4: K and M cannot both be selected
    s.add(Not(And(K, M)))
    
    # Condition 5: If M is selected, both P and R must be selected
    s.add(Implies(M, And(P, R)))
    
    return s

# For each option (X, Y), we check if there exists a valid configuration
# where NEITHER X nor Y is selected.
# If UNSAT (no such configuration), then at least one MUST be selected,
# meaning the option is the correct answer.

found_options = []

# Option A: F or K
s = get_base_solver()
s.add(Not(F), Not(K))
if s.check() == unsat:
    found_options.append("A")

# Option B: F or M
s = get_base_solver()
s.add(Not(F), Not(M))
if s.check() == unsat:
    found_options.append("B")

# Option C: K or M
s = get_base_solver()
s.add(Not(K), Not(M))
if s.check() == unsat:
    found_options.append("C")

# Option D: M or Q
s = get_base_solver()
s.add(Not(M), Not(Q))
if s.check() == unsat:
    found_options.append("D")

# Option E: P or Q
s = get_base_solver()
s.add(Not(P), Not(Q))
if s.check() == unsat:
    found_options.append("E")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")