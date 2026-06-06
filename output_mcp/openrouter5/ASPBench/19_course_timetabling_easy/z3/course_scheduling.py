from z3 import *

# Instance Data
courses = list(range(5))  # 0: Math, 1: Physics, 2: Chemistry, 3: Biology, 4: CS
rooms = list(range(3))    # 0: cap=40, 1: cap=25, 2: cap=20
slots = list(range(4))    # 0: 9-10, 1: 10-11, 2: 2-3, 3: 3-4

course_students = [25, 20, 30, 15, 35]
room_capacity = [40, 25, 20]
teacher_of_course = [0, 1, 2, 1, 0]  # teacher id for each course
teacher_availability = {
    0: [0, 1, 2],
    1: [1, 2, 3],
    2: [0, 2, 3]
}

solver = Solver()

# Decision variables: for each course, assign a room and a time slot
course_room = [Int(f'course_room_{c}') for c in courses]
course_slot = [Int(f'course_slot_{c}') for c in courses]

# Domain constraints
for c in courses:
    solver.add(course_room[c] >= 0, course_room[c] < len(rooms))
    solver.add(course_slot[c] >= 0, course_slot[c] < len(slots))

# Constraint 1: Each course scheduled exactly once (already enforced by single assignment)

# Constraint 2: No two courses can use the same room at the same time
# For each pair of distinct courses, if they share a room, they must have different slots
for i in range(len(courses)):
    for j in range(i+1, len(courses)):
        # Not (same room AND same slot)
        solver.add(Not(And(course_room[i] == course_room[j], course_slot[i] == course_slot[j])))

# Constraint 3: Teachers cannot teach multiple courses simultaneously
# For each pair of courses with the same teacher, they must have different slots
for i in range(len(courses)):
    for j in range(i+1, len(courses)):
        if teacher_of_course[i] == teacher_of_course[j]:
            solver.add(course_slot[i] != course_slot[j])

# Constraint 4: Room capacity must accommodate course enrollment
for c in courses:
    # For each possible room r, if course c is assigned to room r, then students <= capacity
    # Use Or-loop pattern
    solver.add(Or([And(course_room[c] == r, course_students[c] <= room_capacity[r]) for r in rooms]))

# Constraint 5: Courses can only be scheduled when their teacher is available
for c in courses:
    t = teacher_of_course[c]
    avail = teacher_availability[t]
    # course_slot[c] must be one of the available slots
    solver.add(Or([course_slot[c] == s for s in avail]))

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Valid schedule found:")
    for c in courses:
        r = m[course_room[c]].as_long()
        s = m[course_slot[c]].as_long()
        course_names = ["Math", "Physics", "Chemistry", "Biology", "CS"]
        room_names = ["Room0(cap=40)", "Room1(cap=25)", "Room2(cap=20)"]
        slot_names = ["Slot0(9-10)", "Slot1(10-11)", "Slot2(2-3)", "Slot3(3-4)"]
        print(f"  {course_names[c]}: {room_names[r]}, {slot_names[s]}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")