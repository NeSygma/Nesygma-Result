from z3 import *

solver = Solver()

# Declare variables for each item's day (1-6)
H = Int('H')
L = Int('L')
M = Int('M')
S = Int('S')
T = Int('T')
V = Int('V')

# Domain constraints: each day between 1 and 6
solver.add(And(1 <= H, H <= 6))
solver.add(And(1 <= L, L <= 6))
solver.add(And(1 <= M, M <= 6))
solver.add(And(1 <= S, S <= 6))
solver.add(And(1 <= T, T <= 6))
solver.add(And(1 <= V, V <= 6))

# All distinct
solver.add(Distinct([H, L, M, S, T, V]))

# Base constraints from problem
# 1. Sundial not on June 1st
solver.add(S != 1)

# 2. If harmonica earlier than lamp, then mirror earlier than lamp
# (H < L) => (M < L)
solver.add(Or(H >= L, M < L))

# 3. Sundial earlier than mirror and earlier than vase
solver.add(S < M)
solver.add(S < V)

# 4. Table earlier than harmonica or earlier than vase, but not both
# (T < H) XOR (T < V)
solver.add((T < H) != (T < V))

# Now evaluate each answer choice
found_options = []

# Option A: S == 5
solver.push()
solver.add(S == 5)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: S == 4
solver.push()
solver.add(S == 4)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: L == 5 and M == 6
solver.push()
solver.add(And(L == 5, M == 6))
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: T == 3 and L == 4
solver.push()
solver.add(And(T == 3, L == 4))
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: H == 2 and V == 3
solver.push()
solver.add(And(H == 2, V == 3))
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output according to skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")