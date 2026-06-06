from z3 import *

solver = Solver()

# People
people = ["Alice", "Bob", "Carol", "Dave"]
P = len(people)

# Houses: 1,2,3,4
house = {p: Int(f"house_{p}") for p in people}
for p in people:
    solver.add(house[p] >= 1, house[p] <= 4)
solver.add(Distinct([house[p] for p in people]))

# Colors: 0=Red, 1=Blue, 2=Green, 3=Yellow
color_names = ["Red", "Blue", "Green", "Yellow"]
color = {p: Int(f"color_{p}") for p in people}
for p in people:
    solver.add(color[p] >= 0, color[p] <= 3)
solver.add(Distinct([color[p] for p in people]))

# Pets: 0=Cat, 1=Dog, 2=Bird, 3=Fish
pet_names = ["Cat", "Dog", "Bird", "Fish"]
pet = {p: Int(f"pet_{p}") for p in people}
for p in people:
    solver.add(pet[p] >= 0, pet[p] <= 3)
solver.add(Distinct([pet[p] for p in people]))

# Constraint 4: Alice must live in house 1
solver.add(house["Alice"] == 1)

# Constraint 5: The person with the red color must live in house 2
# red = 0
solver.add(Or([And(color[p] == 0, house[p] == 2) for p in people]))

# Constraint 6: Bob must have a cat (cat = 0)
solver.add(pet["Bob"] == 0)

# Constraint 7: Carol's favorite color must be blue (blue = 1)
solver.add(color["Carol"] == 1)

# Constraint 8: The person with the yellow color must have a fish (yellow = 3, fish = 3)
solver.add(Or([And(color[p] == 3, pet[p] == 3) for p in people]))

# Constraint 9: The person with the green color must live in house 4 (green = 2)
solver.add(Or([And(color[p] == 2, house[p] == 4) for p in people]))

# Constraint 10: Dave must have the dog (dog = 1)
solver.add(pet["Dave"] == 1)

# Constraint 11: Alice cannot have the bird (bird = 2)
solver.add(pet["Alice"] != 2)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Complete Assignment:")
    for p in people:
        h = m[house[p]].as_long()
        c_idx = m[color[p]].as_long()
        p_idx = m[pet[p]].as_long()
        print(f"{p}: House {h}, Color {color_names[c_idx]}, Pet {pet_names[p_idx]}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")