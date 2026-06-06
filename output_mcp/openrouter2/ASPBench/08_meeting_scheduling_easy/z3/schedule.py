from z3 import *

# Problem data
meetings = ['m1','m2','m3','m4','m5']
days = [1,2,3]
slots = [1,2,3]
rooms = ['r1','r2']
# Attendees mapping
attendees = {
    'm1': ['p1','p2','p3'],
    'm2': ['p1','p5'],
    'm3': ['p2','p3'],
    'm4': ['p1','p4'],
    'm5': ['p1','p2','p3']
}
# Preferences: meeting -> (day, slot)
preferences = {
    'm1': (1,1),
    'm2': (1,2),
    'm4': (3,3)
}

# Create solver
opt = Optimize()
# Variables: for each meeting, day, slot, room index
meet_day = {}
meet_slot = {}
meet_room = {}
for m in meetings:
    meet_day[m] = Int(f'day_{m}')
    meet_slot[m] = Int(f'slot_{m}')
    meet_room[m] = Int(f'room_{m}')
    # Domain constraints
    opt.add(meet_day[m] >= 1, meet_day[m] <= 3)
    opt.add(meet_slot[m] >= 1, meet_slot[m] <= 3)
    opt.add(meet_room[m] >= 0, meet_room[m] <= 1)

# Person conflict: no two meetings with same person at same time
for p in ['p1','p2','p3','p4','p5']:
    # find meetings that include this person
    mlist = [m for m in meetings if p in attendees[m]]
    for i in range(len(mlist)):
        for j in range(i+1, len(mlist)):
            mi = mlist[i]
            mj = mlist[j]
            opt.add(Or(meet_day[mi] != meet_day[mj], meet_slot[mi] != meet_slot[mj]))

# Room conflict: only one meeting per room per time slot
for i in range(len(meetings)):
    for j in range(i+1, len(meetings)):
        mi = meetings[i]
        mj = meetings[j]
        opt.add(Or(meet_day[mi] != meet_day[mj],
                   meet_slot[mi] != meet_slot[mj],
                   meet_room[mi] != meet_room[mj]))

# Preference violations
violations = []
for m in meetings:
    if m in preferences:
        pref_day, pref_slot = preferences[m]
        viol = Bool(f'viol_{m}')
        opt.add(viol == Not(And(meet_day[m] == pref_day, meet_slot[m] == pref_slot)))
        violations.append(If(viol, 1, 0))
    else:
        # no preference, no violation
        violations.append(0)

# Objective: minimize total violations
opt.minimize(Sum(violations))

# Solve
result = opt.check()
if result == sat:
    model = opt.model()
    schedule = []
    for m in meetings:
        d = model[meet_day[m]].as_long()
        s = model[meet_slot[m]].as_long()
        r = model[meet_room[m]].as_long()
        schedule.append((m, d, s, rooms[r]))
    # compute preference violations
    pref_viol = 0
    for m in meetings:
        if m in preferences:
            pref_day, pref_slot = preferences[m]
            d = model[meet_day[m]].as_long()
            s = model[meet_slot[m]].as_long()
            if not (d == pref_day and s == pref_slot):
                pref_viol += 1
    print("STATUS: sat")
    print("schedule:", schedule)
    print("conflicts: []")
    print("preference_violations:", pref_viol)
    print("feasible: True")
else:
    print("STATUS: unsat")
    if result == unsat:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")