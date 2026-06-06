from z3 import *

# We have 4 lectures, positions 0,1,2,3 (earliest to latest)
# Topics: lithographs (L), oil paintings (O), sculptures (S), watercolors (W)
# Historians: Farley (F), Garcia (G), Holden (H), Jiang (J)

L, O, S, W = Ints('L O S W')
F, G, H, J = Ints('F G H J')

solver = Solver()

for var in [L, O, S, W, F, G, H, J]:
    solver.add(var >= 0, var <= 3)

solver.add(Distinct(L, O, S, W))
solver.add(Distinct(F, G, H, J))

# Constraints
solver.add(O < L)
solver.add(W < L)
solver.add(F < O)
solver.add(H < G)
solver.add(H < J)

# The problem asks "which one of the following MUST be true?"
# This means we need to find which option is entailed by the premises.
# An option MUST be true if it holds in ALL possible models.
# So we check: is there a model where the option is FALSE?
# If no model exists where the option is false, then it MUST be true.

# For each option, we check if Not(option) is satisfiable.
# If Not(option) is unsat, then option MUST be true.

found_options = []
for letter, constr in [("A", F < S), ("B", H < L), ("C", S < G), ("D", S < J), ("E", W < G)]:
    solver.push()
    solver.add(Not(constr))  # Check if it's possible for this to be false
    if solver.check() == unsat:
        # If it's impossible for it to be false, it MUST be true
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