from z3 import *

# Data
num_courses = 5
rooms = 3
times = 4
capacity = [40, 25, 20]
students = [25, 20, 30, 15, 35]
teacher_of = [0, 1, 2, 1, 0]  # course -> teacher id

# Teacher availability per slot (0-indexed)
teacher_avail = {
    0: [0,1,2],
    1: [1,2,3],
    2: [0,2,3]
}

solver = Solver()

# Variables
room = [Int(f"room_{i}") for i in range(num_courses)]
time = [Int(f"time_{i}") for i in range(num_courses)]
pair = [Int(f"pair_{i}") for i in range(num_courses)]

# Constraints
for c in range(num_courses):
    # domain
    solver.add(room[c] >= 0, room[c] < rooms)
    solver.add(time[c] >= 0, time[c] < times)
    # availability
    avail_list = teacher_avail[teacher_of[c]]
    # Or over allowed slots
    avail_c = Or([time[c] == s for s in avail_list])
    solver.add(avail_c)
    # capacity
    solver.add(students[c] <= capacity[room[c]])
    # pair encoding
    solver.add(pair[c] == 4 * room[c] + time[c])

# All pairs distinct
solver.add(Distinct(pair))

# Check
BENCHMARK_MODE = True
result = solver.check()
if result == sat:
    print("STATUS: sat")
    m = solver.model()
    for c in range(num_courses):
        print(f"Course {c}: Room {m[room[c]]}, Time {m[time[c]]}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")