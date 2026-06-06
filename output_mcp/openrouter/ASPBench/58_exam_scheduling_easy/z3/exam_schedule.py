from z3 import *

# Exams
exams = ['E1','E2','E3','E4','E5','E6']
# Variables for each exam
slot = {e: Int(f'slot_{e}') for e in exams}
room = {e: Int(f'room_{e}') for e in exams}

solver = Solver()
# Domain constraints
for e in exams:
    solver.add(slot[e] >= 0, slot[e] < 3)   # 3 time slots: 0,1,2
    solver.add(room[e] >= 0, room[e] < 2)   # 2 rooms: 0 (R1), 1 (R2)

# Student enrollments
enrollments = {
    'S1': ['E1','E3','E5'],
    'S2': ['E1','E4','E6'],
    'S3': ['E2','E3','E6'],
    'S4': ['E2','E4','E5']
}
# No student conflicts: exams of same student must be in different slots
for s, exams_list in enrollments.items():
    for i in range(len(exams_list)):
        for j in range(i+1, len(exams_list)):
            e1 = exams_list[i]
            e2 = exams_list[j]
            solver.add(slot[e1] != slot[e2])

# Room capacities (both 3)
capacity = [3,3]
# Student count per exam (all have 2 students)
student_count = {
    'E1':2,'E2':2,'E3':2,'E4':2,'E5':2,'E6':2
}
for e in exams:
    # If room == r then student_count[e] <= capacity[r]
    # Since capacities are equal, this is always true, but we encode it.
    constraints = []
    for r in range(2):
        constraints.append(Implies(room[e] == r, student_count[e] <= capacity[r]))
    solver.add(And(constraints))

# Check satisfiability
result = solver.check()
if result == sat:
    m = solver.model()
    # Build schedule output
    room_names = ['R1','R2']
    print('STATUS: sat')
    print('schedule:')
    for e in exams:
        slot_val = m[slot[e]].as_long()
        room_idx = m[room[e]].as_long()
        print(f'  {e}: slot {slot_val}, room {room_names[room_idx]}')
    # conflicts resolved is true if model satisfies constraints (it does)
    print('conflicts_resolved: True')
    # room utilization: count exams per room
    util = {name:0 for name in room_names}
    for e in exams:
        room_idx = m[room[e]].as_long()
        util[room_names[room_idx]] += 1
    print('room_utilization:', util)
else:
    print('STATUS: unsat')