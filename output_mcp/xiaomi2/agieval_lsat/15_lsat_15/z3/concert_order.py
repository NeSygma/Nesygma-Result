from z3 import *

# Each composition gets a position 1-8
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
comps = [F, H, L, O, P, R, S, T]
names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

solver = Solver()

# All positions are 1-8 and distinct
for c in comps:
    solver.add(And(c >= 1, c <= 8))
solver.add(Distinct(comps))

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Constraint 2: At least two compositions between F and R
# |F - R| >= 3
solver.add(Or(F - R >= 3, R - F >= 3))

# Constraint 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Constraint 4: The eighth composition is either L or H
solver.add(Or(L == 8, H == 8))

# Constraint 5: P is performed before S
solver.add(P < S)

# Constraint 6: At least one composition between O and S
# |O - S| >= 2
solver.add(Or(O - S >= 2, S - O >= 2))

# Additional condition: O is performed immediately after T
solver.add(T + 1 == O)

# Now find all possible positions for F
possible_F_positions = set()
for pos in range(1, 9):
    solver.push()
    solver.add(F == pos)
    if solver.check() == sat:
        possible_F_positions.add(pos)
        m = solver.model()
        print(f"F={pos} is SAT: " + ", ".join(f"{n}={m[c]}" for n, c in zip(names, comps)))
    solver.pop()

print(f"\nPossible positions for F: {sorted(possible_F_positions)}")

# Now check each answer choice
answer_map = {
    "A": [1, 2],
    "B": [2, 3],
    "C": [4, 6],
    "D": [4, 7],
    "E": [6, 7],
}

found_options = []
for letter, positions in answer_map.items():
    # Check if F's possible positions are exactly the set in this answer
    if set(positions) == possible_F_positions:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    # Also check if any answer is a superset that contains all possible positions
    for letter, positions in answer_map.items():
        if possible_F_positions.issubset(set(positions)):
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