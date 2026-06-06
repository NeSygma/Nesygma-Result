from z3 import *

# Articles: G, H, J (finance); Q, R, S (nutrition); Y (wildlife)
# Assign numbers for convenience
G, H, J, Q, R, S, Y = 0, 1, 2, 3, 4, 5, 6
articles = [G, H, J, Q, R, S, Y]

# Position variables for each article
pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')
pos_Q = Int('pos_Q')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_Y = Int('pos_Y')

solver = Solver()

# Domain constraints: positions 1..7
for p in [pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y]:
    solver.add(p >= 1, p <= 7)

# All positions distinct
solver.add(Distinct(pos_G, pos_H, pos_J, pos_Q, pos_R, pos_S, pos_Y))

# Topic mapping: finance = {G, H, J}, nutrition = {Q, R, S}, wildlife = {Y}
# We'll need to know topic of each position. Instead of mapping position to article,
# we can create an array of article IDs per position using a list of variables.
# But we already have article->position. To check consecutive topics, we need to know
# which article is at each position. We can create a function that given a position,
# returns the article ID. Since we have only 7 positions, we can create 7 variables
# representing the article at each position, and link them to the pos_* variables.
# Let's do that: create article_at_pos[i] for i=1..7.
article_at_pos = [Int(f'article_at_pos_{i}') for i in range(1, 8)]
for i in range(1, 8):
    solver.add(article_at_pos[i-1] >= 0, article_at_pos[i-1] <= 6)

# All article_at_pos distinct (since each article appears once)
solver.add(Distinct(article_at_pos))

# Link article_at_pos to pos_* variables: for each article, the position where it appears
# equals the pos_* variable.
# We'll use a mapping from article ID to its position variable.
article_to_pos = {G: pos_G, H: pos_H, J: pos_J, Q: pos_Q, R: pos_R, S: pos_S, Y: pos_Y}
for art, pos_var in article_to_pos.items():
    # For each position i, if article_at_pos[i-1] == art, then pos_var == i.
    # Use Or-loop.
    solver.add(Or([And(article_at_pos[i-1] == art, pos_var == i) for i in range(1, 8)]))

# Constraint: consecutive articles cannot cover the same topic.
# Define a function to get topic of an article ID.
def topic_of(art):
    # finance: 0,1,2; nutrition: 3,4,5; wildlife: 6
    return If(Or(art == G, art == H, art == J), 0,
              If(Or(art == Q, art == R, art == S), 1, 2))

for i in range(1, 7):
    art1 = article_at_pos[i-1]
    art2 = article_at_pos[i]
    solver.add(topic_of(art1) != topic_of(art2))

# Conditional: S can be earlier than Q only if Q is third.
# i.e., (pos_S < pos_Q) => (pos_Q == 3)
solver.add(Implies(pos_S < pos_Q, pos_Q == 3))

# S must be earlier than Y
solver.add(pos_S < pos_Y)

# J earlier than G, and G earlier than R
solver.add(pos_J < pos_G)
solver.add(pos_G < pos_R)

# Y is fourth
solver.add(pos_Y == 4)

# Now define option constraints
opt_a_constr = (pos_J == 2)
opt_b_constr = (pos_J == 3)
opt_c_constr = (pos_Q == 1)
opt_d_constr = (pos_Q == 3)
opt_e_constr = (pos_R == 7)

# Evaluate each option using the skeleton
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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