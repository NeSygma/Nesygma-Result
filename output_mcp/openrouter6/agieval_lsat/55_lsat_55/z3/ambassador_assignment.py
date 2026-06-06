from z3 import *

# Candidate constants
J, K, L, N, O = 0, 1, 2, 3, 4

# Assignment variables for each country
assign_V = Int('assign_V')
assign_Y = Int('assign_Y')
assign_Z = Int('assign_Z')

# Domain constraints: each assignment must be one of the candidates
solver = Solver()
solver.add(assign_V >= 0, assign_V <= 4)
solver.add(assign_Y >= 0, assign_Y <= 4)
solver.add(assign_Z >= 0, assign_Z <= 4)

# All assignments distinct
solver.add(assign_V != assign_Y)
solver.add(assign_V != assign_Z)
solver.add(assign_Y != assign_Z)

# Helper functions to count occurrences of each candidate
def count_of(candidate):
    return Sum([If(assign_V == candidate, 1, 0),
                If(assign_Y == candidate, 1, 0),
                If(assign_Z == candidate, 1, 0)])

count_J = count_of(J)
count_K = count_of(K)
count_L = count_of(L)
count_N = count_of(N)
count_O = count_of(O)

# Constraint 1: Exactly one of Kayne or Novetzke is assigned
solver.add(count_K + count_N == 1)

# Constraint 2: If Jaramillo assigned then Kayne assigned
solver.add(Or(count_J == 0, count_K >= 1))

# Constraint 3: If Ong assigned to Venezuela, Kayne not assigned to Yemen
solver.add(Implies(assign_V == O, assign_Y != K))

# Constraint 4: If Landon assigned, then Landon assigned to Zambia
solver.add(Or(count_L == 0, assign_Z == L))

# Define options: each option is a pair of unassigned candidates
options = [
    ("A", [J, N]),   # Jaramillo and Novetzke
    ("B", [J, O]),   # Jaramillo and Ong
    ("C", [K, L]),   # Kayne and Landon
    ("D", [K, N]),   # Kayne and Novetzke
    ("E", [L, O]),   # Landon and Ong
]

found_options = []
for letter, unassigned in options:
    solver.push()
    # For each unassigned candidate, ensure they are not assigned
    for cand in unassigned:
        solver.add(count_of(cand) == 0)
    # For each assigned candidate (the other three), ensure they are assigned at least once
    all_candidates = [J, K, L, N, O]
    assigned = [c for c in all_candidates if c not in unassigned]
    for cand in assigned:
        solver.add(count_of(cand) >= 1)
    # Check satisfiability
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result according to required skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")