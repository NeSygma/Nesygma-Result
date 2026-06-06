from z3 import *

solver = Solver()

# Declare variables for each antique's day (1-6)
H = Int('H')  # harmonica
L = Int('L')  # lamp
M = Int('M')  # mirror
S = Int('S')  # sundial
T = Int('T')  # table
V = Int('V')  # vase

# Base constraints
solver.add(Distinct([H, L, M, S, T, V]))
solver.add(S != 1)
solver.add(Implies(H < L, M < L))
solver.add(S < M)
solver.add(S < V)
# Exclusive OR: exactly one of (T < H) and (T < V) is true
solver.add((T < H) != (T < V))

# Define each option as a list of assignments in order from day1 to day6
options = {
    "A": [H, T, S, L, V, M],  # harmonica, table, sundial, lamp, vase, mirror
    "B": [L, H, S, M, V, T],  # lamp, harmonica, sundial, mirror, vase, table
    "C": [H, S, T, M, L, V],  # harmonica, sundial, table, mirror, lamp, vase
    "D": [S, M, H, T, V, L],  # sundial, mirror, harmonica, table, vase, lamp
    "E": [V, S, L, H, T, M]   # vase, sundial, lamp, harmonica, table, mirror
}

found_options = []
for letter, order in options.items():
    solver.push()
    # Add constraints that each variable equals the day index (1-based)
    for day, var in enumerate(order, start=1):
        solver.add(var == day)
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