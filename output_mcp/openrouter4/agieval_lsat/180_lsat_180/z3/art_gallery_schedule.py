from z3 import *

# Students: Grecia=0, Hakeem=1, Joe=2, Katya=3, Louise=4
# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
# Shifts: first=0, second=1

NUM_STUDENTS = 5
NUM_DAYS = 5
NUM_SHIFTS = 2

solver = Solver()

# schedule[day][shift] = student (0-4)
schedule = [[Int(f'schedule_{d}_{s}') for s in range(NUM_SHIFTS)] for d in range(NUM_DAYS)]

# Domain constraints
for d in range(NUM_DAYS):
    for s in range(NUM_SHIFTS):
        solver.add(And(schedule[d][s] >= 0, schedule[d][s] < NUM_STUDENTS))

# Constraint 1: Each student works exactly 2 shifts
for student in range(NUM_STUDENTS):
    count = Sum([If(schedule[d][s] == student, 1, 0) for d in range(NUM_DAYS) for s in range(NUM_SHIFTS)])
    solver.add(count == 2)

# Constraint 2: No student works both shifts of any day
for d in range(NUM_DAYS):
    solver.add(schedule[d][0] != schedule[d][1])

# Constraint 3: On two consecutive days, Louise (4) works the second shift
consecutive_louise = Or([And(schedule[d][1] == 4, schedule[d+1][1] == 4) for d in range(NUM_DAYS-1)])
solver.add(consecutive_louise)

# Constraint 4: On two nonconsecutive days, Grecia (0) works the first shift
nonconsecutive_grecia = Or([And(schedule[d1][0] == 0, schedule[d2][0] == 0, d2 > d1 + 1) 
                           for d1 in range(NUM_DAYS) for d2 in range(d1+1, NUM_DAYS)])
solver.add(nonconsecutive_grecia)

# Constraint 5: Katya (3) works on Tuesday (day 1) and Friday (day 4)
# Katya works exactly 2 shifts total, so she works one shift on Tuesday and one on Friday
solver.add(Or(schedule[1][0] == 3, schedule[1][1] == 3))
solver.add(Or(schedule[4][0] == 3, schedule[4][1] == 3))

# Katya does NOT work on Monday, Wednesday, or Thursday
for d in range(NUM_DAYS):
    if d != 1 and d != 4:
        solver.add(schedule[d][0] != 3)
        solver.add(schedule[d][1] != 3)

# Constraint 6: Hakeem (1) and Joe (2) work on the same day at least once
same_day_hj = Or([And(
    Or(schedule[d][0] == 1, schedule[d][1] == 1),
    Or(schedule[d][0] == 2, schedule[d][1] == 2)
) for d in range(NUM_DAYS)])
solver.add(same_day_hj)

# Constraint 7: Grecia (0) and Louise (4) never work on the same day
for d in range(NUM_DAYS):
    grecia_works = Or(schedule[d][0] == 0, schedule[d][1] == 0)
    louise_works = Or(schedule[d][0] == 4, schedule[d][1] == 4)
    solver.add(Not(And(grecia_works, louise_works)))

# Solve and print
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    student_names = ["Grecia", "Hakeem", "Joe", "Katya", "Louise"]
    print("\nSchedule:")
    for d in range(NUM_DAYS):
        s1 = m[schedule[d][0]].as_long()
        s2 = m[schedule[d][1]].as_long()
        print(f"{day_names[d]}: First shift = {student_names[s1]}, Second shift = {student_names[s2]}")
    
    # Count shifts per student
    print("\nShifts per student:")
    for student in range(NUM_STUDENTS):
        count = 0
        for d in range(NUM_DAYS):
            for s in range(NUM_SHIFTS):
                if m[schedule[d][s]].as_long() == student:
                    count += 1
        print(f"{student_names[student]}: {count} shifts")
    
    # Verify Grecia non-consecutive first shifts
    print("\nVerification:")
    grecia_first_days = [d for d in range(NUM_DAYS) if m[schedule[d][0]].as_long() == 0]
    print(f"Grecia first shift days: {[day_names[d] for d in grecia_first_days]}")
    
    louise_second_days = [d for d in range(NUM_DAYS) if m[schedule[d][1]].as_long() == 4]
    print(f"Louise second shift days: {[day_names[d] for d in louise_second_days]}")
    
    katya_days = [d for d in range(NUM_DAYS) if m[schedule[d][0]].as_long() == 3 or m[schedule[d][1]].as_long() == 3]
    print(f"Katya works on: {[day_names[d] for d in katya_days]}")
    
    hakeem_days = [d for d in range(NUM_DAYS) if m[schedule[d][0]].as_long() == 1 or m[schedule[d][1]].as_long() == 1]
    joe_days = [d for d in range(NUM_DAYS) if m[schedule[d][0]].as_long() == 2 or m[schedule[d][1]].as_long() == 2]
    common_days = [d for d in hakeem_days if d in joe_days]
    print(f"Hakeem works on: {[day_names[d] for d in hakeem_days]}")
    print(f"Joe works on: {[day_names[d] for d in joe_days]}")
    print(f"Hakeem and Joe work together on: {[day_names[d] for d in common_days]}")
    
    grecia_days = [d for d in range(NUM_DAYS) if m[schedule[d][0]].as_long() == 0 or m[schedule[d][1]].as_long() == 0]
    louise_days_total = [d for d in range(NUM_DAYS) if m[schedule[d][0]].as_long() == 4 or m[schedule[d][1]].as_long() == 4]
    print(f"Grecia works on: {[day_names[d] for d in grecia_days]}")
    print(f"Louise works on: {[day_names[d] for d in louise_days_total]}")
    overlap = [d for d in grecia_days if d in louise_days_total]
    print(f"Grecia and Louise same day (should be empty): {[day_names[d] for d in overlap]}")
    
    print("\nANSWER SUMMARY:")
    print("The problem's answer choices (cookbook publication) don't match this scheduling domain.")
    print("Please provide the correct answer choices for this specific problem.")

elif result == unsat:
    print("STATUS: unsat")
    print("No valid schedule found. Need to refine constraints.")
else:
    print("STATUS: unknown")