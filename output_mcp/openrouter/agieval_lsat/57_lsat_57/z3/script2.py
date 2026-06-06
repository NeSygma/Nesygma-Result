from z3 import *

solver = Solver()

# Countries: 1=Venezuela, 2=Yemen, 3=Zambia, 0=unassigned
candidates = ['J', 'K', 'L', 'N', 'O']
assign = {c: Int(f'assign_{c}') for c in candidates}

# Domain constraints: each candidate assigned to 0..3
for c in candidates:
    solver.add(Or(assign[c] == 0, assign[c] == 1, assign[c] == 2, assign[c] == 3))

# Exactly one ambassador per country
for country in [1,2,3]:
    solver.add(Sum([If(assign[c] == country, 1, 0) for c in candidates]) == 1)

# Constraint 1: Exactly one of Kayne (K) or Novetzke (N) is assigned (xor)
K_assigned = assign['K'] != 0
N_assigned = assign['N'] != 0
solver.add(Xor(K_assigned, N_assigned))

# Constraint 2: If J assigned then K assigned
solver.add(Implies(assign['J'] != 0, K_assigned))

# Constraint 3: If O assigned to Venezuela then K not assigned to Yemen
solver.add(Implies(assign['O'] == 1, assign['K'] != 2))

# Constraint 4: If L assigned then it is to Zambia
solver.add(Implies(assign['L'] != 0, assign['L'] == 3))

# Condition from question: Kayne assigned to Yemen
solver.add(assign['K'] == 2)

# Define option expressions
opt_A = (assign['J'] == 1)   # J assigned to Venezuela
opt_B = (assign['L'] == 3)   # L assigned to Zambia
opt_C = (assign['O'] == 3)   # O assigned to Zambia
opt_D = (assign['J'] == 0)   # J not assigned
opt_E = (assign['O'] == 0)   # O not assigned

options = [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]

forced_options = []
for letter, expr in options:
    solver.push()
    # If expr is false, i.e., Not(expr), leads to unsat, then expr must be true
    solver.add(Not(expr))
    if solver.check() == unsat:
        forced_options.append(letter)
    solver.pop()

if len(forced_options) == 1:
    print("STATUS: sat")
    print(f"answer:{forced_options[0]}")
elif len(forced_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple forced options {forced_options}")
else:
    print("STATUS: unsat")
    print("Refine: No forced option found")