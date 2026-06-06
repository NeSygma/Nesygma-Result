from z3 import *

# Articles and their topics
finance = ['G', 'H', 'J']
nutrition = ['Q', 'R', 'S']
wildlife = ['Y']
all_articles = finance + nutrition + wildlife

# Position variables: slot[i] = article at position i (1-indexed)
slot = [Int(f'slot_{i}') for i in range(1, 8)]  # slots 1-7

# Map article to index for easier constraints
article_to_idx = {article: i for i, article in enumerate(all_articles)}
idx_to_article = {i: article for i, article in enumerate(all_articles)}

def count_solutions(base_constraints, extra_constraint=None):
    """Count number of solutions given base constraints and optional extra constraint"""
    s = Solver()
    # Add base constraints
    for constraint in base_constraints:
        s.add(constraint)
    # Add extra constraint if provided
    if extra_constraint:
        s.add(extra_constraint)
    
    # Count solutions by enumerating all possibilities
    solutions = []
    decision_vars = slot
    
    while s.check() == sat:
        m = s.model()
        # Get the current solution
        sol = tuple((var, m[var]) for var in decision_vars)
        solutions.append(sol)
        # Block this solution
        s.add(Or([var != m[var] for var in decision_vars]))
    
    return len(solutions)

# Build base constraints
base_constraints = []

# Each slot gets an article index (0-6)
for i in range(7):
    base_constraints.append(slot[i] >= 0)
    base_constraints.append(slot[i] <= 6)

# All slots get distinct articles
base_constraints.append(Distinct(slot))

# Topic constraints: consecutive articles cannot have same topic
def get_topic(article):
    if article in finance:
        return 'finance'
    elif article in nutrition:
        return 'nutrition'
    else:
        return 'wildlife'

# For each consecutive pair of slots, ensure different topics
for i in range(6):
    # We need to express: if slot[i] == idx and slot[i+1] == jdx, then topics differ
    # Use Or-Loop pattern
    constraints = []
    for idx1 in range(7):
        for idx2 in range(7):
            if get_topic(idx_to_article[idx1]) != get_topic(idx_to_article[idx2]):
                constraints.append(And(slot[i] == idx1, slot[i+1] == idx2))
    base_constraints.append(Or(constraints))

# Constraint 2: S can be earlier than Q only if Q is third
# Find indices for S and Q
idx_S = article_to_idx['S']
idx_Q = article_to_idx['Q']
# S earlier than Q means: position of S < position of Q
# We need to find positions of S and Q
pos_S = Int('pos_S')
pos_Q = Int('pos_Q')
base_constraints.append(Or([And(slot[i] == idx_S, pos_S == i+1) for i in range(7)]))
base_constraints.append(Or([And(slot[i] == idx_Q, pos_Q == i+1) for i in range(7)]))
base_constraints.append(Implies(pos_S < pos_Q, pos_Q == 2))  # Q is third means position 3 (index 2)

# Constraint 3: S must be earlier than Y
idx_Y = article_to_idx['Y']
pos_Y = Int('pos_Y')
base_constraints.append(Or([And(slot[i] == idx_Y, pos_Y == i+1) for i in range(7)]))
base_constraints.append(pos_S < pos_Y)

# Constraint 4: J must be earlier than G, and G must be earlier than R
idx_J = article_to_idx['J']
idx_G = article_to_idx['G']
idx_R = article_to_idx['R']
pos_J = Int('pos_J')
pos_G = Int('pos_G')
pos_R = Int('pos_R')
base_constraints.append(Or([And(slot[i] == idx_J, pos_J == i+1) for i in range(7)]))
base_constraints.append(Or([And(slot[i] == idx_G, pos_G == i+1) for i in range(7)]))
base_constraints.append(Or([And(slot[i] == idx_R, pos_R == i+1) for i in range(7)]))
base_constraints.append(pos_J < pos_G)
base_constraints.append(pos_G < pos_R)

# Test each option
found_options = []

# Option A: H is fourth
idx_H = article_to_idx['H']
count_A = count_solutions(base_constraints, slot[3] == idx_H)  # slot[3] is position 4
if count_A == 1:
    found_options.append('A')

# Option B: H is sixth
count_B = count_solutions(base_constraints, slot[5] == idx_H)  # slot[5] is position 6
if count_B == 1:
    found_options.append('B')

# Option C: R is fourth
count_C = count_solutions(base_constraints, slot[3] == idx_R)
if count_C == 1:
    found_options.append('C')

# Option D: R is seventh
count_D = count_solutions(base_constraints, slot[6] == idx_R)
if count_D == 1:
    found_options.append('D')

# Option E: Y is fifth
count_E = count_solutions(base_constraints, slot[4] == idx_Y)
if count_E == 1:
    found_options.append('E')

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")