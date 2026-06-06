from z3 import *

solver = Solver()

# Declare symbolic variables for each employee's parking space
robertson = Int('robertson')
souza = Int('souza')
togowa = Int('togowa')
vaughn = Int('vaughn')
xu = Int('xu')
young = Int('young')

# Each employee gets a unique parking space (1-6)
spaces = [robertson, souza, togowa, vaughn, xu, young]
solver.add(Distinct(spaces))
solver.add([space >= 1 for space in spaces])
solver.add([space <= 6 for space in spaces])

# Constraints from the problem
solver.add(young > togowa)  # Young must be assigned a higher-numbered parking space than Togowa
solver.add(xu > souza)      # Xu must be assigned a higher-numbered parking space than Souza
solver.add(robertson > young)  # Robertson must be assigned a higher-numbered parking space than Young
solver.add(Or(robertson == 1, robertson == 2, robertson == 3, robertson == 4))  # Robertson must be assigned parking space #1, #2, #3, or #4

# Additional constraint from the question: Young is assigned a higher-numbered parking space than Souza
solver.add(young > souza)

# Define the constraints for each multiple-choice option
# (A) Togowa is assigned parking space #1
opt_a_constr = (togowa == 1)

# (B) Young is assigned parking space #2
opt_b_constr = (young == 2)

# (C) Robertson is assigned parking space #3
opt_c_constr = (robertson == 3)

# (D) Souza is assigned parking space #3
opt_d_constr = (souza == 3)

# (E) Vaughn is assigned parking space #4
opt_e_constr = (vaughn == 4)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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