from z3 import *

# We have 6 bays, each gets a cargo type.
# Let's use a different encoding: for each bay 1..6, what cargo is there?
# cargo types: 0=fuel, 1=grain, 2=livestock, 3=machinery, 4=produce, 5=textiles

cargo_names = ["fuel", "grain", "livestock", "machinery", "produce", "textiles"]

# bay[i] = cargo type at bay i (1-indexed)
bay = [Int(f"bay_{i}") for i in range(1, 7)]

solver = Solver()

# Each bay has a cargo type 0..5
for i in range(6):
    solver.add(bay[i] >= 0, bay[i] <= 5)

# All bays have distinct cargo types
solver.add(Distinct(bay))

# grain (1) > livestock (2) in bay numbers
# grain bay number > livestock bay number
# grain is at bay[i] where bay[i] == 1, livestock at bay[j] where bay[j] == 2, and i+1 > j+1
# So: position_of_grain > position_of_livestock
# position_of_grain = index i where bay[i] == 1
# We can use: Sum([If(bay[i] == 1, i+1, 0) for i in range(6)]) is the bay number of grain
grain_pos = Sum([If(bay[i] == 1, i+1, 0) for i in range(6)])
livestock_pos = Sum([If(bay[i] == 2, i+1, 0) for i in range(6)])
textiles_pos = Sum([If(bay[i] == 5, i+1, 0) for i in range(6)])
produce_pos = Sum([If(bay[i] == 4, i+1, 0) for i in range(6)])
fuel_pos = Sum([If(bay[i] == 0, i+1, 0) for i in range(6)])
machinery_pos = Sum([If(bay[i] == 3, i+1, 0) for i in range(6)])

# 1. grain > livestock
solver.add(grain_pos > livestock_pos)

# 2. livestock > textiles
solver.add(livestock_pos > textiles_pos)

# 3. produce > fuel
solver.add(produce_pos > fuel_pos)

# 4. textiles is next to produce: |textiles_pos - produce_pos| == 1
solver.add(Or(textiles_pos == produce_pos + 1, textiles_pos == produce_pos - 1))

# Additional: exactly one bay between machinery and grain: |machinery_pos - grain_pos| == 2
solver.add(Or(machinery_pos == grain_pos + 2, machinery_pos == grain_pos - 2))

# Enumerate all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = tuple(m.eval(bay[i]).as_long() for i in range(6))
    solutions.append(sol)
    # Block this solution
    solver.add(Or([bay[i] != m.eval(bay[i]).as_long() for i in range(6)]))

print(f"Total solutions: {len(solutions)}")
for idx, sol in enumerate(solutions):
    print(f"Solution {idx+1}: ", end="")
    for i in range(6):
        print(f"Bay {i+1}: {cargo_names[sol[i]]}", end=", ")
    print()

# Determine fixed bays
fixed_count = 0
for i in range(6):
    types_at_bay = set(sol[i] for sol in solutions)
    if len(types_at_bay) == 1:
        fixed_count += 1
        print(f"Bay {i+1} is fixed: {cargo_names[list(types_at_bay)[0]]}")
    else:
        print(f"Bay {i+1} is NOT fixed: {[cargo_names[t] for t in types_at_bay]}")

print(f"Number of fixed bays: {fixed_count}")

# Now evaluate answer choices
# The answer choices are: A: two, B: three, C: four, D: five, E: six
# We just need to check which one matches fixed_count
# Since fixed_count is a concrete number, we can directly compare

if fixed_count == 2:
    print("STATUS: sat")
    print("answer:A")
elif fixed_count == 3:
    print("STATUS: sat")
    print("answer:B")
elif fixed_count == 4:
    print("STATUS: sat")
    print("answer:C")
elif fixed_count == 5:
    print("STATUS: sat")
    print("answer:D")
elif fixed_count == 6:
    print("STATUS: sat")
    print("answer:E")
else:
    print("STATUS: unsat")
    print("Refine: No matching option")