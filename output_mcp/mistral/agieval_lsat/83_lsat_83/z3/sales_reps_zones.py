from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each sales representative's zone
# 1: Zone 1, 2: Zone 2, 3: Zone 3
kim = Int('kim')
mahr = Int('mahr')
parra = Int('parra')
quinn = Int('quinn')
stuckey = Int('stuckey')
tiao = Int('tiao')
udall = Int('udall')

# Each representative works in exactly one zone
solver = Solver()
solver.add(kim >= 1, kim <= 3)
solver.add(mahr >= 1, mahr <= 3)
solver.add(parra >= 1, parra <= 3)
solver.add(quinn >= 1, quinn <= 3)
solver.add(stuckey >= 1, stuckey <= 3)
solver.add(tiao >= 1, tiao <= 3)
solver.add(udall >= 1, udall <= 3)

# Constraint: Either Parra or Tiao (but not both) works in Zone 1
solver.add(Or(And(parra == 1, tiao != 1), And(tiao == 1, parra != 1)))

# Constraint: Either Tiao or Udall (but not both) works in Zone 2
solver.add(Or(And(tiao == 2, udall != 2), And(udall == 2, tiao != 2)))

# Constraint: Parra and Quinn work in the same sales zone
solver.add(parra == quinn)

# Constraint: Stuckey and Udall work in the same sales zone
solver.add(stuckey == udall)

# Constraint: More representatives in Zone 3 than in Zone 2
zone_counts = [
    kim, mahr, parra, quinn, stuckey, tiao, udall
]
count_zone1 = Sum([If(z == 1, 1, 0) for z in zone_counts])
count_zone2 = Sum([If(z == 2, 1, 0) for z in zone_counts])
count_zone3 = Sum([If(z == 3, 1, 0) for z in zone_counts])
solver.add(count_zone3 > count_zone2)

# Conditional: If more representatives work in Zone 1 than in Zone 3
# Then evaluate the options
solver.push()
solver.add(count_zone1 > count_zone3)

# Now evaluate each option to see which could be true
found_options = []

# Option A: Kim works in Zone 2
solver.push()
solver.add(kim == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Mahr works in Zone 2
solver.push()
solver.add(mahr == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Parra works in Zone 3
solver.push()
solver.add(parra == 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Tiao works in Zone 1
solver.push()
solver.add(tiao == 1)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Udall works in Zone 3
solver.push()
solver.add(udall == 3)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

solver.pop()  # Pop the conditional constraint

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")