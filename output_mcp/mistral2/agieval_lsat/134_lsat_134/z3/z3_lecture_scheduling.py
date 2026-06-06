from z3 import *

solver = Solver()

# Entities and their attributes
lectures = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]
locations = ["Gladwyn", "Howard"]

# Decision variables:
# pos[i] = position (1 to 5) of lecture i
# loc[i] = location of lecture i (0 for Gladwyn, 1 for Howard)
pos = {lecture: Int(f"pos_{lecture}") for lecture in lectures}
loc = {lecture: Int(f"loc_{lecture}") for lecture in lectures}

# Helper: lecture at position p
lecture_at_pos = {p: Const(f"lecture_at_pos_{p}", StringSort()) for p in range(1, 6)}

# Base constraints
# Each lecture has a unique position
solver.add(Distinct(list(pos.values())))

# Each position has a unique lecture
for p in range(1, 6):
    solver.add(Or([lecture_at_pos[p] == lecture for lecture in lectures]))
    solver.add(Distinct([lecture_at_pos[p] for p in range(1, 6)]))

# Position bounds
for lecture in lectures:
    solver.add(pos[lecture] >= 1, pos[lecture] <= 5)

# First lecture is in Gladwyn Hall
solver.add(pos[lectures[0]] == 1)  # Assuming lectures[0] is oystercatchers, but we need to generalize
solver.add(loc[lectures[0]] == 0)  # 0 for Gladwyn

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

# Link position and lecture_at_pos
for lecture in lectures:
    solver.add(lecture_at_pos[pos[lecture]] == lecture)

# Base constraints for multiple choice options
# We will now test each option

found_options = []

# Option A: oystercatchers, petrels, rails, sandpipers, terns
solver.push()
# Assign positions based on option A
solver.add(pos["oystercatchers"] == 1)
solver.add(pos["petrels"] == 2)
solver.add(pos["rails"] == 3)
solver.add(pos["sandpipers"] == 4)
solver.add(pos["terns"] == 5)
# Assign locations based on option A (inferred from constraints)
# petrels is in Gladwyn (from constraints)
# sandpipers is in Howard (from constraints)
# First lecture (oystercatchers) is in Gladwyn (from constraints)
# Fourth lecture (sandpipers) is in Howard (from constraints)
# Exactly three in Gladwyn: oystercatchers, petrels, rails, terns? But terns is last, so likely Gladwyn?
# We need to infer locations for rails and terns to satisfy exactly three in Gladwyn
# For now, assume:
# oystercatchers: Gladwyn (0)
# petrels: Gladwyn (0)
# rails: Gladwyn (0)
# sandpipers: Howard (1)
# terns: Howard (1)
# This would be 3 in Gladwyn (oystercatchers, petrels, rails) and 2 in Howard (sandpipers, terns)
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
# Locations:
# First lecture (petrels) must be in Gladwyn
# sandpipers must be in Howard
# petrels must be in Gladwyn (from constraints)
# terns must be earlier than petrels? No, petrels is first, so this violates the constraint that terns is earlier than petrels.
# This option is invalid due to the terns < petrels constraint.
solver.add(loc["petrels"] == 0)
solver.add(loc["sandpipers"] == 1)
solver.add(loc["oystercatchers"] == 0)  # inferred
solver.add(loc["terns"] == 0)  # inferred
solver.add(loc["rails"] == 0)  # inferred

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
# Locations:
# First lecture (rails) must be in Gladwyn
# sandpipers must be in Howard
# petrels must be in Gladwyn
# terns < petrels: satisfied (3 < 4)
# sandpipers < oystercatchers: satisfied (2 < 5)
# Exactly three in Gladwyn: rails, petrels, oystercatchers? But oystercatchers is last, and sandpipers is Howard, terns is Howard?
# Let's assign:
# rails: Gladwyn (0)
# sandpipers: Howard (1)
# terns: Howard (1)
# petrels: Gladwyn (0)
# oystercatchers: Gladwyn (0)
# This gives 3 in Gladwyn (rails, petrels, oystercatchers) and 2 in Howard (sandpipers, terns)
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
# Locations:
# First lecture (sandpipers) must be in Gladwyn, but sandpipers must be in Howard (from constraints). Contradiction.
# This option is invalid.
solver.add(loc["sandpipers"] == 1)  # sandpipers must be in Howard
solver.add(loc["terns"] == 0)  # inferred
solver.add(loc["oystercatchers"] == 0)  # inferred
solver.add(loc["rails"] == 0)  # inferred
solver.add(loc["petrels"] == 0)  # petrels must be in Gladwyn

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
# Locations:
# First lecture (terns) must be in Gladwyn
# sandpipers must be in Howard
# petrels must be in Gladwyn
# terns < petrels: satisfied (1 < 2)
# sandpipers < oystercatchers: satisfied (3 < 4)
# Exactly three in Gladwyn: terns, petrels, rails? Or rails is last, so likely Gladwyn?
# Assign:
# terns: Gladwyn (0)
# petrels: Gladwyn (0)
# sandpipers: Howard (1)
# oystercatchers: Gladwyn (0)
# rails: Gladwyn (0)
# This gives 4 in Gladwyn (terns, petrels, oystercatchers, rails) and 1 in Howard (sandpipers). Violates exactly three in Gladwyn.
# So this option is invalid.
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