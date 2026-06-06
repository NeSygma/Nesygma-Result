from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Define singers as integers for clarity
K = 0  # Kammer
L = 1  # Lugo
T = 2  # Trillo
W = 3  # Waite
Y = 4  # Yoshida
Z = 5  # Zinn

# Create a solver
solver = Solver()

# pos[i] = singer assigned to position i (1-indexed, 1..6)
pos = [Int(f'pos_{i}') for i in range(1, 7)]

# order[s] = position (1-indexed) of singer s
order = [Int(f'order_{s}') for s in range(6)]

# Each position is assigned to a distinct singer
solver.add(Distinct(pos))

# Each singer is assigned to a distinct position
solver.add(Distinct(order))

# Link pos and order: pos[i-1] = s iff order[s] = i
for i in range(1, 7):
    for s in range(6):
        solver.add(Implies(order[s] == i, pos[i-1] == s))
        solver.add(Implies(pos[i-1] == s, order[s] == i))

# All positions are between 0 and 5 (singers)
for p in pos:
    solver.add(p >= 0, p <= 5)

# All orders are between 1 and 6
for o in order:
    solver.add(o >= 1, o <= 6)

# The fourth audition cannot be recorded → pos[3] (4th position) cannot be K or L
solver.add(Or(pos[3] != K, pos[3] != L))

# The fifth audition must be recorded → pos[4] (5th position) must be K or L
solver.add(Or(pos[4] == K, pos[4] == L))

# Waite's audition must take place earlier than the two recorded auditions (K and L)
solver.add(order[W] < order[K])
solver.add(order[W] < order[L])

# Kammer's audition must take place earlier than Trillo's audition
solver.add(order[K] < order[T])

# Zinn's audition must take place earlier than Yoshida's audition
solver.add(order[Z] < order[Y])

# Now evaluate the multiple-choice options for Yoshida's position
# Options: (A) fifth (B) fourth (C) third (D) second (E) first
found_options = []

# Option A: Yoshida is fifth
solver.push()
solver.add(order[Y] == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Yoshida is fourth
solver.push()
solver.add(order[Y] == 4)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Yoshida is third
solver.push()
solver.add(order[Y] == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Yoshida is second
solver.push()
solver.add(order[Y] == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Yoshida is first
solver.push()
solver.add(order[Y] == 1)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")