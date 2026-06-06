from z3 import *

# Problem Data
num_courses = 5
num_rooms = 3
num_slots = 4

course_students = [25, 20, 30, 15, 35]
course_teacher = [0, 1, 2, 1, 0]
room_capacity = [40, 25, 20]
teacher_availability = {
    0: [0, 1, 2],
    1: [1, 2, 3],
    2: [0, 2, 3]
}

# Solver
solver = Solver()

# Variables
course_room = [Int(f'course_room_{c}') for c in range(num_courses)]
course_slot = [Int(f'course_slot_{c}') for c in range(num_courses)]

# Domain Constraints
for c in range(num_courses):
    solver.add(course_room[c] >= 0, course_room[c] < num_rooms)
    solver.add(course_slot[c] >= 0, course_slot[c] < num_slots)

# Constraint 2: No two courses can use the same room at the same time
for i in range(num_courses):
    for j in range(i + 1, num_courses):
        solver.add(Not(And(course_room[i] == course_room[j], course_slot[i] == course_slot[j])))

# Constraint 3: Teachers cannot teach multiple courses simultaneously
for i in range(num_courses):
    for j in range(i + 1, num_courses):
        if course_teacher[i] == course_teacher[j]:
            solver.add(course_slot[i] != course_slot[j])

# Constraint 4: Room capacity must accommodate course enrollment
for c in range(num_courses):
    # Use Or-loop to check capacity based on assigned room
    solver.add(Or([And(course_room[c] == r, room_capacity[r] >= course_students[c]) for r in range(num_rooms)]))

# Constraint 5: Courses can only be scheduled when their teacher is available
for c in range(num_courses):
    teacher = course_teacher[c]
    available_slots = teacher_availability[teacher]
    solver.add(Or([course_slot[c] == s for s in available_slots]))

# Solve
result = solver.check()

if result == sat:
    print("STATUS: sat")
    model = solver.model()
    for c in range(num_courses):
        r = model.eval(course_room[c]).as_long()
        s = model.eval(course_slot[c]).as_long()
        print(f"Course {c} (Teacher {course_teacher[c]}, Students {course_students[c]}): Room {r} (Cap {room_capacity[r]}), Slot {s}")
else:
    print("STATUS: unsat")