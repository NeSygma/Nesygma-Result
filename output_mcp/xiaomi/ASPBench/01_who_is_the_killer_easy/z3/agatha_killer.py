from z3 import *

# People: 0=Agatha, 1=Butler, 2=Charles
N = 3
Agatha, Butler, Charles = 0, 1, 2

solver = Solver()

# --- Decision Variables ---
# hates[i][j] = True if person i hates person j
hates = [[Bool(f"hates_{i}_{j}") for j in range(N)] for i in range(N)]

# richer[i][j] = True if person i is richer than person j
richer = [[Bool(f"richer_{i}_{j}") for j in range(N)] for i in range(N)]

# killer is the person who killed Agatha
killer = Int('killer')
solver.add(killer >= 0, killer <= 2)

# --- Constraint 1: A killer always hates their victim ---
# killed(killer, Agatha) => hates(killer, Agatha)
for k in range(N):
    solver.add(Implies(killer == k, hates[k][Agatha]))

# --- Constraint 2: A killer is no richer than their victim ---
# killed(killer, Agatha) => NOT richer(killer, Agatha)
for k in range(N):
    solver.add(Implies(killer == k, Not(richer[k][Agatha])))

# --- Constraint 3: Charles hates no one that Agatha hates ---
# For all y: hates(Agatha, y) => NOT hates(Charles, y)
for y in range(N):
    solver.add(Implies(hates[Agatha][y], Not(hates[Charles][y])))

# --- Constraint 4: Agatha hates everybody except the Butler ---
# For all y: y != Butler => hates(Agatha, y)
for y in range(N):
    if y != Butler:
        solver.add(hates[Agatha][y] == True)
    else:
        solver.add(hates[Agatha][y] == False)

# --- Constraint 5: Butler hates everyone not richer than Agatha ---
# For all y: NOT richer(y, Agatha) => hates(Butler, y)
for y in range(N):
    solver.add(Implies(Not(richer[y][Agatha]), hates[Butler][y]))

# --- Constraint 6: Butler hates everyone whom Agatha hates ---
# For all y: hates(Agatha, y) => hates(Butler, y)
for y in range(N):
    solver.add(Implies(hates[Agatha][y], hates[Butler][y]))

# --- Constraint 7: No one hates everyone ---
# For all x: exists y such that NOT hates(x, y)
for x in range(N):
    solver.add(Or([Not(hates[x][y]) for y in range(N)]))

# --- Constraint 8: Agatha is the victim (already encoded via killer targeting Agatha) ---

# --- Solve ---
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    k = m[killer].as_long()
    names = {0: "Agatha", 1: "Butler", 2: "Charles"}
    print("STATUS: sat")
    print(f"killer = {k}")
    print(f"killer_name = {names[k]}")
    
    # Print full model for verification
    print("\n--- Full Model ---")
    print("Hates matrix:")
    for i in range(N):
        for j in range(N):
            val = m.evaluate(hates[i][j], model_completion=True)
            print(f"  hates({names[i]}, {names[j]}) = {val}")
    print("Richer matrix:")
    for i in range(N):
        for j in range(N):
            val = m.evaluate(richer[i][j], model_completion=True)
            print(f"  richer({names[i]}, {names[j]}) = {val}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")