from z3 import *

solver = Solver()

# 8 suites numbered 0..7 (representing positions 1..8)
N = 8

# We'll use Int variables for each attribute per suite.
# Each variable takes a value 0..7 representing which option.

# Nationalities: 0=American, 1=Brazilian, 2=Canadian, 3=Dutch, 4=Egyptian, 5=French, 6=German, 7=Hungarian
nat = [Int(f'nat_{i}') for i in range(N)]

# Professions: 0=Architect, 1=Biologist, 2=Chemist, 3=Doctor, 4=Engineer, 5=Lawyer, 6=Musician, 7=Pilot
prof = [Int(f'prof_{i}') for i in range(N)]

# Car brands: 0=Audi, 1=BMW, 2=Ford, 3=Honda, 4=Mercedes, 5=Nissan, 6=Toyota, 7=Volvo
car = [Int(f'car_{i}') for i in range(N)]

# Drinks: 0=Coffee, 1=Juice, 2=Milk, 3=Soda, 4=Tea, 5=Water, 6=Wine, 7=Whiskey
drink = [Int(f'drink_{i}') for i in range(N)]

# Music: 0=Blues, 1=Classical, 2=Folk, 3=Jazz, 4=Pop, 5=Rap, 6=Reggae, 7=Rock
music = [Int(f'music_{i}') for i in range(N)]

# Pets: 0=Cat, 1=Dog, 2=Fish, 3=Hamster, 4=Lizard, 5=Parrot, 6=Rabbit, 7=Snake
pet = [Int(f'pet_{i}') for i in range(N)]

# Destinations: 0=Bali, 1=Dubai, 2=London, 3=New York, 4=Paris, 5=Rome, 6=Sydney, 7=Tokyo
dest = [Int(f'dest_{i}') for i in range(N)]

# All variables domain 0..7
all_vars = nat + prof + car + drink + music + pet + dest
for v in all_vars:
    solver.add(v >= 0, v <= 7)

# Each attribute group has all distinct values
solver.add(Distinct(nat))
solver.add(Distinct(prof))
solver.add(Distinct(car))
solver.add(Distinct(drink))
solver.add(Distinct(music))
solver.add(Distinct(pet))
solver.add(Distinct(dest))

# Constraint 1: The person in suite #4 drinks Milk (suite index 3)
solver.add(drink[3] == 2)  # Milk = 2

# Constraint 2: The Hungarian lives in suite #4 (index 3)
solver.add(nat[3] == 7)  # Hungarian = 7

# Constraint 3: The American is a Lawyer
# American = 0, Lawyer = 5
# For each suite i: if nat[i] == 0 then prof[i] == 5
for i in range(N):
    solver.add(Implies(nat[i] == 0, prof[i] == 5))

# Constraint 4: The person who drives a BMW is a Biologist
# BMW = 1, Biologist = 1
for i in range(N):
    solver.add(Implies(car[i] == 1, prof[i] == 1))

# Constraint 5: The Canadian owns a Snake
# Canadian = 2, Snake = 7
for i in range(N):
    solver.add(Implies(nat[i] == 2, pet[i] == 7))

# Constraint 6: The person who listens to Classical music drives an Audi
# Classical = 1, Audi = 0
for i in range(N):
    solver.add(Implies(music[i] == 1, car[i] == 0))

# Constraint 7: The German drinks Coffee
# German = 6, Coffee = 0
for i in range(N):
    solver.add(Implies(nat[i] == 6, drink[i] == 0))

# Constraint 8: The person going to Tokyo is a Chemist
# Tokyo = 7, Chemist = 2
for i in range(N):
    solver.add(Implies(dest[i] == 7, prof[i] == 2))

# Constraint 9: The Engineer's suite is immediately to the left of the Lawyer's suite
# Engineer = 4, Lawyer = 5
# For each i from 0 to 6: if prof[i] == 4 then prof[i+1] == 5
for i in range(N - 1):
    solver.add(Implies(prof[i] == 4, prof[i+1] == 5))

# Constraint 10: The Dog owner lives next to the Volvo driver
# Dog = 1, Volvo = 7
# For each i, j such that |i-j| == 1: if pet[i] == 1 then car[j] == 7
# We'll encode: there exists adjacent pair (i,j) with pet[i]==1 and car[j]==7
adj_dog_volvo = False
for i in range(N):
    for j in range(N):
        if abs(i - j) == 1:
            adj_dog_volvo = Or(adj_dog_volvo, And(pet[i] == 1, car[j] == 7))
solver.add(adj_dog_volvo)

# Constraint 11: The Rock music listener lives next to the Pop music listener
# Rock = 7, Pop = 4
adj_rock_pop = False
for i in range(N):
    for j in range(N):
        if abs(i - j) == 1:
            adj_rock_pop = Or(adj_rock_pop, And(music[i] == 7, music[j] == 4))
solver.add(adj_rock_pop)

# Constraint 12: The person going to Paris lives next to the Fish owner
# Paris = 4, Fish = 2
adj_paris_fish = False
for i in range(N):
    for j in range(N):
        if abs(i - j) == 1:
            adj_paris_fish = Or(adj_paris_fish, And(dest[i] == 4, pet[j] == 2))
solver.add(adj_paris_fish)

# Constraint 13: The Pilot lives in an even-numbered suite
# Pilot = 7, even-numbered suites: indices 1,3,5,7 (suite numbers 2,4,6,8)
# Actually suite numbers: 1=odd, 2=even, 3=odd, 4=even, 5=odd, 6=even, 7=odd, 8=even
# So even-numbered suites are indices 1,3,5,7
pilot_even = Or([prof[i] == 7 for i in [1, 3, 5, 7]])
solver.add(pilot_even)

# Constraint 14: The Wine drinker's suite is to the right of the Coffee drinker's suite
# Wine = 6, Coffee = 0
# There exists i, j such that i < j and drink[i] == 0 and drink[j] == 6
wine_right_of_coffee = False
for i in range(N):
    for j in range(N):
        if i < j:
            wine_right_of_coffee = Or(wine_right_of_coffee, And(drink[i] == 0, drink[j] == 6))
solver.add(wine_right_of_coffee)

# Constraint 15: The Ford driver has a neighbor who drinks Tea
# Ford = 2, Tea = 4
ford_tea_neighbor = False
for i in range(N):
    for j in range(N):
        if abs(i - j) == 1:
            ford_tea_neighbor = Or(ford_tea_neighbor, And(car[i] == 2, drink[j] == 4))
solver.add(ford_tea_neighbor)

# Constraint 16: The Nissan driver does not live in suite #1 or #8
# Nissan = 5, suite #1 is index 0, suite #8 is index 7
for i in [0, 7]:
    solver.add(car[i] != 5)

# Constraint 17: The Jazz listener's suite number is less than the Blues listener's suite number
# Jazz = 3, Blues = 0
jazz_less_than_blues = False
for i in range(N):
    for j in range(N):
        if i < j:
            jazz_less_than_blues = Or(jazz_less_than_blues, And(music[i] == 3, music[j] == 0))
solver.add(jazz_less_than_blues)

# Constraint 18: The Dutch person lives in suite #1 (index 0)
# Dutch = 3
solver.add(nat[0] == 3)

# Also need to ensure that for constraint 9, the Engineer is immediately left of Lawyer.
# But we also need to ensure that if prof[i] == 5 (Lawyer), then prof[i-1] == 4 (Engineer)
# Actually constraint 9 says "Engineer's suite is immediately to the left of the Lawyer's suite"
# So for each i from 1 to 7: if prof[i] == 5 then prof[i-1] == 4
for i in range(1, N):
    solver.add(Implies(prof[i] == 5, prof[i-1] == 4))

# Also need to ensure that the American is a Lawyer (constraint 3) - already done above.
# But we also need to ensure that the Lawyer is American (since each profession is unique and each nationality is unique)
# Actually constraint 3 says "The American is a Lawyer" - this means the person who is American has profession Lawyer.
# Since each profession is unique, there is exactly one Lawyer, and that person is American.
# Our Implies encoding already handles this: if nat[i]==0 then prof[i]==5.
# But we also need the converse: if prof[i]==5 then nat[i]==0.
# Let's add that.
for i in range(N):
    solver.add(Implies(prof[i] == 5, nat[i] == 0))

# Similarly for constraint 4: BMW driver is Biologist, and Biologist drives BMW
for i in range(N):
    solver.add(Implies(prof[i] == 1, car[i] == 1))

# Constraint 5: Canadian owns Snake, and Snake owner is Canadian
for i in range(N):
    solver.add(Implies(pet[i] == 7, nat[i] == 2))

# Constraint 6: Classical listener drives Audi, and Audi driver listens to Classical
for i in range(N):
    solver.add(Implies(car[i] == 0, music[i] == 1))

# Constraint 7: German drinks Coffee, and Coffee drinker is German
for i in range(N):
    solver.add(Implies(drink[i] == 0, nat[i] == 6))

# Constraint 8: Tokyo goer is Chemist, and Chemist goes to Tokyo
for i in range(N):
    solver.add(Implies(prof[i] == 2, dest[i] == 7))

print("Solving...")
result = solver.check()
print(f"Result: {result}")

if result == sat:
    m = solver.model()
    
    # Map values to names
    nationalities = ["American", "Brazilian", "Canadian", "Dutch", "Egyptian", "French", "German", "Hungarian"]
    professions = ["Architect", "Biologist", "Chemist", "Doctor", "Engineer", "Lawyer", "Musician", "Pilot"]
    cars = ["Audi", "BMW", "Ford", "Honda", "Mercedes", "Nissan", "Toyota", "Volvo"]
    drinks = ["Coffee", "Juice", "Milk", "Soda", "Tea", "Water", "Wine", "Whiskey"]
    musics = ["Blues", "Classical", "Folk", "Jazz", "Pop", "Rap", "Reggae", "Rock"]
    pets = ["Cat", "Dog", "Fish", "Hamster", "Lizard", "Parrot", "Rabbit", "Snake"]
    destinations = ["Bali", "Dubai", "London", "New York", "Paris", "Rome", "Sydney", "Tokyo"]
    
    print("\n=== SOLUTION ===")
    for i in range(N):
        n = m[nat[i]].as_long()
        p = m[prof[i]].as_long()
        c = m[car[i]].as_long()
        d = m[drink[i]].as_long()
        mu = m[music[i]].as_long()
        pe = m[pet[i]].as_long()
        de = m[dest[i]].as_long()
        print(f"Suite {i+1}: {nationalities[n]}, {professions[p]}, {cars[c]}, {drinks[d]}, {musics[mu]}, {pets[pe]}, {destinations[de]}")
    
    # Find lizard owner
    for i in range(N):
        if m[pet[i]].as_long() == 4:  # Lizard = 4
            lizard_owner_nat = m[nat[i]].as_long()
            print(f"\nLizard owner: {nationalities[lizard_owner_nat]} (Suite {i+1})")
    
    print("\nSTATUS: sat")
else:
    print("STATUS: unsat")
    print("No solution found.")