from z3 import *

solver = Solver()

# Variables: position of each historian's lecture (1-4)
F = Int('F')  # Farley
G = Int('G')  # Garcia
H = Int('H')  # Holden
J = Int('J')  # Jiang

# Variables: position of each topic's lecture (1-4)
L = Int('L')  # Lithographs
O = Int('O')  # Oil paintings
S = Int('S')  # Sculptures
W = Int('W')  # Watercolors

# All positions are between 1 and 4
for v in [F, G, H, J, L, O, S, W]:
    solver.add(v >= 1, v <= 4)

# All historians have distinct positions
solver.add(Distinct(F, G, H, J))

# All topics have distinct positions
solver.add(Distinct(L, O, S, W))

# Each historian gives exactly one topic, so the mapping is a bijection
# We model this by saying the set of historian positions equals the set of topic positions
# (which is guaranteed since both are permutations of {1,2,3,4})

# Constraints:
# 1. Oil paintings and watercolors both earlier than lithographs
solver.add(O < L)
solver.add(W < L)

# 2. Farley's lecture earlier than oil paintings
solver.add(F < O)

# 3. Holden's lecture earlier than both Garcia's and Jiang's
solver.add(H < G)
solver.add(H < J)

# Now evaluate each option
# We need to check which MUST be true (i.e., is true in ALL valid models)
# An option "must be true" if its negation is unsatisfiable

options = {
    "A": F < S,           # Farley's lecture is earlier than sculptures
    "B": H < L,           # Holden's lecture is earlier than lithographs
    "C": S < G,           # Sculptures lecture is earlier than Garcia's
    "D": S < J,           # Sculptures lecture is earlier than Jiang's
    "E": W < G,           # Watercolors lecture is earlier than Garcia's
}

must_be_true = []
for letter, constr in options.items():
    # Check if negation is unsatisfiable (meaning the option must be true)
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

print(f"Options that must be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")