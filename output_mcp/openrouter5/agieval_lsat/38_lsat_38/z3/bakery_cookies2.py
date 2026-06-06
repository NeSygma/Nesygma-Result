from z3 import *

# Let's re-interpret the question.
# "How many of the days, Monday through Friday, are such that at most two batches of cookies could be made on that day?"
# 
# This could mean: For each day, consider ALL possible valid schedules. 
# Is it POSSIBLE (could be) that on that day, at most 2 batches are made?
# If yes, that day qualifies.
# 
# Let's check each day: is there a valid schedule where at most 2 batches are on that day?

days_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
qualifying_days = []

for d in range(5):
    solver = Solver()
    
    day_O = [Int(f'day_O_{i}') for i in range(3)]
    day_P = [Int(f'day_P_{i}') for i in range(3)]
    day_S = [Int(f'day_S_{i}') for i in range(3)]
    
    for i in range(3):
        solver.add(And(day_O[i] >= 0, day_O[i] <= 4))
        solver.add(And(day_P[i] >= 0, day_P[i] <= 4))
        solver.add(And(day_S[i] >= 0, day_S[i] <= 4))
    
    solver.add(Distinct(day_O))
    solver.add(Distinct(day_P))
    solver.add(Distinct(day_S))
    
    solver.add(Or([day_O[i] == 0 for i in range(3)] +
                  [day_P[i] == 0 for i in range(3)] +
                  [day_S[i] == 0 for i in range(3)]))
    
    solver.add(day_O[1] == day_P[0])
    solver.add(day_S[1] == 3)
    
    # Constraint: at most 2 batches on day d
    batches_on_d = Sum([If(day_O[i] == d, 1, 0) for i in range(3)] +
                       [If(day_P[i] == d, 1, 0) for i in range(3)] +
                       [If(day_S[i] == d, 1, 0) for i in range(3)])
    solver.add(batches_on_d <= 2)
    
    if solver.check() == sat:
        m = solver.model()
        print(f"Day {d} ({days_names[d]}): possible to have <=2 batches")
        # Print the schedule
        for kind, arr in [("Oatmeal", day_O), ("Peanut Butter", day_P), ("Sugar", day_S)]:
            vals = [m.eval(arr[i]).as_long() for i in range(3)]
            print(f"  {kind}: {vals}")
        qualifying_days.append(d)
    else:
        print(f"Day {d} ({days_names[d]}): NOT possible to have <=2 batches")

print(f"\nQualifying days: {qualifying_days}")
print(f"Count: {len(qualifying_days)}")

count = len(qualifying_days)
found_options = []
for letter, expected_count in [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
    if count == expected_count:
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