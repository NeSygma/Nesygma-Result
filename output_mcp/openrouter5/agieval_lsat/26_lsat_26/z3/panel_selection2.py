from z3 import *

solver = Solver()

# Scientists: botanists F, G, H; chemists K, L, M; zoologists P, Q, R
F, G, H = Bools('F G H')
K, L, M = Bools('K L M')
P, Q, R = Bools('P Q R')

# Condition 1: At least one of each type
solver.add(Or(F, G, H))
solver.add(Or(K, L, M))
solver.add(Or(P, Q, R))

# Condition 2: If more than one botanist selected, then at most one zoologist selected
more_than_one_botanist = Sum([If(b, 1, 0) for b in [F, G, H]]) >= 2
at_most_one_zoologist = Sum([If(z, 1, 0) for z in [P, Q, R]]) <= 1
solver.add(Implies(more_than_one_botanist, at_most_one_zoologist))

# Condition 3: F and K cannot both be selected
solver.add(Not(And(F, K)))

# Condition 4: K and M cannot both be selected
solver.add(Not(And(K, M)))

# Condition 5: If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Additional condition: M is the ONLY chemist selected
solver.add(M)
solver.add(Not(K))
solver.add(Not(L))

# Let's see what models exist to understand the constraints better
print("All valid models under the given conditions:")
solver.push()
count = 0
while solver.check() == sat and count < 20:
    m = solver.model()
    selected = [s for s in [F, G, H, K, L, M, P, Q, R] if is_true(m.eval(s))]
    print(f"Model {count+1}: {[str(s) for s in selected]}")
    # Block this model
    solver.add(Or([s != is_true(m.eval(s)) for s in [F, G, H, K, L, M, P, Q, R]]))
    count += 1
solver.pop()

print()

# Now let's check each option more carefully
# The question asks: "which one of the following MUST be true?"
# So we need to check if an option is true in ALL valid models.
# An option "must be true" if adding its negation leads to unsat.

for letter, constr in [("A", And(F, G)), ("B", And(G, H)), ("C", And(H, P)), 
                        ("D", And(F, G, H)), ("E", And(P, Q, R))]:
    s = Solver()
    # Add all base constraints
    s.add(Or(F, G, H))
    s.add(Or(K, L, M))
    s.add(Or(P, Q, R))
    s.add(Implies(Sum([If(b, 1, 0) for b in [F, G, H]]) >= 2, 
                  Sum([If(z, 1, 0) for z in [P, Q, R]]) <= 1))
    s.add(Not(And(F, K)))
    s.add(Not(And(K, M)))
    s.add(Implies(M, And(P, R)))
    s.add(M)
    s.add(Not(K))
    s.add(Not(L))
    # Add negation of the option
    s.add(Not(constr))
    result = s.check()
    if result == unsat:
        print(f"Option {letter}: MUST BE TRUE (negation leads to unsat)")
    else:
        print(f"Option {letter}: NOT necessarily true")