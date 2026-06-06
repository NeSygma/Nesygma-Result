from z3 import *

F, G, H = Bools('F G H')  # botanists
K, L, M = Bools('K L M')  # chemists
P, Q, R = Bools('P Q R')  # zoologists

all_vars = [F, G, H, K, L, M, P, Q, R]

solver = Solver()

# The panel has exactly 5 scientists
solver.add(Sum([If(v, 1, 0) for v in all_vars]) == 5)

# G and H are selected (the premise of the conditional question)
solver.add(G)
solver.add(H)

# Condition 1: At least one of each type
solver.add(Or(F, G, H))  # at least one botanist (trivially true since G,H)
solver.add(Or(K, L, M))  # at least one chemist
solver.add(Or(P, Q, R))  # at least one zoologist

# Condition 2: If more than one botanist, then at most one zoologist
# G and H are selected, so more_than_one_botanist is true.
# Therefore at most one zoologist.
at_least_two_zoologists = Or(And(P, Q), And(P, R), And(Q, R))
solver.add(Not(at_least_two_zoologists))
# Combined with at least one zoologist -> exactly one zoologist.

# Condition 3: F and K cannot both be selected
solver.add(Not(And(F, K)))

# Condition 4: K and M cannot both be selected
solver.add(Not(And(K, M)))

# Condition 5: If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Enumerate all solutions
solutions = []
count = 0

while solver.check() == sat and count < 50:
    m = solver.model()
    sol = {str(v): m.eval(v, model_completion=True) for v in all_vars}
    solutions.append(sol)
    count += 1
    solver.add(Or([v != m.eval(v, model_completion=True) for v in all_vars]))

print(f"Found {count} valid configurations with G, H, and exactly 5 total:")
for i, sol in enumerate(solutions):
    selected = [name for name in ['F','G','H','K','L','M','P','Q','R'] if sol[name] == True]
    print(f"  {i+1}. Selected: {', '.join(selected)}")

# Now check each option
print()
print("Checking each option (must include at least one of the pair in ALL solutions):")
for letter, (x_name, y_name) in [("A", ("F","K")), ("B", ("F","M")), ("C", ("K","M")), ("D", ("M","Q")), ("E", ("P","Q"))]:
    all_satisfy = True
    for sol in solutions:
        if sol[x_name] == False and sol[y_name] == False:
            all_satisfy = False
            break
    if all_satisfy:
        print(f"  Option {letter} ({x_name} or {y_name}): NECESSARY")
    else:
        print(f"  Option {letter} ({x_name} or {y_name}): NOT necessary")