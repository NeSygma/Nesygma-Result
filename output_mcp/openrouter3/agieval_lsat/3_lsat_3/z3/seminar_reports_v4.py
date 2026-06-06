from z3 import *

# Students
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
N = len(students)

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
D = 3

# Time slots: 0=morning, 1=afternoon
S = 2

# Decision variables: For each student, which day and slot they give report
day_of_report = {}
slot_of_report = {}
for s in students:
    day_of_report[s] = Int(f"day_{s}")
    slot_of_report[s] = Int(f"slot_{s}")

solver = Solver()

# Constraint: Each student either doesn't participate (day=-1, slot=-1) or participates exactly once
for s in students:
    solver.add(Or(
        And(day_of_report[s] == -1, slot_of_report[s] == -1),
        And(day_of_report[s] >= 0, day_of_report[s] < D, slot_of_report[s] >= 0, slot_of_report[s] < S)
    ))

# Exactly 6 students participate
participating = [If(day_of_report[s] >= 0, 1, 0) for s in students]
solver.add(Sum(participating) == 6)

# Each day has exactly 2 reports (one morning, one afternoon)
for d in range(D):
    morning_count = Sum([If(And(day_of_report[s] == d, slot_of_report[s] == 0), 1, 0) for s in students])
    afternoon_count = Sum([If(And(day_of_report[s] == d, slot_of_report[s] == 1), 1, 0) for s in students])
    solver.add(morning_count == 1)
    solver.add(afternoon_count == 1)

# Constraint: Tuesday is the only day George can give a report
solver.add(day_of_report["George"] == 1)  # Tuesday is index 1

# Constraint: Neither Olivia nor Robert can give an afternoon report
solver.add(slot_of_report["Olivia"] != 1)  # If participating, not afternoon
solver.add(slot_of_report["Robert"] != 1)  # If participating, not afternoon

# Constraint: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is on Wednesday
for d in range(D):
    if d == 2:  # Wednesday, exception
        continue
    next_d = d + 1
    # If Nina gives report on day d, then next day must have both Helen and Irving
    solver.add(Implies(
        day_of_report["Nina"] == d,
        And(day_of_report["Helen"] == next_d, day_of_report["Irving"] == next_d)
    ))

# Now, we need to evaluate the answer choices
# The question: Which pair of students, if they give reports on the same day as each other, must give reports on Wednesday?
# This means: For each pair, we need to check if there exists any valid assignment where they give reports on the same day,
# but NOT on Wednesday. If such an assignment exists, then the pair does NOT necessarily give reports on Wednesday.
# If NO such assignment exists (i.e., whenever they give reports on the same day, it must be Wednesday), then that's the answer.

found_options = []

for letter, pair in [("A", ("George", "Lenore")), 
                     ("B", ("Helen", "Nina")), 
                     ("C", ("Irving", "Robert")), 
                     ("D", ("Kyle", "Nina")), 
                     ("E", ("Olivia", "Kyle"))]:
    
    # Check if it's possible for this pair to give reports on the same day that is NOT Wednesday
    # We'll test each non-Wednesday day (Monday and Tuesday)
    possible_non_wednesday = False
    
    for d in [0, 1]:  # Monday and Tuesday
        test_solver = Solver()
        
        # Re-declare variables for test_solver
        test_day_of_report = {}
        test_slot_of_report = {}
        for s in students:
            test_day_of_report[s] = Int(f"test_day_{s}_{d}_{letter}")
            test_slot_of_report[s] = Int(f"test_slot_{s}_{d}_{letter}")
        
        # Add base constraints
        for s in students:
            test_solver.add(Or(
                And(test_day_of_report[s] == -1, test_slot_of_report[s] == -1),
                And(test_day_of_report[s] >= 0, test_day_of_report[s] < D, test_slot_of_report[s] >= 0, test_slot_of_report[s] < S)
            ))
        
        participating_test = [If(test_day_of_report[s] >= 0, 1, 0) for s in students]
        test_solver.add(Sum(participating_test) == 6)
        
        for d2 in range(D):
            morning_count = Sum([If(And(test_day_of_report[s] == d2, test_slot_of_report[s] == 0), 1, 0) for s in students])
            afternoon_count = Sum([If(And(test_day_of_report[s] == d2, test_slot_of_report[s] == 1), 1, 0) for s in students])
            test_solver.add(morning_count == 1)
            test_solver.add(afternoon_count == 1)
        
        test_solver.add(test_day_of_report["George"] == 1)
        test_solver.add(test_slot_of_report["Olivia"] != 1)
        test_solver.add(test_slot_of_report["Robert"] != 1)
        
        for d2 in range(D):
            if d2 == 2:
                continue
            next_d2 = d2 + 1
            test_solver.add(Implies(
                test_day_of_report["Nina"] == d2,
                And(test_day_of_report["Helen"] == next_d2, test_day_of_report["Irving"] == next_d2)
            ))
        
        # Add the pair constraint: both give reports on day d
        p1, p2 = pair
        test_solver.add(test_day_of_report[p1] == d)
        test_solver.add(test_day_of_report[p2] == d)
        
        # Check if this is possible
        if test_solver.check() == sat:
            possible_non_wednesday = True
            break
    
    # If it's NOT possible for the pair to give reports on the same day that is NOT Wednesday,
    # then they MUST give reports on Wednesday (if they give reports on the same day at all)
    if not possible_non_wednesday:
        found_options.append(letter)

# Now apply the exact logic string from the requirement
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")