from z3 import *

solver = Solver()

# Variables: each person assigned to zone 1, 2, or 3
Kim = Int('Kim')
Mahr = Int('Mahr')
Parra = Int('Parra')
Quinn = Int('Quinn')
Stuckey = Int('Stuckey')
Tiao = Int('Tiao')
Udall = Int('Udall')

people = [Kim, Mahr, Parra, Quinn, Stuckey, Tiao, Udall]

# Each person works in exactly one zone (1, 2, or 3)
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

# Constraint 5: More reps in Zone 3 than in Zone 2
count_z1 = Sum([If(p == 1, 1, 0) for p in people])
count_z2 = Sum([If(p == 2, 1, 0) for p in people])
count_z3 = Sum([If(p == 3, 1, 0) for p in people])

solver.add(count_z3 > count_z2)

# Additional condition: More reps in Zone 1 than in Zone 3
solver.add(count_z1 > count_z3)

# Now test each answer choice
# (A) Kim works in Zone 2
opt_a = (Kim == 2)
# (B) Mahr works in Zone 2
opt_b = (Mahr == 2)
# (C) Parra works in Zone 3
opt_c = (Parra == 3)
# (D) Tiao works in Zone 1
opt_d = (Tiao == 1)
# (E) Udall works in Zone 3
opt_e = (Udall == 3)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: Kim={m[Kim]}, Mahr={m[Mahr]}, Parra={m[Parra]}, Quinn={m[Quinn]}, Stuckey={m[Stuckey]}, Tiao={m[Tiao]}, Udall={m[Udall]}")
    else:
        print(f"Option {letter} is UNSAT")
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