from z3 import *

# Define band constants
Uneasy = 0
Vegemite = 1
Wellspring = 2
Xpert = 3
Yardsign = 4
Zircon = 5

# Create solver
solver = Solver()

# Assignment variables: assign[i] is the band in slot i (0-indexed: slot 1 is index 0, slot 6 is index 5)
assign = [Int(f'assign_{i}') for i in range(6)]

# Each slot has a unique band
solver.add(Distinct(assign))

# Vegemite performs earlier than Zircon
for i in range(6):
    solver.add(Implies(assign[i] == Vegemite, Sum([If(assign[j] == Zircon, 1, 0) for j in range(i+1, 6)]) >= 1))

# Wellspring and Zircon each perform earlier than Xpert
for i in range(6):
    solver.add(Implies(assign[i] == Wellspring, Sum([If(assign[j] == Xpert, 1, 0) for j in range(i+1, 6)]) >= 1))
    solver.add(Implies(assign[i] == Zircon, Sum([If(assign[j] == Xpert, 1, 0) for j in range(i+1, 6)]) >= 1))

# Uneasy performs in one of the last three slots (slots 4,5,6 -> indices 3,4,5)
solver.add(Or([assign[i] == Uneasy for i in range(3, 6)]))

# Yardsign performs in one of the first three slots (slots 1,2,3 -> indices 0,1,2)
solver.add(Or([assign[i] == Yardsign for i in range(0, 3)]))

# Now test each option for slot five (index 4)
found_options = []

# Option A: Uneasy in slot five (index 4)
solver.push()
solver.add(assign[4] == Uneasy)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Vegemite in slot five (index 4)
solver.push()
solver.add(assign[4] == Vegemite)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Wellspring in slot five (index 4)
solver.push()
solver.add(assign[4] == Wellspring)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Xpert in slot five (index 4)
solver.push()
solver.add(assign[4] == Xpert)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Zircon in slot five (index 4)
solver.push()
solver.add(assign[4] == Zircon)
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