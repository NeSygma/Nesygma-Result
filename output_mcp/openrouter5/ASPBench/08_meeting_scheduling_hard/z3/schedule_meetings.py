from z3 import *

# ============================================================
# Data
# ============================================================
rooms = ["r1", "r2", "r3", "r4"]
days = list(range(1, 6))       # 1..5
slots = list(range(1, 5))      # 1..4
meetings = list(range(1, 21))  # m1..m20
people = list(range(1, 21))    # p1..p20

# Room equipment sets
room_equip = {
    "r1": {"projector", "whiteboard", "video", "confcall"},
    "r2": {"projector", "whiteboard", "confcall"},
    "r3": {"whiteboard", "confcall"},
    "r4": {"projector", "video"},
}

# Meeting equipment requirements (by meeting number)
meeting_req = {
    1:  {"projector"},
    2:  {"whiteboard"},
    3:  {"confcall"},
    4:  {"video", "projector"},
    5:  {"projector", "confcall"},
    6:  {"whiteboard", "confcall"},
    7:  {"projector", "whiteboard", "confcall"},
    8:  {"video", "confcall"},
    9:  {"projector", "video"},
    10: {"projector", "whiteboard"},
    11: {"projector"},
    12: {"whiteboard"},
    13: {"confcall"},
    14: {"video", "projector"},
    15: {"projector", "confcall"},
    16: {"whiteboard", "confcall"},
    17: {"projector", "whiteboard", "confcall"},
    18: {"video", "confcall"},
    19: {"projector", "video"},
    20: {"projector", "whiteboard"},
}

# Meeting attendees (4 per meeting)
attendees = {
    1:  [1, 3, 6, 8],
    2:  [2, 4, 7, 9],
    3:  [3, 5, 8, 10],
    4:  [4, 6, 9, 11],
    5:  [5, 7, 10, 12],
    6:  [6, 8, 11, 13],
    7:  [7, 9, 12, 14],
    8:  [8, 10, 13, 15],
    9:  [9, 11, 14, 16],
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
    20: [20, 2, 5, 7],
}

# ============================================================
# Decision Variables
# ============================================================
# For each meeting m, we assign a day (1..5), slot (1..4), room (0..3 index)
meeting_day = [Int(f"day_{m}") for m in meetings]
meeting_slot = [Int(f"slot_{m}") for m in meetings]
meeting_room = [Int(f"room_{m}") for m in meetings]  # 0=r1, 1=r2, 2=r3, 3=r4

solver = Solver()

# ============================================================
# Domain constraints
# ============================================================
for m in meetings:
    solver.add(1 <= meeting_day[m-1], meeting_day[m-1] <= 5)
    solver.add(1 <= meeting_slot[m-1], meeting_slot[m-1] <= 4)
    solver.add(0 <= meeting_room[m-1], meeting_room[m-1] <= 3)

# ============================================================
# Constraint 1: Each meeting assigned to exactly one (day,slot,room) — implicit from variables
# ============================================================

# ============================================================
# Constraint 2: Person Availability — no person attends two meetings at same (day,slot)
# ============================================================
# For each person, for each pair of meetings they attend, ensure they don't overlap
for p in people:
    # Find all meetings this person attends
    p_meetings = [m for m in meetings if p in attendees[m]]
    # For each pair of meetings this person attends, they must not be at same (day,slot)
    for i in range(len(p_meetings)):
        for j in range(i+1, len(p_meetings)):
            mi = p_meetings[i]
            mj = p_meetings[j]
            solver.add(Not(And(meeting_day[mi-1] == meeting_day[mj-1],
                               meeting_slot[mi-1] == meeting_slot[mj-1])))

# ============================================================
# Constraint 3: Room Occupancy — each room at most one meeting per (day,slot)
# ============================================================
for d in days:
    for s in slots:
        for r_idx in range(4):
            # Count meetings assigned to this (d,s,r)
            count = Sum([If(And(meeting_day[m-1] == d,
                                meeting_slot[m-1] == s,
                                meeting_room[m-1] == r_idx), 1, 0) for m in meetings])
            solver.add(count <= 1)

# ============================================================
# Constraint 4: Equipment Requirements
# ============================================================
# Map room index to room name
room_names = ["r1", "r2", "r3", "r4"]

for m in meetings:
    req = meeting_req[m]
    # The room assigned to meeting m must have all required equipment
    # For each room index, check if it satisfies all requirements
    valid_rooms = []
    for r_idx, rname in enumerate(room_names):
        equip = room_equip[rname]
        if req.issubset(equip):
            valid_rooms.append(r_idx)
    # meeting_room[m-1] must be one of the valid rooms
    solver.add(Or([meeting_room[m-1] == vr for vr in valid_rooms]))

# ============================================================
# Solve
# ============================================================
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("feasible: True")
    print("schedule:")
    for m in meetings:
        d = model[meeting_day[m-1]]
        s = model[meeting_slot[m-1]]
        r_idx = model[meeting_room[m-1]].as_long()
        rname = room_names[r_idx]
        print(f"  m{m}: day={d}, slot={s}, room={rname}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")