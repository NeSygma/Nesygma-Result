from z3 import *

solver = Solver()

# Declare symbolic variables for the order of houses
# We have 7 positions: 0 (first morning), 1 (second morning), 2 (third afternoon), 3 (fourth afternoon), 4 (fifth afternoon), 5 (sixth evening), 6 (seventh evening)
houses = [Int(f'house_{i}') for i in range(7)]

# Each house is one of J, K, L, M, N, O, P
# We will use integers 0-6 to represent J, K, L, M, N, O, P for simplicity
# Let's map: J=0, K=1, L=2, M=3, N=4, O=5, P=6
all_houses = [0, 1, 2, 3, 4, 5, 6]

# Each position must be assigned a unique house
solver.add(Distinct(houses))

# Add constraints for each house
for pos in range(7):
    solver.add(Or([houses[pos] == h for h in all_houses]))

# Rule 1: J must be shown in the evening (positions 5 and 6)
solver.add(Or(houses[5] == 0, houses[6] == 0))

# Rule 2: K cannot be shown in the morning (positions 0 and 1)
solver.add(Not(Or(houses[0] == 1, houses[1] == 1)))

# Rule 3: L must be shown after K and before M
# We need to find the positions of K, L, and M
# Let's define auxiliary variables for the positions of K, L, and M
k_pos = Int('k_pos')
l_pos = Int('l_pos')
m_pos = Int('m_pos')

# Constraints for k_pos, l_pos, m_pos
solver.add(k_pos >= 0, k_pos < 7)
solver.add(l_pos >= 0, l_pos < 7)
solver.add(m_pos >= 0, m_pos < 7)
solver.add(Distinct([k_pos, l_pos, m_pos]))

# Each of k_pos, l_pos, m_pos must correspond to the actual position of K, L, M
solver.add(Or([And(houses[i] == 1, k_pos == i) for i in range(7)]))
solver.add(Or([And(houses[i] == 2, l_pos == i) for i in range(7)]))
solver.add(Or([And(houses[i] == 3, m_pos == i) for i in range(7)]))

# L must be shown after K
solver.add(l_pos > k_pos)

# L must be shown before M
solver.add(l_pos < m_pos)

# Now, evaluate each option
found_options = []

# Option A: K is shown in the evening (positions 5 or 6)
opt_a_constr = Or(houses[5] == 1, houses[6] == 1)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
    print("Option A is valid")
else:
    print("Option A is invalid")
solver.pop()

# Option B: L is shown in the afternoon (positions 2, 3, or 4)
opt_b_constr = Or([houses[i] == 2 for i in range(2, 5)])
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
    print("Option B is valid")
else:
    print("Option B is invalid")
solver.pop()

# Option C: L is shown in the evening (positions 5 or 6)
opt_c_constr = Or(houses[5] == 2, houses[6] == 2)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
    print("Option C is valid")
else:
    print("Option C is invalid")
solver.pop()

# Option D: M is shown in the morning (positions 0 or 1)
opt_d_constr = Or(houses[0] == 3, houses[1] == 3)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
    print("Option D is valid")
else:
    print("Option D is invalid")
solver.pop()

# Option E: M is shown in the afternoon (positions 2, 3, or 4)
opt_e_constr = Or([houses[i] == 3 for i in range(2, 5)])
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
    print("Option E is valid")
else:
    print("Option E is invalid")
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