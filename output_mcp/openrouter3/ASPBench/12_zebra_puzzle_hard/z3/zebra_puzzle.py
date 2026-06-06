from z3 import *

# Create solver
solver = Solver()

# Number of suites
N = 8

# Declare variables for each attribute across suites
nationalities = [Int(f'nat_{i}') for i in range(N)]
professions = [Int(f'prof_{i}') for i in range(N)]
cars = [Int(f'car_{i}') for i in range(N)]
drinks = [Int(f'drink_{i}') for i in range(N)]
music = [Int(f'music_{i}') for i in range(N)]
pets = [Int(f'pet_{i}') for i in range(N)]
destinations = [Int(f'dest_{i}') for i in range(N)]

# Define constants for attribute values (0-7 for each category)
# Nationalities: American=0, Brazilian=1, Canadian=2, Dutch=3, Egyptian=4, French=5, German=6, Hungarian=7
# Professions: Architect=0, Biologist=1, Chemist=2, Doctor=3, Engineer=4, Lawyer=5, Musician=6, Pilot=7
# Cars: Audi=0, BMW=1, Ford=2, Honda=3, Mercedes=4, Nissan=5, Toyota=6, Volvo=7
# Drinks: Coffee=0, Juice=1, Milk=2, Soda=3, Tea=4, Water=5, Wine=6, Whiskey=7
# Music: Blues=0, Classical=1, Folk=2, Jazz=3, Pop=4, Rap=5, Reggae=6, Rock=7
# Pets: Cat=0, Dog=1, Fish=2, Hamster=3, Lizard=4, Parrot=5, Rabbit=6, Snake=7
# Destinations: Bali=0, Dubai=1, London=2, New York=3, Paris=4, Rome=5, Sydney=6, Tokyo=7

# Each attribute value must appear exactly once per category
solver.add(Distinct(nationalities))
solver.add(Distinct(professions))
solver.add(Distinct(cars))
solver.add(Distinct(drinks))
solver.add(Distinct(music))
solver.add(Distinct(pets))
solver.add(Distinct(destinations))

# All variables must be in range 0-7
for i in range(N):
    solver.add(nationalities[i] >= 0, nationalities[i] <= 7)
    solver.add(professions[i] >= 0, professions[i] <= 7)
    solver.add(cars[i] >= 0, cars[i] <= 7)
    solver.add(drinks[i] >= 0, drinks[i] <= 7)
    solver.add(music[i] >= 0, music[i] <= 7)
    solver.add(pets[i] >= 0, pets[i] <= 7)
    solver.add(destinations[i] >= 0, destinations[i] <= 7)

# Constraint 1: The person in suite #4 drinks Milk (suite index 3)
solver.add(drinks[3] == 2)  # Milk = 2

# Constraint 2: The Hungarian lives in suite #4 (suite index 3)
solver.add(nationalities[3] == 7)  # Hungarian = 7

# Constraint 3: The American is a Lawyer
# Find suite where nationality is American (0) and profession is Lawyer (5)
solver.add(Or([And(nationalities[i] == 0, professions[i] == 5) for i in range(N)]))

# Constraint 4: The person who drives a BMW is a Biologist
# Find suite where car is BMW (1) and profession is Biologist (1)
solver.add(Or([And(cars[i] == 1, professions[i] == 1) for i in range(N)]))

# Constraint 5: The Canadian owns a Snake
# Find suite where nationality is Canadian (2) and pet is Snake (7)
solver.add(Or([And(nationalities[i] == 2, pets[i] == 7) for i in range(N)]))

# Constraint 6: The person who listens to Classical music drives an Audi
# Find suite where music is Classical (1) and car is Audi (0)
solver.add(Or([And(music[i] == 1, cars[i] == 0) for i in range(N)]))

# Constraint 7: The German drinks Coffee
# Find suite where nationality is German (6) and drink is Coffee (0)
solver.add(Or([And(nationalities[i] == 6, drinks[i] == 0) for i in range(N)]))

# Constraint 8: The person going to Tokyo is a Chemist
# Find suite where destination is Tokyo (7) and profession is Chemist (2)
solver.add(Or([And(destinations[i] == 7, professions[i] == 2) for i in range(N)]))

# Constraint 9: The Engineer's suite is immediately to the left of the Lawyer's suite
# Engineer = 4, Lawyer = 5
for i in range(N-1):
    solver.add(Implies(professions[i] == 4, professions[i+1] == 5))

# Constraint 10: The Dog owner lives next to the Volvo driver
# Dog = 1, Volvo = 7
for i in range(N):
    # Dog owner at i, Volvo driver at i-1 or i+1
    neighbors = []
    if i > 0:
        neighbors.append(cars[i-1] == 7)
    if i < N-1:
        neighbors.append(cars[i+1] == 7)
    if neighbors:
        solver.add(Implies(pets[i] == 1, Or(neighbors)))

# Constraint 11: The Rock music listener lives next to the Pop music listener
# Rock = 7, Pop = 4
for i in range(N):
    neighbors = []
    if i > 0:
        neighbors.append(music[i-1] == 4)
    if i < N-1:
        neighbors.append(music[i+1] == 4)
    if neighbors:
        solver.add(Implies(music[i] == 7, Or(neighbors)))

# Constraint 12: The person going to Paris lives next to the Fish owner
# Paris = 4, Fish = 2
for i in range(N):
    neighbors = []
    if i > 0:
        neighbors.append(pets[i-1] == 2)
    if i < N-1:
        neighbors.append(pets[i+1] == 2)
    if neighbors:
        solver.add(Implies(destinations[i] == 4, Or(neighbors)))

# Constraint 13: The Pilot lives in an even-numbered suite
# Pilot = 7
for i in range(N):
    if (i+1) % 2 == 0:  # even-numbered suite (2,4,6,8)
        solver.add(Implies(professions[i] == 7, True))  # Just mark that Pilot can be here
    else:  # odd-numbered suite (1,3,5,7)
        solver.add(Implies(professions[i] == 7, False))  # Pilot cannot be here

# Constraint 14: The Wine drinker's suite is to the right of the Coffee drinker's suite
# Wine = 6, Coffee = 0
for i in range(N):
    for j in range(i+1, N):
        solver.add(Implies(And(drinks[i] == 0, drinks[j] == 6), True))
# More precise: There exists some i < j such that drinks[i] == 0 and drinks[j] == 6
solver.add(Or([And(drinks[i] == 0, drinks[j] == 6) for i in range(N) for j in range(i+1, N)]))

# Constraint 15: The Ford driver has a neighbor who drinks Tea
# Ford = 2, Tea = 4
for i in range(N):
    neighbors = []
    if i > 0:
        neighbors.append(drinks[i-1] == 4)
    if i < N-1:
        neighbors.append(drinks[i+1] == 4)
    if neighbors:
        solver.add(Implies(cars[i] == 2, Or(neighbors)))

# Constraint 16: The Nissan driver does not live in suite #1 or #8
# Nissan = 5
solver.add(cars[0] != 5)  # suite 1
solver.add(cars[7] != 5)  # suite 8

# Constraint 17: The Jazz listener's suite number is less than the Blues listener's suite number
# Jazz = 3, Blues = 0
for i in range(N):
    for j in range(i+1, N):
        solver.add(Implies(And(music[i] == 3, music[j] == 0), True))
# More precise: There exists some i < j such that music[i] == 3 and music[j] == 0
solver.add(Or([And(music[i] == 3, music[j] == 0) for i in range(N) for j in range(i+1, N)]))

# Constraint 18: The Dutch person lives in suite #1
solver.add(nationalities[0] == 3)  # Dutch = 3

# Check and print results
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("\nSolution:")
    
    # Define reverse mappings for printing
    nat_names = ["American", "Brazilian", "Canadian", "Dutch", "Egyptian", "French", "German", "Hungarian"]
    prof_names = ["Architect", "Biologist", "Chemist", "Doctor", "Engineer", "Lawyer", "Musician", "Pilot"]
    car_names = ["Audi", "BMW", "Ford", "Honda", "Mercedes", "Nissan", "Toyota", "Volvo"]
    drink_names = ["Coffee", "Juice", "Milk", "Soda", "Tea", "Water", "Wine", "Whiskey"]
    music_names = ["Blues", "Classical", "Folk", "Jazz", "Pop", "Rap", "Reggae", "Rock"]
    pet_names = ["Cat", "Dog", "Fish", "Hamster", "Lizard", "Parrot", "Rabbit", "Snake"]
    dest_names = ["Bali", "Dubai", "London", "New York", "Paris", "Rome", "Sydney", "Tokyo"]
    
    lizard_owner_nationality = None
    
    for i in range(N):
        suite_num = i + 1
        nat = int(m.evaluate(nationalities[i]))
        prof = int(m.evaluate(professions[i]))
        car = int(m.evaluate(cars[i]))
        drink = int(m.evaluate(drinks[i]))
        mus = int(m.evaluate(music[i]))
        pet = int(m.evaluate(pets[i]))
        dest = int(m.evaluate(destinations[i]))
        
        print(f"Suite {suite_num}: {nat_names[nat]}, {prof_names[prof]}, {car_names[car]}, {drink_names[drink]}, {music_names[mus]}, {pet_names[pet]}, {dest_names[dest]}")
        
        if pet == 4:  # Lizard
            lizard_owner_nationality = nat_names[nat]
    
    print(f"\nlizard_owner: {lizard_owner_nationality}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")