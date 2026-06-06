from z3 import *

# Declare symbolic variables for each representative's zone
Kim = Int('Kim')
Mahr = Int('Mahr')
Parra = Int('Parra')
Quinn = Int('Quinn')
Stuckey = Int('Stuckey')
Tiao = Int('Tiao')
Udall = Int('Udall')

# All representatives are assigned to one of the three zones
solver = Solver()
solver.add(Kim >= 1, Kim <= 3)
solver.add(Mahr >= 1, Mahr <= 3)
solver.add(Parra >= 1, Parra <= 3)
solver.add(Quinn >= 1, Quinn <= 3)
solver.add(Stuckey >= 1, Stuckey <= 3)
solver.add(Tiao >= 1, Tiao <= 3)
solver.add(Udall >= 1, Udall <= 3)

# Constraint 1: Either Parra or Tiao (but not both) works in Zone 1
solver.add(Or(And(Parra == 1, Tiao != 1), And(Tiao == 1, Parra != 1)))

# Constraint 2: Either Tiao or Udall (but not both) works in Zone 2
solver.add(Or(And(Tiao == 2, Udall != 2), And(Udall == 2, Tiao != 2)))

# Constraint 3: Parra and Quinn work in the same zone
solver.add(Parra == Quinn)

# Constraint 4: Stuckey and Udall work in the same zone
solver.add(Stuckey == Udall)

# Constraint 5: More representatives in Zone 3 than in Zone 2
# Count the number of representatives in Zone 3 and Zone 2
zone3_count = Sum([If(Kim == 3, 1, 0),
                   If(Mahr == 3, 1, 0),
                   If(Parra == 3, 1, 0),
                   If(Quinn == 3, 1, 0),
                   If(Stuckey == 3, 1, 0),
                   If(Tiao == 3, 1, 0),
                   If(Udall == 3, 1, 0)])

zone2_count = Sum([If(Kim == 2, 1, 0),
                   If(Mahr == 2, 1, 0),
                   If(Parra == 2, 1, 0),
                   If(Quinn == 2, 1, 0),
                   If(Stuckey == 2, 1, 0),
                   If(Tiao == 2, 1, 0),
                   If(Udall == 2, 1, 0)])

solver.add(zone3_count > zone2_count)

# Define the answer choices as constraints for Zone 3
# Option A: Kim, Mahr
opt_a = And(Kim == 3, Mahr == 3,
            Parra != 3, Quinn != 3,
            Or(Stuckey != 3, Udall != 3),
            Tiao != 3)

# Option B: Kim, Tiao
opt_b = And(Kim == 3, Tiao == 3,
            Mahr != 3,
            Parra != 3, Quinn != 3,
            Or(Stuckey != 3, Udall != 3))

# Option C: Parra, Quinn
opt_c = And(Parra == 3, Quinn == 3,
            Or(Kim != 3, Mahr != 3),
            Or(Stuckey != 3, Udall != 3),
            Tiao != 3)

# Option D: Stuckey, Tiao, Udall
opt_d = And(Stuckey == 3, Tiao == 3, Udall == 3,
            Or(Kim != 3, Mahr != 3),
            Parra != 3, Quinn != 3)

# Option E: Parra, Quinn, Stuckey, Udall
opt_e = And(Parra == 3, Quinn == 3, Stuckey == 3, Udall == 3,
            Or(Kim != 3, Mahr != 3),
            Tiao != 3)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
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