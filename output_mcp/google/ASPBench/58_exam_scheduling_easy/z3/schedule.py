from z3 import *

# Exams: E1, E2, E3, E4, E5, E6 (indices 0-5)
# Students: S1, S2, S3, S4
# Enrollments:
# S1: E1, E3, E5 (0, 2, 4)
# S2: E1, E4, E6 (0, 3, 5)
# S3: E2, E3, E6 (1, 2, 5)
# S4: E2, E4, E5 (1, 3, 4)

num_exams = 6
num_slots = 3
num_rooms = 2 # R1=1, R2=2

solver = Solver()

# Variables
# slot[e] in {1, 2, 3}
# room[e] in {1, 2}
slot = [Int(f'slot_{i}') for i in range(num_exams)]
room = [Int(f'room_{i}') for i in range(num_exams)]

# Domain constraints
for i in range(num_exams):
    solver.add(slot[i] >= 1, slot[i] <= num_slots)
    solver.add(room[i] >= 1, room[i] <= num_rooms)

# Constraint 2: No student conflicts
# S1: E1, E3, E5
solver.add(Distinct(slot[0], slot[2], slot[4]))
# S2: E1, E4, E6
solver.add(Distinct(slot[0], slot[3], slot[5]))
# S3: E2, E3, E6
solver.add(Distinct(slot[1], slot[2], slot[5]))
# S4: E2, E4, E5
solver.add(Distinct(slot[1], slot[3], slot[4]))

# Constraint 4: Unique assignments (No two exams in the same room at the same time)
for i in range(num_exams):
    for j in range(i + 1, num_exams):
        solver.add(Not(And(slot[i] == slot[j], room[i] == room[j])))

# Constraint 3: Room capacity (2 students per exam, capacity 3)
# Since we have at most one exam per room per slot, this is always satisfied (2 <= 3).

result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    for i in range(num_exams):
        print(f"E{i+1}: Slot={m[slot[i]]}, Room=R{m[room[i]]}")
else:
    print("STATUS: unsat")