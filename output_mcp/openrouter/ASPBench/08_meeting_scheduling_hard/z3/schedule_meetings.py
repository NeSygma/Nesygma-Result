from z3 import *

# Benchmark mode flag
BENCHMARK_MODE = True

# Data definitions
rooms = ['r1', 'r2', 'r3', 'r4']
room_idx = {r:i for i,r in enumerate(rooms)}

# Meeting list
meetings = [f'm{i}' for i in range(1,21)]
meeting_idx = {m:i for i,m in enumerate(meetings)}

# Equipment requirements per meeting
req = {
    'm1': ['projector'], 'm11': ['projector'],
    'm2': ['whiteboard'], 'm12': ['whiteboard'],
    'm3': ['confcall'], 'm13': ['confcall'],
    'm4': ['video','projector'], 'm14': ['video','projector'],
    'm5': ['projector','confcall'], 'm15': ['projector','confcall'],
    'm6': ['whiteboard','confcall'], 'm16': ['whiteboard','confcall'],
    'm7': ['projector','whiteboard','confcall'], 'm17': ['projector','whiteboard','confcall'],
    'm8': ['video','confcall'], 'm18': ['video','confcall'],
    'm9': ['projector','video'], 'm19': ['projector','video'],
    'm10': ['projector','whiteboard'], 'm20': ['projector','whiteboard'],
}

# Room equipment sets
room_eq = {
    'r1': {'projector','whiteboard','video','confcall'},
    'r2': {'projector','whiteboard','confcall'},
    'r3': {'whiteboard','confcall'},
    'r4': {'projector','video'},
}

# Precompute allowed rooms per meeting based on equipment
allowed_rooms = {}
for m in meetings:
    needed = set(req[m])
    allowed = [room_idx[r] for r in rooms if needed.issubset(room_eq[r])]
    allowed_rooms[m] = allowed

# Attendees per meeting
attendees = {
    'm1': ['p1','p3','p6','p8'],
    'm2': ['p2','p4','p7','p9'],
    'm3': ['p3','p5','p8','p10'],
    'm4': ['p4','p6','p9','p11'],
    'm5': ['p5','p7','p10','p12'],
    'm6': ['p6','p8','p11','p13'],
    'm7': ['p7','p9','p12','p14'],
    'm8': ['p8','p10','p13','p15'],
    'm9': ['p9','p11','p14','p16'],
    'm10': ['p10','p12','p15','p17'],
    'm11': ['p11','p13','p16','p18'],
    'm12': ['p12','p14','p17','p19'],
    'm13': ['p13','p15','p18','p20'],
    'm14': ['p14','p16','p19','p1'],
    'm15': ['p15','p17','p20','p2'],
    'm16': ['p16','p18','p1','p3'],
    'm17': ['p17','p19','p2','p4'],
    'm18': ['p18','p20','p3','p5'],
    'm19': ['p19','p1','p4','p6'],
    'm20': ['p20','p2','p5','p7'],
}

people = [f'p{i}' for i in range(1,21)]

# Decision variables
day = [Int(f'day_{i}') for i in range(20)]
slot = [Int(f'slot_{i}') for i in range(20)]
room = [Int(f'room_{i}') for i in range(20)]

solver = Solver()

# Domain constraints
for i in range(20):
    solver.add(day[i] >= 1, day[i] <= 5)
    solver.add(slot[i] >= 1, slot[i] <= 4)
    solver.add(Or([room[i] == r for r in range(4)]))
    # Equipment constraint: room must be in allowed list
    allowed = allowed_rooms[meetings[i]]
    solver.add(Or([room[i] == r for r in allowed]))

# Person availability constraints
# Build map person -> list of meeting indices they attend
person_meetings = {p: [] for p in people}
for m, att in attendees.items():
    idx = meeting_idx[m]
    for p in att:
        person_meetings[p].append(idx)

for p, mids in person_meetings.items():
    # for each pair of meetings for this person
    for i in range(len(mids)):
        for j in range(i+1, len(mids)):
            mi = mids[i]
            mj = mids[j]
            solver.add(Not(And(day[mi] == day[mj], slot[mi] == slot[mj])))

# Room occupancy constraints
for i in range(20):
    for j in range(i+1, 20):
        solver.add(Not(And(room[i] == room[j], day[i] == day[j], slot[i] == slot[j])))

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print('STATUS: sat')
    for i, meet in enumerate(meetings):
        d = m.eval(day[i]).as_long()
        s = m.eval(slot[i]).as_long()
        r_idx = m.eval(room[i]).as_long()
        r_name = rooms[r_idx]
        print(f'{meet}: day={d}, slot={s}, room={r_name}')
elif result == unsat:
    print('STATUS: unsat')
    if BENCHMARK_MODE:
        print('RAW_RESULT: unsat (modeling error in benchmark mode)')
else:
    print('STATUS: unknown')