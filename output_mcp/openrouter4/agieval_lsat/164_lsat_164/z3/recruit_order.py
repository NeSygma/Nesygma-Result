from z3 import *

solver = Solver()

# 7 accomplices, positions 1-7
p = Int('Peters')
q = Int('Quinn')
r = Int('Rovero')
s = Int('Stanton')
t = Int('Tao')
v = Int('Villas')
w = Int('White')

people = [p, q, r, s, t, v, w]

# Domain: each position is 1 through 7
for person in people:
    solver.add(person >= 1, person <= 7)

# All distinct positions
solver.add(Distinct(people))

# Constraint 1: Stanton not immediately before or after Tao
# |s - t| != 1
solver.add(Not(Or(s == t - 1, s == t + 1)))

# Constraint 2: Quinn earlier than Rovero
solver.add(q < r)

# Constraint 3: Villas immediately before White
solver.add(v + 1 == w)

# Constraint 4: Peters was recruited fourth
solver.add(p == 4)

# Constraint 5 (new): Tao was recruited second
solver.add(t == 2)

# Now check each option
options = {
    "A": q == 3,  # Quinn third
    "B": r == 5,  # Rovero fifth
    "C": s == 6,  # Stanton sixth
    "D": v == 6,  # Villas sixth
    "E": w == 3   # White third
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        # Print the model for this option
        m = solver.model()
        print(f"Option {letter} is possible:")
        print(f"  Peters={m[p]}, Quinn={m[q]}, Rovero={m[r]}, Stanton={m[s]}, Tao={m[t]}, Villas={m[v]}, White={m[w]}")
    else:
        print(f"Option {letter} is not possible.")
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