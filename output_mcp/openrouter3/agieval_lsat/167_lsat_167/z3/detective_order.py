from z3 import *

# Create solver
solver = Solver()

# Define positions for each person
Peters = Int('Peters')
Quinn = Int('Quinn')
Rovero = Int('Rovero')
Stanton = Int('Stanton')
Tao = Int('Tao')
Villas = Int('Villas')
White = Int('White')

# All positions are between 1 and 7
people = [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]
for p in people:
    solver.add(p >= 1, p <= 7)

# All positions are distinct
solver.add(Distinct(people))

# Base constraints from problem
# 1. Stanton was recruited neither immediately before nor immediately after Tao
solver.add(Not(Or(Stanton == Tao + 1, Stanton == Tao - 1)))

# 2. Quinn was recruited earlier than Rovero
solver.add(Quinn < Rovero)

# 3. Villas was recruited immediately before White
solver.add(Villas == White - 1)

# 4. Peters was recruited fourth
solver.add(Peters == 4)

# Additional constraint: White was recruited immediately before Quinn
solver.add(White == Quinn - 1)

# Now test each answer choice for position 6
# We need to find which person MUST be in position 6 in all valid models
# We'll test each option by checking if it's possible for that person NOT to be in position 6
# If it's impossible (unsat), then that person MUST be in position 6

# First, let's find all valid models to see which person is always in position 6
# We'll use a different approach: check each person's position in all models

# We'll collect all possible models (limited to avoid infinite loop)
models = []
decision_vars = [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]

# To find all solutions, we loop and 'block' the current model
while solver.check() == sat:
    m = solver.model()
    # Capture the specific values that define a 'unique' solution
    sol = {v: m.eval(v, model_completion=True) for v in decision_vars}
    models.append(sol)
    # Blocking Clause: Add a constraint that at least one variable must be different
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))
    # Limit to reasonable number of models
    if len(models) > 100:
        break

print(f"Found {len(models)} valid models")

# Now check which person is always in position 6
position_6_counts = {}
for person in decision_vars:
    position_6_counts[person] = 0

for model in models:
    for person in decision_vars:
        if model[person] == 6:
            position_6_counts[person] += 1

print("Position 6 counts:")
for person, count in position_6_counts.items():
    print(f"  {person}: {count} times")

# Determine which person must be in position 6
must_be_sixth = []
for person in decision_vars:
    if position_6_counts[person] == len(models) and len(models) > 0:
        must_be_sixth.append(person)

if len(must_be_sixth) == 1:
    person_name = str(must_be_sixth[0])
    print(f"\n{person_name} must be sixth in all models")
    
    # Map to answer choices
    answer_map = {
        'Quinn': 'A',
        'Rovero': 'B',
        'Stanton': 'C',
        'Villas': 'D',
        'White': 'E'
    }
    
    if person_name in answer_map:
        print("STATUS: sat")
        print(f"answer:{answer_map[person_name]}")
    else:
        print("STATUS: unsat")
        print("Refine: Person not in answer choices")
elif len(must_be_sixth) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple people must be sixth: {must_be_sixth}")
else:
    print("STATUS: unsat")
    print("Refine: No person must be sixth")