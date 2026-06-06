from z3 import *

solver = Solver()

# Articles and their positions (1-7)
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')
articles = [G, H, J, Q, R, S, Y]
names = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']

# Each article has a unique position from 1 to 7
for a in articles:
    solver.add(a >= 1, a <= 7)
solver.add(Distinct(articles))

# Topic assignments (for adjacency constraint)
# Finance: G, H, J  (topic 0)
# Nutrition: Q, R, S (topic 1)
# Wildlife: Y        (topic 2)
# We'll use a function to get topic from position

# For consecutive positions, topics must differ.
# We need: for each position p (1..6), the article at p and p+1 have different topics.
# Finance articles: G, H, J
# Nutrition articles: Q, R, S
# Wildlife: Y

# Helper: is article 'a' at position p?
def at_pos(a, p):
    return a == p

# For each consecutive pair of positions (p, p+1), they can't be same topic
# Same topic pairs: (G,H), (G,J), (H,J) for finance; (Q,R), (Q,S), (R,S) for nutrition
# Y is alone in wildlife, so no same-topic conflict with Y

for p in range(1, 7):
    # Both at position p and p+1 cannot both be finance
    solver.add(Not(Or(
        And(at_pos(G, p), at_pos(H, p+1)),
        And(at_pos(H, p), at_pos(G, p+1)),
        And(at_pos(G, p), at_pos(J, p+1)),
        And(at_pos(J, p), at_pos(G, p+1)),
        And(at_pos(H, p), at_pos(J, p+1)),
        And(at_pos(J, p), at_pos(H, p+1)),
    )))
    # Both at position p and p+1 cannot both be nutrition
    solver.add(Not(Or(
        And(at_pos(Q, p), at_pos(R, p+1)),
        And(at_pos(R, p), at_pos(Q, p+1)),
        And(at_pos(Q, p), at_pos(S, p+1)),
        And(at_pos(S, p), at_pos(Q, p+1)),
        And(at_pos(R, p), at_pos(S, p+1)),
        And(at_pos(S, p), at_pos(R, p+1)),
    )))

# Constraint 2: S can be earlier than Q only if Q is third
# Equivalently: S >= Q OR Q == 3
solver.add(Or(S >= Q, Q == 3))

# Constraint 3: S must be earlier than Y
solver.add(S < Y)

# Constraint 4: J < G < R
solver.add(J < G)
solver.add(G < R)

# Given: Y is fourth
solver.add(Y == 4)

# Now check each answer choice
# "Must be true" means negation is unsatisfiable
options = {
    "A": J == 2,
    "B": J == 3,
    "C": Q == 1,
    "D": Q == 3,
    "E": R == 7,
}

must_be_true = []
for letter, constr in options.items():
    solver.push()
    solver.add(Not(constr))
    result = solver.check()
    if result == unsat:
        must_be_true.append(letter)
    solver.pop()

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")

# Also print a sample model for verification
solver.push()
if solver.check() == sat:
    m = solver.model()
    print("\nSample model:")
    for name, var in zip(names, articles):
        print(f"  Position {m[var]}: {name}")
solver.pop()