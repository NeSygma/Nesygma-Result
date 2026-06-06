from z3 import *

solver = Solver()

# Articles
G, H, J, Q, R, S, Y = Ints('G H J Q R S Y')

# Domain: each article is at a position 1-7
all_articles = [G, H, J, Q, R, S, Y]
for a in all_articles:
    solver.add(a >= 1, a <= 7)

# All distinct positions
solver.add(Distinct(all_articles))

# Condition 1: Consecutive articles cannot cover the same topic.
# Finance = {G, H, J}, Nutrition = {Q, R, S}, Wildlife = {Y}
# No two finance articles can be consecutive
for a, b in [(G, H), (G, J), (H, J)]:
    solver.add(Not(Or(a - b == 1, b - a == 1)))

# No two nutrition articles can be consecutive
for a, b in [(Q, R), (Q, S), (R, S)]:
    solver.add(Not(Or(a - b == 1, b - a == 1)))

# Condition 2: S can be earlier than Q only if Q is third.
# If S < Q, then Q == 3. Equivalently: Or(Q == 3, Q < S)
solver.add(Implies(S < Q, Q == 3))

# Condition 3: S must be earlier than Y.
solver.add(S < Y)

# Condition 4: J must be earlier than G, and G must be earlier than R.
solver.add(J < G)
solver.add(G < R)

# Additional: Y is fourth.
solver.add(Y == 4)

# Check if we can get at least one model
print("Checking if the problem is satisfiable with Y=4...")
result = solver.check()
print(f"Base result: {result}")

if result == sat:
    m = solver.model()
    print(f"G={m[G]}, H={m[H]}, J={m[J]}, Q={m[Q]}, R={m[R]}, S={m[S]}, Y={m[Y]}")
    
    # Now test each option: does it MUST be true?
    # An option "must be true" if its negation is UNSAT.
    print("\nTesting which options MUST be true (negation test):")
    must_be_true = []
    for letter, constr in [("A", J == 2), ("B", J == 3), ("C", Q == 1), ("D", Q == 3), ("E", R == 7)]:
        s2 = Solver()
        # Add all base constraints
        for a in all_articles:
            s2.add(a >= 1, a <= 7)
        s2.add(Distinct(all_articles))
        for a, b in [(G, H), (G, J), (H, J)]:
            s2.add(Not(Or(a - b == 1, b - a == 1)))
        for a, b in [(Q, R), (Q, S), (R, S)]:
            s2.add(Not(Or(a - b == 1, b - a == 1)))
        s2.add(Implies(S < Q, Q == 3))
        s2.add(S < Y)
        s2.add(J < G)
        s2.add(G < R)
        s2.add(Y == 4)
        # Add the negation of the option
        s2.add(Not(constr))
        if s2.check() == unsat:
            must_be_true.append(letter)
    
    print(f"Options that must be true: {must_be_true}")
    
    if len(must_be_true) == 1:
        print("STATUS: sat")
        print(f"answer:{must_be_true[0]}")
    elif len(must_be_true) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple must-be-true options found {must_be_true}")
    else:
        print("STATUS: unsat")
        print("Refine: No options must be true")
else:
    print("STATUS: unsat")
    print("Refine: Base problem is unsatisfiable")