from z3 import *

# Base constraints
def add_base_constraints(solver, reviews):
    # Each student reviews at least one play
    for i in range(5):
        solver.add(Or(reviews[i][0], reviews[i][1], reviews[i][2]))
    
    # Count of plays each student reviews
    count = [Int(f"count_{i}") for i in range(5)]
    for i in range(5):
        solver.add(count[i] == Sum([If(reviews[i][j], 1, 0) for j in range(3)]))
    
    # Condition 1: Kramer and Lopez each review fewer plays than Megregian
    solver.add(count[1] < count[3])  # Kramer < Megregian
    solver.add(count[2] < count[3])  # Lopez < Megregian
    
    # Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
    for j in range(3):
        solver.add(Implies(reviews[0][j], Not(reviews[2][j])))
        solver.add(Implies(reviews[0][j], Not(reviews[3][j])))
    
    # Condition 3: Kramer and O'Neill both review Tamerlane
    solver.add(reviews[1][1] == True)
    solver.add(reviews[4][1] == True)
    
    # Condition 4: Exactly two students review exactly the same play(s)
    pair_eq = {}
    for i in range(5):
        for k in range(i+1, 5):
            pair_eq[(i,k)] = And([reviews[i][j] == reviews[k][j] for j in range(3)])
    
    solver.add(Sum([If(pair_eq[(i,k)], 1, 0) for i in range(5) for k in range(i+1, 5)]) == 1)
    
    # Additional condition: Jiang does NOT review Tamerlane
    solver.add(reviews[0][1] == False)

# Test each option: check if negation is unsatisfiable (option must be true)
options = [
    ("A", lambda r: r[0][0]),  # Jiang reviews Sunset
    ("B", lambda r: r[2][2]),  # Lopez reviews Undulation
    ("C", lambda r: r[3][0]),  # Megregian reviews Sunset
    ("D", lambda r: r[3][1]),  # Megregian reviews Tamerlane
    ("E", lambda r: r[4][2]),  # O'Neill reviews Undulation
]

must_be_true = []
for letter, opt_fn in options:
    s = Solver()
    reviews = [[Bool(f"reviews_{i}_{j}") for j in range(3)] for i in range(5)]
    add_base_constraints(s, reviews)
    s.add(Not(opt_fn(reviews)))  # Try to find a model where option is FALSE
    if s.check() == unsat:
        must_be_true.append(letter)

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")