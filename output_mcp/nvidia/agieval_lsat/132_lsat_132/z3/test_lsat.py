from z3 import *

# Define movies indices: 0=H, 1=M, 2=R, 3=S, 4=W
# Define slots: s1_7, s1_9, s2_7, s2_9, s3_8
s1_7 = Int('s1_7')
s1_9 = Int('s1_9')
s2_7 = Int('s2_7')
s2_9 = Int('s2_9')
s3_8 = Int('s3_8')

# All movies must be assigned to distinct slots
solver = Solver()
solver.add(Distinct([s1_7, s1_9, s2_7, s2_9, s3_8]))
# Domain constraints: each slot must be in 0..4
solver.add(Or([s1_7 == i for i in range(5)]))
solver.add(Or([s1_9 == i for i in range(5)]))
solver.add(Or([s2_7 == i for i in range(5)]))
solver.add(Or([s2_9 == i for i in range(5)]))
solver.add(Or([s3_8 == i for i in range(5)]))

# Helper: map index to movie name for readability (not needed for solver)
# Constraints:
# 1. Western (W) begins before Horror (H)
# We need to compare times: times are encoded by slot type: 7,8,9.
# We can define a function to get time value: 7->0, 8->1, 9->2 maybe.
# But we can directly enforce: if a slot is s1_7 or s2_7 => time=7; if s3_8 => time=8; if s1_9 or s2_9 => time=9.
# So we can enforce: if a variable equals 4 (W), then its time must be earlier than H's time.
# We'll implement using boolean conditions.

# Define boolean for each slot being time 7,8,9
def time_var(slot):
    # returns a Bool indicating if slot is a 7-time slot
    pass