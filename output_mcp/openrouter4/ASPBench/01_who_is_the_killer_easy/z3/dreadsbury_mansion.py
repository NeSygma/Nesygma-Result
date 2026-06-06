from z3 import *

solver = Solver()

N = 3

# hates(i, j): person i hates person j
hates = Function('hates', IntSort(), IntSort(), BoolSort())
# richer(i, j): person i is richer than person j
richer = Function('richer', IntSort(), IntSort(), BoolSort())

# killer variable
killer = Int('killer')
solver.add(killer >= 0, killer <= 2)

# --- Domain axioms for 'richer' (strict partial order) ---
# Irreflexive: no one is richer than themselves
for i in range(N):
    solver.add(Not(richer(i, i)))

# Asymmetric: if i is richer than j, then j is not richer than i
for i in range(N):
    for j in range(N):
        if i != j:
            solver.add(Implies(richer(i, j), Not(richer(j, i))))

# Transitive: if i richer than j and j richer than k, then i richer than k
for i in range(N):
    for j in range(N):
        for k in range(N):
            if i != j and j != k and i != k:
                solver.add(Implies(And(richer(i, j), richer(j, k)), richer(i, k)))

# --- Constraint 1: Killer hates victim (Agatha = 0) ---
solver.add(hates(killer, 0))

# --- Constraint 2: Killer is no richer than victim ---
solver.add(Not(richer(killer, 0)))

# --- Constraint 3: Charles hates no one that Agatha hates ---
# For all j: if hates(0, j) then Not(hates(2, j))
for j in range(N):
    solver.add(Implies(hates(0, j), Not(hates(2, j))))

# --- Constraint 4: Agatha hates everybody except the butler (index 1) ---
# Agatha hates all other people (excluding herself and the butler)
for j in range(N):
    if j != 0 and j != 1:
        solver.add(hates(0, j))
# Agatha does NOT hate the butler
solver.add(Not(hates(0, 1)))

# --- Constraint 5: The butler hates everyone not richer than Aunt Agatha ---
# For all j: if Not(richer(j, 0)) then hates(1, j)
for j in range(N):
    solver.add(Implies(Not(richer(j, 0)), hates(1, j)))

# --- Constraint 6: The butler hates everyone whom Agatha hates ---
# For all j: if hates(0, j) then hates(1, j)
for j in range(N):
    solver.add(Implies(hates(0, j), hates(1, j)))

# --- Constraint 7: No one hates everyone ---
# For each i, there exists at least one j such that Not(hates(i, j))
for i in range(N):
    solver.add(Or([Not(hates(i, j)) for j in range(N)]))

# --- Constraint 8: Agatha is the victim (already encoded as 0) ---

# Check
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    killer_val = m.eval(killer).as_long()
    names = ["Agatha", "Butler", "Charles"]
    print("STATUS: sat")
    print(f"killer = {killer_val}")
    print(f"killer_name = {names[killer_val]}")
    # Also print the hates and richer relations for debugging
    print("\nHates matrix:")
    for i in range(N):
        row = []
        for j in range(N):
            row.append(str(m.eval(hates(i, j))))
        print(f"  Person {i} ({names[i]}): {row}")
    print("\nRicher matrix:")
    for i in range(N):
        row = []
        for j in range(N):
            row.append(str(m.eval(richer(i, j))))
        print(f"  Person {i} ({names[i]}): {row}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")