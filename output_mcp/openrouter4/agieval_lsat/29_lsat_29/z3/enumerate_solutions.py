from z3 import *

F, G, H = Bools('F G H')  # botanists
K, L, M = Bools('K L M')  # chemists
P, Q, R = Bools('P Q R')  # zoologists

solver = Solver()
solver.add(G)
solver.add(H)

# Condition 1: At least one of each type
solver.add(Or(F, G, H))
solver.add(Or(K, L, M))
solver.add(Or(P, Q, R))

# Condition 2: If more than one botanist, then at most one zoologist
more_than_one_botanist = Or(And(F, G), And(F, H), And(G, H))
at_least_two_zoologists = Or(And(P, Q), And(P, R), And(Q, R))
solver.add(Implies(more_than_one_botanist, Not(at_least_two_zoologists)))

# Condition 3: F and K cannot both be selected
solver.add(Not(And(F, K)))

# Condition 4: K and M cannot both be selected
solver.add(Not(And(K, M)))

# Condition 5: If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

all_vars = [F, G, H, K, L, M, P, Q, R]
solutions = []
count = 0

while solver.check() == sat and count < 50:
    m = solver.model()
    sol = {str(v): m.eval(v, model_completion=True) for v in all_vars}
    solutions.append(sol)
    count += 1
    # Block this solution
    solver.add(Or([v != m.eval(v, model_completion=True) for v in all_vars]))

print(f"Found {count} valid configurations with G and H selected:")
for i, sol in enumerate(solutions):
    print(f"  {i+1}. ", end="")
    for name in ['F','G','H','K','L','M','P','Q','R']:
        print(f"{name}={sol[name]}", end=" ")
    print()

# Now analyze what MUST be true across all solutions
print()
print("Analyzing what MUST be true:")
for var_name in ['F','G','H','K','L','M','P','Q','R']:
    vals = [sol[var_name] for sol in solutions]
    if all(v == True for v in vals):
        print(f"  {var_name} MUST be selected (True in all solutions)")
    elif all(v == False for v in vals):
        print(f"  {var_name} MUST NOT be selected (False in all solutions)")
    else:
        print(f"  {var_name} is optional (mixed)")

# Check each option
print()
print("Checking each option (must include at least one):")
for letter, pair in [("A", ("F","K")), ("B", ("F","M")), ("C", ("K","M")), ("D", ("M","Q")), ("E", ("P","Q"))]:
    x, y = pair
    all_satisfy = True
    for sol in solutions:
        if sol[x] == False and sol[y] == False:
            all_satisfy = False
            break
    if all_satisfy:
        print(f"  Option {letter} ({x} or {y}): NECESSARY (always at least one selected)")
    else:
        print(f"  Option {letter} ({x} or {y}): NOT necessary (counterexample exists)")