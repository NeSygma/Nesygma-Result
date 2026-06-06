from z3 import *

# Initialize solver
solver = Solver()

# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
days = range(5)

# Kinds of cookies
kinds = ["oatmeal", "peanut_butter", "sugar"]

# Batches: 1, 2, 3
batches = [1, 2, 3]

# Decision variables: batch_day[kind][batch] = day
batch_day = {
    kind: {batch: Int(f"{kind}_batch_{batch}") for batch in batches}
    for kind in kinds
}

# Constraint 1: No two batches of the same kind on the same day
for kind in kinds:
    solver.add(Distinct([batch_day[kind][batch] for batch in batches]))

# Constraint 2: At least one batch on Monday (day 0)
solver.add(Or([batch_day[kind][batch] == 0 for kind in kinds for batch in batches]))

# Constraint 3: The second batch of oatmeal is made on the same day as the first batch of peanut butter
solver.add(batch_day["oatmeal"][2] == batch_day["peanut_butter"][1])

# Constraint 4: The second batch of sugar cookies is made on Thursday (day 3)
solver.add(batch_day["sugar"][2] == 3)

# Condition: Exactly one batch is made on Friday (day 4)
# Count the number of batches on Friday
count_friday = Sum([If(batch_day[kind][batch] == 4, 1, 0) for kind in kinds for batch in batches])
solver.add(count_friday == 1)

# Now evaluate each option
found_options = []

# Option A: The first batch of sugar cookies is made on Monday (day 0)
solver.push()
solver.add(batch_day["sugar"][1] == 0)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The first batch of oatmeal cookies is made on Tuesday (day 1)
solver.push()
solver.add(batch_day["oatmeal"][1] == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: The third batch of oatmeal cookies is made on Friday (day 4)
solver.push()
solver.add(batch_day["oatmeal"][3] == 4)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The first batch of peanut butter cookies is made on Wednesday (day 2)
solver.push()
solver.add(batch_day["peanut_butter"][1] == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The second batch of peanut butter cookies is made on Tuesday (day 1)
solver.push()
solver.add(batch_day["peanut_butter"][2] == 1)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")