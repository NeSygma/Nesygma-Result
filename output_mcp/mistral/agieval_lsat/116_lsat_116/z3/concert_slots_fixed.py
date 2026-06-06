from z3 import *

# Create solver
solver = Solver()

# Slot variables: slot[i] is the band in slot i (0-indexed: slot 1 is index 0, slot 6 is index 5)
# Bands: Uneasy=0, Vegemite=1, Wellspring=2, Xpert=3, Yardsign=4, Zircon=5
slot = [Int(f'slot_{i}') for i in range(6)]

# Each slot has a unique band
solver.add(Distinct(slot))

# Vegemite performs in an earlier slot than Zircon
# This means the index of Vegemite (1) is less than the index of Zircon (5)
# To encode this, we add a constraint that for all i, j: if slot[i] == 1 and slot[j] == 5, then i < j
# We can do this by ensuring that the minimum index where slot[i] == 1 is less than the minimum index where slot[j] == 5
# But since we don't know the indices, we can instead add a constraint that the slot index for 1 is less than the slot index for 5
# We can do this by adding a constraint that for all i, j: slot[i] == 1 => slot[j] != 5 for all j <= i
# But this is complex, so we instead use the following trick:
# We add a constraint that the slot index for 1 is less than the slot index for 5 by using the fact that the slot array is a permutation
# We can do this by adding a constraint that the slot index for 1 is less than the slot index for 5
# We can do this by adding a constraint that the slot index for 1 is less than the slot index for 5
# We can do this by adding a constraint that the slot index for 1 is less than the slot index for 5

# Instead, we can use the following approach:
# For each pair of bands, we can add a constraint that the slot index for band a is less than the slot index for band b
# We can do this by using the fact that the slot array is a permutation and adding a constraint that the slot index for band a is less than the slot index for band b

# To encode "Vegemite (1) is earlier than Zircon (5)", we add:
solver.add(And([
    Implies(slot[i] == 1, And([slot[j] != 5 for j in range(i+1, 6)])) for i in range(6)
]))

# To encode "Wellspring (2) and Zircon (5) are earlier than Xpert (3)", we add:
solver.add(And([
    Implies(slot[i] == 2, And([slot[j] != 3 for j in range(i+1, 6)])) for i in range(6)
]))
solver.add(And([
    Implies(slot[i] == 5, And([slot[j] != 3 for j in range(i+1, 6)])) for i in range(6)
]))

# Uneasy (0) performs in one of the last three slots (indices 3,4,5)
solver.add(Or([slot[i] == 0 for i in range(3, 6)]))

# Yardsign (4) performs in one of the first three slots (indices 0,1,2)
solver.add(Or([slot[i] == 4 for i in range(0, 3)]))

# Now test each option for slot five (index 4)
found_options = []

# Option A: Uneasy in slot five (index 4)
solver.push()
solver.add(slot[4] == 0)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Vegemite in slot five (index 4)
solver.push()
solver.add(slot[4] == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Wellspring in slot five (index 4)
solver.push()
solver.add(slot[4] == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Xpert in slot five (index 4)
solver.push()
solver.add(slot[4] == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Zircon in slot five (index 4)
solver.push()
solver.add(slot[4] == 5)
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