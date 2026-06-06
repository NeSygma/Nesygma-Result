from z3 import *

# Define constants
DAYS = [1,2,3]
SLOTS = [1,2,3]
ROOMS = [0,1]  # 0 -> r1, 1 -> r2
room_names = {0: 'r1', 1: 'r2'}

meetings = ['m1','m2','m3','m4','m5']
# Mapping meeting index
mid = {m:i for i,m in enumerate(meetings)}

# Attendees per meeting
attendees = {
    'm1': ['p1','p2','p3'],
    'm2': ['p1','p5'],
    'm3': ['p2','p3'],
    'm4': ['p1','p4'],
    'm5': ['p1','p2','p3']
}

# Preferences (day,slot) for some meetings
prefs = {
    'm1': (1,1),
    'm2': (1,2),
    'm4': (3,3)
}

# Decision variables per meeting
Day = [Int(f'Day_{m}') for m in meetings]
Slot = [Int(f'Slot_{m}') for m in meetings]
Room = [Int(f'Room_{m}') for m in meetings]

opt = Optimize()

# Domain constraints
for i in range(len(meetings)):
    opt.add(Or([Day[i] == d for d in DAYS]))
    opt.add(Or([Slot[i] == s for s in SLOTS]))
    opt.add(Or([Room[i] == r for r in ROOMS]))

# Conflict constraints: same person cannot be in two meetings at same day&slot
# Build list of meetings per person
person_meetings = {}
for m, pers in attendees.items():
    for p in pers:
        person_meetings.setdefault(p, []).append(m)

# For each person, for each pair of distinct meetings, add conflict
for p, mlist in person_meetings.items():
    for i in range(len(mlist)):
        for j in range(i+1, len(mlist)):
            mi = mlist[i]
            mj = mlist[j]
            ii = mid[mi]
            jj = mid[mj]
            # Not both same day and same slot
            opt.add(Or(Day[ii] != Day[jj], Slot[ii] != Slot[jj]))

# Room conflict: at most one meeting per room per day/slot
for i in range(len(meetings)):
    for j in range(i+1, len(meetings)):
        opt.add(Or(Day[i] != Day[j], Slot[i] != Slot[j], Room[i] != Room[j]))

# Preference violation penalty
penalties = []
for m in meetings:
    if m in prefs:
        d_pref, s_pref = prefs[m]
        i = mid[m]
        penalties.append(If(Or(Day[i] != d_pref, Slot[i] != s_pref), 1, 0))
    else:
        penalties.append(IntVal(0))

pref_viol = Sum(penalties)
opt.minimize(pref_viol)

# Solve
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    # Build schedule output
    schedule = []
    for m in meetings:
        i = mid[m]
        d = model[Day[i]].as_long()
        s = model[Slot[i]].as_long()
        r = model[Room[i]].as_long()
        schedule.append((m, d, s, room_names[r]))
    # Print schedule lines
    for entry in schedule:
        print(f"schedule: {entry}")
    # Preference violations
    pv = model.eval(pref_viol, model_completion=True).as_long()
    print(f"preference_violations: {pv}")
    print("feasible: True")
else:
    print("STATUS: unsat")
    print("feasible: False")