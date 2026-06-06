from z3 import *

solver = Solver()

# Days: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday
# Cookie types: 0=Oatmeal, 1=Peanut Butter, 2=Sugar
# Batches: 1st, 2nd, 3rd for each type

# Variables: batch[type][batch_num] = day (0-4)
oat = [Int(f'oat_{i}') for i in range(3)]  # oatmeal batches 1,2,3
pb = [Int(f'pb_{i}') for i in range(3)]    # peanut butter batches 1,2,3
sug = [Int(f'sug_{i}') for i in range(3)]  # sugar batches 1,2,3

# Each batch is made on a day 0-4 (Monday-Friday)
for b in oat + pb + sug:
    solver.add(b >= 0, b <= 4)

# No two batches of the same kind on the same day
solver.add(Distinct(oat))
solver.add(Distinct(pb))
solver.add(Distinct(sug))

# At least one batch on Monday (day 0)
all_batches = oat + pb + sug
solver.add(Or([b == 0 for b in all_batches]))

# The second batch of oatmeal is made on the same day as the first batch of peanut butter
solver.add(oat[1] == pb[0])

# The second batch of sugar cookies is made on Thursday (day 3)
solver.add(sug[1] == 3)

# No batch on Wednesday (day 2)
for b in all_batches:
    solver.add(b != 2)

# Check satisfiability first
result = solver.check()
print(f"Base constraints check: {result}")

if result == sat:
    m = solver.model()
    print("Sample model:")
    for i in range(3):
        print(f"  oat[{i}] = {m[oat[i]]}")
    for i in range(3):
        print(f"  pb[{i}] = {m[pb[i]]}")
    for i in range(3):
        print(f"  sug[{i}] = {m[sug[i]]}")
    
    # Count batches per day
    for d in range(5):
        day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][d]
        count = sum(1 for b in all_batches if m.evaluate(b == d))
        print(f"  {day_name}: {count} batches")

# Now enumerate ALL models to check which options hold universally
# We'll use the blocking clause approach
all_models = []
temp_solver = Solver()
for b in oat + pb + sug:
    temp_solver.add(b >= 0, b <= 4)
temp_solver.add(Distinct(oat))
temp_solver.add(Distinct(pb))
temp_solver.add(Distinct(sug))
temp_solver.add(Or([b == 0 for b in all_batches]))
temp_solver.add(oat[1] == pb[0])
temp_solver.add(sug[1] == 3)
for b in all_batches:
    temp_solver.add(b != 2)

while temp_solver.check() == sat:
    m = temp_solver.model()
    model_vals = {}
    for b in all_batches:
        model_vals[str(b)] = m.evaluate(b).as_long()
    all_models.append(model_vals)
    # Block this model
    temp_solver.add(Or([b != m.evaluate(b) for b in all_batches]))

print(f"\nTotal models found: {len(all_models)}")

# For each model, compute counts per day and check options
option_holds = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
for model_vals in all_models:
    counts = [0]*5
    for v in model_vals.values():
        counts[v] += 1
    
    if counts[1] == 3:
        option_holds["A"] += 1
    if counts[4] == 3:
        option_holds["B"] += 1
    if counts[0] >= 2:
        option_holds["C"] += 1
    if counts[3] >= 2:
        option_holds["D"] += 1
    if counts[0] < counts[1]:
        option_holds["E"] += 1

print("\nOption analysis (how many models each holds in):")
for letter in ["A", "B", "C", "D", "E"]:
    print(f"  Option {letter}: {option_holds[letter]}/{len(all_models)} models")

must_be_true = [letter for letter in ["A", "B", "C", "D", "E"] if option_holds[letter] == len(all_models)]
print(f"\nMust be true (holds in ALL models): {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")