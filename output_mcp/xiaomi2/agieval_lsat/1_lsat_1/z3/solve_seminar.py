from z3 import *

# Students: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
# Days: Monday=0, Tuesday=1, Wednesday=2
# Slots: morning=0, afternoon=1
# So 6 slots total: (day, slot) pairs

# We'll encode each option directly and check constraints

# Constraint 1: Tuesday is the only day George can give a report
# Constraint 2: Neither Olivia nor Robert can give an afternoon report
# Constraint 3: If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is on Wednesday

# Define student names for reference
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]

# Each option is a dict mapping (day, slot) -> student index
options = {
    "A": {
        (0,0): 1, (0,1): 7,  # Mon: Helen, Robert
        (1,0): 6, (1,1): 2,  # Tues: Olivia, Irving
        (2,0): 4, (2,1): 3,  # Wed: Lenore, Kyle
    },
    "B": {
        (0,0): 2, (0,1): 6,  # Mon: Irving, Olivia
        (1,0): 1, (1,1): 3,  # Tues: Helen, Kyle
        (2,0): 5, (2,1): 4,  # Wed: Nina, Lenore
    },
    "C": {
        (0,0): 4, (0,1): 1,  # Mon: Lenore, Helen
        (1,0): 0, (1,1): 3,  # Tues: George, Kyle
        (2,0): 7, (2,1): 2,  # Wed: Robert, Irving
    },
    "D": {
        (0,0): 5, (0,1): 1,  # Mon: Nina, Helen
        (1,0): 7, (1,1): 2,  # Tues: Robert, Irving
        (2,0): 6, (2,1): 4,  # Wed: Olivia, Lenore
    },
    "E": {
        (0,0): 6, (0,1): 5,  # Mon: Olivia, Nina
        (1,0): 2, (1,1): 1,  # Tues: Irving, Helen
        (2,0): 3, (2,1): 0,  # Wed: Kyle, George
    },
}

found_options = []

for letter, sched in options.items():
    solver = Solver()
    
    # Build the schedule as Z3 variables for encoding constraints
    # day d, slot s -> student
    report = {}
    for d in range(3):
        for s in range(2):
            report[(d,s)] = Int(f"report_{d}_{s}")
            # Fix to the option's value
            solver.add(report[(d,s)] == sched[(d,s)])
    
    # Exactly 6 distinct students (2 don't report)
    all_students = [report[(d,s)] for d in range(3) for s in range(2)]
    solver.add(Distinct(all_students))
    
    # Each student in valid range
    for v in all_students:
        solver.add(v >= 0, v <= 7)
    
    # Constraint 1: George (0) can only report on Tuesday (day=1)
    for d in range(3):
        for s in range(2):
            solver.add(Implies(report[(d,s)] == 0, d == 1))
    
    # Constraint 2: Olivia (6) and Robert (7) cannot give afternoon (slot=1) reports
    for d in range(3):
        solver.add(report[(d,1)] != 6)  # Olivia not afternoon
        solver.add(report[(d,1)] != 7)  # Robert not afternoon
    
    # Constraint 3: If Nina (5) gives a report on day d (not Wednesday),
    # then on day d+1, both Helen (1) and Irving (2) must give reports
    for d in range(3):  # Nina's report day
        for s in range(2):
            # If Nina reports on day d and d < 2 (not Wednesday)
            nina_on_d_s = (report[(d,s)] == 5)
            if d < 2:
                # Next day d+1 must have both Helen and Irving
                next_day = d + 1
                helen_next = Or(report[(next_day,0)] == 1, report[(next_day,1)] == 1)
                irving_next = Or(report[(next_day,0)] == 2, report[(next_day,1)] == 2)
                solver.add(Implies(nina_on_d_s, And(helen_next, irving_next)))
    
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter}: SAT")
        for d, day_name in enumerate(["Monday", "Tuesday", "Wednesday"]):
            for s, slot_name in enumerate(["morning", "afternoon"]):
                stud = m[report[(d,s)]].as_long()
                print(f"  {day_name} {slot_name}: {students[stud]}")
    else:
        print(f"Option {letter}: UNSAT")

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")