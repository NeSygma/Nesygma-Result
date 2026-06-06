from z3 import *

solver = Solver()

# Days: 1 = June 1st, ..., 6 = June 6th
H, L, M, S, T, V = Ints('H L M S T V')

# All days are 1 through 6
days = [H, L, M, S, T, V]
for d in days:
    solver.add(d >= 1, d <= 6)

# All distinct
solver.add(Distinct(days))

# Constraint 1: The sundial is not auctioned on June 1st.
solver.add(S != 1)

# Constraint 2: If H < L then M < L
solver.add(Implies(H < L, M < L))

# Constraint 3: S < M and S < V
solver.add(S < M)
solver.add(S < V)

# Constraint 4: (T < H) XOR (T < V) -- exactly one of them is true
solver.add(Xor(T < H, T < V))

# --- Options ---

# Option A: Sundial on June 5th
opt_a = (S == 5)

# Option B: Sundial on June 4th
opt_b = (S == 4)

# Option C: Lamp on June 5th and mirror on June 6th
opt_c = And(L == 5, M == 6)

# Option D: Table on June 3rd and lamp on June 4th
opt_d = And(T == 3, L == 4)

# Option E: Harmonica on June 2nd and vase on June 3rd
opt_e = And(H == 2, V == 3)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
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