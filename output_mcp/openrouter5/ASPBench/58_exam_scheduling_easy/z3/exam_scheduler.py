from z3 import *

# Create solver
solver = Solver()

# Exams
exams = ["E1", "E2", "E3", "E4", "E5", "E6"]
num_exams = len(exams)

# Time slots: 3 slots available (day and slot combinations)
# We'll use slot indices 0, 1, 2 representing the 3 available time slots
num_slots = 3

# Rooms
rooms = ["R1", "R2"]
num_rooms = len(rooms)

# Room capacities
room_capacity = {"R1": 3, "R2": 3}

# Student enrollments
students = {
    "S1": ["E1", "E3", "E5"],
    "S2": ["E1", "E4", "E6"],
    "S3": ["E2", "E3", "E6"],
    "S4": ["E2", "E4", "E5"]
}

# Enrollment sizes (number of students per exam)
# E1: S1, S2 -> 2
# E2: S3, S4 -> 2
# E3: S1, S3 -> 2
# E4: S2, S4 -> 2
# E5: S1, S4 -> 2
# E6: S2, S3 -> 2
exam_enrollment = {
    "E1": 2, "E2": 2, "E3": 2, "E4": 2, "E5": 2, "E6": 2
}

# Decision variables:
# For each exam, assign a time slot (0, 1, or 2) and a room (0 for R1, 1 for R2)
exam_slot = [Int(f"slot_{e}") for e in exams]
exam_room = [Int(f"room_{e}") for e in exams]

# Domain constraints
for i in range(num_exams):
    solver.add(exam_slot[i] >= 0, exam_slot[i] < num_slots)
    solver.add(exam_room[i] >= 0, exam_room[i] < num_rooms)

# Constraint 1 & 4: All exams scheduled, unique assignments (handled by the variables themselves)

# Constraint 2: No student conflicts
# For each student, all their enrolled exams must be in different time slots
for student, student_exams in students.items():
    # Get indices of exams this student is enrolled in
    exam_indices = [exams.index(e) for e in student_exams]
    # All these exams must have different time slots
    solver.add(Distinct([exam_slot[i] for i in exam_indices]))

# Constraint 3: Room capacity
# The number of students in an exam must not exceed the room capacity
for i in range(num_exams):
    # Room capacity is 3 for both rooms, and each exam has at most 2 students
    # So this constraint is automatically satisfied, but we add it for completeness
    solver.add(exam_enrollment[exams[i]] <= room_capacity[rooms[0]])  # both rooms have capacity 3

# Also: no two exams in the same room at the same time slot
# (This is implied by the problem - a room can only host one exam per slot)
for i in range(num_exams):
    for j in range(i+1, num_exams):
        # If same time slot, they cannot be in the same room
        solver.add(Not(And(exam_slot[i] == exam_slot[j], exam_room[i] == exam_room[j])))

# Check for solution
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Schedule found:")
    for i in range(num_exams):
        slot_val = m[exam_slot[i]].as_long()
        room_val = m[exam_room[i]].as_long()
        print(f"  {exams[i]}: Slot {slot_val}, Room {rooms[room_val]}")
    
    # Compute room utilization
    room_counts = {r: 0 for r in rooms}
    for i in range(num_exams):
        room_val = m[exam_room[i]].as_long()
        room_counts[rooms[room_val]] += 1
    
    print(f"\nRoom utilization: {room_counts}")
    print(f"Conflicts resolved: True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")