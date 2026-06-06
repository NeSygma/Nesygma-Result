from z3 import *

solver = Solver()

# Define symbolic constants for each accomplice
Peters, Quinn, Rovero, Stanton, Tao, Villas, White = Ints('Peters Quinn Rovero Stanton Tao Villas White')

# Peters, Quinn, Rovero, Stanton, Tao, Villas, White are distinct
solver.add(Peters != Quinn, Peters != Rovero, Peters != Stanton, Peters != Tao, Peters != Villas, Peters != White)
solver.add(Quinn != Rovero, Quinn != Stanton, Quinn != Tao, Quinn != Villas, Quinn != White)
solver.add(Rovero != Stanton, Rovero != Tao, Rovero != Villas, Rovero != White)
solver.add(Stanton != Tao, Stanton != Villas, Stanton != White)
solver.add(Tao != Villas, Tao != White)
solver.add(Villas != White)

# order is a list of 7 integers representing the order of recruitment
# Each position in the order is assigned one of the accomplices
order = [Int(f"pos_{i}") for i in range(7)]

# Each position must be assigned to exactly one accomplice
solver.add(Distinct(order))

# Peters was recruited fourth (position 3, since indexing starts at 0)
solver.add(order[3] == Peters)

# Villas was recruited immediately before White
# This means that Villas and White must be adjacent in the order, with Villas before White
solver.add(Or(
    And(order[0] == Villas, order[1] == White),
    And(order[1] == Villas, order[2] == White),
    And(order[2] == Villas, order[3] == White),
    And(order[3] == Villas, order[4] == White),
    And(order[4] == Villas, order[5] == White),
    And(order[5] == Villas, order[6] == White)
))

# Quinn was recruited earlier than Rovero
# This means that Quinn's position is less than Rovero's position
# We need to ensure that Quinn appears before Rovero in the order
solver.add(Or(
    And(order[0] == Quinn, Or(order[1] == Rovero, order[2] == Rovero, order[3] == Rovero, order[4] == Rovero, order[5] == Rovero, order[6] == Rovero)),
    And(order[1] == Quinn, Or(order[2] == Rovero, order[3] == Rovero, order[4] == Rovero, order[5] == Rovero, order[6] == Rovero)),
    And(order[2] == Quinn, Or(order[3] == Rovero, order[4] == Rovero, order[5] == Rovero, order[6] == Rovero)),
    And(order[3] == Quinn, Or(order[4] == Rovero, order[5] == Rovero, order[6] == Rovero)),
    And(order[4] == Quinn, Or(order[5] == Rovero, order[6] == Rovero)),
    And(order[5] == Quinn, order[6] == Rovero)
))

# Stanton was recruited neither immediately before nor immediately after Tao
# This means that Stanton and Tao cannot be adjacent in the order
for i in range(6):
    solver.add(Not(And(Or(order[i] == Stanton, order[i] == Tao), Or(order[i+1] == Stanton, order[i+1] == Tao))))

# Now, evaluate each option
found_options = []

# Option A: Quinn, Tao, Stanton, Peters, Villas, White, Rovero
solver.push()
opt_a_constr = And(
    order[0] == Quinn,
    order[1] == Tao,
    order[2] == Stanton,
    order[3] == Peters,
    order[4] == Villas,
    order[5] == White,
    order[6] == Rovero
)
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Quinn, White, Rovero, Peters, Stanton, Villas, Tao
solver.push()
opt_b_constr = And(
    order[0] == Quinn,
    order[1] == White,
    order[2] == Rovero,
    order[3] == Peters,
    order[4] == Stanton,
    order[5] == Villas,
    order[6] == Tao
)
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Villas, White, Quinn, Stanton, Peters, Tao, Rovero
solver.push()
opt_c_constr = And(
    order[0] == Villas,
    order[1] == White,
    order[2] == Quinn,
    order[3] == Stanton,
    order[4] == Peters,
    order[5] == Tao,
    order[6] == Rovero
)
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Villas, White, Stanton, Peters, Quinn, Tao, Rovero
solver.push()
opt_d_constr = And(
    order[0] == Villas,
    order[1] == White,
    order[2] == Stanton,
    order[3] == Peters,
    order[4] == Quinn,
    order[5] == Tao,
    order[6] == Rovero
)
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Villas, White, Stanton, Peters, Rovero, Tao, Quinn
solver.push()
opt_e_constr = And(
    order[0] == Villas,
    order[1] == White,
    order[2] == Stanton,
    order[3] == Peters,
    order[4] == Rovero,
    order[5] == Tao,
    order[6] == Quinn
)
solver.add(opt_e_constr)
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