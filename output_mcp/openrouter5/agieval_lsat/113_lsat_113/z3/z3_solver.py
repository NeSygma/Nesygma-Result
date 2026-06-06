from z3 import *

solver = Solver()

# 7 positions (1-indexed for readability)
positions = range(1, 8)

# Variables: each article's position
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Each article gets a distinct position from 1 to 7
articles = [G, H, J, Q, R, S, Y]
solver.add(Distinct(articles))
for a in articles:
    solver.add(a >= 1, a <= 7)

# Topic constraints: consecutive articles cannot cover the same topic
# Finance: G, H, J
# Nutrition: Q, R, S
# Wildlife: Y

# For each pair of consecutive positions (p, p+1), ensure they are not same topic
# We need to encode: for each position p from 1 to 6,
# if article at p is in {G,H,J} then article at p+1 cannot be in {G,H,J}
# if article at p is in {Q,R,S} then article at p+1 cannot be in {Q,R,S}
# if article at p is Y then article at p+1 cannot be Y

# Helper: is article a at position p?
def at_pos(a, p):
    return a == p

for p in range(1, 7):
    # Finance block: if any finance article is at p, then no finance article at p+1
    finance_at_p = Or([at_pos(a, p) for a in [G, H, J]])
    finance_at_p1 = Or([at_pos(a, p+1) for a in [G, H, J]])
    solver.add(Implies(finance_at_p, Not(finance_at_p1)))
    
    # Nutrition block
    nutrition_at_p = Or([at_pos(a, p) for a in [Q, R, S]])
    nutrition_at_p1 = Or([at_pos(a, p+1) for a in [Q, R, S]])
    solver.add(Implies(nutrition_at_p, Not(nutrition_at_p1)))
    
    # Wildlife block (only Y)
    wildlife_at_p = (Y == p)
    wildlife_at_p1 = (Y == p+1)
    solver.add(Implies(wildlife_at_p, Not(wildlife_at_p1)))

# S can be earlier than Q only if Q is third.
# "S can be earlier than Q only if Q is third" means:
# If S < Q, then Q == 3.
# Equivalently: Not(S < Q) OR Q == 3
solver.add(Implies(S < Q, Q == 3))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# Additional constraint from the question: J is third
solver.add(J == 3)

# Now evaluate each option
found_options = []

# Option A: G is fourth
opt_a = (G == 4)

# Option B: H is sixth
opt_b = (H == 6)

# Option C: Q is first
opt_c = (Q == 1)

# Option D: S is second
opt_d = (S == 2)

# Option E: Y is fifth
opt_e = (Y == 5)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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