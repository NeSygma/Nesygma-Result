from z3 import *

# Define the options for each attribute
nationalities = ["American", "Brazilian", "Canadian", "Dutch", "Egyptian", "French", "German", "Hungarian"]
professions = ["Architect", "Biologist", "Chemist", "Doctor", "Engineer", "Lawyer", "Musician", "Pilot"]
car_brands = ["Audi", "BMW", "Ford", "Honda", "Mercedes", "Nissan", "Toyota", "Volvo"]
drinks = ["Coffee", "Juice", "Milk", "Soda", "Tea", "Water", "Wine", "Whiskey"]
music_genres = ["Blues", "Classical", "Folk", "Jazz", "Pop", "Rap", "Reggae", "Rock"]
pets = ["Cat", "Dog", "Fish", "Hamster", "Lizard", "Parrot", "Rabbit", "Snake"]
destinations = ["Bali", "Dubai", "London", "New York", "Paris", "Rome", "Sydney", "Tokyo"]

# Create a solver
solver = Solver()

# Declare symbolic variables for each suite and attribute
# We'll use Int variables to represent indices into the option lists
nationality = [Int(f"nationality_{i}") for i in range(8)]
profession = [Int(f"profession_{i}") for i in range(8)]
car = [Int(f"car_{i}") for i in range(8)]
drink = [Int(f"drink_{i}") for i in range(8)]
music = [Int(f"music_{i}") for i in range(8)]
pet = [Int(f"pet_{i}") for i in range(8)]
destination = [Int(f"destination_{i}") for i in range(8)]

# Helper function to ensure all values in a list are distinct
def all_distinct(lst):
    return Distinct(lst)

# Add constraints for each attribute to be a permutation of 0-7
for attr in [nationality, profession, car, drink, music, pet, destination]:
    solver.add(all_distinct(attr))
    for i in range(8):
        solver.add(attr[i] >= 0, attr[i] < 8)

# Constraint 1: Suite #4 drinks Milk
# Suite indices are 0-based, so suite 4 is index 3
solver.add(drink[3] == drinks.index("Milk"))

# Constraint 2: Hungarian lives in suite #4
solver.add(nationality[3] == nationalities.index("Hungarian"))

# Constraint 3: American is a Lawyer
# Find the suite with American nationality and ensure it's a Lawyer
american_suite = Int("american_suite")
solver.add(Or([nationality[i] == nationalities.index("American") for i in range(8)]))
for i in range(8):
    solver.add(Implies(nationality[i] == nationalities.index("American"), profession[i] == professions.index("Lawyer")))

# Constraint 4: BMW driver is a Biologist
solver.add(Or([And(car[i] == car_brands.index("BMW"), profession[i] == professions.index("Biologist")) for i in range(8)]))

# Constraint 5: Canadian owns a Snake
solver.add(Or([And(nationality[i] == nationalities.index("Canadian"), pet[i] == pets.index("Snake")) for i in range(8)]))

# Constraint 6: Classical music listener drives an Audi
solver.add(Or([And(music[i] == music_genres.index("Classical"), car[i] == car_brands.index("Audi")) for i in range(8)]))

# Constraint 7: German drinks Coffee
solver.add(Or([And(nationality[i] == nationalities.index("German"), drink[i] == drinks.index("Coffee")) for i in range(8)]))

# Constraint 8: Tokyo destination is a Chemist
solver.add(Or([And(destination[i] == destinations.index("Tokyo"), profession[i] == professions.index("Chemist")) for i in range(8)]))

# Constraint 9: Engineer's suite is immediately to the left of the Lawyer's suite
for i in range(7):
    solver.add(Implies(profession[i] == professions.index("Engineer"), profession[i+1] == professions.index("Lawyer")))

# Constraint 10: Dog owner lives next to the Volvo driver
for i in range(7):
    solver.add(Implies(pet[i] == pets.index("Dog"), Or(car[i+1] == car_brands.index("Volvo"), i > 0 and car[i-1] == car_brands.index("Volvo"))))
for i in range(1, 8):
    solver.add(Implies(pet[i] == pets.index("Dog"), Or(car[i-1] == car_brands.index("Volvo"), i < 7 and car[i+1] == car_brands.index("Volvo"))))

# Constraint 11: Rock music listener lives next to the Pop music listener
for i in range(7):
    solver.add(Implies(music[i] == music_genres.index("Rock"), Or(music[i+1] == music_genres.index("Pop"), i > 0 and music[i-1] == music_genres.index("Pop"))))
for i in range(1, 8):
    solver.add(Implies(music[i] == music_genres.index("Rock"), Or(music[i-1] == music_genres.index("Pop"), i < 7 and music[i+1] == music_genres.index("Pop"))))

# Constraint 12: Paris destination lives next to the Fish owner
for i in range(7):
    solver.add(Implies(destination[i] == destinations.index("Paris"), Or(pet[i+1] == pets.index("Fish"), i > 0 and pet[i-1] == pets.index("Fish"))))
for i in range(1, 8):
    solver.add(Implies(destination[i] == destinations.index("Paris"), Or(pet[i-1] == pets.index("Fish"), i < 7 and pet[i+1] == pets.index("Fish"))))

# Constraint 13: Pilot lives in an even-numbered suite (1-based: 2,4,6,8 -> 0-based: 1,3,5,7)
solver.add(Or([profession[i] == professions.index("Pilot") for i in [1, 3, 5, 7]]))

# Constraint 14: Wine drinker's suite is to the right of the Coffee drinker's suite
coffee_suite = Int("coffee_suite")
wine_suite = Int("wine_suite")
solver.add(Or([drink[i] == drinks.index("Coffee") for i in range(8)]))
solver.add(Or([drink[i] == drinks.index("Wine") for i in range(8)]))
for i in range(8):
    for j in range(8):
        if i < j:
            solver.add(Implies(And(drink[i] == drinks.index("Coffee"), drink[j] == drinks.index("Wine")), j > i))

# Constraint 15: Ford driver has a neighbor who drinks Tea
for i in range(7):
    solver.add(Implies(car[i] == car_brands.index("Ford"), Or(drink[i+1] == drinks.index("Tea"), i > 0 and drink[i-1] == drinks.index("Tea"))))
for i in range(1, 8):
    solver.add(Implies(car[i] == car_brands.index("Ford"), Or(drink[i-1] == drinks.index("Tea"), i < 7 and drink[i+1] == drinks.index("Tea"))))

# Constraint 16: Nissan driver does not live in suite #1 or #8 (0-based: 0 or 7)
solver.add(Not(car[0] == car_brands.index("Nissan")))
solver.add(Not(car[7] == car_brands.index("Nissan")))

# Constraint 17: Jazz listener's suite number is less than the Blues listener's suite number
solver.add(Or([music[i] == music_genres.index("Jazz") for i in range(8)]))
solver.add(Or([music[i] == music_genres.index("Blues") for i in range(8)]))
for i in range(8):
    for j in range(8):
        if i < j:
            solver.add(Implies(And(music[i] == music_genres.index("Jazz"), music[j] == music_genres.index("Blues")), i < j))

# Constraint 18: Dutch person lives in suite #1 (0-based index 0)
solver.add(nationality[0] == nationalities.index("Dutch"))

# Check if the problem is satisfiable
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract the solution
    solution = []
    for i in range(8):
        suite = {
            "suite": i + 1,
            "nationality": nationalities[model[nationality[i]].as_long()],
            "profession": professions[model[profession[i]].as_long()],
            "car": car_brands[model[car[i]].as_long()],
            "drink": drinks[model[drink[i]].as_long()],
            "music": music_genres[model[music[i]].as_long()],
            "pet": pets[model[pet[i]].as_long()],
            "destination": destinations[model[destination[i]].as_long()]
        }
        solution.append(suite)
    
    # Print the solution
    for suite in solution:
        print(f"Suite {suite['suite']}: Nationality={suite['nationality']}, Profession={suite['profession']}, Car={suite['car']}, Drink={suite['drink']}, Music={suite['music']}, Pet={suite['pet']}, Destination={suite['destination']}")
    
    # Find the lizard owner's nationality
    lizard_owner = None
    for suite in solution:
        if suite['pet'] == "Lizard":
            lizard_owner = suite['nationality']
            break
    
    if lizard_owner:
        print(f"lizard_owner: {lizard_owner}")
    else:
        print("lizard_owner: Not found")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")