from z3 import *

# Base constraints solver for original problem (excluding Wellspring < Xpert and Zircon < Xpert)
solver_orig = Solver()

# Six slots and six bands
slots = range(1, 7)
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]

# Assign each band to a unique slot
assign_orig = {band: Int(f"{band}_orig") for band in bands}
for band in bands:
    solver_orig.add(And(assign_orig[band] >= 1, assign_orig[band] <= 6))
solver_orig.add(Distinct(list(assign_orig.values())))

# Original constraints (excluding Wellspring < Xpert and Zircon < Xpert)
solver_orig.add(assign_orig["Vegemite"] < assign_orig["Zircon"])  # Vegemite earlier than Zircon
solver_orig.add(Or(assign_orig["Uneasy"] == 4, assign_orig["Uneasy"] == 5, assign_orig["Uneasy"] == 6))  # Uneasy in last three slots
solver_orig.add(Or(assign_orig["Yardsign"] == 1, assign_orig["Yardsign"] == 2, assign_orig["Yardsign"] == 3))  # Yardsign in first three slots

# Collect possible positions for each band under original constraints
orig_positions = {band: set() for band in bands}
while solver_orig.check() == sat:
    m = solver_orig.model()
    for band in bands:
        orig_positions[band].add(m.eval(assign_orig[band]))
    solver_orig.add(Or([assign_orig[band] != m.eval(assign_orig[band]) for band in bands]))

# Now test each substitution option for equivalence
found_options = []

# Option A: Only Uneasy can perform in a later slot than Xpert.
# This means Xpert must be in slot 3 or earlier, and Uneasy must be after Xpert.
solver_A = Solver()
assign_A = {band: Int(f"{band}_A") for band in bands}
for band in bands:
    solver_A.add(And(assign_A[band] >= 1, assign_A[band] <= 6))
solver_A.add(Distinct(list(assign_A.values())))
solver_A.add(assign_A["Vegemite"] < assign_A["Zircon"])  # Vegemite earlier than Zircon
solver_A.add(Or(assign_A["Uneasy"] == 4, assign_A["Uneasy"] == 5, assign_A["Uneasy"] == 6))  # Uneasy in last three slots
solver_A.add(Or(assign_A["Yardsign"] == 1, assign_A["Yardsign"] == 2, assign_A["Yardsign"] == 3))  # Yardsign in first three slots
solver_A.add(assign_A["Xpert"] <= 3)
solver_A.add(assign_A["Uneasy"] > assign_A["Xpert"])

positions_A = {band: set() for band in bands}
while solver_A.check() == sat:
    m = solver_A.model()
    for band in bands:
        positions_A[band].add(m.eval(assign_A[band]))
    solver_A.add(Or([assign_A[band] != m.eval(assign_A[band]) for band in bands]))

if all(positions_A[band] == orig_positions[band] for band in bands):
    found_options.append("A")

# Option B: Vegemite performs in an earlier slot than Wellspring, which performs in an earlier slot than Zircon.
solver_B = Solver()
assign_B = {band: Int(f"{band}_B") for band in bands}
for band in bands:
    solver_B.add(And(assign_B[band] >= 1, assign_B[band] <= 6))
solver_B.add(Distinct(list(assign_B.values())))
solver_B.add(assign_B["Vegemite"] < assign_B["Zircon"])  # Vegemite earlier than Zircon
solver_B.add(Or(assign_B["Uneasy"] == 4, assign_B["Uneasy"] == 5, assign_B["Uneasy"] == 6))  # Uneasy in last three slots
solver_B.add(Or(assign_B["Yardsign"] == 1, assign_B["Yardsign"] == 2, assign_B["Yardsign"] == 3))  # Yardsign in first three slots
solver_B.add(assign_B["Vegemite"] < assign_B["Wellspring"])
solver_B.add(assign_B["Wellspring"] < assign_B["Zircon"])

positions_B = {band: set() for band in bands}
while solver_B.check() == sat:
    m = solver_B.model()
    for band in bands:
        positions_B[band].add(m.eval(assign_B[band]))
    solver_B.add(Or([assign_B[band] != m.eval(assign_B[band]) for band in bands]))

if all(positions_B[band] == orig_positions[band] for band in bands):
    found_options.append("B")

# Option C: Vegemite and Wellspring each perform in an earlier slot than Xpert.
solver_C = Solver()
assign_C = {band: Int(f"{band}_C") for band in bands}
for band in bands:
    solver_C.add(And(assign_C[band] >= 1, assign_C[band] <= 6))
solver_C.add(Distinct(list(assign_C.values())))
solver_C.add(assign_C["Vegemite"] < assign_C["Zircon"])  # Vegemite earlier than Zircon
solver_C.add(Or(assign_C["Uneasy"] == 4, assign_C["Uneasy"] == 5, assign_C["Uneasy"] == 6))  # Uneasy in last three slots
solver_C.add(Or(assign_C["Yardsign"] == 1, assign_C["Yardsign"] == 2, assign_C["Yardsign"] == 3))  # Yardsign in first three slots
solver_C.add(assign_C["Vegemite"] < assign_C["Xpert"])
solver_C.add(assign_C["Wellspring"] < assign_C["Xpert"])

positions_C = {band: set() for band in bands}
while solver_C.check() == sat:
    m = solver_C.model()
    for band in bands:
        positions_C[band].add(m.eval(assign_C[band]))
    solver_C.add(Or([assign_C[band] != m.eval(assign_C[band]) for band in bands]))

if all(positions_C[band] == orig_positions[band] for band in bands):
    found_options.append("C")

# Option D: Xpert performs either immediately before or immediately after Uneasy.
solver_D = Solver()
assign_D = {band: Int(f"{band}_D") for band in bands}
for band in bands:
    solver_D.add(And(assign_D[band] >= 1, assign_D[band] <= 6))
solver_D.add(Distinct(list(assign_D.values())))
solver_D.add(assign_D["Vegemite"] < assign_D["Zircon"])  # Vegemite earlier than Zircon
solver_D.add(Or(assign_D["Uneasy"] == 4, assign_D["Uneasy"] == 5, assign_D["Uneasy"] == 6))  # Uneasy in last three slots
solver_D.add(Or(assign_D["Yardsign"] == 1, assign_D["Yardsign"] == 2, assign_D["Yardsign"] == 3))  # Yardsign in first three slots
solver_D.add(Or(assign_D["Uneasy"] == assign_D["Xpert"] + 1, assign_D["Uneasy"] == assign_D["Xpert"] - 1))

positions_D = {band: set() for band in bands}
while solver_D.check() == sat:
    m = solver_D.model()
    for band in bands:
        positions_D[band].add(m.eval(assign_D[band]))
    solver_D.add(Or([assign_D[band] != m.eval(assign_D[band]) for band in bands]))

if all(positions_D[band] == orig_positions[band] for band in bands):
    found_options.append("D")

# Option E: Xpert performs in either slot five or slot six.
solver_E = Solver()
assign_E = {band: Int(f"{band}_E") for band in bands}
for band in bands:
    solver_E.add(And(assign_E[band] >= 1, assign_E[band] <= 6))
solver_E.add(Distinct(list(assign_E.values())))
solver_E.add(assign_E["Vegemite"] < assign_E["Zircon"])  # Vegemite earlier than Zircon
solver_E.add(Or(assign_E["Uneasy"] == 4, assign_E["Uneasy"] == 5, assign_E["Uneasy"] == 6))  # Uneasy in last three slots
solver_E.add(Or(assign_E["Yardsign"] == 1, assign_E["Yardsign"] == 2, assign_E["Yardsign"] == 3))  # Yardsign in first three slots
solver_E.add(Or(assign_E["Xpert"] == 5, assign_E["Xpert"] == 6))

positions_E = {band: set() for band in bands}
while solver_E.check() == sat:
    m = solver_E.model()
    for band in bands:
        positions_E[band].add(m.eval(assign_E[band]))
    solver_E.add(Or([assign_E[band] != m.eval(assign_E[band]) for band in bands]))

if all(positions_E[band] == orig_positions[band] for band in bands):
    found_options.append("E")

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")