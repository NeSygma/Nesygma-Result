from z3 import *

solver = Solver()

# Articles and their positions (1-7)
G, H, J = Ints('G H J')
Q, R, S = Ints('Q R S')
Y = Int('Y')

articles = [G, H, J, Q, R, S, Y]
article_names = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']

# Each article has a position 1-7
for a in articles:
    solver.add(a >= 1, a <= 7)

# All articles in different positions
solver.add(Distinct(articles))

# Topics: Finance = {G, H, J}, Nutrition = {Q, R, S}, Wildlife = {Y}
# Consecutive articles cannot cover the same topic
# For each pair of positions p and p+1, the articles at those positions must be from different topics
for p in range(1, 7):
    # Articles at position p and p+1 must not both be finance, not both nutrition
    # Finance articles: G, H, J
    # Nutrition articles: Q, R, S
    # Wildlife: Y (only one, so no consecutive wildlife issue)
    
    # Not both finance at consecutive positions
    solver.add(Not(And(
        Or(G == p, H == p, J == p),
        Or(G == p+1, H == p+1, J == p+1)
    )))
    
    # Not both nutrition at consecutive positions
    solver.add(Not(And(
        Or(Q == p, R == p, S == p),
        Or(Q == p+1, R == p+1, S == p+1)
    )))

# S can be earlier than Q only if Q is third
# If S < Q then Q == 3
solver.add(Implies(S < Q, Q == 3))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Now test each answer choice to see which one fully determines the order
# An answer "fully determines" if adding that constraint yields exactly one solution

def count_solutions(extra_constraint, name):
    """Count distinct solutions with the extra constraint."""
    s = Solver()
    s.add(solver.assertions())
    s.add(extra_constraint)
    
    solutions = []
    while s.check() == sat:
        m = s.model()
        sol = tuple(m.eval(a).as_long() for a in articles)
        solutions.append(sol)
        # Block this solution
        s.add(Or([a != m.eval(a) for a in articles]))
    
    return solutions

# Define answer choice constraints
opt_a = (H == 4)  # H is fourth
opt_b = (H == 6)  # H is sixth
opt_c = (R == 4)  # R is fourth
opt_d = (R == 7)  # R is seventh
opt_e = (Y == 5)  # Y is fifth

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e),
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        # Count how many solutions exist with this constraint
        solutions = count_solutions(constr, letter)
        if len(solutions) == 1:
            found_options.append(letter)
            print(f"Option {letter}: UNIQUE solution - {dict(zip(article_names, solutions[0]))}")
        else:
            print(f"Option {letter}: {len(solutions)} solutions (not fully determined)")
    else:
        print(f"Option {letter}: UNSAT (impossible)")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")