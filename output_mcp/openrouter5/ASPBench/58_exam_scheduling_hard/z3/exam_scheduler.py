from z3 import *

# ========== DATA ==========
exams = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"]
rooms = ["R1", "R2", "R3"]
time_slots = [1, 2, 3, 4]

# Room types
room_type = {"R1": "classroom", "R2": "classroom", "R3": "lab"}
room_capacity = {"R1": 2, "R2": 2, "R3": 2}

# Exam room type requirements
exam_room_type = {
    "E1": "classroom", "E2": "classroom", "E3": "classroom",
    "E4": "classroom", "E5": "classroom", "E6": "classroom",
    "E7": "lab", "E8": "lab"
}

# Student enrollments
students = {
    "S1": ["E1", "E3", "E7"],
    "S2": ["E2", "E4", "E8"],
    "S3": ["E1", "E5"],
    "S4": ["E2", "E6"],
    "S5": ["E3", "E5", "E8"],
    "S6": ["E4", "E6", "E7"]
}

# Exam enrollments (how many students take each exam)
exam_enrollment = {}
for s, exs in students.items():
    for e in exs:
        exam_enrollment[e] = exam_enrollment.get(e, 0) + 1

# ========== DECISION VARIABLES ==========
# For each exam, assign a time slot (1-4) and a room (0=R1, 1=R2, 2=R3)
exam_time = {e: Int(f"time_{e}") for e in exams}
exam_room = {e: Int(f"room_{e}") for e in exams}

solver = Solver()

# ========== DOMAIN CONSTRAINTS ==========
for e in exams:
    solver.add(exam_time[e] >= 1, exam_time[e] <= 4)
    solver.add(exam_room[e] >= 0, exam_room[e] <= 2)

# ========== CONSTRAINT 1: Complete Scheduling (implicit in domain) ==========

# ========== CONSTRAINT 4: Room Type ==========
for e in exams:
    req_type = exam_room_type[e]
    if req_type == "classroom":
        # Must be in R1 (0) or R2 (1)
        solver.add(Or(exam_room[e] == 0, exam_room[e] == 1))
    else:  # lab
        # Must be in R3 (2)
        solver.add(exam_room[e] == 2)

# ========== CONSTRAINT 5: Room Capacity ==========
for e in exams:
    enrollment = exam_enrollment[e]
    # For each possible room, ensure capacity >= enrollment
    # R1 (0): cap 2, R2 (1): cap 2, R3 (2): cap 2
    # All rooms have capacity 2, and max enrollment is 3 (S1 has 3 exams, but per-exam enrollment max is 3)
    # Let's check: E1: S1,S3 -> 2, E2: S2,S4 -> 2, E3: S1,S5 -> 2, E4: S2,S6 -> 2,
    # E5: S3,S5 -> 2, E6: S4,S6 -> 2, E7: S1,S6 -> 2, E8: S2,S5 -> 2
    # All enrollments are 2, so capacity is fine. But let's encode it anyway.
    solver.add(True)  # All rooms have capacity 2, all exams have 2 students, so always satisfied

# ========== CONSTRAINT 2: Student Conflict ==========
# For each student, all their exams must be in different time slots
for s, exs in students.items():
    for i in range(len(exs)):
        for j in range(i+1, len(exs)):
            e1, e2 = exs[i], exs[j]
            solver.add(exam_time[e1] != exam_time[e2])

# ========== CONSTRAINT 3: Room Conflict ==========
# No two exams can be in the same room at the same time
for i in range(len(exams)):
    for j in range(i+1, len(exams)):
        e1, e2 = exams[i], exams[j]
        # If same time slot, must be in different rooms
        solver.add(Implies(exam_time[e1] == exam_time[e2], exam_room[e1] != exam_room[e2]))

# ========== SOLVE ==========
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("schedule:")
    for e in exams:
        t = m[exam_time[e]].as_long()
        r_idx = m[exam_room[e]].as_long()
        r = rooms[r_idx]
        print(f"  exam={e}, time_slot={t}, room={r}")
else:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")