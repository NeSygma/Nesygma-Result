from z3 import *

# Declare variables for each cargo type (bay number)
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

solver = Solver()

# All variables are between 1 and 6
solver.add(And(1 <= fuel, fuel <= 6))
solver.add(And(1 <= grain, grain <= 6))
solver.add(And(1 <= livestock, livestock <= 6))
solver.add(And(1 <= machinery, machinery <= 6))
solver.add(And(1 <= produce, produce <= 6))
solver.add(And(1 <= textiles, textiles <= 6))

# All distinct
solver.add(Distinct([fuel, grain, livestock, machinery, produce, textiles]))

# Given constraints
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Or(produce - textiles == 1, textiles - produce == 1))  # next to each other

# Additional given: bay 4 is holding produce
solver.add(produce == 4)

# Enumerate all solutions and collect possible cargo types per bay
bay_possible = {i: set() for i in range(1, 7)}  # bay number -> set of cargo types

# We'll also collect all solutions to count determined bays
solutions = []

while solver.check() == sat:
    model = solver.model()
    # Get assignment for each cargo type, converting to Python int
    assign = {
        'fuel': int(model.eval(fuel, model_completion=True).as_long()),
        'grain': int(model.eval(grain, model_completion=True).as_long()),
        'livestock': int(model.eval(livestock, model_completion=True).as_long()),
        'machinery': int(model.eval(machinery, model_completion=True).as_long()),
        'produce': int(model.eval(produce, model_completion=True).as_long()),
        'textiles': int(model.eval(textiles, model_completion=True).as_long()),
    }
    solutions.append(assign)
    # For each bay number, add the cargo type assigned to it
    for cargo, bay in assign.items():
        bay_possible[bay].add(cargo)
    
    # Blocking clause: at least one variable differs from its model value
    blocking_clause = Or([
        fuel != model.eval(fuel, model_completion=True),
        grain != model.eval(grain, model_completion=True),
        livestock != model.eval(livestock, model_completion=True),
        machinery != model.eval(machinery, model_completion=True),
        produce != model.eval(produce, model_completion=True),
        textiles != model.eval(textiles, model_completion=True),
    ])
    solver.add(blocking_clause)

print(f"Total solutions found: {len(solutions)}")
print("Possible assignments per bay:")
for bay in range(1, 7):
    print(f"Bay {bay}: {bay_possible[bay]}")

# Count how many bays have exactly one possible cargo type
determined_bays = 0
for bay in range(1, 7):
    if len(bay_possible[bay]) == 1:
        determined_bays += 1

print(f"Determined bays: {determined_bays}")

# Map to answer choices
answer_map = {
    2: 'A',
    3: 'B',
    4: 'C',
    5: 'D',
    6: 'E'
}

if determined_bays in answer_map:
    answer_letter = answer_map[determined_bays]
    print(f"answer:{answer_letter}")
else:
    print("answer:unknown")