from z3 import *

# Students: 0:G, 1:H, 2:I, 3:K, 4:L, 5:N, 6:O, 7:R
# Slots: 0:Mon-AM, 1:Mon-PM, 2:Tue-AM, 3:Tue-PM, 4:Wed-AM, 5:Wed-PM

def solve():
    solver = Solver()
    
    # Each slot has exactly one student, or no student? 
    # "Exactly six will give individual oral reports"
    # "Exactly two reports will be given each day"
    # So all 6 slots must be filled by 6 distinct students.
    
    # Let's represent the assignment as a function from slot to student
    # slot_to_student[slot] = student_id
    slot_to_student = [Int(f'slot_{i}') for i in range(6)]
    
    # Each slot has a student from 0-7
    for i in range(6):
        solver.add(slot_to_student[i] >= 0, slot_to_student[i] <= 7)
        
    # All 6 students must be distinct
    solver.add(Distinct(slot_to_student))
    
    # C2: Tuesday is the only day on which George can give a report.
    # George is 0. If George is in a slot, it must be 2 or 3.
    # If George is not in any slot, that's also fine.
    for i in range(6):
        solver.add(Implies(slot_to_student[i] == 0, Or(i == 2, i == 3)))
        
    # C3: Neither Olivia (6) nor Robert (7) can give an afternoon report.
    # Afternoon slots are 1, 3, 5.
    for i in [1, 3, 5]:
        solver.add(slot_to_student[i] != 6)
        solver.add(slot_to_student[i] != 7)
        
    # C4: If Nina (5) gives a report, then on the next day Helen (1) and Irving (2) must both give reports, 
    # unless Nina's report is given on Wednesday (slots 4, 5).
    # Nina's day:
    # Mon: 0, 1
    # Tue: 2, 3
    # Wed: 4, 5
    
    # If Nina is in slot 0 or 1, then H and I must be in slots 2 and 3.
    nina_in_mon = Or(slot_to_student[0] == 5, slot_to_student[1] == 5)
    h_and_i_in_tue = And(Or(slot_to_student[2] == 1, slot_to_student[3] == 1),
                         Or(slot_to_student[2] == 2, slot_to_student[3] == 2))
    solver.add(Implies(nina_in_mon, h_and_i_in_tue))
    
    # If Nina is in slot 2 or 3, then H and I must be in slots 4 and 5.
    nina_in_tue = Or(slot_to_student[2] == 5, slot_to_student[3] == 5)
    h_and_i_in_wed = And(Or(slot_to_student[4] == 1, slot_to_student[5] == 1),
                         Or(slot_to_student[4] == 2, slot_to_student[5] == 2))
    solver.add(Implies(nina_in_tue, h_and_i_in_wed))
    
    # Define the options
    # Students: 0:G, 1:H, 2:I, 3:K, 4:L, 5:N, 6:O, 7:R
    # A: Mon-AM: H(1), Mon-PM: R(7), Tue-AM: O(6), Tue-PM: I(2), Wed-AM: L(4), Wed-PM: K(3)
    # B: Mon-AM: I(2), Mon-PM: O(6), Tue-AM: H(1), Tue-PM: K(3), Wed-AM: N(5), Wed-PM: L(4)
    # C: Mon-AM: L(4), Mon-PM: H(1), Tue-AM: G(0), Tue-PM: K(3), Wed-AM: R(7), Wed-PM: I(2)
    # D: Mon-AM: N(5), Mon-PM: H(1), Tue-AM: R(7), Tue-PM: I(2), Wed-AM: O(6), Wed-PM: L(4)
    # E: Mon-AM: O(6), Mon-PM: N(5), Tue-AM: I(2), Tue-PM: H(1), Wed-AM: K(3), Wed-PM: G(0)
    
    options = [
        ("A", [1, 7, 6, 2, 4, 3]),
        ("B", [2, 6, 1, 3, 5, 4]),
        ("C", [4, 1, 0, 3, 7, 2]),
        ("D", [5, 1, 7, 2, 6, 4]),
        ("E", [6, 5, 2, 1, 3, 0])
    ]
    
    found_options = []
    for name, assignment in options:
        solver.push()
        for i in range(6):
            solver.add(slot_to_student[i] == assignment[i])
        if solver.check() == sat:
            found_options.append(name)
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

solve()