from z3 import *

# Data
num_courses = 5
num_rooms = 3
num_slots = 4

# Course data
students = [25, 20, 30, 15, 35]
teachers = [0, 1, 2, 1, 0]

# Room capacities
capacity = [40, 25, 20]

# Teacher availability (list of allowed slots)
teacher_avail = {
    0: [0, 1, 2],
    1: [1, 2, 3],
    2: [0, 2, 3]
}

solver = Solver()

# Variables
room = [Int(f"room_{i}") for i in range(num_courses)]
slot = [Int(f"slot_{i}") for i in range(num_courses)]

# Domain constraints
for i in range(num_courses):
    solver.add(room[i] >= 0, room[i] < num_rooms)
    solver.add(slot[i] >= 0, slot[i] < num_slots)

# Capacity constraints
for i in range(num_courses):
    # capacity[room[i]] >= students[i]
    # Use Or over possible rooms
    caps = [And(room[i] == r, capacity[r] >= students[i]) for r in range(num_rooms)]
    solver.add(Or(caps))

# Teacher availability constraints
for i in range(num_courses):
    avail = teacher_avail[teachers[i]]
    solver.add(Or([slot[i] == s for s in avail]))

# No two courses share same room and slot
for i in range(num_courses):
    for j in range(i+1, num_courses):
        solver.add(Not(And(room[i] == room[j], slot[i] == slot[j])))

# Teacher cannot teach multiple courses at same time
for i in range(num_courses):
    for j in range(i+1, num_courses):
        if teachers[i] == teachers[j]:
            solver.add(slot[i] != slot[j])

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    for i in range(num_courses):
        r = m.eval(room[i]).as_long()
        s = m.eval(slot[i]).as_long()
        print(f"Course {i}: room = {r}, slot = {s}")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")