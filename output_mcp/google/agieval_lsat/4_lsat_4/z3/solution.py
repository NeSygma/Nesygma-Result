from z3 import *

# Students: 0:G, 1:H, 2:I, 3:K, 4:L, 5:N, 6:O, 7:R
# Slots: 0:MonM, 1:MonA, 2:TueM, 3:TueA, 4:WedM, 5:WedA
slot_in_student = [Int(f'slot_in_student_{i}') for i in range(8)]
student_in_slot = [Int(f'student_in_slot_{i}') for i in range(6)]

solver = Solver()

# Domain constraints
for i in range(8):
    solver.add(slot_in_student[i] >= -1, slot_in_student[i] <= 5)
for i in range(6):
    solver.add(student_in_slot[i] >= 0, student_in_slot[i] <= 7)

# Each slot has a unique student
solver.add(Distinct(student_in_slot))

# Consistency
for s in range(8):
    solver.add(Or(slot_in_student[s] == -1, 
                  Or([student_in_slot[slot] == s for slot in range(6)])))
    for slot in range(6):
        solver.add(Implies(slot_in_student[s] == slot, student_in_slot[slot] == s))

# Exactly 6 students give reports
solver.add(Sum([If(slot_in_student[i] != -1, 1, 0) for i in range(8)]) == 6)

# C1: George (0) can only give a report on Tuesday (slots 2, 3)
solver.add(Or(slot_in_student[0] == -1, slot_in_student[0] == 2, slot_in_student[0] == 3))

# C2: Olivia (6) and Robert (7) cannot give an afternoon report (slots 1, 3, 5)
for s in [6, 7]:
    solver.add(Not(Or(slot_in_student[s] == 1, slot_in_student[s] == 3, slot_in_student[s] == 5)))

# C3: If Nina (5) gives a report, then on the next day Helen (1) and Irving (2) must both give reports, unless Nina's report is on Wednesday.
# Nina on Mon (0, 1) -> H, I on Tue (2, 3)
# Nina on Tue (2, 3) -> H, I on Wed (4, 5)
# Nina on Wed (4, 5) -> No condition
solver.add(Implies(Or(slot_in_student[5] == 0, slot_in_student[5] == 1), 
                   And(Or(slot_in_student[1] == 2, slot_in_student[1] == 3), 
                       Or(slot_in_student[2] == 2, slot_in_student[2] == 3))))
solver.add(Implies(Or(slot_in_student[5] == 2, slot_in_student[5] == 3), 
                   And(Or(slot_in_student[1] == 4, slot_in_student[1] == 5), 
                       Or(slot_in_student[2] == 4, slot_in_student[2] == 5))))

# Q: George (0), Nina (5), and Robert (7) give reports and they do so on different days.
solver.add(slot_in_student[0] != -1)
solver.add(slot_in_student[5] != -1)
solver.add(slot_in_student[7] != -1)

# Different days:
# G is on Tue (2, 3).
# N and R are on Mon (0, 1) and Wed (4, 5).
# G's day is 1 (0-indexed: 0=Mon, 1=Tue, 2=Wed)
solver.add(Or(slot_in_student[0] == 2, slot_in_student[0] == 3))
# N and R are on Mon or Wed
solver.add(Or(slot_in_student[5] == 0, slot_in_student[5] == 1, slot_in_student[5] == 4, slot_in_student[5] == 5))
solver.add(Or(slot_in_student[7] == 0, slot_in_student[7] == 1, slot_in_student[7] == 4, slot_in_student[7] == 5))
# N and R are on different days
day_N = If(Or(slot_in_student[5] == 0, slot_in_student[5] == 1), 0, 2)
day_R = If(Or(slot_in_student[7] == 0, slot_in_student[7] == 1), 0, 2)
solver.add(day_N != day_R)

# Options
opt_a_constr = Or(slot_in_student[1] == 4, slot_in_student[1] == 5)
opt_b_constr = Or(slot_in_student[5] == 0, slot_in_student[5] == 1)
opt_c_constr = Or(slot_in_student[5] == 2, slot_in_student[5] == 3)
opt_d_constr = Or(slot_in_student[6] == 0, slot_in_student[6] == 1)
opt_e_constr = Or(slot_in_student[7] == 4, slot_in_student[7] == 5)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")