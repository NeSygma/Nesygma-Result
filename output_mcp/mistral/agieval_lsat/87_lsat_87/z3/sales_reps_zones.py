from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each sales representative's zone
# 0: Zone 1, 1: Zone 2, 2: Zone 3
kim = Int('kim')
mahr = Int('mahr')
parra = Int('parra')
quinn = Int('quinn')
stuckey = Int('stuckey')
tiao = Int('tiao')
udall = Int('udall')

# Base constraints: each representative is in exactly one zone
solver = Solver()
solver.add(kim >= 0, kim <= 2)
solver.add(mahr >= 0, mahr <= 2)
solver.add(parra >= 0, parra <= 2)
solver.add(quinn >= 0, quinn <= 2)
solver.add(stuckey >= 0, stuckey <= 2)
solver.add(tiao >= 0, tiao <= 2)
solver.add(udall >= 0, udall <= 2)

# Either Parra or Tiao (but not both) works in Zone 1
solver.add(Or(And(parra == 0, tiao != 0), And(tiao == 0, parra != 0)))

# Either Tiao or Udall (but not both) works in Zone 2
solver.add(Or(And(tiao == 1, udall != 1), And(udall == 1, tiao != 1)))

# Parra and Quinn work in the same sales zone
solver.add(parra == quinn)

# Stuckey and Udall work in the same sales zone
solver.add(stuckey == udall)

# There are more representatives in Zone 3 than in Zone 2
# Count the number of representatives in Zone 3 and Zone 2
zone_counts = [
    Sum([If(kim == 2, 1, 0), 
         If(mahr == 2, 1, 0), 
         If(parra == 2, 1, 0), 
         If(quinn == 2, 1, 0), 
         If(stuckey == 2, 1, 0), 
         If(tiao == 2, 1, 0), 
         If(udall == 2, 1, 0)]) == 
    Sum([If(kim == 1, 1, 0), 
         If(mahr == 1, 1, 0), 
         If(parra == 1, 1, 0), 
         If(quinn == 1, 1, 0), 
         If(stuckey == 1, 1, 0), 
         If(tiao == 1, 1, 0), 
         If(udall == 1, 1, 0)]) + 1
]
solver.add(zone_counts)

# Additional condition for the question: Mahr and Stuckey work in the same zone
solver.add(mahr == stuckey)

# Evaluate each option
found_options = []

# Option A: Kim works in Zone 2
solver.push()
solver.add(kim == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Mahr works in Zone 1
solver.push()
solver.add(mahr == 0)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Parra works in Zone 3
solver.push()
solver.add(parra == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Stuckey works in Zone 2
solver.push()
solver.add(stuckey == 1)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Tiao works in Zone 1
solver.push()
solver.add(tiao == 0)
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