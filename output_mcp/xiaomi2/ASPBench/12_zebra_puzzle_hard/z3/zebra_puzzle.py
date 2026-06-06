from z3 import *

solver = Solver()

N = 8  # suites 1..8 (0-indexed as 0..7)

# Attribute mappings (for readability in output)
nat_names = ["American", "Brazilian", "Canadian", "Dutch", "Egyptian", "French", "German", "Hungarian"]
prof_names = ["Architect", "Biologist", "Chemist", "Doctor", "Engineer", "Lawyer", "Musician", "Pilot"]
car_names = ["Audi", "BMW", "Ford", "Honda", "Mercedes", "Nissan", "Toyota", "Volvo"]
drink_names = ["Coffee", "Juice", "Milk", "Soda", "Tea", "Water", "Wine", "Whiskey"]
music_names = ["Blues", "Classical", "Folk", "Jazz", "Pop", "Rap", "Reggae", "Rock"]
pet_names = ["Cat", "Dog", "Fish", "Hamster", "Lizard", "Parrot", "Rabbit", "Snake"]
dest_names = ["Bali", "Dubai", "London", "New York", "Paris", "Rome", "Sydney", "Tokyo"]

# Create variables: for each suite i, 7 attributes
nat = [Int(f'nat_{i}') for i in range(N)]
prof = [Int(f'prof_{i}') for i in range(N)]
car = [Int(f'car_{i}') for i in range(N)]
drink = [Int(f'drink_{i}') for i in range(N)]
music = [Int(f'music_{i}') for i in range(N)]
pet = [Int(f'pet_{i}') for i in range(N)]
dest = [Int(f'dest_{i}') for i in range(N)]

# Domain constraints: all values in 0..7
for i in range(N):
    solver.add(nat[i] >= 0, nat[i] < 8)
    solver.add(prof[i] >= 0, prof[i] < 8)
    solver.add(car[i] >= 0, car[i] < 8)
    solver.add(drink[i] >= 0, drink[i] < 8)
    solver.add(music[i] >= 0, music[i] < 8)
    solver.add(pet[i] >= 0, pet[i] < 8)
    solver.add(dest[i] >= 0, dest[i] < 8)

# All-different constraints for each attribute across suites
solver.add(Distinct(nat))
solver.add(Distinct(prof))
solver.add(Distinct(car))
solver.add(Distinct(drink))
solver.add(Distinct(music))
solver.add(Distinct(pet))
solver.add(Distinct(dest))

# Constraint 1: Suite 4 (index 3) drinks Milk (2)
solver.add(drink[3] == 2)

# Constraint 2: Hungarian (7) in suite 4 (index 3)
solver.add(nat[3] == 7)

# Constraint 3: American (0) is Lawyer (5)
for i in range(N):
    solver.add(Implies(nat[i] == 0, prof[i] == 5))
    solver.add(Implies(prof[i] == 5, nat[i] == 0))

# Constraint 4: BMW (1) driver is Biologist (1)
for i in range(N):
    solver.add(Implies(car[i] == 1, prof[i] == 1))
    solver.add(Implies(prof[i] == 1, car[i] == 1))

# Constraint 5: Canadian (2) owns Snake (7)
for i in range(N):
    solver.add(Implies(nat[i] == 2, pet[i] == 7))
    solver.add(Implies(pet[i] == 7, nat[i] == 2))

# Constraint 6: Classical (1) music listener drives Audi (0)
for i in range(N):
    solver.add(Implies(music[i] == 1, car[i] == 0))
    solver.add(Implies(car[i] == 0, music[i] == 1))

# Constraint 7: German (6) drinks Coffee (0)
for i in range(N):
    solver.add(Implies(nat[i] == 6, drink[i] == 0))
    solver.add(Implies(drink[i] == 0, nat[i] == 6))

# Constraint 8: Tokyo (7) destination is Chemist (2)
for i in range(N):
    solver.add(Implies(dest[i] == 7, prof[i] == 2))
    solver.add(Implies(prof[i] == 2, dest[i] == 7))

# Constraint 9: Engineer (4) immediately left of Lawyer (5)
solver.add(Or([And(prof[i] == 4, prof[i+1] == 5) for i in range(N-1)]))

# Constraint 10: Dog (1) owner next to Volvo (7) driver
adj_pairs_10 = []
for i in range(N):
    for j in range(N):
        if abs(i - j) == 1:
            adj_pairs_10.append(And(pet[i] == 1, car[j] == 7))
solver.add(Or(adj_pairs_10))

# Constraint 11: Rock (7) listener next to Pop (4) listener
adj_pairs_11 = []
for i in range(N):
    for j in range(N):
        if abs(i - j) == 1:
            adj_pairs_11.append(And(music[i] == 7, music[j] == 4))
solver.add(Or(adj_pairs_11))

# Constraint 12: Paris (4) destination next to Fish (2) owner
adj_pairs_12 = []
for i in range(N):
    for j in range(N):
        if abs(i - j) == 1:
            adj_pairs_12.append(And(dest[i] == 4, pet[j] == 2))
solver.add(Or(adj_pairs_12))

# Constraint 13: Pilot (7) in even-numbered suite (1-indexed: 2,4,6,8 -> 0-indexed: 1,3,5,7)
for i in range(N):
    solver.add(Implies(prof[i] == 7, (i + 1) % 2 == 0))

# Constraint 14: Wine (6) drinker's suite is to the right of Coffee (0) drinker's suite
for i in range(N):
    for j in range(N):
        solver.add(Implies(And(drink[i] == 6, drink[j] == 0), i > j))

# Constraint 15: Ford (2) driver has a neighbor who drinks Tea (4)
for i in range(N):
    neighbors = []
    if i - 1 >= 0:
        neighbors.append(drink[i-1] == 4)
    if i + 1 < N:
        neighbors.append(drink[i+1] == 4)
    if neighbors:
        solver.add(Implies(car[i] == 2, Or(neighbors)))

# Constraint 16: Nissan (5) driver not in suite 1 (index 0) or suite 8 (index 7)
solver.add(car[0] != 5)
solver.add(car[7] != 5)

# Constraint 17: Jazz (3) listener's suite number < Blues (0) listener's suite number (1-indexed)
for i in range(N):
    for j in range(N):
        solver.add(Implies(And(music[i] == 3, music[j] == 0), (i + 1) < (j + 1)))

# Constraint 18: Dutch (3) in suite 1 (index 0)
solver.add(nat[0] == 3)

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    # Build solution
    solution = []
    for i in range(N):
        suite = {
            "suite": i + 1,
            "nationality": nat_names[m.evaluate(nat[i]).as_long()],
            "profession": prof_names[m.evaluate(prof[i]).as_long()],
            "car": car_names[m.evaluate(car[i]).as_long()],
            "drink": drink_names[m.evaluate(drink[i]).as_long()],
            "music": music_names[m.evaluate(music[i]).as_long()],
            "pet": pet_names[m.evaluate(pet[i]).as_long()],
            "destination": dest_names[m.evaluate(dest[i]).as_long()],
        }
        solution.append(suite)
    
    # Print solution
    for s in solution:
        print(f"Suite {s['suite']}: {s['nationality']}, {s['profession']}, {s['car']}, {s['drink']}, {s['music']}, {s['pet']}, {s['destination']}")
    
    # Find lizard owner
    for s in solution:
        if s['pet'] == 'Lizard':
            print(f"Lizard owner nationality: {s['nationality']}")
            break

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")