from z3 import *

# Base constraints solver
solver = Solver()

# Six slots and six bands
slots = range(1, 7)
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]

# Assign each band to a unique slot
assign = {band: Int(f"{band}") for band in bands}
for band in bands:
    solver.add(And(assign[band] >= 1, assign[band] <= 6))
solver.add(Distinct(list(assign.values())))

# Original constraints (excluding Wellspring < Xpert and Zircon < Xpert)
solver.add(assign["Vegemite"] < assign["Zircon"])  # Vegemite earlier than Zircon
solver.add(Or(assign["Uneasy"] == 4, assign["Uneasy"] == 5, assign["Uneasy"] == 6))  # Uneasy in last three slots
solver.add(Or(assign["Yardsign"] == 1, assign["Yardsign"] == 2, assign["Yardsign"] == 3))  # Yardsign in first three slots

# Store the original solver's possible assignments
original_solutions = []
while solver.check() == sat:
    m = solver.model()
    original_solutions.append({band: m.eval(assign[band]) for band in bands})
    solver.add(Or([assign[band] != m.eval(assign[band]) for band in bands]))

# Reset solver for substitution checks
solver = Solver()
for band in bands:
    solver.add(And(assign[band] >= 1, assign[band] <= 6))
solver.add(Distinct(list(assign.values())))
solver.add(assign["Vegemite"] < assign["Zircon"])  # Vegemite earlier than Zircon
solver.add(Or(assign["Uneasy"] == 4, assign["Uneasy"] == 5, assign["Uneasy"] == 6))  # Uneasy in last three slots
solver.add(Or(assign["Yardsign"] == 1, assign["Yardsign"] == 2, assign["Yardsign"] == 3))  # Yardsign in first three slots

# Now test each substitution option for equivalence
found_options = []

# Option A: Only Uneasy can perform in a later slot than Xpert.
# This means Xpert must be in slot 3 or earlier, and Uneasy must be after Xpert.
solver.push()
solver.add(assign["Xpert"] <= 3)
solver.add(assign["Uneasy"] > assign["Xpert"])
sub_solutions = []
while solver.check() == sat:
    m = solver.model()
    sub_solutions.append({band: m.eval(assign[band]) for band in bands})
    solver.add(Or([assign[band] != m.eval(assign[band]) for band in bands]))
solver.pop()

# Check if sub_solutions is equivalent to original_solutions
if sub_solutions == original_solutions:
    found_options.append("A")

# Option B: Vegemite performs in an earlier slot than Wellspring, which performs in an earlier slot than Zircon.
solver.push()
solver.add(assign["Vegemite"] < assign["Wellspring"])
solver.add(assign["Wellspring"] < assign["Zircon"])
sub_solutions = []
while solver.check() == sat:
    m = solver.model()
    sub_solutions.append({band: m.eval(assign[band]) for band in bands})
    solver.add(Or([assign[band] != m.eval(assign[band]) for band in bands]))
solver.pop()

if sub_solutions == original_solutions:
    found_options.append("B")

# Option C: Vegemite and Wellspring each perform in an earlier slot than Xpert.
solver.push()
solver.add(assign["Vegemite"] < assign["Xpert"])
solver.add(assign["Wellspring"] < assign["Xpert"])
sub_solutions = []
while solver.check() == sat:
    m = solver.model()
    sub_solutions.append({band: m.eval(assign[band]) for band in bands})
    solver.add(Or([assign[band] != m.eval(assign[band]) for band in bands]))
solver.pop()

if sub_solutions == original_solutions:
    found_options.append("C")

# Option D: Xpert performs either immediately before or immediately after Uneasy.
solver.push()
solver.add(Or(assign["Uneasy"] == assign["Xpert"] + 1, assign["Uneasy"] == assign["Xpert"] - 1))
sub_solutions = []
while solver.check() == sat:
    m = solver.model()
    sub_solutions.append({band: m.eval(assign[band]) for band in bands})
    solver.add(Or([assign[band] != m.eval(assign[band]) for band in bands]))
solver.pop()

if sub_solutions == original_solutions:
    found_options.append("D")

# Option E: Xpert performs in either slot five or slot six.
solver.push()
solver.add(Or(assign["Xpert"] == 5, assign["Xpert"] == 6))
sub_solutions = []
while solver.check() == sat:
    m = solver.model()
    sub_solutions.append({band: m.eval(assign[band]) for band in bands})
    solver.add(Or([assign[band] != m.eval(assign[band]) for band in bands]))
solver.pop()

if sub_solutions == original_solutions:
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