from z3 import *

# BENCHMARK_MODE: ON (model-finding with refinement on unsat)
BENCHMARK_MODE = True

# Define accomplices as integer constants for clarity
Peters = 0
Quinn = 1
Rovero = 2
Stanton = 3
Tao = 4
Villas = 5
White = 6

# Declare the order: a list of 7 Z3 integers, each representing an accomplice at a position
order = [Int(f'order_{i}') for i in range(7)]

# Helper: Ensure each position is assigned to exactly one accomplice and all are distinct
solver = Solver()
solver.add([And(order[i] >= 0, order[i] <= 6) for i in range(7)])
solver.add(Distinct(order))

# Constraint 1: Peters was recruited fourth (position 4 -> index 3)
solver.add(order[3] == Peters)

# Constraint 2: Villas was recruited immediately before White
# There exists an index i such that order[i] == Villas and order[i+1] == White
solver.add(Or([And(order[i] == Villas, order[i+1] == White) for i in range(6)]))

# Constraint 3: White was recruited immediately before Quinn
# There exists an index j such that order[j] == White and order[j+1] == Quinn
solver.add(Or([And(order[j] == White, order[j+1] == Quinn) for j in range(6)]))

# Constraint 4: Quinn was recruited earlier than Rovero
# If Quinn is at position i and Rovero at position j, then i < j
solver.add(Or([And(order[i] == Quinn, order[j] == Rovero, i < j) for i in range(7) for j in range(7) if i != j]))

# Constraint 5: Stanton was recruited neither immediately before nor immediately after Tao
# For all i, not (order[i] == Stanton and order[i+1] == Tao) and not (order[i] == Tao and order[i+1] == Stanton)
solver.add([Not(And(order[i] == Stanton, order[i+1] == Tao)) for i in range(6)])
solver.add([Not(And(order[i] == Tao, order[i+1] == Stanton)) for i in range(6)])

# Now, evaluate each multiple-choice option for "who must be sixth (position 6, index 5)?"
found_options = []

# Option A: Quinn is sixth
solver_a = Solver()
solver_a.add(solver.assertions())
solver_a.add(order[5] == Quinn)
if solver_a.check() == sat:
    found_options.append("A")

# Option B: Rovero is sixth
solver_b = Solver()
solver_b.add(solver.assertions())
solver_b.add(order[5] == Rovero)
if solver_b.check() == sat:
    found_options.append("B")

# Option C: Stanton is sixth
solver_c = Solver()
solver_c.add(solver.assertions())
solver_c.add(order[5] == Stanton)
if solver_c.check() == sat:
    found_options.append("C")

# Option D: Villas is sixth
solver_d = Solver()
solver_d.add(solver.assertions())
solver_d.add(order[5] == Villas)
if solver_d.check() == sat:
    found_options.append("D")

# Option E: White is sixth
solver_e = Solver()
solver_e.add(solver.assertions())
solver_e.add(order[5] == White)
if solver_e.check() == sat:
    found_options.append("E")

# Decide output based on found options
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")