from z3 import *

# Seven positions 0..6
# Articles: G, H, J, Q, R, S, Y
# Topics: Finance (G, H, J), Nutrition (Q, R, S), Wildlife (Y)

# Use Int variables for positions of each article
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
pos = {a: Int(f'pos_{a}') for a in articles}

solver = Solver()

# Each position is 0..6
for a in articles:
    solver.add(pos[a] >= 0, pos[a] <= 6)

# All positions distinct
solver.add(Distinct([pos[a] for a in articles]))

# Consecutive articles cannot cover the same topic
# Finance: G, H, J (topic 0)
# Nutrition: Q, R, S (topic 1)
# Wildlife: Y (topic 2)

# For each position i, we need to know which article is at position i
# Use an Array for symbolic indexing
ArticleAt = Array('ArticleAt', IntSort(), IntSort())
# article_at[i] = index of article at position i (0=G,1=H,2=J,3=Q,4=R,5=S,6=Y)
for i in range(7):
    solver.add(ArticleAt[i] >= 0, ArticleAt[i] <= 6)

# All positions have distinct articles
solver.add(Distinct([ArticleAt[i] for i in range(7)]))

# Link pos[a] and ArticleAt: ArticleAt[pos[a]] == idx_of(a)
article_indices = {'G':0, 'H':1, 'J':2, 'Q':3, 'R':4, 'S':5, 'Y':6}
for a, idx in article_indices.items():
    # ArticleAt[pos[a]] == idx
    # Use Or-loop pattern since pos[a] is symbolic
    solver.add(Or([And(pos[a] == i, ArticleAt[i] == idx) for i in range(7)]))

# Also: pos[a] == i iff ArticleAt[i] == idx
for i in range(7):
    for a, idx in article_indices.items():
        solver.add(Implies(ArticleAt[i] == idx, pos[a] == i))

# Topic function
topic = Function('topic', IntSort(), IntSort())
# Define topic for each article index
for a, idx in article_indices.items():
    if a in ['G', 'H', 'J']:
        solver.add(topic(idx) == 0)
    elif a in ['Q', 'R', 'S']:
        solver.add(topic(idx) == 1)
    else:  # Y
        solver.add(topic(idx) == 2)

# Consecutive constraint: for i in 0..5, topic(ArticleAt[i]) != topic(ArticleAt[i+1])
for i in range(6):
    solver.add(topic(ArticleAt[i]) != topic(ArticleAt[i+1]))

# S can be earlier than Q only if Q is third.
# If S < Q (pos[S] < pos[Q]), then Q must be at position 3 (pos[Q] == 2, 0-indexed)
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 2))

# S must be earlier than Y
solver.add(pos['S'] < pos['Y'])

# J must be earlier than G, and G must be earlier than R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

# Now evaluate each option
# Option A: H is fourth (position 3)
opt_a = (pos['H'] == 3)
# Option B: H is sixth (position 5)
opt_b = (pos['H'] == 5)
# Option C: R is fourth (position 3)
opt_c = (pos['R'] == 3)
# Option D: R is seventh (position 6)
opt_d = (pos['R'] == 6)
# Option E: Y is fifth (position 4)
opt_e = (pos['Y'] == 4)

# The question asks: which option FULLY DETERMINES the order?
# So for each option, we need to check if there is EXACTLY ONE solution.
# Let's count solutions for each option.

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    
    # Count solutions
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        sol = tuple(m.eval(pos[a], model_completion=True).as_long() for a in articles)
        solutions.append(sol)
        # Block this solution
        solver.add(Or([pos[a] != m.eval(pos[a], model_completion=True) for a in articles]))
    
    solver.pop()
    
    if len(solutions) == 1:
        found_options.append(letter)
        print(f"Option {letter}: exactly 1 solution - {solutions[0]}")
    else:
        print(f"Option {letter}: {len(solutions)} solutions")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")