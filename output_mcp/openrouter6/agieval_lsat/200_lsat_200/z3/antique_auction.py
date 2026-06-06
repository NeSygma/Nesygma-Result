from z3 import *

solver = Solver()

# Variables for each item's auction day (1..6)
H = Int('H')  # harmonica
L = Int('L')  # lamp
M = Int('M')  # mirror
S = Int('S')  # sundial
T = Int('T')  # table
V = Int('V')  # vase

# Domain constraints: each day between 1 and 6
solver.add(And(1 <= H, H <= 6))
solver.add(And(1 <= L, L <= 6))
solver.add(And(1 <= M, M <= 6))
solver.add(And(1 <= S, S <= 6))
solver.add(And(1 <= T, T <= 6))
solver.add(And(1 <= V, V <= 6))

# All distinct
solver.add(Distinct([H, L, M, S, T, V]))

# Condition 1: Sundial not on June 1
solver.add(S != 1)

# Condition 2: If harmonica earlier than lamp, then mirror earlier than lamp
solver.add(Implies(H < L, M < L))

# Condition 3: Sundial earlier than mirror and earlier than vase
solver.add(S < M)
solver.add(S < V)

# Condition 4: Table earlier than harmonica OR earlier than vase, but not both
# Exactly one of (T < H) and (T < V) is true
solver.add( (T < H) != (T < V) )

# Now test each option
found_options = []

# Option A: mirror on June 2nd
solver.push()
solver.add(M == 2)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: lamp on June 2nd
solver.push()
solver.add(L == 2)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: vase on June 2nd
solver.push()
solver.add(V == 2)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: lamp on June 3rd
solver.push()
solver.add(L == 3)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: mirror on June 5th
solver.push()
solver.add(M == 5)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")