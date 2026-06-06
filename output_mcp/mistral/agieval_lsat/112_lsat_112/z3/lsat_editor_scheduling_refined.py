from z3 import *

# Create solver
solver = Solver()

# Articles
articles = [G, H, J, Q, R, S, Y] = Ints('G H J Q R S Y')

# Positions: 1 through 7
positions = [p1, p2, p3, p4, p5, p6, p7] = Ints('p1 p2 p3 p4 p5 p6 p7')

# Each position is assigned a unique article
solver.add(Distinct(positions))

# Map each article to its position
solver.add(p1 == G, p2 == H, p3 == J, p4 == Q, p5 == R, p6 == S, p7 == Y)

# Topics: 0=finance (G,H,J), 1=nutrition (Q,R,S), 2=wildlife (Y)
def get_topic(a):
    return If(a == G, 0,
           If(a == H, 0,
           If(a == J, 0,
           If(a == Q, 1,
           If(a == R, 1,
           If(a == S, 1, 2))))))

# Constraint 1: Consecutive articles cannot cover the same topic
for i in range(6):
    solver.add(get_topic(positions[i]) != get_topic(positions[i+1]))

# Constraint 2: S can be earlier than Q only if Q is third
# If S < Q then Q == 3
solver.add(Implies(S < Q, Q == 3))

# Constraint 3: S must be earlier than Y
solver.add(S < Y)

# Constraint 4: J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Now evaluate the multiple choice options
found_options = []

# Option A: G is second
solver.push()
solver.add(G == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: H is second
solver.push()
solver.add(H == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: S is second
solver.push()
solver.add(S == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: R is third
solver.push()
solver.add(R == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Y is third
solver.push()
solver.add(Y == 3)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")