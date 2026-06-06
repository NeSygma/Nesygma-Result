from z3 import *

solver = Solver()

# Articles: G, H, J (finance), Q, R, S (nutrition), Y (wildlife)
# Positions: 1-7
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')
articles = [G, H, J, Q, R, S, Y]

# Each article gets a unique position from 1 to 7
for a in articles:
    solver.add(a >= 1, a <= 7)
solver.add(Distinct(articles))

# Topics: finance = {G, H, J}, nutrition = {Q, R, S}, wildlife = {Y}
# Consecutive articles cannot cover the same topic
# Finance articles: G, H, J
# Nutrition articles: Q, R, S
# Wildlife: Y

# For each pair of consecutive positions, the articles at those positions
# cannot both be finance, cannot both be nutrition
# (wildlife only has one article so no consecutive wildlife issue)

# Helper: is article 'a' finance?
def is_finance(a):
    return Or(a == G, a == H, a == J)

# Helper: is article 'a' nutrition?
def is_nutrition(a):
    return Or(a == Q, a == R, a == S)

# For positions 1-2, 2-3, ..., 6-7: consecutive articles can't share topic
for pos in range(1, 7):
    # Find which article is at position pos and pos+1
    # We need: NOT(both finance) AND NOT(both nutrition)
    # For each pair of articles, if they are at consecutive positions, they can't share topic
    
    # Get articles at position pos and pos+1
    at_pos = [a for a in articles]
    at_next = [a for a in articles]
    
    # For all pairs (a1, a2) where a1 is at pos and a2 is at pos+1:
    # Not(both finance) and Not(both nutrition)
    for a1 in articles:
        for a2 in articles:
            solver.add(Implies(And(a1 == pos, a2 == pos + 1),
                               And(Not(And(is_finance(a1), is_finance(a2))),
                                   Not(And(is_nutrition(a1), is_nutrition(a2))))))

# S can be earlier than Q only if Q is third
# Equivalently: if S < Q then Q == 3
solver.add(Implies(S < Q, Q == 3))

# S must be earlier than Y
solver.add(S < Y)

# J must be earlier than G, and G must be earlier than R
solver.add(J < G)
solver.add(G < R)

# G is fourth
solver.add(G == 4)

# Now test each option
found_options = []

# (A) H is fifth
solver.push()
solver.add(H == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) J is first
solver.push()
solver.add(J == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) Q is second
solver.push()
solver.add(Q == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) S is fifth
solver.push()
solver.add(S == 5)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Y is sixth
solver.push()
solver.add(Y == 6)
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