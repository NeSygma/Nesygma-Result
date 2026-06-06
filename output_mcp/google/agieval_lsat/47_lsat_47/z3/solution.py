from z3 import *

# Students: 0:Jiang, 1:Kramer, 2:Lopez, 3:Megregian, 4:O'Neill
# Plays: 0:Sunset, 1:Tamerlane, 2:Undulation
students = range(5)
plays = range(3)

# reviews[s][p] is True if student s reviews play p
reviews = [[Bool(f"r_{s}_{p}") for p in plays] for s in students]

# Each student reviews at least one play
for s in students:
    solver = Solver()
    # (Wait, I need to define the solver outside the loop)

def get_base_constraints():
    solver = Solver()
    
    # Each student reviews at least one play
    for s in students:
        solver.add(Or([reviews[s][p] for p in plays]))
        
    # count[s] = number of plays reviewed by student s
    count = [Sum([If(reviews[s][p], 1, 0) for p in plays]) for s in students]
    
    # set_of_plays[s] = bitmask of plays reviewed by student s
    set_of_plays = [Sum([If(reviews[s][p], 2**p, 0) for p in plays]) for s in students]
    
    # Condition 1: Kramer and Lopez each review fewer plays than Megregian
    solver.add(count[1] < count[3])
    solver.add(count[2] < count[3])
    
    # Condition 2: Neither Lopez nor Megregian reviews any play Jiang reviews
    for p in plays:
        solver.add(Implies(reviews[0][p], And(Not(reviews[2][p]), Not(reviews[3][p]))))
        
    # Condition 3: Kramer and O'Neill both review Tamerlane (index 1)
    solver.add(reviews[1][1] == True)
    solver.add(reviews[4][1] == True)
    
    # Condition 4: Exactly two of the students review exactly the same play or plays as each other
    # This means exactly one pair (i, j) with i < j has set_of_plays[i] == set_of_plays[j]
    # and no other pairs are equal.
    pairs = [(i, j) for i in range(5) for j in range(i + 1, 5)]
    solver.add(Sum([If(set_of_plays[i] == set_of_plays[j], 1, 0) for (i, j) in pairs]) == 1)
    
    # Jiang does not review Tamerlane
    solver.add(reviews[0][1] == False)
    
    return solver

# Define options
# (A) Jiang reviews Sunset (p=0)
# (B) Lopez reviews Undulation (p=2)
# (C) Megregian reviews Sunset (p=0)
# (D) Megregian reviews Tamerlane (p=1)
# (E) O'Neill reviews Undulation (p=2)

solver = get_base_constraints()

found_options = []
options = [
    ("A", reviews[0][0]),
    ("B", reviews[2][2]),
    ("C", reviews[3][0]),
    ("D", reviews[3][1]),
    ("E", reviews[4][2])
]

for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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