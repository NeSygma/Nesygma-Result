from z3 import *

# Create symbolic constants for each article
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Create solver
solver = Solver()

# Each article will have a position (1 through 7)
pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')
pos_Q = Int('pos_Q')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_Y = Int('pos_Y')

# Each position is unique and in range 1-7
solver.add(Distinct([pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]))
solver.add(pos_G >= 1, pos_G <= 7)
solver.add(pos_H >= 1, pos_H <= 7)
solver.add(pos_J >= 1, pos_J <= 7)
solver.add(pos_Q >= 1, pos_Q <= 7)
solver.add(pos_R >= 1, pos_R <= 7)
solver.add(pos_S >= 1, pos_S <= 7)
solver.add(pos_Y >= 1, pos_Y <= 7)

# Define topics: 0=finance (G,H,J), 1=nutrition (Q,R,S), 2=wildlife (Y)
def get_topic(a, pos_a):
    return If(a == G, 0,
           If(a == H, 0,
           If(a == J, 0,
           If(a == Q, 1,
           If(a == R, 1,
           If(a == S, 1, 2))))))

# Constraint 1: S can be earlier than Q only if Q is third
# If pos_S < pos_Q then pos_Q == 3
solver.add(Implies(pos_S < pos_Q, pos_Q == 3))

# Constraint 2: S must be earlier than Y
solver.add(pos_S < pos_Y)

# Constraint 3: J must be earlier than G, and G must be earlier than R
solver.add(pos_J < pos_G)
solver.add(pos_G < pos_R)

# Constraint 4: Consecutive articles cannot cover the same topic
# We need to ensure that for any two articles a and b, if pos(a) = i and pos(b) = i+1, then topic(a) != topic(b)
# We'll add this for all pairs of articles
articles = [G, H, J, Q, R, S, Y]
positions = [pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]

# Add constraint that the mapping from articles to positions is bijective
# Each position 1-7 has exactly one article
for pos_val in range(1, 8):
    solver.add(Or(
        [p == pos_val for p in positions]
    ))

# Add constraint for consecutive positions: for each i from 1 to 6,
# the topics of the articles at positions i and i+1 must differ
for i in range(1, 7):
    # For each article at position i and each article at position i+1, their topics must differ
    for a_idx in range(len(articles)):
        for b_idx in range(len(articles)):
            solver.add(Implies(
                And(positions[a_idx] == i, positions[b_idx] == i+1),
                get_topic(articles[a_idx], positions[a_idx]) != get_topic(articles[b_idx], positions[b_idx])
            ))

# Now evaluate the multiple choice options
found_options = []

# Option A: G is second
solver.push()
solver.add(pos_G == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: H is second
solver.push()
solver.add(pos_H == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: S is second
solver.push()
solver.add(pos_S == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: R is third
solver.push()
solver.add(pos_R == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Y is third
solver.push()
solver.add(pos_Y == 3)
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