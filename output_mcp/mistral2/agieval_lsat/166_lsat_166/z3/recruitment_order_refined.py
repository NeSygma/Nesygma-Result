from z3 import *

solver = Solver()

# Declare symbolic variables for the recruitment order (0 to 6, where 0 is first and 6 is last)
# Each position is assigned an accomplice: Peters=0, Quinn=1, Rovero=2, Stanton=3, Tao=4, Villas=5, White=6
order = [Int(f'order_{i}') for i in range(7)]

# Each position must be assigned a unique accomplice
accomplices = [0, 1, 2, 3, 4, 5, 6]  # Peters, Quinn, Rovero, Stanton, Tao, Villas, White
solver.add(Distinct(order))

# Peters was recruited fourth (position 3, 0-based index)
solver.add(order[3] == 0)

# Villas was recruited immediately before White
# This means there exists an index i such that order[i] = 5 and order[i+1] = 6
solver.add(Or([And(order[i] == 5, order[i+1] == 6) for i in range(6)]))

# Quinn was recruited earlier than Rovero
# Quinn=1, Rovero=2
solver.add(Or([And(order[i] == 1, order[j] == 2, i < j) for i in range(7) for j in range(7) if i < j]))

# Stanton was recruited neither immediately before nor immediately after Tao
# Stanton=3, Tao=4
for i in range(6):
    solver.add(Not(And(order[i] == 3, order[i+1] == 4)))
    solver.add(Not(And(order[i] == 4, order[i+1] == 3)))

# Additional constraints from the question:
# White was recruited earlier than Rovero and Rovero was recruited earlier than Tao
# White=6, Rovero=2, Tao=4
# We need to enforce that the position of White is less than the position of Rovero, and the position of Rovero is less than the position of Tao
# To do this, we first find the positions of White, Rovero, and Tao
white_pos = Int('white_pos')
rovero_pos = Int('rovero_pos')
tao_pos = Int('tao_pos')

solver.add(white_pos == order.index(6))
solver.add(rovero_pos == order.index(2))
solver.add(tao_pos == order.index(4))

solver.add(white_pos < rovero_pos)
solver.add(rovero_pos < tao_pos)

# Now, evaluate each option to see which one could be true
found_options = []

# Option A: Quinn was recruited first
solver.push()
solver.add(order[0] == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Rovero was recruited third
solver.push()
solver.add(order[2] == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Stanton was recruited second
solver.push()
solver.add(order[1] == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Tao was recruited sixth
solver.push()
solver.add(order[5] == 4)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Villas was recruited sixth
solver.push()
solver.add(order[5] == 5)
if solver.check() == sat:
    found_options.append("E")
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