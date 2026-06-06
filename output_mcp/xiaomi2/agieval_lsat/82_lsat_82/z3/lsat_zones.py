from z3 import *

# Sales reps: Kim=0, Mahr=1, Parra=2, Quinn=3, Stuckey=4, Tiao=5, Udall=6
# Zones: 1, 2, 3
names = ["Kim", "Mahr", "Parra", "Quinn", "Stuckey", "Tiao", "Udall"]
KIM, MAHR, PARRA, QUINN, STUCKEY, TIAO, UDALL = range(7)

# Base constraints (always true)
def base_constraints(solver, zone):
    # Each rep assigned to zone 1, 2, or 3
    for i in range(7):
        solver.add(Or(zone[i] == 1, zone[i] == 2, zone[i] == 3))
    
    # Constraint 1: Either Parra or Tiao (but not both) in Zone 1
    solver.add(Xor(zone[PARRA] == 1, zone[TIAO] == 1))
    
    # Constraint 2: Either Tiao or Udall (but not both) in Zone 2
    solver.add(Xor(zone[TIAO] == 2, zone[UDALL] == 2))
    
    # Constraint 3: Parra and Quinn in the same zone
    solver.add(zone[PARRA] == zone[QUINN])
    
    # Constraint 4: Stuckey and Udall in the same zone
    solver.add(zone[STUCKEY] == zone[UDALL])
    
    # Constraint 5: More reps in Zone 3 than Zone 2
    count_z2 = Sum([If(zone[i] == 2, 1, 0) for i in range(7)])
    count_z3 = Sum([If(zone[i] == 3, 1, 0) for i in range(7)])
    solver.add(count_z3 > count_z2)

# Define each option as a zone assignment
options = {
    "A": {KIM: 1, PARRA: 1, STUCKEY: 2, UDALL: 2, MAHR: 3, QUINN: 3, TIAO: 3},
    "B": {KIM: 1, TIAO: 1, STUCKEY: 2, UDALL: 2, MAHR: 3, PARRA: 3, QUINN: 3},
    "C": {PARRA: 1, QUINN: 1, KIM: 2, UDALL: 2, MAHR: 3, STUCKEY: 3, TIAO: 3},
    "D": {STUCKEY: 1, UDALL: 1, KIM: 2, TIAO: 2, MAHR: 3, PARRA: 3, QUINN: 3},
    "E": {TIAO: 1, KIM: 2, PARRA: 2, QUINN: 2, STUCKEY: 3, UDALL: 3, MAHR: 3},
}

found_options = []
for letter, assignment in options.items():
    solver = Solver()
    zone = [Int(f'zone_{names[i]}') for i in range(7)]
    base_constraints(solver, zone)
    
    # Add the specific option's assignment
    for rep, z in assignment.items():
        solver.add(zone[rep] == z)
    
    if solver.check() == sat:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")