from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Assign IDs to antiques for easier handling
harmonica = 0
lamp = 1
mirror = 2
sundial = 3
table = 4
vase = 5

# Create a solver
solver = Solver()

# auction is a Z3 Array from day (0-5) to antique (0-5)
# Use Z3 Array to allow symbolic indexing
auction = Array('auction', IntSort(), IntSort())

# Each antique is auctioned exactly once (permutation)
# We need to ensure that the array is a permutation of the antiques
# This is tricky with Arrays, so we'll use a Python list of variables and then convert to an Array
# Alternative: Use a Python list of variables and enforce distinctness and range
auction_vars = [Int(f'auction_{i}') for i in range(6)]
for a in [harmonica, lamp, mirror, sundial, table, vase]:
    solver.add(Or([auction_vars[i] == a for i in range(6)]))
solver.add(Distinct(auction_vars))

# Helper function to check if antique x is auctioned before antique y
def before(x, y):
    # There exists a day i where x is auctioned and a day j where y is auctioned, and i < j
    return Or([And(auction_vars[i] == x, auction_vars[j] == y, i < j) for i in range(6) for j in range(6)])

# Constraint 1: The sundial is not auctioned on June 1st (day 0)
solver.add(auction_vars[0] != sundial)

# Constraint 2: If harmonica is before lamp, then mirror is before lamp
solver.add(Implies(before(harmonica, lamp), before(mirror, lamp)))

# Constraint 3: Sundial is before mirror AND sundial is before vase
solver.add(before(sundial, mirror))
solver.add(before(sundial, vase))

# Constraint 4: Table is before harmonica OR before vase, but not both
solver.add(Xor(before(table, harmonica), before(table, vase)))

# Find the day when vase is auctioned
vase_day = Int('vase_day')
solver.add(vase_day >= 0, vase_day <= 5)
solver.add(auction_vars[vase_day] == vase)

# The day immediately preceding the vase day
prev_day = Int('prev_day')
solver.add(prev_day == vase_day - 1)
solver.add(prev_day >= 0)  # Ensure it's a valid day (not negative)

# Now, check each option to see if it can be the antique on the day before vase
found_options = []

# Option A: harmonica is on the day before vase
solver.push()
solver.add(auction_vars[prev_day] == harmonica)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: lamp is on the day before vase
solver.push()
solver.add(auction_vars[prev_day] == lamp)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: mirror is on the day before vase
solver.push()
solver.add(auction_vars[prev_day] == mirror)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: sundial is on the day before vase
solver.push()
solver.add(auction_vars[prev_day] == sundial)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: table is on the day before vase
solver.push()
solver.add(auction_vars[prev_day] == table)
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