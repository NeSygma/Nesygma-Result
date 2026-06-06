from z3 import *

solver = Solver()

# Countries: 1=Venezuela, 2=Yemen, 3=Zambia, 0=unassigned
candidates = ['J', 'K', 'L', 'N', 'O']
assign = {c: Int(f'assign_{c}') for c in candidates}

# Domain constraints
for c in candidates:
    solver.add(Or(assign[c] == 0, assign[c] == 1, assign[c] == 2, assign[c] == 3))

# Exactly one ambassador per country
for country in [1,2,3]:
    solver.add(Sum([If(assign[c] == country, 1, 0) for c in candidates]) == 1)

# No ambassador assigned to more than one country is ensured by single int per candidate

# Constraint 1: Exactly one of Kayne (K) or Novetzke (N) is assigned (xor)
# Means (K assigned) xor (N assigned)
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
opt_A = (assign['J'] == 1)          # J assigned to Venezuela
opt_B = (assign['L'] == 3)          # L assigned to Zambia
opt_C = (assign['O'] == 3)          # O assigned to Zambia
opt_D = (assign['J'] == 0)          # J not assigned
opt_E = (assign['O'] == 0)          # O not assigned

options = [
    ("A", opt_A),
    ("B", opt_B),
    ("C", opt_C),
    ("D", opt_D),
    ("E", opt_E)
]

found_options = []
for letter, expr in options:
    # Build constraint: this option true, all other options false
    other_false = []
    for l2, expr2 in options:
        if l2 != letter:
            other_false.append(Not(expr2))
    solver.push()
    solver.add(expr)
    solver.add(And(other_false))
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")