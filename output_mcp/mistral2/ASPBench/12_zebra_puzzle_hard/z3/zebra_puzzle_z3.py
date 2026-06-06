from z3 import *

# Define EnumSorts for each attribute
Nationality = EnumSort('Nationality', ['American', 'Brazilian', 'Canadian', 'Dutch', 'Egyptian', 'French', 'German', 'Hungarian'])
Profession = EnumSort('Profession', ['Architect', 'Biologist', 'Chemist', 'Doctor', 'Engineer', 'Lawyer', 'Musician', 'Pilot'])
CarBrand = EnumSort('CarBrand', ['Audi', 'BMW', 'Ford', 'Honda', 'Mercedes', 'Nissan', 'Toyota', 'Volvo'])
Drink = EnumSort('Drink', ['Coffee', 'Juice', 'Milk', 'Soda', 'Tea', 'Water', 'Wine', 'Whiskey'])
MusicGenre = EnumSort('MusicGenre', ['Blues', 'Classical', 'Folk', 'Jazz', 'Pop', 'Rap', 'Reggae', 'Rock'])
Pet = EnumSort('Pet', ['Cat', 'Dog', 'Fish', 'Hamster', 'Lizard', 'Parrot', 'Rabbit', 'Snake'])
Destination = EnumSort('Destination', ['Bali', 'Dubai', 'London', 'NewYork', 'Paris', 'Rome', 'Sydney', 'Tokyo'])

# Extract values for convenience
Nat = Nationality
Prof = Profession
Car = CarBrand
Dr = Drink
Mus = MusicGenre
P = Pet
Dest = Destination

# Create solver
solver = Solver()

# Create arrays for each attribute, indexed by suite number (1-8)
# We use 1-based indexing for suites
nationality = [Const(f'nationality_{i}', Nationality) for i in range(1, 9)]
profession = [Const(f'profession_{i}', Profession) for i in range(1, 9)]
car_brand = [Const(f'car_brand_{i}', CarBrand) for i in range(1, 9)]
drink = [Const(f'drink_{i}', Drink) for i in range(1, 9)]
music_genre = [Const(f'music_genre_{i}', MusicGenre) for i in range(1, 9)]
pet = [Const(f'pet_{i}', Pet) for i in range(1, 9)]
destination = [Const(f'destination_{i}', Destination) for i in range(1, 9)]

# Helper: All values in an attribute are distinct
solver.add(Distinct(nationality))
solver.add(Distinct(profession))
solver.add(Distinct(car_brand))
solver.add(Distinct(drink))
solver.add(Distinct(music_genre))
solver.add(Distinct(pet))
solver.add(Distinct(destination))

# Constraint 1: Suite #4 drinks Milk
solver.add(drink[3] == Dr.Milk)

# Constraint 2: The Hungarian lives in suite #4
solver.add(nationality[3] == Nat.Hungarian)

# Constraint 3: The American is a Lawyer
solver.add(ForAll([i], Implies(nationality[i-1] == Nat.American, profession[i-1] == Prof.Lawyer)))

# Constraint 4: The person who drives a BMW is a Biologist
solver.add(ForAll([i], Implies(car_brand[i-1] == Car.BMW, profession[i-1] == Prof.Biologist)))

# Constraint 5: The Canadian owns a Snake
solver.add(ForAll([i], Implies(nationality[i-1] == Nat.Canadian, pet[i-1] == P.Snake)))

# Constraint 6: The person who listens to Classical music drives an Audi
solver.add(ForAll([i], Implies(music_genre[i-1] == Mus.Classical, car_brand[i-1] == Car.Audi)))

# Constraint 7: The German drinks Coffee
solver.add(ForAll([i], Implies(nationality[i-1] == Nat.German, drink[i-1] == Dr.Coffee)))

# Constraint 8: The person going to Tokyo is a Chemist
solver.add(ForAll([i], Implies(destination[i-1] == Dest.Tokyo, profession[i-1] == Prof.Chemist)))

# Constraint 9: The Engineer's suite is immediately to the left of the Lawyer's suite
solver.add(Or(
    And(profession[0] == Prof.Engineer, profession[1] == Prof.Lawyer),
    And(profession[1] == Prof.Engineer, profession[2] == Prof.Lawyer),
    And(profession[2] == Prof.Engineer, profession[3] == Prof.Lawyer),
    And(profession[3] == Prof.Engineer, profession[4] == Prof.Lawyer),
    And(profession[4] == Prof.Engineer, profession[5] == Prof.Lawyer),
    And(profession[5] == Prof.Engineer, profession[6] == Prof.Lawyer),
    And(profession[6] == Prof.Engineer, profession[7] == Prof.Lawyer)
))

# Constraint 10: The Dog owner lives next to the Volvo driver
solver.add(Or(
    And(pet[0] == P.Dog, Or(car_brand[0] == Car.Volvo, car_brand[1] == Car.Volvo)),
    And(pet[1] == P.Dog, Or(car_brand[0] == Car.Volvo, car_brand[1] == Car.Volvo, car_brand[2] == Car.Volvo)),
    And(pet[2] == P.Dog, Or(car_brand[1] == Car.Volvo, car_brand[2] == Car.Volvo, car_brand[3] == Car.Volvo)),
    And(pet[3] == P.Dog, Or(car_brand[2] == Car.Volvo, car_brand[3] == Car.Volvo, car_brand[4] == Car.Volvo)),
    And(pet[4] == P.Dog, Or(car_brand[3] == Car.Volvo, car_brand[4] == Car.Volvo, car_brand[5] == Car.Volvo)),
    And(pet[5] == P.Dog, Or(car_brand[4] == Car.Volvo, car_brand[5] == Car.Volvo, car_brand[6] == Car.Volvo)),
    And(pet[6] == P.Dog, Or(car_brand[5] == Car.Volvo, car_brand[6] == Car.Volvo, car_brand[7] == Car.Volvo)),
    And(pet[7] == P.Dog, Or(car_brand[6] == Car.Volvo, car_brand[7] == Car.Volvo))
))

# Constraint 11: The Rock music listener lives next to the Pop music listener
solver.add(Or(
    And(music_genre[0] == Mus.Rock, Or(music_genre[0] == Mus.Pop, music_genre[1] == Mus.Pop)),
    And(music_genre[1] == Mus.Rock, Or(music_genre[0] == Mus.Pop, music_genre[1] == Mus.Pop, music_genre[2] == Mus.Pop)),
    And(music_genre[2] == Mus.Rock, Or(music_genre[1] == Mus.Pop, music_genre[2] == Mus.Pop, music_genre[3] == Mus.Pop)),
    And(music_genre[3] == Mus.Rock, Or(music_genre[2] == Mus.Pop, music_genre[3] == Mus.Pop, music_genre[4] == Mus.Pop)),
    And(music_genre[4] == Mus.Rock, Or(music_genre[3] == Mus.Pop, music_genre[4] == Mus.Pop, music_genre[5] == Mus.Pop)),
    And(music_genre[5] == Mus.Rock, Or(music_genre[4] == Mus.Pop, music_genre[5] == Mus.Pop, music_genre[6] == Mus.Pop)),
    And(music_genre[6] == Mus.Rock, Or(music_genre[5] == Mus.Pop, music_genre[6] == Mus.Pop, music_genre[7] == Mus.Pop)),
    And(music_genre[7] == Mus.Rock, Or(music_genre[6] == Mus.Pop, music_genre[7] == Mus.Pop))
))

# Constraint 12: The person going to Paris lives next to the Fish owner
solver.add(Or(
    And(destination[0] == Dest.Paris, Or(pet[0] == P.Fish, pet[1] == P.Fish)),
    And(destination[1] == Dest.Paris, Or(pet[0] == P.Fish, pet[1] == P.Fish, pet[2] == P.Fish)),
    And(destination[2] == Dest.Paris, Or(pet[1] == P.Fish, pet[2] == P.Fish, pet[3] == P.Fish)),
    And(destination[3] == Dest.Paris, Or(pet[2] == P.Fish, pet[3] == P.Fish, pet[4] == P.Fish)),
    And(destination[4] == Dest.Paris, Or(pet[3] == P.Fish, pet[4] == P.Fish, pet[5] == P.Fish)),
    And(destination[5] == Dest.Paris, Or(pet[4] == P.Fish, pet[5] == P.Fish, pet[6] == P.Fish)),
    And(destination[6] == Dest.Paris, Or(pet[5] == P.Fish, pet[6] == P.Fish, pet[7] == P.Fish)),
    And(destination[7] == Dest.Paris, Or(pet[6] == P.Fish, pet[7] == P.Fish))
))

# Constraint 13: The Pilot lives in an even-numbered suite
solver.add(Or(profession[1] == Prof.Pilot, profession[3] == Prof.Pilot, profession[5] == Prof.Pilot, profession[7] == Prof.Pilot))

# Constraint 14: The Wine drinker's suite is to the right of the Coffee drinker's suite
solver.add(Or(
    And(drink[0] == Dr.Coffee, Or(drink[1] == Dr.Wine, drink[2] == Dr.Wine, drink[3] == Dr.Wine, drink[4] == Dr.Wine, drink[5] == Dr.Wine, drink[6] == Dr.Wine, drink[7] == Dr.Wine)),
    And(drink[1] == Dr.Coffee, Or(drink[2] == Dr.Wine, drink[3] == Dr.Wine, drink[4] == Dr.Wine, drink[5] == Dr.Wine, drink[6] == Dr.Wine, drink[7] == Dr.Wine)),
    And(drink[2] == Dr.Coffee, Or(drink[3] == Dr.Wine, drink[4] == Dr.Wine, drink[5] == Dr.Wine, drink[6] == Dr.Wine, drink[7] == Dr.Wine)),
    And(drink[3] == Dr.Coffee, Or(drink[4] == Dr.Wine, drink[5] == Dr.Wine, drink[6] == Dr.Wine, drink[7] == Dr.Wine)),
    And(drink[4] == Dr.Coffee, Or(drink[5] == Dr.Wine, drink[6] == Dr.Wine, drink[7] == Dr.Wine)),
    And(drink[5] == Dr.Coffee, Or(drink[6] == Dr.Wine, drink[7] == Dr.Wine)),
    And(drink[6] == Dr.Coffee, drink[7] == Dr.Wine)
))

# Constraint 15: The Ford driver has a neighbor who drinks Tea
solver.add(Or(
    And(car_brand[0] == Car.Ford, Or(drink[0] == Dr.Tea, drink[1] == Dr.Tea)),
    And(car_brand[1] == Car.Ford, Or(drink[0] == Dr.Tea, drink[1] == Dr.Tea, drink[2] == Dr.Tea)),
    And(car_brand[2] == Car.Ford, Or(drink[1] == Dr.Tea, drink[2] == Dr.Tea, drink[3] == Dr.Tea)),
    And(car_brand[3] == Car.Ford, Or(drink[2] == Dr.Tea, drink[3] == Dr.Tea, drink[4] == Dr.Tea)),
    And(car_brand[4] == Car.Ford, Or(drink[3] == Dr.Tea, drink[4] == Dr.Tea, drink[5] == Dr.Tea)),
    And(car_brand[5] == Car.Ford, Or(drink[4] == Dr.Tea, drink[5] == Dr.Tea, drink[6] == Dr.Tea)),
    And(car_brand[6] == Car.Ford, Or(drink[5] == Dr.Tea, drink[6] == Dr.Tea, drink[7] == Dr.Tea)),
    And(car_brand[7] == Car.Ford, Or(drink[6] == Dr.Tea, drink[7] == Dr.Tea))
))

# Constraint 16: The Nissan driver does not live in suite #1 or #8
solver.add(Or(
    car_brand[1] == Car.Nissan,
    car_brand[2] == Car.Nissan,
    car_brand[3] == Car.Nissan,
    car_brand[4] == Car.Nissan,
    car_brand[5] == Car.Nissan,
    car_brand[6] == Car.Nissan
))

# Constraint 17: The Jazz listener's suite number is less than the Blues listener's suite number
solver.add(Or(
    And(music_genre[0] == Mus.Jazz, Or(music_genre[1] == Mus.Blues, music_genre[2] == Mus.Blues, music_genre[3] == Mus.Blues, music_genre[4] == Mus.Blues, music_genre[5] == Mus.Blues, music_genre[6] == Mus.Blues, music_genre[7] == Mus.Blues)),
    And(music_genre[1] == Mus.Jazz, Or(music_genre[2] == Mus.Blues, music_genre[3] == Mus.Blues, music_genre[4] == Mus.Blues, music_genre[5] == Mus.Blues, music_genre[6] == Mus.Blues, music_genre[7] == Mus.Blues)),
    And(music_genre[2] == Mus.Jazz, Or(music_genre[3] == Mus.Blues, music_genre[4] == Mus.Blues, music_genre[5] == Mus.Blues, music_genre[6] == Mus.Blues, music_genre[7] == Mus.Blues)),
    And(music_genre[3] == Mus.Jazz, Or(music_genre[4] == Mus.Blues, music_genre[5] == Mus.Blues, music_genre[6] == Mus.Blues, music_genre[7] == Mus.Blues)),
    And(music_genre[4] == Mus.Jazz, Or(music_genre[5] == Mus.Blues, music_genre[6] == Mus.Blues, music_genre[7] == Mus.Blues)),
    And(music_genre[5] == Mus.Jazz, Or(music_genre[6] == Mus.Blues, music_genre[7] == Mus.Blues)),
    And(music_genre[6] == Mus.Jazz, music_genre[7] == Mus.Blues)
))

# Constraint 18: The Dutch person lives in suite #1
solver.add(nationality[0] == Nat.Dutch)

# Check satisfiability
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Print solution for each suite
    solution = []
    for i in range(8):
        suite = i + 1
        sol = {
            "suite": suite,
            "nationality": model[nationality[i]],
            "profession": model[profession[i]],
            "car_brand": model[car_brand[i]],
            "drink": model[drink[i]],
            "music_genre": model[music_genre[i]],
            "pet": model[pet[i]],
            "destination": model[destination[i]]
        }
        solution.append(sol)
        print(f"Suite {suite}:")
        print(f"  Nationality: {sol['nationality']}")
        print(f"  Profession: {sol['profession']}")
        print(f"  Car Brand: {sol['car_brand']}")
        print(f"  Drink: {sol['drink']}")
        print(f"  Music Genre: {sol['music_genre']}")
        print(f"  Pet: {sol['pet']}")
        print(f"  Destination: {sol['destination']}")
        print()
    
    # Find the lizard owner
    lizard_owner = None
    for sol in solution:
        if sol["pet"] == P.Lizard:
            lizard_owner = sol["nationality"]
            break
    
    print(f"Lizard owner nationality: {lizard_owner}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")