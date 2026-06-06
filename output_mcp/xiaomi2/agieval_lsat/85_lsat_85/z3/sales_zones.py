from z3 import *

solver = Solver()

# Sales reps: 0=Kim, 1=Mahr, 2=Parra, 3=Quinn, 4=Stuckey, 5=Tiao, 6=Udall
names = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]
zone = [Int(f'zone_{n}') for n in names]

# Each rep works in exactly one zone (1, 2, or 3)
for z in zone:
    solver.add(Or(z == 1, z == 2, z == 3))

# Constraint 1: Exactly one of Parra or Tiao works in Zone 1
solver.add(Or(And(zone[2] == 1, zone[5] != 1), And(zone[2] != 1, zone[5] == 1)))

# Constraint 2: Exactly one of Tiao or Udall works in Zone 2
solver.add(Or(And(zone[5] == 2, zone[6] != 2), And(zone[5] != 2, zone[6] == 2)))

# Constraint 3: Parra and Quinn work in the same zone
solver.add(zone[2] == zone[3])

# Constraint 4: Stuckey and Udall work in the same zone
solver.add(zone[4] == zone[6])

# Constraint 5: More reps in Zone 3 than Zone 2
count_z2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
count_z3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
solver.add(count_z3 > count_z2)

# Define each option as "exactly these reps are in Zone 3"
# Option A: Kim, Mahr in Zone 3 (and only them)
opt_a_constr = And(
    zone[0] == 3, zone[1] == 3,  # Kim, Mahr in Zone 3
    zone[2] != 3, zone[3] != 3, zone[4] != 3, zone[5] != 3, zone[6] != 3  # others not in Zone 3
)

# Option B: Kim, Tiao in Zone 3
opt_b_constr = And(
    zone[0] == 3, zone[5] == 3,
    zone[1] != 3, zone[2] != 3, zone[3] != 3, zone[4] != 3, zone[6] != 3
)

# Option C: Parra, Quinn in Zone 3
opt_c_constr = And(
    zone[2] == 3, zone[3] == 3,
    zone[0] != 3, zone[1] != 3, zone[4] != 3, zone[5] != 3, zone[6] != 3
)

# Option D: Stuckey, Tiao, Udall in Zone 3
opt_d_constr = And(
    zone[4] == 3, zone[5] == 3, zone[6] == 3,
    zone[0] != 3, zone[1] != 3, zone[2] != 3, zone[3] != 3
)

# Option E: Parra, Quinn, Stuckey, Udall in Zone 3
opt_e_constr = And(
    zone[2] == 3, zone[3] == 3, zone[4] == 3, zone[6] == 3,
    zone[0] != 3, zone[1] != 3, zone[5] != 3
)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for i, n in enumerate(names):
            print(f"  {n} -> Zone {m[zone[i]]}")
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