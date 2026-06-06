from z3 import *

solver = Solver()

# Variables for counts per section per photographer
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# Non-negativity
solver.add(L_F >= 0, L_G >= 0, L_H >= 0)
solver.add(M_F >= 0, M_G >= 0, M_H >= 0)
solver.add(S_F >= 0, S_G >= 0, S_H >= 0)

# 1. Each section has exactly two photos
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# 2. Each photographer appears 1 to 3 times total
Total_F = L_F + M_F + S_F
Total_G = L_G + M_G + S_G
Total_H = L_H + M_H + S_H
solver.add(Total_F >= 1, Total_F <= 3)
solver.add(Total_G >= 1, Total_G <= 3)
solver.add(Total_H >= 1, Total_H <= 3)

# 3. At least one Lifestyle photo by a photographer who also has at least one Metro photo
solver.add(Or(
    And(L_F >= 1, M_F >= 1),
    And(L_G >= 1, M_G >= 1),
    And(L_H >= 1, M_H >= 1)
))

# 4. Hue's Lifestyle photos equals Fuentes Sports photos
solver.add(L_H == S_F)

# 5. Gagnon not in Sports
solver.add(S_G == 0)

# Conditional: both Lifestyle photos are by Hue
solver.add(L_H == 2)
solver.add(L_F == 0)
solver.add(L_G == 0)

# Enumerate all solutions
solutions = []
decision_vars = [L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H]
while solver.check() == sat:
    m = solver.model()
    sol = {v: m.eval(v, model_completion=True) for v in decision_vars}
    solutions.append(sol)
    # Blocking clause
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"Found {len(solutions)} solutions.")
for i, sol in enumerate(solutions):
    print(f"Solution {i+1}:")
    for v in decision_vars:
        print(f"  {v} = {sol[v]}")
    Total_F_val = sol[L_F] + sol[M_F] + sol[S_F]
    Total_G_val = sol[L_G] + sol[M_G] + sol[S_G]
    Total_H_val = sol[L_H] + sol[M_H] + sol[S_H]
    print(f"  Total Fuentes = {Total_F_val}")
    print(f"  Total Gagnon = {Total_G_val}")
    print(f"  Total Hue = {Total_H_val}")

# Determine which totals are constant across all solutions
if solutions:
    totals_F = [sol[L_F] + sol[M_F] + sol[S_F] for sol in solutions]
    totals_G = [sol[L_G] + sol[M_G] + sol[S_G] for sol in solutions]
    totals_H = [sol[L_H] + sol[M_H] + sol[S_H] for sol in solutions]
    if len(set(totals_F)) == 1:
        print(f"Fuentes total forced: {totals_F[0]}")
    if len(set(totals_G)) == 1:
        print(f"Gagnon total forced: {totals_G[0]}")
    if len(set(totals_H)) == 1:
        print(f"Hue total forced: {totals_H[0]}")
else:
    print("No solutions found.")