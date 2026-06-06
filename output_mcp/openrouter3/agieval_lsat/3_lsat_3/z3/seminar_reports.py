from z3 import *

# Students
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_to_idx = {s: i for i, s in enumerate(students)}
N = len(students)

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
days = ["Monday", "Tuesday", "Wednesday"]
D = len(days)

# Time slots: 0=morning, 1=afternoon
slots = ["morning", "afternoon"]
S = len(slots)

# Decision variables: assignment[student][day][slot] = Bool
# True if student gives report on that day and slot
assignment = {}
for s in students:
    assignment[s] = {}
    for d in days:
        assignment[s][d] = {}
        for sl in slots:
            assignment[s][d][sl] = Bool(f"{s}_{d}_{sl}")

solver = Solver()

# Constraint 1: Exactly 6 students give reports (each student gives at most 1 report total)
# Actually, each student can give at most one report total (since they're individual reports)
# But we need exactly 6 students participating
participating = [Bool(f"part_{s}") for s in students]
for i, s in enumerate(students):
    # Student participates if they give any report
    solver.add(participating[i] == Or([assignment[s][d][sl] for d in days for sl in slots]))
solver.add(Sum(participating) == 6)

# Constraint 2: Each day has exactly 2 reports (one morning, one afternoon)
for d in days:
    # Morning: exactly one student
    morning_students = [assignment[s][d]["morning"] for s in students]
    solver.add(Sum([If(morning_students[i], 1, 0) for i in range(N)]) == 1)
    # Afternoon: exactly one student
    afternoon_students = [assignment[s][d]["afternoon"] for s in students]
    solver.add(Sum([If(afternoon_students[i], 1, 0) for i in range(N)]) == 1)

# Constraint 3: Tuesday is the only day George can give a report
# George can only give report on Tuesday
for d in days:
    if d == "Tuesday":
        # George must give exactly one report on Tuesday
        solver.add(Or([assignment["George"]["Tuesday"]["morning"], 
                       assignment["George"]["Tuesday"]["afternoon"]]))
    else:
        # George cannot give reports on other days
        for sl in slots:
            solver.add(Not(assignment["George"][d][sl]))

# Constraint 4: Neither Olivia nor Robert can give an afternoon report
for d in days:
    solver.add(Not(assignment["Olivia"][d]["afternoon"]))
    solver.add(Not(assignment["Robert"][d]["afternoon"]))

# Constraint 5: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is on Wednesday
# We need to model this carefully
# For each day Nina gives a report (except Wednesday), the next day must have both Helen and Irving
for d_idx, d in enumerate(days):
    if d == "Wednesday":
        continue  # Exception: if Nina's report is on Wednesday, no constraint
    # Next day
    next_d = days[d_idx + 1]
    # For each slot Nina could give report
    for sl in slots:
        # If Nina gives report on day d, slot sl, then next day must have both Helen and Irving
        # They could be in morning or afternoon (any slot)
        helen_next = Or([assignment["Helen"][next_d]["morning"], 
                         assignment["Helen"][next_d]["afternoon"]])
        irving_next = Or([assignment["Irving"][next_d]["morning"], 
                          assignment["Irving"][next_d]["afternoon"]])
        solver.add(Implies(assignment["Nina"][d][sl], And(helen_next, irving_next)))

# Additional constraint: Each student can give at most one report total
for s in students:
    total_reports = Sum([If(assignment[s][d][sl], 1, 0) for d in days for sl in slots])
    solver.add(total_reports <= 1)

# Now, we need to evaluate the answer choices
# The question: Which pair of students, if they give reports on the same day as each other, must give reports on Wednesday?
# This means: For each pair, we need to check if there exists any valid assignment where they give reports on the same day (any day),
# but NOT on Wednesday. If such an assignment exists, then the pair does NOT necessarily give reports on Wednesday.
# If NO such assignment exists (i.e., whenever they give reports on the same day, it must be Wednesday), then that's the answer.

# We'll test each option by adding the constraint that the pair gives reports on the same day (but NOT necessarily Wednesday),
# and checking if there's a solution where that day is NOT Wednesday.

found_options = []

for letter, pair in [("A", ("George", "Lenore")), 
                     ("B", ("Helen", "Nina")), 
                     ("C", ("Irving", "Robert")), 
                     ("D", ("Kyle", "Nina")), 
                     ("E", ("Olivia", "Kyle"))]:
    
    # We need to check: Is it possible for this pair to give reports on the same day that is NOT Wednesday?
    # If YES, then they don't necessarily give reports on Wednesday.
    # If NO (i.e., any solution where they give reports on same day forces that day to be Wednesday), then they must give on Wednesday.
    
    # We'll create a solver that checks if there exists a valid assignment where:
    # 1. The pair gives reports on the same day
    # 2. That day is NOT Wednesday
    # If such an assignment exists, then the pair does NOT necessarily give reports on Wednesday.
    
    test_solver = Solver()
    
    # Add all base constraints to test_solver
    # We need to copy all constraints from the main solver
    # Instead of copying, we'll rebuild the constraints in test_solver
    
    # Re-declare variables for test_solver (they need to be separate instances)
    test_assignment = {}
    for s in students:
        test_assignment[s] = {}
        for d in days:
            test_assignment[s][d] = {}
            for sl in slots:
                test_assignment[s][d][sl] = Bool(f"test_{s}_{d}_{sl}")
    
    # Add base constraints to test_solver
    test_participating = [Bool(f"test_part_{s}") for s in students]
    for i, s in enumerate(students):
        test_solver.add(test_participating[i] == Or([test_assignment[s][d][sl] for d in days for sl in slots]))
    test_solver.add(Sum(test_participating) == 6)
    
    for d in days:
        morning_students = [test_assignment[s][d]["morning"] for s in students]
        test_solver.add(Sum([If(morning_students[i], 1, 0) for i in range(N)]) == 1)
        afternoon_students = [test_assignment[s][d]["afternoon"] for s in students]
        test_solver.add(Sum([If(afternoon_students[i], 1, 0) for i in range(N)]) == 1)
    
    for d in days:
        if d == "Tuesday":
            test_solver.add(Or([test_assignment["George"]["Tuesday"]["morning"], 
                                test_assignment["George"]["Tuesday"]["afternoon"]]))
        else:
            for sl in slots:
                test_solver.add(Not(test_assignment["George"][d][sl]))
    
    for d in days:
        test_solver.add(Not(test_assignment["Olivia"][d]["afternoon"]))
        test_solver.add(Not(test_assignment["Robert"][d]["afternoon"]))
    
    for d_idx, d in enumerate(days):
        if d == "Wednesday":
            continue
        next_d = days[d_idx + 1]
        for sl in slots:
            helen_next = Or([test_assignment["Helen"][next_d]["morning"], 
                             test_assignment["Helen"][next_d]["afternoon"]])
            irving_next = Or([test_assignment["Irving"][next_d]["morning"], 
                              test_assignment["Irving"][next_d]["afternoon"]])
            test_solver.add(Implies(test_assignment["Nina"][d][sl], And(helen_next, irving_next)))
    
    for s in students:
        total_reports = Sum([If(test_assignment[s][d][sl], 1, 0) for d in days for sl in slots])
        test_solver.add(total_reports <= 1)
    
    # Now add the pair constraint: They give reports on the same day (but we don't specify which day)
    # We need to check if there exists a solution where that day is NOT Wednesday
    # So we'll try each day except Wednesday and see if any works
    
    possible_non_wednesday = False
    
    for d in days:
        if d == "Wednesday":
            continue
        
        # Check if it's possible for both to give reports on day d (any slots)
        pair_solver = Solver()
        
        # Copy all constraints from test_solver to pair_solver
        # Instead of copying, we'll rebuild again (simpler for this small problem)
        pair_assignment = {}
        for s in students:
            pair_assignment[s] = {}
            for d2 in days:
                pair_assignment[s][d2] = {}
                for sl in slots:
                    pair_assignment[s][d2][sl] = Bool(f"pair_{s}_{d2}_{sl}")
        
        pair_participating = [Bool(f"pair_part_{s}") for s in students]
        for i, s in enumerate(students):
            pair_solver.add(pair_participating[i] == Or([pair_assignment[s][d2][sl] for d2 in days for sl in slots]))
        pair_solver.add(Sum(pair_participating) == 6)
        
        for d2 in days:
            morning_students = [pair_assignment[s][d2]["morning"] for s in students]
            pair_solver.add(Sum([If(morning_students[i], 1, 0) for i in range(N)]) == 1)
            afternoon_students = [pair_assignment[s][d2]["afternoon"] for s in students]
            pair_solver.add(Sum([If(afternoon_students[i], 1, 0) for i in range(N)]) == 1)
        
        for d2 in days:
            if d2 == "Tuesday":
                pair_solver.add(Or([pair_assignment["George"]["Tuesday"]["morning"], 
                                    pair_assignment["George"]["Tuesday"]["afternoon"]]))
            else:
                for sl in slots:
                    pair_solver.add(Not(pair_assignment["George"][d2][sl]))
        
        for d2 in days:
            pair_solver.add(Not(pair_assignment["Olivia"][d2]["afternoon"]))
            pair_solver.add(Not(pair_assignment["Robert"][d2]["afternoon"]))
        
        for d_idx2, d2 in enumerate(days):
            if d2 == "Wednesday":
                continue
            next_d2 = days[d_idx2 + 1]
            for sl in slots:
                helen_next = Or([pair_assignment["Helen"][next_d2]["morning"], 
                                 pair_assignment["Helen"][next_d2]["afternoon"]])
                irving_next = Or([pair_assignment["Irving"][next_d2]["morning"], 
                                  pair_assignment["Irving"][next_d2]["afternoon"]])
                pair_solver.add(Implies(pair_assignment["Nina"][d2][sl], And(helen_next, irving_next)))
        
        for s in students:
            total_reports = Sum([If(pair_assignment[s][d2][sl], 1, 0) for d2 in days for sl in slots])
            pair_solver.add(total_reports <= 1)
        
        # Add the pair constraint: both give reports on day d
        p1, p2 = pair
        # They must each give exactly one report on day d (could be morning or afternoon)
        pair_solver.add(Or([pair_assignment[p1][d]["morning"], pair_assignment[p1][d]["afternoon"]]))
        pair_solver.add(Or([pair_assignment[p2][d]["morning"], pair_assignment[p2][d]["afternoon"]]))
        
        # Check if this is possible
        if pair_solver.check() == sat:
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