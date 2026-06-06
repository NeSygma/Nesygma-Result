from z3 import *

# Candidates: J=1, K=2, L=3, N=4, O=5
# Countries: V=1, Y=2, Z=3
# 0 means None

solver = Solver()

# Variables for each candidate's assignment
J, K, L, N, O = Ints('J K L N O')
candidates = [J, K, L, N, O]
for c in candidates:
    solver.add(c >= 0, c <= 3)

# Variables for each country's assigned candidate
V, Y, Z = Ints('V Y Z')
countries = [V, Y, Z]
for c in countries:
    solver.add(c >= 0, c <= 5)

# Link candidates and countries
for cand_idx, cand_var in enumerate(candidates, 1):
    solver.add(
        Or(
            cand_var == 0,
            And(cand_var == 1, V == cand_idx),
            And(cand_var == 2, Y == cand_idx),
            And(cand_var == 3, Z == cand_idx)
        )
    )

for country_idx, country_var in enumerate(countries, 1):
    solver.add(
        Or(
            country_var == 0,
            And(country_var == 1, J == country_idx),
            And(country_var == 2, K == country_idx),
            And(country_var == 3, L == country_idx),
            And(country_var == 4, N == country_idx),
            And(country_var == 5, O == country_idx)
        )
    )

# Constraint 1: Exactly 3 candidates assigned
assigned_count = Sum([If(c != 0, 1, 0) for c in candidates])
solver.add(assigned_count == 3)

# Constraint 2: Either K or N, but not both
solver.add(Xor(K != 0, N != 0))

# Constraint 3: If J is assigned, then K is assigned
solver.add(Implies(J != 0, K != 0))

# Constraint 4: If O is assigned to V, K is not assigned to Y
solver.add(Implies(O == 1, K != 2))

# Constraint 5: If L is assigned, it is to Z
solver.add(Implies(L != 0, L == 3))

# Question condition: K is assigned to Y
solver.add(K == 2)

# Options
options = [
    ("A", J == 1),
    ("B", L == 3),
    ("C", O == 3),
    ("D", J == 0),
    ("E", O == 0)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# We need the one that MUST be true.
# If an option is NOT true in some valid model, it's not the answer.
# So we check: Is the negation of the option unsatisfiable?
# (i.e., is the option true in ALL valid models?)

must_be_true = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")