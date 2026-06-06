from z3 import *

# Declare variables for each person's zone (1,2,3)
Kim = Int('Kim')
Mahr = Int('Mahr')
Parra = Int('Parra')
Quinn = Int('Quinn')
Stuckey = Int('Stuckey')
Tiao = Int('Tiao')
Udall = Int('Udall')

solver = Solver()

# Domain constraints: each zone between 1 and 3
persons = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]
for p in persons:
    solver.add(p >= 1, p <= 3)

# Constraint 1: Either Parra or Tiao (but not both) works in Zone 1.
solver.add(Or(And(Parra == 1, Tiao != 1), And(Parra != 1, Tiao == 1)))

# Constraint 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add(Or(And(Tiao == 2, Udall != 2), And(Tiao != 2, Udall == 2)))

# Constraint 3: Parra and Quinn work in the same sales zone.
solver.add(Parra == Quinn)

# Constraint 4: Stuckey and Udall work in the same sales zone.
solver.add(Stuckey == Udall)

# Constraint 5: More reps in Zone 3 than Zone 2.
count2 = Sum([If(p == 2, 1, 0) for p in persons])
count3 = Sum([If(p == 3, 1, 0) for p in persons])
solver.add(count3 > count2)

# Additional condition: More reps in Zone 1 than Zone 3.
count1 = Sum([If(p == 1, 1, 0) for p in persons])
solver.add(count1 > count3)

# Now evaluate each option
found_options = []

# Option A: Kim works in Zone 2.
solver.push()
solver.add(Kim == 2)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: Mahr works in Zone 2.
solver.push()
solver.add(Mahr == 2)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: Parra works in Zone 3.
solver.push()
solver.add(Parra == 3)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: Tiao works in Zone 1.
solver.push()
solver.add(Tiao == 1)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Udall works in Zone 3.
solver.push()
solver.add(Udall == 3)
if solver.check() == sat:
    found_options.append('E')
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