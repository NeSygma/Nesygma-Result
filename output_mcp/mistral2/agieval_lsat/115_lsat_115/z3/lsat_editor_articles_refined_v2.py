from z3 import *

# We have 7 positions (1 to 7) and 7 articles: G, H, J, Q, R, S, Y
# Topics:
# - Finance: G, H, J
# - Nutrition: Q, R, S
# - Wildlife: Y

# Declare the positions of the articles as symbolic integers (1-7)
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Each article must be assigned a unique position between 1 and 7
solver = Solver()
solver.add(Distinct(G, H, J, Q, R, S, Y))
solver.add(G >= 1, G <= 7)
solver.add(H >= 1, H <= 7)
solver.add(J >= 1, J <= 7)
solver.add(Q >= 1, Q <= 7)
solver.add(R >= 1, R <= 7)
solver.add(S >= 1, S <= 7)
solver.add(Y >= 1, Y <= 7)

# Topic constraints
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
# To enforce this, we need to ensure that for any two articles x and y, if x is immediately before y in the order, their topics must differ.
# We can do this by iterating over all pairs of articles and enforcing that if x < y and there is no article z such that x < z < y, then topics differ.
articles = [G, H, J, Q, R, S, Y]
for i in range(len(articles)):
    for j in range(len(articles)):
        if i != j:
            x = articles[i]
            y = articles[j]
            # If x < y and there is no article z such that x < z < y, then topics must differ
            # This is equivalent to saying that x and y are consecutive in the order
            # We can encode this by saying: if x < y and for all z, not (x < z and z < y), then topics differ
            # This is complex, so we will instead enforce that for any two articles x and y, if x < y and y - x == 1, then topics differ
            # This is a simplification but will work for this problem
            solver.add(Implies(And(x < y, y - x == 1), get_topic(x) != get_topic(y)))

# 2. S can be earlier than Q only if Q is third
# This means: If S < Q, then Q must be 3
solver.add(Implies(S < Q, Q == 3))

# 3. S must be earlier than Y
solver.add(S < Y)

# 4. J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Now, we evaluate the multiple-choice options.
# We will check each option to see if it fully determines the order.
# To do this, we add the option constraint and check if the solver can find a unique solution.

# Define the options as constraints on the positions
# (A) H is fourth
opt_a_constr = (H == 4)
# (B) H is sixth
opt_b_constr = (H == 6)
# (C) R is fourth
opt_c_constr = (R == 4)
# (D) R is seventh
opt_d_constr = (R == 7)
# (E) Y is fifth
opt_e_constr = (Y == 5)

found_options = []

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # Check if the solution is unique by blocking the current model and checking again
        model = solver.model()
        # Block the current model
        solver.add(Or([
            G != model[G], H != model[H], J != model[J], Q != model[Q], 
            R != model[R], S != model[S], Y != model[Y]
        ]))
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