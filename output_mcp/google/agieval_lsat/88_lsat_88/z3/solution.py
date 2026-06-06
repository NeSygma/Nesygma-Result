from z3 import *

solver = Solver()

# Variables
# P[i] = 0 for Wayne, 1 for Zara
# T[i] = True for Traditional, False for Modern
P = [Int(f'P_{i}') for i in range(5)]
T = [Bool(f'T_{i}') for i in range(5)]

for i in range(5):
    solver.add(Or(P[i] == 0, P[i] == 1))

# C1: The third solo is a traditional piece.
solver.add(T[2] == True)

# C2: Exactly two of the traditional pieces are performed consecutively.
# This means there is exactly one pair (i, i+1) such that T[i] and T[i+1] are both True.
# And no other consecutive pairs.
consecutive_pairs = [And(T[i], T[i+1]) for i in range(4)]
solver.add(Sum([If(pair, 1, 0) for pair in consecutive_pairs]) == 1)

# C3: In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
# Wayne = 0, Zara = 1. Traditional = True, Modern = False.
# (P[3] == 0 and T[3] == True) or (P[3] == 1 and T[3] == False)
solver.add(Or(And(P[3] == 0, T[3] == True), And(P[3] == 1, T[3] == False)))

# C4: The pianist who performs the second solo does not perform the fifth solo.
solver.add(P[1] != P[4])

# C5: No traditional piece is performed until Wayne performs at least one modern piece.
# If T[i] is True, there must exist j < i such that P[j] == 0 and T[j] == False.
for i in range(5):
    # If T[i] is True, then there exists j < i such that P[j] == 0 and T[j] == False
    exists_wayne_modern_before = Or([And(P[j] == 0, T[j] == False) for j in range(i)])
    solver.add(Implies(T[i], exists_wayne_modern_before))

# Options
# (A) 1, 3, 4
# (B) 2, 3, 4
# (C) 3, 4
# (D) 3, 5
# (E) 4, 5

def is_traditional(i):
    return T[i]

options = [
    ("A", [is_traditional(0), Not(is_traditional(1)), is_traditional(2), is_traditional(3), Not(is_traditional(4))]),
    ("B", [Not(is_traditional(0)), is_traditional(1), is_traditional(2), is_traditional(3), Not(is_traditional(4))]),
    ("C", [Not(is_traditional(0)), Not(is_traditional(1)), is_traditional(2), is_traditional(3), Not(is_traditional(4))]),
    ("D", [Not(is_traditional(0)), Not(is_traditional(1)), is_traditional(2), Not(is_traditional(3)), is_traditional(4)]),
    ("E", [Not(is_traditional(0)), Not(is_traditional(1)), Not(is_traditional(2)), is_traditional(3), is_traditional(4)])
]

found_options = []
for letter, constr_list in options:
    solver.push()
    for c in constr_list:
        solver.add(c)
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