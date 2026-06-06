from z3 import *

# Solver instance
solver = Solver()

# Problem data
num_courses = 5
num_rooms = 3
num_slots = 4

# Course data
students = [25, 20, 30, 15, 35]
teachers = [0, 1, 2, 1, 0]

# Room capacities
room_caps = [40, 25, 20]

# Teacher availability
teacher_avail = {
    0: [0, 1, 2],
    1: [1, 2, 3],
    2: [0, 2, 3]
}

# Decision variables: room and slot for each course
room = [Int(f'room_{i}') for i in range(num_courses)]
slot = [Int(f'slot_{i}') for i in range(num_courses)]

# Domain constraints for rooms and slots
for i in range(num_courses):
    solver.add(Or([room[i] == r for r in range(num_rooms)]))
    solver.add(Or([slot[i] == s for s in range(num_slots)]))

# Capacity constraints: chosen room must accommodate students
for i in range(num_courses):
    valid_rooms = [r for r in range(num_rooms) if room_caps[r] >= students[i]]
    solver.add(Or([room[i] == r for r in valid_rooms]))

# Teacher availability constraints
for i in range(num_courses):
    avail = teacher_avail[teachers[i]]
    solver.add(Or([slot[i] == s for s in avail]))

# No two courses in same room at same time
for i in range(num_courses):
    for j in range(i + 1, num_courses):
        solver.add(Or(room[i] != room[j], slot[i] != slot[j]))

# Teacher cannot teach multiple courses simultaneously
for i in range(num_courses):
    for j in range(i + 1, num_courses):
        if teachers[i] == teachers[j]:
            solver.add(slot[i] != slot[j])

# Check satisfiability
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    for i in range(num_courses):
        print(f"course_{i} = (room {m[room[i]]}, slot {m[slot[i]]})")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")