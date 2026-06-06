from z3 import *

# Instance Data
days = [1, 2, 3]
slots = [1, 2, 3]
rooms = [0, 1]  # 0 = r1 (conference), 1 = r2 (meeting)
meetings = [0, 1, 2, 3, 4]  # m1..m5

# Required attendees per meeting
required = {
    0: [0, 1, 2],  # m1: p1, p2, p3
    1: [0, 4],     # m2: p1, p5
    2: [1, 2],     # m3: p2, p3
    3: [0, 3],     # m4: p1, p4
    4: [0, 1, 2],  # m5: p1, p2, p3
}

# Time preferences: (meeting, day, slot)
preferences = {
    0: (1, 1),  # m1: day 1, slot 1
    1: (1, 2),  # m2: day 1, slot 2
    3: (3, 3),  # m4: day 3, slot 3
}

# Decision variables
# For each meeting: day, slot, room
meeting_day = [Int(f"day_{m}") for m in meetings]
meeting_slot = [Int(f"slot_{m}") for m in meetings]
meeting_room = [Int(f"room_{m}") for m in meetings]

opt = Optimize()

# Domain constraints
for m in meetings:
    opt.add(meeting_day[m] >= 1, meeting_day[m] <= 3)
    opt.add(meeting_slot[m] >= 1, meeting_slot[m] <= 3)
    opt.add(meeting_room[m] >= 0, meeting_room[m] <= 1)

# Constraint 2: No person can attend two meetings at the same time slot
# For each pair of meetings that share a person, they must not be at same (day, slot)
for m1_idx in meetings:
    for m2_idx in meetings:
        if m2_idx > m1_idx:
            # Check if they share any attendee
            if set(required[m1_idx]) & set(required[m2_idx]):
                # They cannot be at same day AND same slot
                opt.add(Not(And(meeting_day[m1_idx] == meeting_day[m2_idx],
                                meeting_slot[m1_idx] == meeting_slot[m2_idx])))

# Constraint 3: Only one meeting per room per time slot
for m1_idx in meetings:
    for m2_idx in meetings:
        if m2_idx > m1_idx:
            # Cannot have same day, same slot, same room
            opt.add(Not(And(meeting_day[m1_idx] == meeting_day[m2_idx],
                            meeting_slot[m1_idx] == meeting_slot[m2_idx],
                            meeting_room[m1_idx] == meeting_room[m2_idx])))

# Objective: Minimize preference violations
pref_violations = Sum([
    If(And(meeting_day[m] == preferences[m][0], meeting_slot[m] == preferences[m][1]), 0, 1)
    for m in preferences
])
opt.minimize(pref_violations)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print(f"preference_violations = {m.eval(pref_violations)}")
    print("Schedule:")
    for mtg in meetings:
        d = m[meeting_day[mtg]]
        s = m[meeting_slot[mtg]]
        r = m[meeting_room[mtg]]
        room_name = "r1" if r == 0 else "r2"
        print(f"  m{mtg+1}: day {d}, slot {s}, room {room_name}")
    print("feasible = True")
else:
    print("STATUS: unsat")
    print("No feasible schedule exists.")