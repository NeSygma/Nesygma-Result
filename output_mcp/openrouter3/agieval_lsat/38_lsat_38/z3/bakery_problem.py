from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
days = 5
# Cookie types: 0=oatmeal, 1=peanut butter, 2=sugar
types = 3
# Batches: 0,1,2 for each type

# For each type and batch, which day it's made
# batch_day[type][batch] = day (0-4)
batch_day = [[Int(f"batch_{t}_{b}") for b in range(3)] for t in range(types)]

solver = Solver()

# Domain constraints: each batch day must be 0-4
for t in range(types):
    for b in range(3):
        solver.add(batch_day[t][b] >= 0)
        solver.add(batch_day[t][b] <= 4)

# Constraint 1: No two batches of same type on same day
for t in range(types):
    solver.add(Distinct([batch_day[t][0], batch_day[t][1], batch_day[t][2]]))

# Constraint 2: At least one batch on Monday (day 0)
# At least one batch among all types and batches is on day 0
solver.add(Or([batch_day[t][b] == 0 for t in range(types) for b in range(3)]))

# Constraint 3: Second oatmeal batch (t=0, b=1) = first peanut butter batch (t=1, b=0)
solver.add(batch_day[0][1] == batch_day[1][0])

# Constraint 4: Second sugar batch (t=2, b=1) is on Thursday (day 3)
solver.add(batch_day[2][1] == 3)

# Now we need to count for each day how many batches are made
# For each day, count batches across all types and batches
batch_counts = [Int(f"count_{d}") for d in range(days)]
for d in range(days):
    # Count how many batches are on day d
    solver.add(batch_counts[d] == Sum([If(batch_day[t][b] == d, 1, 0) for t in range(types) for b in range(3)]))

# Now we need to answer: How many days have at most 2 batches?
# That is, count days where batch_counts[d] <= 2
# Let's define a variable for the answer
answer = Int("answer")

# We need to count days with <= 2 batches
# For each day, define if it satisfies the condition
day_satisfies = [Bool(f"day_satisfies_{d}") for d in range(days)]
for d in range(days):
    solver.add(day_satisfies[d] == (batch_counts[d] <= 2))

# The answer is the sum of days that satisfy
solver.add(answer == Sum([If(day_satisfies[d], 1, 0) for d in range(days)]))

# Now we need to check what answer values are possible
# But the question asks: "How many of the days... are such that at most two batches..."
# This suggests we need to find the actual number given the constraints
# Let's first find a model to see what the answer is

print("Finding a model...")
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Example model:")
    for t in range(types):
        type_name = ["oatmeal", "peanut butter", "sugar"][t]
        for b in range(3):
            day_val = m.evaluate(batch_day[t][b])
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            print(f"  {type_name} batch {b+1}: {day_names[day_val]}")
    
    # Print batch counts per day
    print("\nBatch counts per day:")
    for d in range(days):
        count_val = m.evaluate(batch_counts[d])
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        print(f"  {day_names[d]}: {count_val} batches")
    
    # Print answer
    answer_val = m.evaluate(answer)
    print(f"\nNumber of days with at most 2 batches: {answer_val}")
    
    # Now we need to check which answer choice matches
    # The answer choices are: (A)one (B)two (C)three (D)four (E)five
    # We need to see if answer_val matches exactly one of these
    # But wait, the question might be asking for the number of days that COULD have at most 2 batches
    # Let me re-read: "How many of the days, Monday through Friday, are such that at most two batches of cookies could be made on that day?"
    # This is ambiguous. It could mean:
    # 1. In the actual schedule (given constraints), how many days have ≤2 batches?
    # 2. For how many days is it possible (in some valid schedule) that ≤2 batches are made?
    
    # Looking at the phrasing "could be made", it seems like it's asking about possibility
    # But the constraints fix many things, so maybe it's asking about the actual schedule
    
    # Let me check if the answer is unique across all valid schedules
    # We need to enumerate all solutions or check if answer is fixed
    
    # For now, let's assume it's asking for the number in the actual schedule
    # and that this number is the same for all valid schedules
    
    # Let's check if answer_val is always the same
    # We can try to find another solution with different answer
    solver2 = Solver()
    # Add same constraints
    for t in range(types):
        for b in range(3):
            solver2.add(batch_day[t][b] >= 0)
            solver2.add(batch_day[t][b] <= 4)
    for t in range(types):
        solver2.add(Distinct([batch_day[t][0], batch_day[t][1], batch_day[t][2]]))
    solver2.add(Or([batch_day[t][b] == 0 for t in range(types) for b in range(3)]))
    solver2.add(batch_day[0][1] == batch_day[1][0])
    solver2.add(batch_day[2][1] == 3)
    
    # Add constraint that answer is different
    solver2.add(answer != answer_val)
    
    if solver2.check() == sat:
        print("\nWARNING: Multiple possible answers exist!")
        m2 = solver2.model()
        answer_val2 = m2.evaluate(answer)
        print(f"Another possible answer: {answer_val2}")
    else:
        print("\nAnswer appears to be unique across all valid schedules.")
        
        # Map answer to choice
        if answer_val == 1:
            choice = "A"
        elif answer_val == 2:
            choice = "B"
        elif answer_val == 3:
            choice = "C"
        elif answer_val == 4:
            choice = "D"
        elif answer_val == 5:
            choice = "E"
        else:
            choice = "unknown"
        
        print(f"Answer choice: {choice}")
        
        # Now use the required multiple choice evaluation skeleton
        print("\n--- Multiple Choice Evaluation ---")
        
        # Define options based on answer choices
        # Option A: answer = 1
        # Option B: answer = 2
        # Option C: answer = 3
        # Option D: answer = 4
        # Option E: answer = 5
        
        found_options = []
        
        # Test each option
        for letter, target in [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
            solver_test = Solver()
            # Add base constraints
            for t in range(types):
                for b in range(3):
                    solver_test.add(batch_day[t][b] >= 0)
                    solver_test.add(batch_day[t][b] <= 4)
            for t in range(types):
                solver_test.add(Distinct([batch_day[t][0], batch_day[t][1], batch_day[t][2]]))
            solver_test.add(Or([batch_day[t][b] == 0 for t in range(types) for b in range(3)]))
            solver_test.add(batch_day[0][1] == batch_day[1][0])
            solver_test.add(batch_day[2][1] == 3)
            
            # Add option constraint
            solver_test.add(answer == target)
            
            if solver_test.check() == sat:
                found_options.append(letter)
        
        if len(found_options) == 1:
            print("STATUS: sat")
            print(f"answer:{found_options[0]}")
        elif len(found_options) > 1:
            print("STATUS: unsat")
            print(f"Refine: Multiple options found {found_options}")
        else:
            print("STATUS: unsat")
            print("Refine: No options found")
            
else:
    print("STATUS: unsat")
    print("No solution found - constraints may be inconsistent")