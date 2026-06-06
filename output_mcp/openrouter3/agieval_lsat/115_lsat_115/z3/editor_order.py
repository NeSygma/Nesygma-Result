from z3 import *

# Articles and their topics
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
wildlife = ['Y']

# Create position variables for each article
articles = finance + nutrition + wildlife
pos = {art: Int(f'pos_{art}') for art in articles}

solver = Solver()

# All positions must be between 1 and 7
for art in articles:
    solver.add(pos[art] >= 1, pos[art] <= 7)

# All positions must be distinct
solver.add(Distinct([pos[art] for art in articles]))

# Helper function to get topic of an article
def topic(art):
    if art in finance:
        return 0  # finance
    elif art in nutrition:
        return 1  # nutrition
    else:  # Y
        return 2  # wildlife

# Constraint 1: Consecutive articles cannot cover the same topic
# For each pair of positions (i, i+1), the articles at those positions must have different topics
for i in range(1, 7):
    # For each pair of articles, if they are at consecutive positions, they must have different topics
    for art1 in articles:
        for art2 in articles:
            if art1 != art2:
                # If art1 is at position i and art2 at position i+1, their topics must differ
                solver.add(Implies(And(pos[art1] == i, pos[art2] == i+1), topic(art1) != topic(art2)))

# Constraint 2: S can be earlier than Q only if Q is third
# If pos[S] < pos[Q], then pos[Q] == 3
solver.add(Implies(pos[S] < pos[Q], pos[Q] == 3))

# Constraint 3: S must be earlier than Y
solver.add(pos[S] < pos[Y])

# Constraint 4: J < G < R
solver.add(pos[J] < pos[G])
solver.add(pos[G] < pos[R])

# Now test each option
# Option A: H is fourth
opt_a = (pos['H'] == 4)
# Option B: H is sixth
opt_b = (pos['H'] == 6)
# Option C: R is fourth
opt_c = (pos['R'] == 4)
# Option D: R is seventh
opt_d = (pos['R'] == 7)
# Option E: Y is fifth
opt_e = (pos['Y'] == 5)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    # Count solutions: we need to check if exactly one solution exists
    # We'll do this by finding one solution, then blocking it and checking if another exists
    if solver.check() == sat:
        # Get first solution
        m1 = solver.model()
        # Block this solution
        block = Or([pos[art] != m1[pos[art]] for art in articles])
        solver.add(block)
        # Check if another solution exists
        if solver.check() != sat:
            # Only one solution found
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