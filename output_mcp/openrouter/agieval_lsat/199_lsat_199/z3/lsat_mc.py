from z3 import *

# Variables for each antique day (1..6)
H = Int('H')  # harmonica
L = Int('L')  # lamp
M = Int('M')  # mirror
S = Int('S')  # sundial
T = Int('T')  # table
V = Int('V')  # vase

ants = [H, L, M, S, T, V]
solver = Solver()
# domain constraints
for a in ants:
    solver.add(a >= 1, a <= 6)
# all distinct
solver.add(Distinct(ants))
# constraints
solver.add(S != 1)  # sundial not on June1
solver.add(Implies(H < L, M < L))
solver.add(S < M)
solver.add(S < V)
# XOR for table earlier than harmonica or vase but not both
solver.add((T < H) != (T < V))

# Mapping letters to variables
letter_var = {
    'A': H,
    'B': L,
    'C': M,
    'D': S,
    'E': T,
}

found_options = []
all_letters = ['A','B','C','D','E']
for letter, var in letter_var.items():
    solver.push()
    # enforce that this var is immediately before vase
    solver.add(var == V - 1)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine which option cannot be preceding (i.e., not in found_options)
impossible = [l for l in all_letters if l not in found_options]
# If exactly one impossible, set found_options to that for final printing
if len(impossible) == 1:
    found_options = impossible

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")