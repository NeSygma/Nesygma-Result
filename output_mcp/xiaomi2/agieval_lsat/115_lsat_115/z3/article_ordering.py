from z3 import *

# Article positions (1-7)
G, H, J = Ints('G H J')
Q, R, S = Ints('Q R S')
Y = Int('Y')

articles = [G, H, J, Q, R, S, Y]

# Base constraints
base = []

# All positions 1-7
for a in articles:
    base.append(And(a >= 1, a <= 7))

# All distinct positions
base.append(Distinct(articles))

# Consecutive articles cannot cover the same topic
# Finance: G, H, J — no two finance articles adjacent
for a, b in [(G,H), (G,J), (H,J)]:
    base.append(And(a - b != 1, b - a != 1))

# Nutrition: Q, R, S — no two nutrition articles adjacent
for a, b in [(Q,R), (Q,S), (R,S)]:
    base.append(And(a - b != 1, b - a != 1))

# S can be earlier than Q only if Q is third
# If S < Q, then Q == 3
base.append(Implies(S < Q, Q == 3))

# S must be earlier than Y
base.append(S < Y)

# J < G < R
base.append(J < G)
base.append(G < R)

# Answer options
options = {
    "A": H == 4,
    "B": H == 6,
    "C": R == 4,
    "D": R == 7,
    "E": Y == 5,
}

found_options = []
for letter, constr in options.items():
    s = Solver()
    s.add(base)
    s.add(constr)
    count = 0
    while s.check() == sat:
        m = s.model()
        count += 1
        if count > 1:
            break  # More than one solution, not fully determined
        # Block current solution
        s.add(Or([v != m.eval(v, model_completion=True) for v in articles]))
    if count == 1:
        found_options.append(letter)
        # Print the unique solution for verification
        print(f"Option {letter}: UNIQUE solution found")
    elif count == 0:
        print(f"Option {letter}: No solution (unsat)")
    else:
        print(f"Option {letter}: Multiple solutions exist")

print()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")