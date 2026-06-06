from z3 import *

# Exams: E1..E8
NUM_EXAMS = 8
NUM_SLOTS = 4
NUM_ROOMS = 3

# Variables: time slot (1-4) and room (1-3) for each exam
exam_time = [Int(f"exam_time_{e}") for e in range(NUM_EXAMS)]  # 0-indexed: E1=0, ..., E8=7
exam_room = [Int(f"exam_room_{e}") for e in range(NUM_EXAMS)]  # 0-indexed: R1=1, R2=2, R3=3

solver = Solver()

# Domain constraints
for e in range(NUM_EXAMS):
    solver.add(exam_time[e] >= 1, exam_time[e] <= NUM_SLOTS)
    solver.add(exam_room[e] >= 1, exam_room[e] <= NUM_ROOMS)

# Constraint 1: Complete scheduling is inherent in variable assignment.

# Constraint 4: Room Type
# Classroom required: E1, E2, E3, E4, E5, E6 (exams 0..5)
# Lab required: E7, E8 (exams 6, 7)
# R1 (room 1) and R2 (room 2) are classrooms
# R3 (room 3) is lab
for e in range(6):  # E1..E6
    solver.add(Or(exam_room[e] == 1, exam_room[e] == 2))
for e in range(6, 8):  # E7, E8
    solver.add(exam_room[e] == 3)

# Constraint 5: Room Capacity
# All rooms have capacity 2, and each exam has 2 students enrolled.
# So capacity is always satisfied regardless of room assignment.
# (Included implicitly — no additional constraints needed.)

# Enrollments: for each exam, list of enrolled students
# E1: S1, S3
# E2: S2, S4
# E3: S1, S5
# E4: S2, S6
# E5: S3, S5
# E6: S4, S6
# E7: S1, S6
# E8: S2, S5

# Student exams (0-indexed)
student_exams = [
    [0, 2, 6],      # S1: E1(0), E3(2), E7(6)
    [1, 3, 7],      # S2: E2(1), E4(3), E8(7)
    [0, 4],         # S3: E1(0), E5(4)
    [1, 5],         # S4: E2(1), E6(5)
    [2, 4, 7],      # S5: E3(2), E5(4), E8(7)
    [3, 5, 6]       # S6: E4(3), E6(5), E7(6)
]

# Constraint 2: Student Conflict
# A student cannot be scheduled for two different exams in the same time slot.
for student in student_exams:
    for i in range(len(student)):
        for j in range(i + 1, len(student)):
            e1 = student[i]
            e2 = student[j]
            solver.add(exam_time[e1] != exam_time[e2])

# Constraint 3: Room Conflict
# Two different exams cannot occupy the same (time_slot, room) pair.
for e1 in range(NUM_EXAMS):
    for e2 in range(e1 + 1, NUM_EXAMS):
        solver.add(Or(exam_time[e1] != exam_time[e2], exam_room[e1] != exam_room[e2]))

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("schedule:")
    for e in range(NUM_EXAMS):
        t = m[exam_time[e]].as_long()
        r = m[exam_room[e]].as_long()
        exam_id = f"E{e+1}"
        room_id = f"R{r}"
        print(f"  exam={exam_id}, time_slot={t}, room={room_id}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")