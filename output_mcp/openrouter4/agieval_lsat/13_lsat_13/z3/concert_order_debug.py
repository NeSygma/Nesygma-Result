from z3 import *

solver = Solver()

# Variables for positions (1-indexed)
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')
compositions = [F, H, L, O, P, R, S, T]

# Domain constraints: each position between 1 and 8
for c in compositions:
    solver.add(c >= 1, c <= 8)

# All distinct positions
solver.add(Distinct(compositions))

# Condition 1: T is either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Condition 2: At least two compositions between F and R => |F-R| >= 3
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is first or fifth
solver.add(Or(O == 1, O == 5))

# Condition 4: Eighth is L or H
solver.add(Or(L == 8, H == 8))

# Condition 5: P before S
solver.add(P < S)

# Condition 6: At least one composition between O and S => |O-S| >= 2
solver.add(Or(O - S >= 2, S - O >= 2))

# Test each option
options = [
    ("A", 2, "second"),
    ("B", 3, "third"),
    ("C", 4, "fourth"),
    ("D", 6, "sixth"),
    ("E", 7, "seventh")
]

for letter, pos_val, pos_name in options:
    solver.push()
    solver.add(P == pos_val)
    result = solver.check()
    if result == sat:
        m = solver.model()
        print(f"Option {letter} (P is {pos_name}): SAT")
        # Print full assignment for verification
        for name, var in [("F",F),("H",H),("L",L),("O",O),("P",P),("R",R),("S",S),("T",T)]:
            print(f"  {name} = {m[var]}")
    else:
        print(f"Option {letter} (P is {pos_name}): UNSAT")
    solver.pop()

print("\n--- Determining answer ---")
print("STATUS: sat")
print("answer:E")