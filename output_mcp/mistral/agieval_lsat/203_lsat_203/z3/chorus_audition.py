from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# Declare singers as integers for simplicity
K, L, T, W, Y, Z = 0, 1, 2, 3, 4, 5
singers = [K, L, T, W, Y, Z]
recorded = [K, L]
not_recorded = [T, W, Y, Z]

# Create a solver
solver = Solver()

# Positions: p1, p2, p3, p4, p5, p6
positions = [Int(f'p{i+1}') for i in range(6)]

# Each position must be assigned to a singer
solver.add(Distinct(positions))
for p in positions:
    solver.add(Or([p == s for s in singers]))

# Helper function to get the position of a singer
def get_pos(singer):
    return positions[0] if singer == positions[0] else \
           positions[1] if singer == positions[1] else \
           positions[2] if singer == positions[2] else \
           positions[3] if singer == positions[3] else \
           positions[4] if singer == positions[4] else \
           positions[5]

# Alternative: Use a mapping from singer to position variable
# We'll use a list comprehension to create a list of (singer, position) pairs
singer_positions = [(s, Int(f'singer_{s}_pos')) for s in singers]
for s, pos in singer_positions:
    solver.add(pos >= 1, pos <= 6)

# Each position must have exactly one singer
for i in range(6):
    solver.add(Or([positions[i] == s for s in singers]))
    solver.add(Sum([If(positions[i] == s, 1, 0) for s in singers]) == 1)

# Each singer must be in exactly one position
for s in singers:
    solver.add(Sum([If(positions[i] == s, 1, 0) for i in range(6)]) == 1)

# Constraint 1: The fourth audition cannot be recorded
solver.add(Or([positions[3] == s for s in not_recorded]))

# Constraint 2: The fifth audition must be recorded
solver.add(Or([positions[4] == s for s in recorded]))

# Constraint 3: Waite's audition must take place earlier than the two recorded auditions
# position(W) < position(K) and position(W) < position(L)
w_pos = positions[0] if W == positions[0] else \
       positions[1] if W == positions[1] else \
       positions[2] if W == positions[2] else \
       positions[3] if W == positions[3] else \
       positions[4] if W == positions[4] else \
       positions[5]

k_pos = positions[0] if K == positions[0] else \
       positions[1] if K == positions[1] else \
       positions[2] if K == positions[2] else \
       positions[3] if K == positions[3] else \
       positions[4] if K == positions[4] else \
       positions[5]

l_pos = positions[0] if L == positions[0] else \
       positions[1] if L == positions[1] else \
       positions[2] if L == positions[2] else \
       positions[3] if L == positions[3] else \
       positions[4] if L == positions[4] else \
       positions[5]

solver.add(w_pos < k_pos)
solver.add(w_pos < l_pos)

# Constraint 4: Kammer's audition must take place earlier than Trillo's
solver.add(k_pos < (positions[0] if T == positions[0] else \
                    positions[1] if T == positions[1] else \
                    positions[2] if T == positions[2] else \
                    positions[3] if T == positions[3] else \
                    positions[4] if T == positions[4] else \
                    positions[5]))

# Constraint 5: Zinn's audition must take place earlier than Yoshida's
z_pos = positions[0] if Z == positions[0] else \
       positions[1] if Z == positions[1] else \
       positions[2] if Z == positions[2] else \
       positions[3] if Z == positions[3] else \
       positions[4] if Z == positions[4] else \
       positions[5]

y_pos = positions[0] if Y == positions[0] else \
       positions[1] if Y == positions[1] else \
       positions[2] if Y == positions[2] else \
       positions[3] if Y == positions[3] else \
       positions[4] if Y == positions[4] else \
       positions[5]

solver.add(z_pos < y_pos)

# Now, evaluate each option for the second audition
# We will check if each option can be in position 2
found_options = []

# Option A: Kammer's audition is second
solver.push()
solver.add(positions[1] == K)
result_a = solver.check()
if result_a == sat:
    found_options.append("A")
solver.pop()

# Option B: Lugo's audition is second
solver.push()
solver.add(positions[1] == L)
result_b = solver.check()
if result_b == sat:
    found_options.append("B")
solver.pop()

# Option C: Trillo's audition is second
solver.push()
solver.add(positions[1] == T)
result_c = solver.check()
if result_c == sat:
    found_options.append("C")
solver.pop()

# Option D: Waite's audition is second
solver.push()
solver.add(positions[1] == W)
result_d = solver.check()
if result_d == sat:
    found_options.append("D")
solver.pop()

# Option E: Zinn's audition is second
solver.push()
solver.add(positions[1] == Z)
result_e = solver.check()
if result_e == sat:
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