from z3 import *

solver = Solver()

exams = ['E1','E2','E3','E4','E5','E6','E7','E8']
time_slots = [1,2,3,4]
rooms = [1,2,3]  # 1:R1, 2:R2, 3:R3

# Variables
# time slot assignment for each exam
T = {e: Int(f"t_{e}") for e in exams}
# room assignment for each exam
R = {e: Int(f"r_{e}") for e in exams}

# Domain constraints
for e in exams:
    solver.add(Or([T[e] == ts for ts in time_slots]))
    solver.add(Or([R[e] == rm for rm in rooms]))

# Room type requirements
classroom_exams = ['E1','E2','E3','E4','E5','E6']
lab_exams = ['E7','E8']
for e in classroom_exams:
    solver.add(R[e] <= 2)  # rooms 1 or 2
for e in lab_exams:
    solver.add(R[e] == 3)

# Student enrollments
student_exams = {
    'S1': ['E1','E3','E7'],
    'S2': ['E2','E4','E8'],
    'S3': ['E1','E5'],
    'S4': ['E2','E6'],
    'S5': ['E3','E5','E8'],
    'S6': ['E4','E6','E7']
}

# Student conflict: same student cannot have two exams at same time
for exams_list in student_exams.values():
    for i in range(len(exams_list)):
        for j in range(i+1, len(exams_list)):
            e1 = exams_list[i]
            e2 = exams_list[j]
            solver.add(T[e1] != T[e2])

# Room conflict: at most one exam per room per time slot
for rm in rooms:
    for ts in time_slots:
        solver.add(Sum([If(And(R[e] == rm, T[e] == ts), 1, 0) for e in exams]) <= 1)

# Capacity constraint: all exams have 2 students, all rooms capacity 2
# (trivially satisfied, so omitted)

result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    for e in exams:
        ts = m[T[e]].as_long()
        rm = m[R[e]].as_long()
        room_name = {1:'R1',2:'R2',3:'R3'}[rm]
        print(f"{e} {ts} {room_name}")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")