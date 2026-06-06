from z3 import *

# We have 7 positions (1 to 7) and 7 articles: G, H, J, Q, R, S, Y
# Topics:
# - Finance: G, H, J
# - Nutrition: Q, R, S
# - Wildlife: Y

# Declare the articles as symbolic integers representing their positions (1-7)
# We will use a list to represent the order: order[0] is position 1, order[1] is position 2, etc.
order = [Int(f'order_{i}') for i in range(7)]

# Each position must be assigned a unique article
articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']

# Helper: Map article names to variables for clarity
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')
article_vars = {'G': G, 'H': H, 'J': J, 'Q': Q, 'R': R, 'S': S, 'Y': Y}

# Each article must appear exactly once in the order
solver = Solver()
solver.add(Distinct(order))
for art in articles:
    solver.add(Or([order[i] == article_vars[art] for i in range(7)]))
    for i in range(7):
        solver.add(Implies(order[i] == article_vars[art], And([order[j] != article_vars[art] for j in range(7) if j != i])))

# Topic constraints
# Finance: G, H, J
# Nutrition: Q, R, S
# Wildlife: Y
finance = [G, H, J]
nutrition = [Q, R, S]
wildlife = [Y]

# Helper function to get the topic of an article
def get_topic(art):
    if art in finance:
        return 'finance'
    elif art in nutrition:
        return 'nutrition'
    elif art == Y:
        return 'wildlife'
    else:
        return None

# Constraints from the problem statement
# 1. Consecutive articles cannot cover the same topic
for i in range(6):
    art1 = order[i]
    art2 = order[i+1]
    topic1 = get_topic(art1)
    topic2 = get_topic(art2)
    solver.add(topic1 != topic2)

# 2. S can be earlier than Q only if Q is third
# This means: If S < Q, then Q must be 3rd (i.e., order[2] == Q)
# Equivalently: S < Q implies order[2] == Q
# We can encode this as: Not(S < Q) or order[2] == Q
# Which is: S >= Q or order[2] == Q
solver.add(Or(S >= Q, order[2] == Q))

# 3. S must be earlier than Y
solver.add(S < Y)

# 4. J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Base constraints are now set. Now, we evaluate the multiple-choice options.
# We will check each option to see if it fully determines the order.

# Define the options as constraints on the order
# (A) H is fourth
opt_a_constr = (order[3] == H)
# (B) H is sixth
opt_b_constr = (order[5] == H)
# (C) R is fourth
opt_c_constr = (order[3] == R)
# (D) R is seventh
opt_d_constr = (order[6] == R)
# (E) Y is fifth
opt_e_constr = (order[4] == Y)

# Now, for each option, we check if it fully determines the order.
# To do this, we add the option constraint and check if the solver can find a unique solution.
# We will use the following approach:
# For each option, add the constraint and check if the solver can find a solution.
# If exactly one option leads to a unique solution, that is the answer.

found_options = []

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # Check if the solution is unique by blocking the current model and checking again
        model = solver.model()
        # Block the current model
        solver.add(Or([order[i] != model[order[i]] for i in range(7)]))
        if solver.check() == unsat:
            # Unique solution found
            found_options.append(letter)
        solver.pop()
    else:
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