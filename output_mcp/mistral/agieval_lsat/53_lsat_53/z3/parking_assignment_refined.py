from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# Declare symbolic variables for each employee's parking space
robertson = Int('robertson')
souza = Int('souza')
togowa = Int('togowa')
vaughn = Int('vaughn')
xu = Int('xu')
young = Int('young')

# Base constraints
solver = Solver()

# Each employee gets a unique parking space (1-6)
all_spaces = [robertson, souza, togowa, vaughn, xu, young]
solver.add(Distinct(all_spaces))
solver.add([space >= 1 for space in all_spaces])
solver.add([space <= 6 for space in all_spaces])

# Constraints from the problem
solver.add(young > togowa)  # Young must be assigned a higher-numbered parking space than Togowa
solver.add(xu > souza)      # Xu must be assigned a higher-numbered parking space than Souza
solver.add(robertson > young)  # Robertson must be assigned a higher-numbered parking space than Young
solver.add(Or(robertson == 1, robertson == 2, robertson == 3, robertson == 4))  # Robertson must be assigned parking space #1, #2, #3, or #4

# Additional constraint for this specific question: Robertson is assigned parking space #3
solver.add(robertson == 3)

# Now evaluate each option to see which one must be true
found_options = []

# Option A: Souza is assigned parking space #4
solver.push()
solver.add(souza == 4)
if solver.check() == sat:
    model = solver.model()
    print("Option A model:")
    print(f"robertson = {model[robertson]}")
    print(f"souza = {model[souza]}")
    print(f"togowa = {model[togowa]}")
    print(f"vaughn = {model[vaughn]}")
    print(f"xu = {model[xu]}")
    print(f"young = {model[young]}")
    found_options.append("A")
solver.pop()

# Option B: Togowa is assigned parking space #2
solver.push()
solver.add(togowa == 2)
if solver.check() == sat:
    model = solver.model()
    print("Option B model:")
    print(f"robertson = {model[robertson]}")
    print(f"souza = {model[souza]}")
    print(f"togowa = {model[togowa]}")
    print(f"vaughn = {model[vaughn]}")
    print(f"xu = {model[xu]}")
    print(f"young = {model[young]}")
    found_options.append("B")
solver.pop()

# Option C: Vaughn is assigned parking space #5
solver.push()
solver.add(vaughn == 5)
if solver.check() == sat:
    model = solver.model()
    print("Option C model:")
    print(f"robertson = {model[robertson]}")
    print(f"souza = {model[souza]}")
    print(f"togowa = {model[togowa]}")
    print(f"vaughn = {model[vaughn]}")
    print(f"xu = {model[xu]}")
    print(f"young = {model[young]}")
    found_options.append("C")
solver.pop()

# Option D: Xu is assigned parking space #6
solver.push()
solver.add(xu == 6)
if solver.check() == sat:
    model = solver.model()
    print("Option D model:")
    print(f"robertson = {model[robertson]}")
    print(f"souza = {model[souza]}")
    print(f"togowa = {model[togowa]}")
    print(f"vaughn = {model[vaughn]}")
    print(f"xu = {model[xu]}")
    print(f"young = {model[young]}")
    found_options.append("D")
solver.pop()

# Option E: Young is assigned parking space #2
solver.push()
solver.add(young == 2)
if solver.check() == sat:
    model = solver.model()
    print("Option E model:")
    print(f"robertson = {model[robertson]}")
    print(f"souza = {model[souza]}")
    print(f"togowa = {model[togowa]}")
    print(f"vaughn = {model[vaughn]}")
    print(f"xu = {model[xu]}")
    print(f"young = {model[young]}")
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