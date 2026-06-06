from z3 import *

# Problem parameters
MEETINGS = 20
DAYS = 5
SLOTS = 4
ROOMS = 4

# Room equipment
room_equipment = {
    1: {'projector', 'whiteboard', 'video', 'confcall'},
    2: {'projector', 'whiteboard', 'confcall'},
    3: {'whiteboard', 'confcall'},
    4: {'projector', 'video'}
}

# Meeting equipment requirements (1-indexed)
meeting_requirements = {
    1: {'projector'},
    2: {'whiteboard'},
    3: {'confcall'},
    4: {'video', 'projector'},
    5: {'projector', 'confcall'},
    6: {'whiteboard', 'confcall'},
    7: {'projector', 'whiteboard', 'confcall'},
    8: {'video', 'confcall'},
    9: {'projector', 'video'},
    10: {'projector', 'whiteboard'},
    11: {'projector'},
    12: {'whiteboard'},
    13: {'confcall'},
    14: {'video', 'projector'},
    15: {'projector', 'confcall'},
    16: {'whiteboard', 'confcall'},
    17: {'projector', 'whiteboard', 'confcall'},
    18: {'video', 'confcall'},
    19: {'projector', 'video'},
    20: {'projector', 'whiteboard'}
}

# Meeting attendees (1-indexed meeting -> list of person IDs)
meeting_attendees = {
    1: [1, 3, 6, 8],
    2: [2, 4, 7, 9],
    3: [3, 5, 8, 10],
    4: [4, 6, 9, 11],
    5: [5, 7, 10, 12],
    6: [6, 8, 11, 13],
    7: [7, 9, 12, 14],
    8: [8, 10, 13, 15],
    9: [9, 11, 14, 16],
    10: [10, 12, 15, 17],
    11: [11, 13, 16, 18],
    12: [12, 14, 17, 19],
    13: [13, 15, 18, 20],
    14: [14, 16, 19, 1],
    15: [15, 17, 20, 2],
    16: [16, 18, 1, 3],
    17: [17, 19, 2, 4],
    18: [18, 20, 3, 5],
    19: [19, 1, 4, 6],
    20: [20, 2, 5, 7]
}

# Create boolean variable a_i_d_s_r
var = {}
for i in range(1, MEETINGS + 1):
    for d in range(1, DAYS + 1):
        for s in range(1, SLOTS + 1):
            for r in range(1, ROOMS + 1):
                var[(i, d, s, r)] = Bool(f"a_{i}_{d}_{s}_{r}")

solver = Solver()

# Constraint 1: Each meeting assigned to exactly one (d,s,r)
for i in range(1, MEETINGS + 1):
    solver.add(Sum([var[(i, d, s, r)] for d in range(1, DAYS + 1)
                                 for s in range(1, SLOTS + 1)
                                 for r in range(1, ROOMS + 1)]) == 1)

# Constraint 2: At most one meeting per (d,s,r)
for d in range(1, DAYS + 1):
    for s in range(1, SLOTS + 1):
        for r in range(1, ROOMS + 1):
            solver.add(Sum([var[(i, d, s, r)] for i in range(1, MEETINGS + 1)]) <= 1)

# Constraint 3: Equipment feasibility
# For each meeting i and room r, check if room r has all required equipment
for i in range(1, MEETINGS + 1):
    req = meeting_requirements[i]
    for r in range(1, ROOMS + 1):
        if not req.issubset(room_equipment[r]):
            # Disallow any assignment of meeting i to room r
            solver.add(Sum([var[(i, d, s, r)] for d in range(1, DAYS + 1)
                                         for s in range(1, SLOTS + 1)]) == 0)

# Constraint 4: Person availability
# For each person p, day d, slot s, at most one meeting they attend
for p in range(1, 21):
    for d in range(1, DAYS + 1):
        for s in range(1, SLOTS + 1):
            # Sum over meetings that include person p, across all rooms
            attending_meetings = [i for i in range(1, MEETINGS + 1) if p in meeting_attendees[i]]
            expr = Sum([Sum([var[(i, d, s, r)] for r in range(1, ROOMS + 1)]) for i in attending_meetings])
            solver.add(expr <= 1)

# Check for a solution
result = solver.check()
if result == sat:
    print("STATUS: sat")
    model = solver.model()
    # Output the schedule
    for i in range(1, MEETINGS + 1):
        for d in range(1, DAYS + 1):
            for s in range(1, SLOTS + 1):
                for r in range(1, ROOMS + 1):
                    if is_true(model[var[(i, d, s, r)]]):
                        print(f"meeting {i} day {d} slot {s} room {r}")
                        # Break out of loops after finding assignment
                        raise SystemExit
elif result == unsat:
    print("STATUS: unsat")
    if True:  # BENCHMARK_MODE is ON
        print("RAW_RESULT: unsat (semantic/modeling error; refine required)")
else:
    print("STATUS: unknown")