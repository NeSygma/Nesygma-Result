from z3 import *

solver = Solver()

# Declare the positions (1st to 7th)
positions = [Int(f'pos_{i}') for i in range(1, 8)]

# Each position must be assigned a unique article
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
for i in range(7):
    solver.add(Distinct(positions))

# Assign articles to positions
# We will use a mapping from position to article
# To avoid symbolic indexing issues, we will use a list of Int variables representing the article at each position
# Let's map articles to unique integers for easier handling
article_to_int = {
    'G': 0,
    'H': 1,
    'J': 2,
    'Q': 3,
    'R': 4,
    'S': 5,
    'Y': 6
}

# Create a list of Int variables representing the article at each position
article_vars = [Int(f'article_{i}') for i in range(1, 8)]

# Each article must appear exactly once
solver.add(Distinct(article_vars))

# Add constraints for the articles
for i in range(7):
    solver.add(article_vars[i] >= 0, article_vars[i] <= 6)
    for art, val in article_to_int.items():
        solver.add(Implies(article_vars[i] == val, positions[i] == i+1))

# Topic constraints
# Topics: finance (G, H, J), nutrition (Q, R, S), wildlife (Y)
finance_articles = [article_to_int['G'], article_to_int['H'], article_to_int['J']]
nutrition_articles = [article_to_int['Q'], article_to_int['R'], article_to_int['S']]
wildlife_article = [article_to_int['Y']]

# Consecutive articles cannot cover the same topic
for i in range(6):
    # Get the topic of the current and next article
    curr_art = article_vars[i]
    next_art = article_vars[i+1]
    
    # Finance articles cannot be consecutive
    solver.add(Not(And(Or([curr_art == a for a in finance_articles]), 
                       Or([next_art == a for a in finance_articles]))))
    
    # Nutrition articles cannot be consecutive
    solver.add(Not(And(Or([curr_art == a for a in nutrition_articles]), 
                       Or([next_art == a for a in nutrition_articles]))))
    
    # Wildlife article cannot be consecutive with itself (only one wildlife article)
    solver.add(Not(And(curr_art == article_to_int['Y'], next_art == article_to_int['Y'])))

# S can be earlier than Q only if Q is third
solver.add(Implies(article_vars[0] == article_to_int['S'], article_vars[2] == article_to_int['Q']))
solver.add(Implies(article_vars[1] == article_to_int['S'], article_vars[2] == article_to_int['Q']))
solver.add(Implies(article_vars[2] == article_to_int['S'], article_vars[2] == article_to_int['Q']))
solver.add(Implies(article_vars[3] == article_to_int['S'], article_vars[2] == article_to_int['Q']))
solver.add(Implies(article_vars[4] == article_to_int['S'], article_vars[2] == article_to_int['Q']))
solver.add(Implies(article_vars[5] == article_to_int['S'], article_vars[2] == article_to_int['Q']))

# S must be earlier than Y
solver.add(Or([
    And(article_vars[i] == article_to_int['S'], 
        Or([article_vars[j] == article_to_int['Y'] for j in range(i+1, 7)]))
    for i in range(6)
]))

# J must be earlier than G, and G must be earlier than R
solver.add(Or([
    And(article_vars[i] == article_to_int['J'], 
        Or([And(article_vars[j] == article_to_int['G'], 
                Or([article_vars[k] == article_to_int['R'] for k in range(j+1, 7)]))
            for j in range(i+1, 7)]))
    for i in range(6)
]))

# Now, evaluate the multiple choice options
found_options = []

# Option A: H, S, J, Q, Y, G, R
solver.push()
solver.add(article_vars[0] == article_to_int['H'])
solver.add(article_vars[1] == article_to_int['S'])
solver.add(article_vars[2] == article_to_int['J'])
solver.add(article_vars[3] == article_to_int['Q'])
solver.add(article_vars[4] == article_to_int['Y'])
solver.add(article_vars[5] == article_to_int['G'])
solver.add(article_vars[6] == article_to_int['R'])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: J, Q, G, H, S, Y, R
solver.push()
solver.add(article_vars[0] == article_to_int['J'])
solver.add(article_vars[1] == article_to_int['Q'])
solver.add(article_vars[2] == article_to_int['G'])
solver.add(article_vars[3] == article_to_int['H'])
solver.add(article_vars[4] == article_to_int['S'])
solver.add(article_vars[5] == article_to_int['Y'])
solver.add(article_vars[6] == article_to_int['R'])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Q, J, S, H, Y, G, R
solver.push()
solver.add(article_vars[0] == article_to_int['Q'])
solver.add(article_vars[1] == article_to_int['J'])
solver.add(article_vars[2] == article_to_int['S'])
solver.add(article_vars[3] == article_to_int['H'])
solver.add(article_vars[4] == article_to_int['Y'])
solver.add(article_vars[5] == article_to_int['G'])
solver.add(article_vars[6] == article_to_int['R'])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Q, J, Y, S, G, R, H
solver.push()
solver.add(article_vars[0] == article_to_int['Q'])
solver.add(article_vars[1] == article_to_int['J'])
solver.add(article_vars[2] == article_to_int['Y'])
solver.add(article_vars[3] == article_to_int['S'])
solver.add(article_vars[4] == article_to_int['G'])
solver.add(article_vars[5] == article_to_int['R'])
solver.add(article_vars[6] == article_to_int['H'])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: S, G, Q, J, Y, R, H
solver.push()
solver.add(article_vars[0] == article_to_int['S'])
solver.add(article_vars[1] == article_to_int['G'])
solver.add(article_vars[2] == article_to_int['Q'])
solver.add(article_vars[3] == article_to_int['J'])
solver.add(article_vars[4] == article_to_int['Y'])
solver.add(article_vars[5] == article_to_int['R'])
solver.add(article_vars[6] == article_to_int['H'])
if solver.check() == sat:
    found_options.append("E")
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