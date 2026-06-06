from z3 import *

# Articles and their topics
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
wildlife = ['Y']

# We'll represent the order as a list of 7 variables, each being one of the articles
# But Z3 doesn't have a direct "enum" type, so we'll use integers to represent articles
# Let's map articles to integers: G=0, H=1, J=2, Q=3, R=4, S=5, Y=6
article_to_int = {'G':0, 'H':1, 'J':2, 'Q':3, 'R':4, 'S':5, 'Y':6}
int_to_article = {v:k for k,v in article_to_int.items()}

# Create variables for positions 1-7 (index 0-6)
positions = [Int(f'pos_{i}') for i in range(7)]

solver = Solver()

# Constraint: Each position must be a distinct article (0-6)
for i in range(7):
    solver.add(positions[i] >= 0)
    solver.add(positions[i] <= 6)

# All positions must be different (each article appears exactly once)
solver.add(Distinct(positions))

# Helper function to get topic of an article integer
def topic_of(article_int):
    if int_to_article[article_int] in finance:
        return 0  # finance
    elif int_to_article[article_int] in nutrition:
        return 1  # nutrition
    else:  # wildlife
        return 2

# Constraint 1: Consecutive articles cannot cover the same topic
for i in range(6):
    # For each consecutive pair, their topics must be different
    # We need to express this using Z3's If and Or
    # Since topic_of returns a Python function, we need to use Z3 expressions
    # Let's create a mapping from article int to topic using If
    topic_i = If(positions[i] == article_to_int['G'], 0,
                 If(positions[i] == article_to_int['H'], 0,
                    If(positions[i] == article_to_int['J'], 0,
                       If(positions[i] == article_to_int['Q'], 1,
                          If(positions[i] == article_to_int['R'], 1,
                             If(positions[i] == article_to_int['S'], 1, 2))))))
    topic_next = If(positions[i+1] == article_to_int['G'], 0,
                    If(positions[i+1] == article_to_int['H'], 0,
                       If(positions[i+1] == article_to_int['J'], 0,
                          If(positions[i+1] == article_to_int['Q'], 1,
                             If(positions[i+1] == article_to_int['R'], 1,
                                If(positions[i+1] == article_to_int['S'], 1, 2))))))
    solver.add(topic_i != topic_next)

# Constraint 2: S can be earlier than Q only if Q is third
# This means: If S appears before Q, then Q must be at position 3 (index 2)
# We need to find positions of S and Q
# Let's create variables for the positions of each article
# Actually, we already have positions array where positions[i] = article at position i
# We need the inverse: for each article, what position is it at?
# Let's create position_of_article array
position_of = [Int(f'pos_of_{art}') for art in range(7)]
for art in range(7):
    # position_of[art] is the position (0-6) where article art appears
    solver.add(Or([positions[i] == art for i in range(7)]))
    # And position_of[art] must equal the actual position
    for i in range(7):
        solver.add(Implies(positions[i] == art, position_of[art] == i))

# Now constraint 2: If position_of[S] < position_of[Q], then position_of[Q] == 2
S_int = article_to_int['S']
Q_int = article_to_int['Q']
solver.add(Implies(position_of[S_int] < position_of[Q_int], position_of[Q_int] == 2))

# Constraint 3: S must be earlier than Y
Y_int = article_to_int['Y']
solver.add(position_of[S_int] < position_of[Y_int])

# Constraint 4: J must be earlier than G, and G must be earlier than R
J_int = article_to_int['J']
G_int = article_to_int['G']
R_int = article_to_int['R']
solver.add(position_of[J_int] < position_of[G_int])
solver.add(position_of[G_int] < position_of[R_int])

# Now evaluate each answer choice
# Each choice gives a specific order from first to seventh
# We need to add constraints that match that order

found_options = []

# Option A: H, S, J, Q, Y, G, R
opt_a = And(
    positions[0] == article_to_int['H'],
    positions[1] == article_to_int['S'],
    positions[2] == article_to_int['J'],
    positions[3] == article_to_int['Q'],
    positions[4] == article_to_int['Y'],
    positions[5] == article_to_int['G'],
    positions[6] == article_to_int['R']
)

# Option B: J, Q, G, H, S, Y, R
opt_b = And(
    positions[0] == article_to_int['J'],
    positions[1] == article_to_int['Q'],
    positions[2] == article_to_int['G'],
    positions[3] == article_to_int['H'],
    positions[4] == article_to_int['S'],
    positions[5] == article_to_int['Y'],
    positions[6] == article_to_int['R']
)

# Option C: Q, J, S, H, Y, G, R
opt_c = And(
    positions[0] == article_to_int['Q'],
    positions[1] == article_to_int['J'],
    positions[2] == article_to_int['S'],
    positions[3] == article_to_int['H'],
    positions[4] == article_to_int['Y'],
    positions[5] == article_to_int['G'],
    positions[6] == article_to_int['R']
)

# Option D: Q, J, Y, S, G, R, H
opt_d = And(
    positions[0] == article_to_int['Q'],
    positions[1] == article_to_int['J'],
    positions[2] == article_to_int['Y'],
    positions[3] == article_to_int['S'],
    positions[4] == article_to_int['G'],
    positions[5] == article_to_int['R'],
    positions[6] == article_to_int['H']
)

# Option E: S, G, Q, J, Y, R, H
opt_e = And(
    positions[0] == article_to_int['S'],
    positions[1] == article_to_int['G'],
    positions[2] == article_to_int['Q'],
    positions[3] == article_to_int['J'],
    positions[4] == article_to_int['Y'],
    positions[5] == article_to_int['R'],
    positions[6] == article_to_int['H']
)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
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