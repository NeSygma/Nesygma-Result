from z3 import *

solver = Solver()

# Days 1..6
days = [1, 2, 3, 4, 5, 6]

# Variables for each antique
H, L, M, S, T, V = Ints('H L M S T V')

# Domain constraints
for var in [H, L, M, S, T, V]:
    solver.add(1 <= var, var <= 6)

# All distinct
solver.add(Distinct(H, L, M, S, T, V))

# Rule 1: Sundial not on June 1
solver.add(S != 1)

# Rule 2: If H earlier than L, then M earlier than L
solver.add(Implies(H < L, M < L))

# Rule 3: S earlier than M and S earlier than V
solver.add(S < M)
solver.add(S < V)

# Rule 4: Table earlier than Harmonica OR earlier than Vase, but not both
# (T < H) XOR (T < V)
solver.add(Not((T < H) == (T < V)))

# Additional condition for this question: T later than both M and V
solver.add(T > M)
solver.add(T > V)

# Now evaluate each option
options = []

# Option A: The harmonica is auctioned on an earlier date than the table. (H < T)
solver.push()
solver.add(H < T)
if solver.check() == sat:
    options.append("A")
solver.pop()

# Option B: The table is auctioned on an earlier date than the lamp. (T < L)
solver.push()
solver.add(T < L)
if solver.check() == sat:
    options.append("B")
solver.pop()

# Option C: The table is auctioned on an earlier date than the sundial. (T < S)
solver.push()
solver.add(T < S)
if solver.check() == sat:
    options.append("C")
solver.pop()

# Option D: The mirror is auctioned on an earlier date than the vase. (M < V)
solver.push()
solver.add(M < V)
if solver.check() == sat:
    options.append("D")
solver.pop()

# Option E: The sundial is auctioned on an earlier date than the lamp. (S < L)
solver.push()
solver.add(S < L)
if solver.check() == sat:
    options.append("E")
solver.pop()

if len(options) == 1:
    print("STATUS: sat")
    print(f"answer:{options[0]}")
elif len(options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")