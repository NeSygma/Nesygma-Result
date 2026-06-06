from z3 import *

# Base constraints solver
solver = Solver()

# Declare symbolic variables for each employee's parking space
robertson = Int('robertson')
souza = Int('souza')
togowa = Int('togowa')
vaughn = Int('vaughn')
xu = Int('xu')
young = Int('young')

# Each employee gets a unique space from 1 to 6
spaces = [robertson, souza, togowa, vaughn, xu, young]
solver.add(Distinct(spaces))
solver.add([space >= 1 for space in spaces])
solver.add([space <= 6 for space in spaces])

# Constraints
solver.add(young > togowa)  # Young must be assigned a higher-numbered space than Togowa
solver.add(xu > souza)      # Xu must be assigned a higher-numbered space than Souza
solver.add(robertson > young)  # Robertson must be assigned a higher-numbered space than Young
solver.add(Or(robertson == 1, robertson == 2, robertson == 3, robertson == 4))  # Robertson must be in #1, #2, #3, or #4

# Multiple-choice options
found_options = []

# Option A: #1: Young; #2: Souza; #3: Vaughn; #4: Robertson; #5: Togowa; #6: Xu
solver.push()
solver.add(young == 1)
solver.add(souza == 2)
solver.add(vaughn == 3)
solver.add(robertson == 4)
solver.add(togowa == 5)
solver.add(xu == 6)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: #1: Vaughn; #2: Togowa; #3: Young; #4: Souza; #5: Robertson; #6: Xu
solver.push()
solver.add(vaughn == 1)
solver.add(togowa == 2)
solver.add(young == 3)
solver.add(souza == 4)
solver.add(robertson == 5)
solver.add(xu == 6)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: #1: Togowa; #2: Young; #3: Xu; #4: Robertson; #5: Souza; #6: Vaughn
solver.push()
solver.add(togowa == 1)
solver.add(young == 2)
solver.add(xu == 3)
solver.add(robertson == 4)
solver.add(souza == 5)
solver.add(vaughn == 6)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: #1: Togowa; #2: Robertson; #3: Young; #4: Souza; #5: Vaughn; #6: Xu
solver.push()
solver.add(togowa == 1)
solver.add(robertson == 2)
solver.add(young == 3)
solver.add(souza == 4)
solver.add(vaughn == 5)
solver.add(xu == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: #1: Souza; #2: Togowa; #3: Young; #4: Robertson; #5: Xu; #6: Vaughn
solver.push()
solver.add(souza == 1)
solver.add(togowa == 2)
solver.add(young == 3)
solver.add(robertson == 4)
solver.add(xu == 5)
solver.add(vaughn == 6)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")