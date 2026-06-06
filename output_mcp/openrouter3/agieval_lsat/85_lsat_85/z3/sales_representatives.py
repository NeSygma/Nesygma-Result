from z3 import *

# Declare zone variables for each person
Kim = Int('Kim')
Mahr = Int('Mahr')
Parra = Int('Parra')
Quinn = Int('Quinn')
Stuckey = Int('Stuckey')
Tiao = Int('Tiao')
Udall = Int('Udall')

people = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]

solver = Solver()

# Base constraints: each person works in exactly one zone (1, 2, or 3)
for p in people:
    solver.add(Or(p == 1, p == 2, p == 3))

# Constraint 1: Either Parra or Tiao (but not both) works in Zone 1
solver.add(Or(And(Parra == 1, Tiao != 1), And(Parra != 1, Tiao == 1)))

# Constraint 2: Either Tiao or Udall (but not both) works in Zone 2
solver.add(Or(And(Tiao == 2, Udall != 2), And(Tiao != 2, Udall == 2)))

# Constraint 3: Parra and Quinn work in the same zone
solver.add(Parra == Quinn)

# Constraint 4: Stuckey and Udall work in the same zone
solver.add(Stuckey == Udall)

# Constraint 5: More representatives in Zone 3 than in Zone 2
# Count people in Zone 3 and Zone 2
zone3_count = Sum([If(p == 3, 1, 0) for p in people])
zone2_count = Sum([If(p == 2, 1, 0) for p in people])
solver.add(zone3_count > zone2_count)

# Now test each answer choice
# Answer choices represent the complete list of people in Zone 3
found_options = []

# Option A: Kim, Mahr in Zone 3
solver.push()
solver.add(Kim == 3)
solver.add(Mahr == 3)
# Ensure others are NOT in Zone 3
solver.add(Parra != 3)
solver.add(Quinn != 3)
solver.add(Stuckey != 3)
solver.add(Tiao != 3)
solver.add(Udall != 3)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Kim, Tiao in Zone 3
solver.push()
solver.add(Kim == 3)
solver.add(Tiao == 3)
# Ensure others are NOT in Zone 3
solver.add(Mahr != 3)
solver.add(Parra != 3)
solver.add(Quinn != 3)
solver.add(Stuckey != 3)
solver.add(Udall != 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Parra, Quinn in Zone 3
solver.push()
solver.add(Parra == 3)
solver.add(Quinn == 3)
# Ensure others are NOT in Zone 3
solver.add(Kim != 3)
solver.add(Mahr != 3)
solver.add(Stuckey != 3)
solver.add(Tiao != 3)
solver.add(Udall != 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Stuckey, Tiao, Udall in Zone 3
solver.push()
solver.add(Stuckey == 3)
solver.add(Tiao == 3)
solver.add(Udall == 3)
# Ensure others are NOT in Zone 3
solver.add(Kim != 3)
solver.add(Mahr != 3)
solver.add(Parra != 3)
solver.add(Quinn != 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Parra, Quinn, Stuckey, Udall in Zone 3
solver.push()
solver.add(Parra == 3)
solver.add(Quinn == 3)
solver.add(Stuckey == 3)
solver.add(Udall == 3)
# Ensure others are NOT in Zone 3
solver.add(Kim != 3)
solver.add(Mahr != 3)
solver.add(Tiao != 3)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")