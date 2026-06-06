from z3 import *

solver = Solver()

# Problem data
persons = ['Alice','Bob','Carol','Dave']
color = {p: Int(f'color_{p}') for p in persons}
pet = {p: Int(f'pet_{p}') for p in persons}
house = {p: Int(f'house_{p}') for p in persons}

# Domains
for p in persons:
    solver.add(color[p] >= 0, color[p] <= 3)
    solver.add(pet[p] >= 0, pet[p] <= 3)
    solver.add(house[p] >= 1, house[p] <= 4)

# AllDifferent
solver.add(Distinct([color[p] for p in persons]))
solver.add(Distinct([pet[p] for p in persons]))
solver.add(Distinct([house[p] for p in persons]))

# Constants for colors, pets
red, blue, green, yellow = 0, 1, 2, 3
cat, dog, bird, fish = 0, 1, 2, 3

# Clues
solver.add(house['Alice'] == 1)  # clue 4
for p in persons:
    solver.add(Implies(color[p] == red, house[p] == 2))  # clue 5
solver.add(pet['Bob'] == cat)  # clue 6
solver.add(color['Carol'] == blue)  # clue 7
for p in persons:
    solver.add(Implies(color[p] == yellow, pet[p] == fish))  # clue 8
for p in persons:
    solver.add(Implies(color[p] == green, house[p] == 4))  # clue 9
solver.add(pet['Dave'] == dog)  # clue 10
solver.add(pet['Alice'] != bird)  # clue 11

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    print("STATUS: sat")
    m = solver.model()
    color_names = ["Red","Blue","Green","Yellow"]
    pet_names = ["Cat","Dog","Bird","Fish"]
    for p in persons:
        c_idx = int(m[color[p]])
        p_idx = int(m[pet[p]])
        h_idx = int(m[house[p]])
        print(f"{p} color = {color_names[c_idx]}")
        print(f"{p} pet = {pet_names[p_idx]}")
        print(f"{p} house = {h_idx}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")