from z3 import *

# People: 0=Agatha, 1=Butler, 2=Charles
N = 3

solver = Solver()

# --- Variables ---

# killer: who killed Agatha (0, 1, or 2)
killer = Int('killer')
solver.add(killer >= 0, killer <= 2)

# hates[i][j] = True if person i hates person j
hates = [[Bool(f'hates_{i}_{j}') for j in range(N)] for i in range(N)]

# richer[i][j] = True if person i is richer than person j
richer = [[Bool(f'richer_{i}_{j}') for j in range(N)] for i in range(N)]

# --- Constraints ---

# 1. A killer always hates their victim
# The victim is Agatha (person 0)
solver.add(Implies(killer == 0, hates[0][0]))
solver.add(Implies(killer == 1, hates[1][0]))
solver.add(Implies(killer == 2, hates[2][0]))

# 2. A killer is no richer than their victim
# killer is NOT richer than victim (Agatha = person 0)
# i.e., not (killer richer than victim)
solver.add(Implies(killer == 0, Not(richer[0][0])))
solver.add(Implies(killer == 1, Not(richer[1][0])))
solver.add(Implies(killer == 2, Not(richer[2][0])))

# 3. Charles hates no one that Agatha hates
# For all j: if Agatha hates j, then Charles does NOT hate j
for j in range(N):
    solver.add(Implies(hates[0][j], Not(hates[2][j])))

# 4. Agatha hates everybody except the butler
# Agatha hates person 0 (herself?) and person 2 (Charles), but NOT person 1 (Butler)
solver.add(hates[0][0])  # Agatha hates herself? Let's check: "everybody except the butler" - yes, everyone else
solver.add(Not(hates[0][1]))  # Agatha does NOT hate the butler
solver.add(hates[0][2])  # Agatha hates Charles

# 5. The butler hates everyone not richer than Aunt Agatha
# For all j: if j is NOT richer than Agatha, then butler hates j
# "not richer than Aunt Agatha" means: NOT (j is richer than Agatha)
for j in range(N):
    solver.add(Implies(Not(richer[j][0]), hates[1][j]))

# 6. The butler hates everyone whom Agatha hates
# For all j: if Agatha hates j, then butler hates j
for j in range(N):
    solver.add(Implies(hates[0][j], hates[1][j]))

# 7. No one hates everyone
# For each person i: there exists at least one j such that i does NOT hate j
for i in range(N):
    solver.add(Not(And([hates[i][j] for j in range(N)])))

# 8. Agatha is the victim (already encoded above)

# --- Additional constraints to make the model well-defined ---

# Richer is a strict partial order: asymmetric and transitive
# Asymmetric: if i is richer than j, then j is not richer than i
for i in range(N):
    for j in range(N):
        if i != j:
            solver.add(Implies(richer[i][j], Not(richer[j][i])))

# Irreflexive: no one is richer than themselves
for i in range(N):
    solver.add(Not(richer[i][i]))

# Transitive: if i richer than j and j richer than k, then i richer than k
for i in range(N):
    for j in range(N):
        for k in range(N):
            if i != j and j != k and i != k:
                solver.add(Implies(And(richer[i][j], richer[j][k]), richer[i][k]))

# Also, we need to define "not richer than" properly.
# For constraint 5: "not richer than Aunt Agatha" means NOT (j is richer than Agatha)
# This is already encoded above.

# Let's also add that for any two distinct people, either one is richer than the other or they are equally rich
# (total order / comparability) - this is a reasonable assumption for wealth
for i in range(N):
    for j in range(N):
        if i != j:
            solver.add(Or(richer[i][j], richer[j][i]))

# Check if we can find a solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    k = m[killer].as_long()
    names = ["Agatha", "Butler", "Charles"]
    print("STATUS: sat")
    print(f"killer = {k}")
    print(f"killer_name = {names[k]}")
    print()
    print("Hates matrix:")
    for i in range(N):
        for j in range(N):
            print(f"  {names[i]} hates {names[j]}: {m.eval(hates[i][j])}")
    print()
    print("Richer matrix:")
    for i in range(N):
        for j in range(N):
            print(f"  {names[i]} richer than {names[j]}: {m.eval(richer[i][j])}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")