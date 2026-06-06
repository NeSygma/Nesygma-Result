from z3 import *

# Seven articles: G, H, J, Q, R, S, Y
# Positions 1 through 7
# Topics: Finance: G, H, J; Nutrition: Q, R, S; Wildlife: Y

solver = Solver()

# Create position variables (each article gets a position 1..7)
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
pos = {a: Int(f'pos_{a}') for a in articles}

# Each position is between 1 and 7
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)

# All positions are distinct
solver.add(Distinct([pos[a] for a in articles]))

# Consecutive articles cannot cover the same topic
# Finance: G, H, J
# Nutrition: Q, R, S
# Wildlife: Y
# For any two positions i and i+1, the articles at those positions must have different topics.
# We'll encode this by saying: for each pair of articles with the same topic,
# their positions cannot differ by exactly 1.

# Finance pairs: (G,H), (G,J), (H,J)
finance_pairs = [('G','H'), ('G','J'), ('H','J')]
for a1, a2 in finance_pairs:
    solver.add(Not(pos[a1] - pos[a2] == 1))
    solver.add(Not(pos[a2] - pos[a1] == 1))

# Nutrition pairs: (Q,R), (Q,S), (R,S)
nutrition_pairs = [('Q','R'), ('Q','S'), ('R','S')]
for a1, a2 in nutrition_pairs:
    solver.add(Not(pos[a1] - pos[a2] == 1))
    solver.add(Not(pos[a2] - pos[a1] == 1))

# Wildlife: only Y, so no same-topic consecutive issue with itself.

# S can be earlier than Q only if Q is third.
# (S < Q) implies (Q == 3)
# Equivalently: If S < Q then Q == 3. Contrapositive: If Q != 3 then S >= Q.
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))

# S must be earlier than Y
solver.add(pos['S'] < pos['Y'])

# J must be earlier than G, and G must be earlier than R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Now evaluate each option
# (A) G is second
opt_a = (pos['G'] == 2)
# (B) H is second
opt_b = (pos['H'] == 2)
# (C) S is second
opt_c = (pos['S'] == 2)
# (D) R is third
opt_d = (pos['R'] == 3)
# (E) Y is third
opt_e = (pos['Y'] == 3)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
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