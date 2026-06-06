from z3 import *

# Define the problem using EnumSorts for clarity and correctness

# Suites: 1 to 8 (we'll use indices 0 to 7)

# Nationalities
Nationality = EnumSort('Nationality', ['American', 'Brazilian', 'Canadian', 'Dutch', 'Egyptian', 'French', 'German', 'Hungarian'])
American, Brazilian, Canadian, Dutch, Egyptian, French, German, Hungarian = Nationality[:]

# Professions
Profession = EnumSort('Profession', ['Architect', 'Biologist', 'Chemist', 'Doctor', 'Engineer', 'Lawyer', 'Musician', 'Pilot'])
Architect, Biologist, Chemist, Doctor, Engineer, Lawyer, Musician, Pilot = Profession[:]

# Car Brands
CarBrand = EnumSort('CarBrand', ['Audi', 'BMW', 'Ford', 'Honda', 'Mercedes', 'Nissan', 'Toyota', 'Volvo'])
Audi, BMW, Ford, Honda, Mercedes, Nissan, Toyota, Volvo = CarBrand[:]

# Drinks
Drink = EnumSort('Drink', ['Coffee', 'Juice', 'Milk', 'Soda', 'Tea', 'Water', 'Wine', 'Whiskey'])
Coffee, Juice, Milk, Soda, Tea, Water, Wine, Whiskey = Drink[:]

# Music Genres
MusicGenre = EnumSort('MusicGenre', ['Blues', 'Classical', 'Folk', 'Jazz', 'Pop', 'Rap', 'Reggae', 'Rock'])
Blues, Classical, Folk, Jazz, Pop, Rap, Reggae, Rock = MusicGenre[:]

# Pets
Pet = EnumSort('Pet', ['Cat', 'Dog', 'Fish', 'Hamster', 'Lizard', 'Parrot', 'Rabbit', 'Snake'])
Cat, Dog, Fish, Hamster, Lizard, Parrot, Rabbit, Snake = Pet[:]

# Destinations
Destination = EnumSort('Destination', ['Bali', 'Dubai', 'London', 'New_York', 'Paris', 'Rome', 'Sydney', 'Tokyo'])
Bali, Dubai, London, New_York, Paris, Rome, Sydney, Tokyo = Destination[:]

# Create a solver instance
solver = Solver()

# Number of suites
suites = 8

# Create arrays for each attribute across 8 suites (0-7 representing suites 1-8)
# We'll use Int variables for each attribute per suite

# Nationality per suite
nationality = [Const(f'nationality_{i}', Nationality) for i in range(suites)]

# Profession per suite
profession = [Const(f'profession_{i}', Profession) for i in range(suites)]

# Car brand per suite
car = [Const(f'car_{i}', CarBrand) for i in range(suites)]

# Drink per suite
drink = [Const(f'drink_{i}', Drink) for i in range(suites)]

# Music genre per suite
music = [Const(f'music_{i}', MusicGenre) for i in range(suites)]

# Pet per suite
pet = [Const(f'pet_{i}', Pet) for i in range(suites)]

# Destination per suite
destination = [Const(f'destination_{i}', Destination) for i in range(suites)]

# Helper: All values in each category must be distinct
solver.add(Distinct(nationality))
solver.add(Distinct(profession))
solver.add(Distinct(car))
solver.add(Distinct(drink))
solver.add(Distinct(music))
solver.add(Distinct(pet))
solver.add(Distinct(destination))

# Constraint 1: The person in suite #4 drinks Milk
# Suite #4 is index 3 (0-indexed)
solver.add(drink[3] == Milk)

# Constraint 2: The Hungarian lives in suite #4
solver.add(nationality[3] == Hungarian)

# Constraint 3: The American is a Lawyer
solver.add(Or([And(nationality[i] == American, profession[i] == Lawyer) for i in range(suites)]))

# Constraint 4: The person who drives a BMW is a Biologist
solver.add(Or([And(car[i] == BMW, profession[i] == Biologist) for i in range(suites)]))

# Constraint 5: The Canadian owns a Snake
solver.add(Or([And(nationality[i] == Canadian, pet[i] == Snake) for i in range(suites)]))

# Constraint 6: The person who listens to Classical music drives an Audi
solver.add(Or([And(music[i] == Classical, car[i] == Audi) for i in range(suites)]))

# Constraint 7: The German drinks Coffee
solver.add(Or([And(nationality[i] == German, drink[i] == Coffee) for i in range(suites)]))

# Constraint 8: The person going to Tokyo is a Chemist
solver.add(Or([And(destination[i] == Tokyo, profession[i] == Chemist) for i in range(suites)]))

# Constraint 9: The Engineer's suite is immediately to the left of the Lawyer's suite
solver.add(Or([And(profession[i] == Engineer, profession[i+1] == Lawyer) for i in range(suites-1)]))

# Constraint 10: The Dog owner lives next to the Volvo driver
for i in range(suites):
    constraints = []
    if i > 0:
        constraints.append(And(pet[i] == Dog, car[i-1] == Volvo))
    if i < suites - 1:
        constraints.append(And(pet[i] == Dog, car[i+1] == Volvo))
    solver.add(Or(constraints))

# Constraint 11: The Rock music listener lives next to the Pop music listener
for i in range(suites):
    constraints = []
    if i > 0:
        constraints.append(Or(And(music[i] == Rock, music[i-1] == Pop), And(music[i] == Pop, music[i-1] == Rock)))
    if i < suites - 1:
        constraints.append(Or(And(music[i] == Rock, music[i+1] == Pop), And(music[i] == Pop, music[i+1] == Rock)))
    solver.add(Or(constraints))

# Constraint 12: The person going to Paris lives next to the Fish owner
for i in range(suites):
    constraints = []
    if i > 0:
        constraints.append(And(destination[i] == Paris, pet[i-1] == Fish))
    if i < suites - 1:
        constraints.append(And(destination[i] == Paris, pet[i+1] == Fish))
    solver.add(Or(constraints))

# Constraint 13: The Pilot lives in an even-numbered suite
# Suite numbers: 1-8, even suites are 2,4,6,8 -> indices 1,3,5,7
solver.add(Or([profession[i] == Pilot for i in [1,3,5,7]]))

# Constraint 14: The Wine drinker's suite is to the right of the Coffee drinker's suite
solver.add(Or([And(drink[i] == Coffee, drink[j] == Wine, i < j) for i in range(suites) for j in range(suites) if i < j]))

# Constraint 15: The Ford driver has a neighbor who drinks Tea
for i in range(suites):
    constraints = []
    if i > 0:
        constraints.append(And(car[i] == Ford, drink[i-1] == Tea))
    if i < suites - 1:
        constraints.append(And(car[i] == Ford, drink[i+1] == Tea))
    solver.add(Or(constraints))

# Constraint 16: The Nissan driver does not live in suite #1 or #8
# Suite #1 is index 0, suite #8 is index 7
solver.add(Not(Or(car[0] == Nissan, car[7] == Nissan)))

# Constraint 17: The Jazz listener's suite number is less than the Blues listener's suite number
solver.add(Or([And(music[i] == Jazz, music[j] == Blues, i < j) for i in range(suites) for j in range(suites) if i < j]))

# Constraint 18: The Dutch person lives in suite #1
# Suite #1 is index 0
solver.add(nationality[0] == Dutch)

# Check if the problem is satisfiable
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract and print the solution
    print("\nSolution found:")
    for i in range(suites):
        # Map indices back to suite numbers (1-8)
        suite_num = i + 1
        
        # Helper function to get value name from model
        def get_name(var_list, val):
            for v in var_list:
                if model.eval(var_list[v.index] == val, model_completion=True):
                    return str(val)
            return "Unknown"
        
        # Get attribute values
        nat = model.eval(nationality[i], model_completion=True)
        prof = model.eval(profession[i], model_completion=True)
        car_brand = model.eval(car[i], model_completion=True)
        drink_val = model.eval(drink[i], model_completion=True)
        music_val = model.eval(music[i], model_completion=True)
        pet_val = model.eval(pet[i], model_completion=True)
        dest = model.eval(destination[i], model_completion=True)
        
        # Print the suite information
        print(f"\nSuite {suite_num}:")
        print(f"  Nationality: {nat}")
        print(f"  Profession: {prof}")
        print(f"  Car: {car_brand}")
        print(f"  Drink: {drink_val}")
        print(f"  Music: {music_val}")
        print(f"  Pet: {pet_val}")
        print(f"  Destination: {dest}")
    
    # Identify who owns the lizard
    lizard_owner_index = None
    for i in range(suites):
        if model.eval(pet[i] == Lizard, model_completion=True):
            lizard_owner_index = i
            break
    
    if lizard_owner_index is not None:
        lizard_owner_nationality = model.eval(nationality[lizard_owner_index], model_completion=True)
        print(f"\nThe person who owns the Lizard is: {lizard_owner_nationality}")
    else:
        print("\nERROR: No lizard owner found in the model")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")