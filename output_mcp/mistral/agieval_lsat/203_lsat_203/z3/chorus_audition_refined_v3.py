from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# Singer constants
K, L, T, W, Y, Z = 0, 1, 2, 3, 4, 5
singers = [K, L, T, W, Y, Z]
recorded = [K, L]
not_recorded = [T, W, Y, Z]

# Create a solver
solver = Solver()

# order[0] is the first audition, order[1] is the second, ..., order[5] is the sixth
order = [Int(f'order_{i+1}') for i in range(6)]

# Each position must be assigned to a singer
solver.add(Distinct(order))
for i in range(6):
    solver.add(Or([order[i] == s for s in singers]))

# Constraint 1: The fourth audition cannot be recorded
solver.add(Or([order[3] == s for s in not_recorded]))

# Constraint 2: The fifth audition must be recorded
solver.add(Or([order[4] == s for s in recorded]))

# Constraint 3: Waite's audition must take place earlier than the two recorded auditions
# Find the positions of Waite, Kammer, and Lugo
w_pos = Int('w_pos')
k_pos = Int('k_pos')
l_pos = Int('l_pos')

# Encode the positions of W, K, and L
solver.add(Or([And(order[i] == W, w_pos == i) for i in range(6)]))
solver.add(Or([And(order[i] == K, k_pos == i) for i in range(6)]))
solver.add(Or([And(order[i] == L, l_pos == i) for i in range(6)]))

# Waite's position must be less than Kammer's and Lugo's
solver.add(w_pos < k_pos)
solver.add(w_pos < l_pos)

# Constraint 4: Kammer's audition must take place earlier than Trillo's
# Find the position of Trillo
t_pos = Int('t_pos')
solver.add(Or([And(order[i] == T, t_pos == i) for i in range(6)]))
solver.add(k_pos < t_pos)

# Constraint 5: Zinn's audition must take place earlier than Yoshida's
# Find the positions of Zinn and Yoshida
z_pos = Int('z_pos')
y_pos = Int('y_pos')
solver.add(Or([And(order[i] == Z, z_pos == i) for i in range(6)]))
solver.add(Or([And(order[i] == Y, y_pos == i) for i in range(6)]))
solver.add(z_pos < y_pos)

# Now, evaluate each option for the second audition
found_options = []

# Option A: Kammer's audition is second
solver.push()
solver.add(order[1] == K)
result_a = solver.check()
if result_a == sat:
    found_options.append("A")
solver.pop()

# Option B: Lugo's audition is second
solver.push()
solver.add(order[1] == L)
result_b = solver.check()
if result_b == sat:
    found_options.append("B")
solver.pop()

# Option C: Trillo's audition is second
solver.push()
solver.add(order[1] == T)
result_c = solver.check()
if result_c == sat:
    found_options.append("C")
solver.pop()

# Option D: Waite's audition is second
solver.push()
solver.add(order[1] == W)
result_d = solver.check()
if result_d == sat:
    found_options.append("D")
solver.pop()

# Option E: Zinn's audition is second
solver.push()
solver.add(order[1] == Z)
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