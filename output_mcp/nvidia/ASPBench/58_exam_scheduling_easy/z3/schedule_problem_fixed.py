from z3 import *

# Exams
exams = ['E1','E2','E3','E4','E5','E6']

# Variables
day = {e: Int(f'day_{e}') for e in exams}
time = {e: Int(f'time_{e}') for e in exams}
room = {e: Int(f'room_{e}') for e in exams}
duration = {e: Int(f'duration_{e}') for e in exams}

solver = Solver()

# Domain constraints
for e in exams:
    solver.add(day[e] >= 1, day[e] <= 3)
    solver.add(time[e] >= 1, time[e] <= 3)
    solver.add(room[e] >= 1, room[e] <= 2)  # 1=R1, 2=R2
    solver.add(duration[e] == 1)  # fixed duration

# Conflict constraints: for each student, all (day,time) pairs distinct
student_exams = {
    'S1': ['E1','E3','E5'],
    'S2': ['E1','E4','E6'],
    'S3': ['E2','E3','E6'],
    'S4': ['E2','E4','E5']
}

for s, exams_list in student_exams.items():
    # For each pair, add disequality on (day,time)
    for i in range(len(exams_list)):
        for j in range(i+1, len(exams_list)):
            e1 = exams_list[i]
            e2 = exams_list[j]
            # Not (day[e1]==day[e2] and time[e1]==time[e2])
            solver.add(Or(day[e1] != day[e2], time[e1] != time[e2]))

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print schedule
    for e in exams:
        d = model[day[e]].as_long()
        t = model[time[e]].as_long()
        r = model[room[e]].as_long()
        dur = model[duration[e]].as_long()
        room_name = "R1" if r == 1 else "R2"
        print(f"Exam {e}: day={d} time_slot={t} room={room_name} duration={dur}")
    # Room utilization
    room_counts = {1:0,2:0}
    for e in exams:
        r_val = model[room[e]].as_long()
        room_counts[r_val] += 1
    print(f"room_utilization: {room_counts}")
    # conflicts_resolved is True by construction
    print("conflicts_resolved: True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")