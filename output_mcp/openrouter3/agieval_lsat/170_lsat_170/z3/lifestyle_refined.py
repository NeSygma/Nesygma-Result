from z3 import *

solver = Solver()

# Declare variables
photo = [Int(f'photo_{i}') for i in range(6)]

# Domain constraints
for i in range(6):
    solver.add(Or(photo[i] == 0, photo[i] == 1, photo[i] == 2))

# Photographer counts
f_count = Sum([If(photo[i] == 0, 1, 0) for i in range(6)])
g_count = Sum([If(photo[i] == 1, 1, 0) for i in range(6)])
h_count = Sum([If(photo[i] == 2, 1, 0) for i in range(6)])

solver.add(f_count >= 1, f_count <= 3)
solver.add(g_count >= 1, g_count <= 3)
solver.add(h_count >= 1, h_count <= 3)

# Lifestyle-Metro photographer overlap constraint
lifestyle_has_f = Or(photo[0] == 0, photo[1] == 0)
lifestyle_has_g = Or(photo[0] == 1, photo[1] == 1)
lifestyle_has_h = Or(photo[0] == 2, photo[1] == 2)

metro_has_f = Or(photo[2] == 0, photo[3] == 0)
metro_has_g = Or(photo[2] == 1, photo[3] == 1)
metro_has_h = Or(photo[2] == 2, photo[3] == 2)

solver.add(Or(
    And(lifestyle_has_f, metro_has_f),
    And(lifestyle_has_g, metro_has_g),
    And(lifestyle_has_h, metro_has_h)
))

# Hue in Lifestyle = Fuentes in Sports
h_lifestyle = Sum([If(photo[i] == 2, 1, 0) for i in range(2)])
f_sports = Sum([If(photo[i] == 0, 1, 0) for i in range(4, 6)])
solver.add(h_lifestyle == f_sports)

# No Gagnon in Sports
solver.add(photo[4] != 1)
solver.add(photo[5] != 1)

# Question condition: one Gagnon and one Hue in Lifestyle
solver.add(Or(
    And(photo[0] == 1, photo[1] == 2),
    And(photo[0] == 2, photo[1] == 1)
))

# Define answer options
# A: Exactly one photograph in the Metro section is by Fuentes
opt_a = Sum([If(photo[i] == 0, 1, 0) for i in range(2, 4)]) == 1

# B: Exactly one photograph in the Metro section is by Gagnon
opt_b = Sum([If(photo[i] == 1, 1, 0) for i in range(2, 4)]) == 1

# C: Both photographs in the Metro section are by Gagnon
opt_c = Sum([If(photo[i] == 1, 1, 0) for i in range(2, 4)]) == 2

# D: Exactly one photograph in the Sports section is by Hue
opt_d = Sum([If(photo[i] == 2, 1, 0) for i in range(4, 6)]) == 1

# E: Both photographs in the Sports section are by Hue
opt_e = Sum([If(photo[i] == 2, 1, 0) for i in range(4, 6)]) == 2

# Check which options are necessarily true
# For each option, check if it's true in ALL valid scenarios
# We do this by checking if the negation is unsatisfiable

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
necessary_options = []

for letter, constr in options:
    # Check if the option is necessarily true
    # Create a solver that checks if the option can be false
    s = Solver()
    # Add all base constraints
    s.add([Or(photo[i] == 0, photo[i] == 1, photo[i] == 2) for i in range(6)])
    s.add(f_count >= 1, f_count <= 3)
    s.add(g_count >= 1, g_count <= 3)
    s.add(h_count >= 1, h_count <= 3)
    s.add(Or(
        And(lifestyle_has_f, metro_has_f),
        And(lifestyle_has_g, metro_has_g),
        And(lifestyle_has_h, metro_has_h)
    ))
    s.add(h_lifestyle == f_sports)
    s.add(photo[4] != 1)
    s.add(photo[5] != 1)
    s.add(Or(
        And(photo[0] == 1, photo[1] == 2),
        And(photo[0] == 2, photo[1] == 1)
    ))
    # Add the negation of the option
    s.add(Not(constr))
    
    if s.check() == unsat:
        necessary_options.append(letter)

if len(necessary_options) == 1:
    print("STATUS: sat")
    print(f"answer:{necessary_options[0]}")
elif len(necessary_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple necessary options found {necessary_options}")
else:
    print("STATUS: unsat")
    print("Refine: No necessary options found")