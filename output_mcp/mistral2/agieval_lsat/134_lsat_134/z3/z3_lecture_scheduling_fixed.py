from z3 import *

solver = Solver()

# Lectures
lectures = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]

# Position variables: pos[lecture] = position (1 to 5)
pos = {lecture: Int(f"pos_{lecture}") for lecture in lectures}

# Location variables: loc[lecture] = 0 (Gladwyn) or 1 (Howard)
loc = {lecture: Int(f"loc_{lecture}") for lecture in lectures}

# Base constraints
# Each lecture has a unique position
solver.add(Distinct(list(pos.values())))

# Position bounds
for lecture in lectures:
    solver.add(pos[lecture] >= 1, pos[lecture] <= 5)

# First lecture is in Gladwyn Hall
solver.add(pos["oystercatchers"] == 1)  # First lecture is oystercatchers
solver.add(loc["oystercatchers"] == 0)  # Gladwyn

# Fourth lecture is in Howard Auditorium
solver.add(Or([pos[lecture] == 4 and loc[lecture] == 1 for lecture in lectures]))

# Exactly three lectures are in Gladwyn Hall
solver.add(Sum([If(loc[lecture] == 0, 1, 0) for lecture in lectures]) == 3)

# The lecture on sandpipers is in Howard Auditorium and is given earlier than the lecture on oystercatchers
solver.add(loc["sandpipers"] == 1)
solver.add(pos["sandpipers"] < pos["oystercatchers"])

# The lecture on terns is given earlier than the lecture on petrels, which is in Gladwyn Hall
solver.add(pos["terns"] < pos["petrels"])
solver.add(loc["petrels"] == 0)

# Now test each option
found_options = []

# Option A: oystercatchers, petrels, rails, sandpipers, terns
solver.push()
solver.add(pos["oystercatchers"] == 1)
solver.add(pos["petrels"] == 2)
solver.add(pos["rails"] == 3)
solver.add(pos["sandpipers"] == 4)
solver.add(pos["terns"] == 5)
# Locations inferred from constraints:
# oystercatchers: Gladwyn (0)
# petrels: Gladwyn (0)
# rails: Gladwyn (0) (to satisfy exactly three in Gladwyn)
# sandpipers: Howard (1)
# terns: Howard (1)
solver.add(loc["oystercatchers"] == 0)
solver.add(loc["petrels"] == 0)
solver.add(loc["rails"] == 0)
solver.add(loc["sandpipers"] == 1)
solver.add(loc["terns"] == 1)

if solver.check() == sat:
    found_options.append("A")
else:
    solver.pop()

# Option B: petrels, sandpipers, oystercatchers, terns, rails
solver.push()
solver.add(pos["petrels"] == 1)
solver.add(pos["sandpipers"] == 2)
solver.add(pos["oystercatchers"] == 3)
solver.add(pos["terns"] == 4)
solver.add(pos["rails"] == 5)
# Constraints:
# First lecture must be oystercatchers, but here it is petrels. Invalid.
solver.add(loc["petrels"] == 0)
solver.add(loc["sandpipers"] == 1)

if solver.check() == sat:
    found_options.append("B")
else:
    solver.pop()

# Option C: rails, sandpipers, terns, petrels, oystercatchers
solver.push()
solver.add(pos["rails"] == 1)
solver.add(pos["sandpipers"] == 2)
solver.add(pos["terns"] == 3)
solver.add(pos["petrels"] == 4)
solver.add(pos["oystercatchers"] == 5)
# Constraints:
# First lecture must be oystercatchers, but here it is rails. Invalid.
solver.add(loc["rails"] == 0)
solver.add(loc["sandpipers"] == 1)
solver.add(loc["terns"] == 1)
solver.add(loc["petrels"] == 0)
solver.add(loc["oystercatchers"] == 0)

if solver.check() == sat:
    found_options.append("C")
else:
    solver.pop()

# Option D: sandpipers, terns, oystercatchers, rails, petrels
solver.push()
solver.add(pos["sandpipers"] == 1)
solver.add(pos["terns"] == 2)
solver.add(pos["oystercatchers"] == 3)
solver.add(pos["rails"] == 4)
solver.add(pos["petrels"] == 5)
# Constraints:
# First lecture must be oystercatchers, but here it is sandpipers. Invalid.
solver.add(loc["sandpipers"] == 1)
solver.add(loc["terns"] == 0)
solver.add(loc["oystercatchers"] == 0)
solver.add(loc["rails"] == 0)
solver.add(loc["petrels"] == 0)

if solver.check() == sat:
    found_options.append("D")
else:
    solver.pop()

# Option E: terns, petrels, sandpipers, oystercatchers, rails
solver.push()
solver.add(pos["terns"] == 1)
solver.add(pos["petrels"] == 2)
solver.add(pos["sandpipers"] == 3)
solver.add(pos["oystercatchers"] == 4)
solver.add(pos["rails"] == 5)
# Constraints:
# First lecture must be oystercatchers, but here it is terns. Invalid.
solver.add(loc["terns"] == 0)
solver.add(loc["petrels"] == 0)
solver.add(loc["sandpipers"] == 1)
solver.add(loc["oystercatchers"] == 0)
solver.add(loc["rails"] == 0)

if solver.check() == sat:
    found_options.append("E")
else:
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