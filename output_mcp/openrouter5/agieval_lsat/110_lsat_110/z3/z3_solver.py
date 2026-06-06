from z3 import *

solver = Solver()

# 7 positions (1-indexed)
positions = list(range(1, 8))

# Variables: each article's position
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Each article gets a distinct position from 1 to 7
articles = [G, H, J, Q, R, S, Y]
solver.add(Distinct(articles))
for a in articles:
    solver.add(a >= 1, a <= 7)

# Topics: Finance = {G, H, J}, Nutrition = {Q, R, S}, Wildlife = {Y}
# Consecutive articles cannot cover the same topic.
# For each pair of articles from the same topic, they cannot be consecutive.
# Finance: G, H, J
for a1, a2 in [(G, H), (G, J), (H, J)]:
    solver.add(Abs(a1 - a2) != 1)
# Nutrition: Q, R, S
for a1, a2 in [(Q, R), (Q, S), (R, S)]:
    solver.add(Abs(a1 - a2) != 1)

# S can be earlier than Q only if Q is third.
# If S < Q, then Q == 3.
solver.add(Implies(S < Q, Q == 3))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Given: Y is fourth
solver.add(Y == 4)

# Let's enumerate all solutions to see what's always true
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {str(a): m.eval(a, model_completion=True).as_long() for a in articles}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([a != m.eval(a, model_completion=True) for a in articles]))

print(f"Total solutions: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"Solution {i+1}: G={sol['G']}, H={sol['H']}, J={sol['J']}, Q={sol['Q']}, R={sol['R']}, S={sol['S']}, Y={sol['Y']}")

# Check what's true in ALL solutions
if solutions:
    # For each option, check if it holds in ALL solutions
    for letter, var, val in [("A", J, 2), ("B", J, 3), ("C", Q, 1), ("D", Q, 3), ("E", R, 7)]:
        all_true = all(sol[str(var)] == val for sol in solutions)
        print(f"Option {letter} ({var} == {val}): {'MUST be true' if all_true else 'not necessarily'}")