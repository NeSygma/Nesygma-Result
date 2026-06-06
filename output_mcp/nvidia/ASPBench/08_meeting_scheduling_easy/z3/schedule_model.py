from z3 import *

# Data
meetings = ['m1','m2','m3','m4','m5']
persons = ['p1','p2','p3','p4','p5']
required = {
    'm1': ['p1','p2','p3'],
    'm2': ['p1','p5'],
    'm3': ['p2','p3'],
    'm4': ['p1','p4'],
    'm5': ['p1','p2','p3']
}
pref = {
    'm1': (1,1),
    'm2': (1,2),
    'm4': (3,3)
}
# person_idx = {p:i for i,p in enumerate(persons)}  # not needed

# Optimizer
opt = Optimize()

# Variables
day = {}
slot = {}
room = {}
for m in meetings:
    day[m] = Int(f'day_{m}')
    slot[m] = Int(f'slot_{m}')
    room[m] = Int(f'room_{m}')
    # domain constraints
    opt.add(day[m] >= 1, day[m] <= 3)
    opt.add(slot[m] >= 1, slot[m] <= 3)
    opt.add(room[m] >= 0, room[m] <= 1)  # 0=r1, 1=r2

# Person availability: each person can attend at most one meeting per (day,slot)
for p in persons:
    for d in range(1,4):
        for s in range(1,4):
            relevant = []
            for m in meetings:
                if p in required[m]:
                    relevant.append(If(And(day[m]==d, slot[m]==s), 1, 0))
            opt.add(Sum(relevant) <= 1)

# Room capacity: at most one meeting per room per (day,slot)
for r in [0,1]:
    for d in range(1,4):
        for s in range(1,4):
            relevant = []
            for m in meetings:
                relevant.append(If(And(day[m]==d, slot[m]==s, room[m]==r), 1, 0))
            opt.add(Sum(relevant) <= 1)

# Preference violation variables
violation_int = {}
for m in meetings:
    vi = Int(f'viol_{m}')
    violation_int[m] = vi
    pref_data = pref.get(m)
    if pref_data is not None:
        pref_day, pref_slot = pref_data
        cond = Or(day[m] != pref_day, slot[m] != pref_slot)
        opt.add(violation_int[m] == If(cond, 1, 0))
    else:
        opt.add(violation_int[m] == 0)

# Objective: minimize total violations
total_violations = Sum([violation_int[m] for m in meetings])
opt.minimize(total_violations)

# Solve
result = opt.check()
if result == sat:
    print("STATUS: sat")
    m = opt.model()
    # Build schedule list
    schedule = []
    for mi in meetings:
        d = m[day[mi]]
        s = m[slot[mi]]
        r = m[room[mi]]
        room_name = "r1" if r == 0 else "r2"
        schedule.append(f"{mi}: day={d} slot={s} room={room_name}")
    print("schedule:", schedule)
    # Preference violations count
    viol_count = sum(m[violation_int[mi]] for mi in meetings)
    print("preference_violations:", viol_count)
    # Conflicts (should be empty)
    print("conflicts: []")
    # Feasible flag
    print("feasible: True")
else:
    print("STATUS: unsat")