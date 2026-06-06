from z3 import *

# Domains
nationalities = ["American", "Brazilian", "Canadian", "Dutch", "Egyptian", "French", "German", "Hungarian"]
professions = ["Architect", "Biologist", "Chemist", "Doctor", "Engineer", "Lawyer", "Musician", "Pilot"]
car_brands = ["Audi", "BMW", "Ford", "Honda", "Mercedes", "Nissan", "Toyota", "Volvo"]
drinks = ["Coffee", "Juice", "Milk", "Soda", "Tea", "Water", "Wine", "Whiskey"]
music_genres = ["Blues", "Classical", "Folk", "Jazz", "Pop", "Rap", "Reggae", "Rock"]
pets = ["Cat", "Dog", "Fish", "Hamster", "Lizard", "Parrot", "Rabbit", "Snake"]
destinations = ["Bali", "Dubai", "London", "New York", "Paris", "Rome", "Sydney", "Tokyo"]

# Create integer variables for each attribute per suite (0-indexed suites 0..7)
nationality = [Int(f"nationality_{i}") for i in range(8)]
profession = [Int(f"profession_{i}") for i in range(8)]
car = [Int(f"car_{i}") for i in range(8)]
drink = [Int(f"drink_{i}") for i in range(8)]
music = [Int(f"music_{i}") for i in range(8)]
pet = [Int(f"pet_{i}") for i in range(8)]
destination = [Int(f"destination_{i}") for i in range(8)]

solver = Solver()

# Each attribute variable must be in range 0..7
for i in range(8):
    solver.add(nationality[i] >= 0, nationality[i] <= 7)
    solver.add(profession[i] >= 0, profession[i] <= 7)
    solver.add(car[i] >= 0, car[i] <= 7)
    solver.add(drink[i] >= 0, drink[i] <= 7)
    solver.add(music[i] >= 0, music[i] <= 7)
    solver.add(pet[i] >= 0, pet[i] <= 7)
    solver.add(destination[i] >= 0, destination[i] <= 7)

# All values in each attribute array must be distinct
solver.add(Distinct(nationality))
solver.add(Distinct(profession))
solver.add(Distinct(car))
solver.add(Distinct(drink))
solver.add(Distinct(music))
solver.add(Distinct(pet))
solver.add(Distinct(destination))

# Helper mapping from string to index
def idx(lst, val):
    return lst.index(val)

# Constraint 1: The person in suite #4 drinks Milk (suite #4 is index 3)
solver.add(drink[3] == idx(drinks, "Milk"))

# Constraint 2: The Hungarian lives in suite #4
solver.add(nationality[3] == idx(nationalities, "Hungarian"))

# Constraint 3: The American is a Lawyer
solver.add(Or([And(nationality[i] == idx(nationalities, "American"),
                   profession[i] == idx(professions, "Lawyer"))
               for i in range(8)]))

# Constraint 4: The person who drives a BMW is a Biologist
solver.add(Or([And(car[i] == idx(car_brands, "BMW"),
                   profession[i] == idx(professions, "Biologist"))
               for i in range(8)]))

# Constraint 5: The Canadian owns a Snake
solver.add(Or([And(nationality[i] == idx(nationalities, "Canadian"),
                   pet[i] == idx(pets, "Snake"))
               for i in range(8)]))

# Constraint 6: The person who listens to Classical music drives an Audi
solver.add(Or([And(music[i] == idx(music_genres, "Classical"),
                   car[i] == idx(car_brands, "Audi"))
               for i in range(8)]))

# Constraint 7: The German drinks Coffee
solver.add(Or([And(nationality[i] == idx(nationalities, "German"),
                   drink[i] == idx(drinks, "Coffee"))
               for i in range(8)]))

# Constraint 8: The person going to Tokyo is a Chemist
solver.add(Or([And(destination[i] == idx(destinations, "Tokyo"),
                   profession[i] == idx(professions, "Chemist"))
               for i in range(8)]))

# Constraint 9: The Engineer's suite is immediately to the left of the Lawyer's suite
for i in range(7):
    solver.add(Implies(profession[i] == idx(professions, "Engineer"),
                       profession[i+1] == idx(professions, "Lawyer")))

# Constraint 10: The Dog owner lives next to the Volvo driver
# Use separate constraints for each possible position
for i in range(8):
    dog_cond = pet[i] == idx(pets, "Dog")
    # Build neighbor conditions safely
    neighbor_conditions = []
    if i > 0:
        neighbor_conditions.append(car[i-1] == idx(car_brands, "Volvo"))
    if i < 7:
        neighbor_conditions.append(car[i+1] == idx(car_brands, "Volvo"))
    if neighbor_conditions:
        solver.add(Implies(dog_cond, Or(neighbor_conditions)))

# Constraint 11: The Rock music listener lives next to the Pop music listener
for i in range(8):
    rock_cond = music[i] == idx(music_genres, "Rock")
    neighbor_conditions = []
    if i > 0:
        neighbor_conditions.append(music[i-1] == idx(music_genres, "Pop"))
    if i < 7:
        neighbor_conditions.append(music[i+1] == idx(music_genres, "Pop"))
    if neighbor_conditions:
        solver.add(Implies(rock_cond, Or(neighbor_conditions)))

# Constraint 12: The person going to Paris lives next to the Fish owner
for i in range(8):
    paris_cond = destination[i] == idx(destinations, "Paris")
    neighbor_conditions = []
    if i > 0:
        neighbor_conditions.append(pet[i-1] == idx(pets, "Fish"))
    if i < 7:
        neighbor_conditions.append(pet[i+1] == idx(pets, "Fish"))
    if neighbor_conditions:
        solver.add(Implies(paris_cond, Or(neighbor_conditions)))

# Constraint 13: The Pilot lives in an even-numbered suite
# Suite numbers 1..8, even: 2,4,6,8 -> indices 1,3,5,7
for i in range(8):
    if (i+1) % 2 == 0:  # even suite number
        solver.add(profession[i] == idx(professions, "Pilot"))
    else:
        solver.add(profession[i] != idx(professions, "Pilot"))

# Constraint 14: The Wine drinker's suite is to the right of the Coffee drinker's suite
for i in range(8):
    coffee_cond = drink[i] == idx(drinks, "Coffee")
    wine_right = Or([drink[j] == idx(drinks, "Wine") for j in range(i+1, 8)])
    solver.add(Implies(coffee_cond, wine_right))

# Constraint 15: The Ford driver has a neighbor who drinks Tea
for i in range(8):
    ford_cond = car[i] == idx(car_brands, "Ford")
    neighbor_conditions = []
    if i > 0:
        neighbor_conditions.append(drink[i-1] == idx(drinks, "Tea"))
    if i < 7:
        neighbor_conditions.append(drink[i+1] == idx(drinks, "Tea"))
    if neighbor_conditions:
        solver.add(Implies(ford_cond, Or(neighbor_conditions)))

# Constraint 16: The Nissan driver does not live in suite #1 or #8
solver.add(car[0] != idx(car_brands, "Nissan"))
solver.add(car[7] != idx(car_brands, "Nissan"))

# Constraint 17: The Jazz listener's suite number is less than the Blues listener's suite number
for i in range(8):
    jazz_cond = music[i] == idx(music_genres, "Jazz")
    blues_right = Or([music[j] == idx(music_genres, "Blues") for j in range(i+1, 8)])
    solver.add(Implies(jazz_cond, blues_right))

# Constraint 18: The Dutch person lives in suite #1
solver.add(nationality[0] == idx(nationalities, "Dutch"))

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("\nSolution:")
    for i in range(8):
        suite_num = i + 1
        nat = nationalities[m.evaluate(nationality[i]).as_long()]
        prof = professions[m.evaluate(profession[i]).as_long()]
        car_br = car_brands[m.evaluate(car[i]).as_long()]
        dr = drinks[m.evaluate(drink[i]).as_long()]
        mus = music_genres[m.evaluate(music[i]).as_long()]
        pet_val = pets[m.evaluate(pet[i]).as_long()]
        dest = destinations[m.evaluate(destination[i]).as_long()]
        print(f"Suite {suite_num}: {nat}, {prof}, {car_br}, {dr}, {mus}, {pet_val}, {dest}")
    
    # Find who owns the lizard
    for i in range(8):
        if m.evaluate(pet[i]).as_long() == idx(pets, "Lizard"):
            lizard_owner = nationalities[m.evaluate(nationality[i]).as_long()]
            print(f"\nlizard_owner: {lizard_owner}")
            break
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")