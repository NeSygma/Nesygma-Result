from z3 import *

solver = Solver()

# Three sections: Lifestyle (L), Metro (M), Sports (S)
# Each section has exactly 2 photographs
# Three photographers: Fuentes (F=0), Gagnon (G=1), Hue (H=2)

L0, L1 = Ints('L0 L1')
M0, M1 = Ints('M0 M1')
S0, S1 = Ints('S0 S1')

all_slots = [L0, L1, M0, M1, S0, S1]

for slot in all_slots:
    solver.add(slot >= 0, slot <= 2)

# Count per photographer
count_F = Sum([If(slot == 0, 1, 0) for slot in all_slots])
count_G = Sum([If(slot == 1, 1, 0) for slot in all_slots])
count_H = Sum([If(slot == 2, 1, 0) for slot in all_slots])

solver.add(count_F >= 1, count_F <= 3)
solver.add(count_G >= 1, count_G <= 3)
solver.add(count_H >= 1, count_H <= 3)

# At least one photographer has photos in both Lifestyle and Metro
has_L = [Bool(f'has_L_{p}') for p in range(3)]
has_M = [Bool(f'has_M_{p}') for p in range(3)]

for p in range(3):
    solver.add(has_L[p] == Or(L0 == p, L1 == p))
    solver.add(has_M[p] == Or(M0 == p, M1 == p))

solver.add(Or([And(has_L[p], has_M[p]) for p in range(3)]))

# Hue's photos in Lifestyle = Fuentes' photos in Sports
count_H_L = Sum([If(slot == 2, 1, 0) for slot in [L0, L1]])
count_F_S = Sum([If(slot == 0, 1, 0) for slot in [S0, S1]])
solver.add(count_H_L == count_F_S)

# No Gagnon in Sports
solver.add(S0 != 1)
solver.add(S1 != 1)

# Given: One Lifestyle photo is Gagnon (1), one is Hue (2)
solver.add(Or(And(L0 == 1, L1 == 2), And(L0 == 2, L1 == 1)))

# Let's first enumerate all possible solutions to understand the space
# We'll collect all models and see which options hold in ALL of them (must be true)

# First, let's just check if the base constraints are satisfiable
print("Checking base constraints...")
result = solver.check()
print(f"Base result: {result}")

if result == sat:
    m = solver.model()
    print("Sample model:")
    print(f"  L0={m[L0]}, L1={m[L1]}")
    print(f"  M0={m[M0]}, M1={m[M1]}")
    print(f"  S0={m[S0]}, S1={m[S1]}")
    print(f"  count_F={m.eval(count_F)}, count_G={m.eval(count_G)}, count_H={m.eval(count_H)}")
    
    # Now enumerate all solutions to find what MUST be true
    # Decision variables
    decision_vars = [L0, L1, M0, M1, S0, S1]
    
    solutions = []
    solver.push()
    while solver.check() == sat:
        m = solver.model()
        sol = tuple(m.eval(v, model_completion=True).as_long() for v in decision_vars)
        solutions.append(sol)
        # Block this solution
        solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))
    solver.pop()
    
    print(f"\nTotal solutions: {len(solutions)}")
    for sol in solutions:
        print(f"  L={sol[0]},{sol[1]}  M={sol[2]},{sol[3]}  S={sol[4]},{sol[5]}")
    
    # Now check each option across all solutions
    # An option "must be true" if it holds in ALL solutions
    for letter, opt_name, opt_check in [
        ("A", "Exactly one Metro by Fuentes", lambda sol: sum(1 for v in [sol[2], sol[3]] if v == 0) == 1),
        ("B", "Exactly one Metro by Gagnon", lambda sol: sum(1 for v in [sol[2], sol[3]] if v == 1) == 1),
        ("C", "Both Metro by Gagnon", lambda sol: sol[2] == 1 and sol[3] == 1),
        ("D", "Exactly one Sports by Hue", lambda sol: sum(1 for v in [sol[4], sol[5]] if v == 2) == 1),
        ("E", "Both Sports by Hue", lambda sol: sol[4] == 2 and sol[5] == 2),
    ]:
        holds_in_all = all(opt_check(sol) for sol in solutions)
        print(f"Option {letter} ({opt_name}): holds in all = {holds_in_all}")
else:
    print("Base constraints are unsatisfiable!")