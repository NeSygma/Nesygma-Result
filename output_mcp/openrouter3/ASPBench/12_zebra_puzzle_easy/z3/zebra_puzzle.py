from z3 import *

# Create solver
solver = Solver()

# Houses are 0-4 (representing houses 1-5)
houses = range(5)

# Attribute domains
colors = ["Red", "Green", "White", "Yellow", "Blue"]
nationalities = ["Brit", "Swede", "Dane", "Norwegian", "German"]
drinks = ["Tea", "Coffee", "Milk", "Beer", "Water"]
cigarettes = ["Pall Mall", "Dunhill", "Blends", "Blue Master", "Prince"]
pets = ["Dog", "Birds", "Cats", "Horse", "Zebra"]

# Create variables: for each house, store which attribute value it has
# We'll use integer indices 0-4 for each attribute type
color_of_house = [Int(f"color_{i}") for i in houses]
nationality_of_house = [Int(f"nationality_{i}") for i in houses]
drink_of_house = [Int(f"drink_{i}") for i in houses]
cigarette_of_house = [Int(f"cigarette_{i}") for i in houses]
pet_of_house = [Int(f"pet_{i}") for i in houses]

# Each attribute value must appear exactly once across all houses
# For colors: each house has a color index 0-4, all distinct
solver.add(Distinct(color_of_house))
solver.add(Distinct(nationality_of_house))
solver.add(Distinct(drink_of_house))
solver.add(Distinct(cigarette_of_house))
solver.add(Distinct(pet_of_house))

# Domain constraints: each variable must be between 0 and 4
for i in houses:
    solver.add(And(color_of_house[i] >= 0, color_of_house[i] <= 4))
    solver.add(And(nationality_of_house[i] >= 0, nationality_of_house[i] <= 4))
    solver.add(And(drink_of_house[i] >= 0, drink_of_house[i] <= 4))
    solver.add(And(cigarette_of_house[i] >= 0, cigarette_of_house[i] <= 4))
    solver.add(And(pet_of_house[i] >= 0, pet_of_house[i] <= 4))

# Map attribute values to indices
color_idx = {color: i for i, color in enumerate(colors)}
nationality_idx = {nat: i for i, nat in enumerate(nationalities)}
drink_idx = {drink: i for i, drink in enumerate(drinks)}
cigarette_idx = {cig: i for i, cig in enumerate(cigarettes)}
pet_idx = {pet: i for i, pet in enumerate(pets)}

# Constraint 1: The Brit lives in the red house
# Brit index = 0, Red index = 0
solver.add(nationality_of_house[color_of_house.index(color_idx["Red"])] == nationality_idx["Brit"])

# Constraint 2: The Swede keeps dogs as pets
# Swede index = 1, Dog index = 0
solver.add(pet_of_house[nationality_of_house.index(nationality_idx["Swede"])] == pet_idx["Dog"])

# Constraint 3: The Dane drinks tea
# Dane index = 2, Tea index = 0
solver.add(drink_of_house[nationality_of_house.index(nationality_idx["Dane"])] == drink_idx["Tea"])

# Constraint 4: The green house is on the left of the white house (directly adjacent)
# Green index = 1, White index = 2
# Find house with green, house with white, ensure white = green + 1
green_house = color_of_house.index(color_idx["Green"])
white_house = color_of_house.index(color_idx["White"])
solver.add(white_house == green_house + 1)

# Constraint 5: The green house's owner drinks coffee
# Green index = 1, Coffee index = 1
solver.add(drink_of_house[green_house] == drink_idx["Coffee"])

# Constraint 6: The person who smokes Pall Mall rears birds
# Pall Mall index = 0, Birds index = 1
solver.add(pet_of_house[cigarette_of_house.index(cigarette_idx["Pall Mall"])] == pet_idx["Birds"])

# Constraint 7: The owner of the yellow house smokes Dunhill
# Yellow index = 3, Dunhill index = 1
solver.add(cigarette_of_house[color_of_house.index(color_idx["Yellow"])] == cigarette_idx["Dunhill"])

# Constraint 8: The person living in the center house (house 3) drinks milk
# House index 2 (since 0-based), Milk index = 2
solver.add(drink_of_house[2] == drink_idx["Milk"])

# Constraint 9: The Norwegian lives in the first house (house 1)
# House index 0, Norwegian index = 3
solver.add(nationality_of_house[0] == nationality_idx["Norwegian"])

# Constraint 10: The person who smokes Blends lives next to the one who keeps cats
# Blends index = 2, Cats index = 2
# Find house with Blends, ensure cats in house+1 or house-1
blends_house = cigarette_of_house.index(cigarette_idx["Blends"])
cats_house = pet_of_house.index(pet_idx["Cats"])
solver.add(Or(blends_house == cats_house + 1, blends_house == cats_house - 1))

# Constraint 11: The person who keeps a horse lives next to the person who smokes Dunhill
# Horse index = 3, Dunhill index = 1
horse_house = pet_of_house.index(pet_idx["Horse"])
dunhill_house = cigarette_of_house.index(cigarette_idx["Dunhill"])
solver.add(Or(horse_house == dunhill_house + 1, horse_house == dunhill_house - 1))

# Constraint 12: The owner who smokes Blue Master drinks beer
# Blue Master index = 3, Beer index = 3
solver.add(drink_of_house[cigarette_of_house.index(cigarette_idx["Blue Master"])] == drink_idx["Beer"])

# Constraint 13: The German smokes Prince
# German index = 4, Prince index = 4
solver.add(cigarette_of_house[nationality_of_house.index(nationality_idx["German"])] == cigarette_idx["Prince"])

# Constraint 14: The Norwegian lives next to the blue house
# Norwegian index = 3, Blue index = 4
norwegian_house = nationality_of_house.index(nationality_idx["Norwegian"])
blue_house = color_of_house.index(color_idx["Blue"])
solver.add(Or(norwegian_house == blue_house + 1, norwegian_house == blue_house - 1))

# Constraint 15: The person who smokes Blends has a neighbor who drinks water
# Blends index = 2, Water index = 4
blends_house = cigarette_of_house.index(cigarette_idx["Blends"])
water_house = drink_of_house.index(drink_idx["Water"])
solver.add(Or(blends_house == water_house + 1, blends_house == water_house - 1))

# Check and print results
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("\nSolution:")
    
    # Create solution array
    solution = []
    for house_num in range(5):
        house_idx = house_num  # 0-based index
        house_data = {
            "house": house_num + 1,
            "color": colors[m.eval(color_of_house[house_idx]).as_long()],
            "nationality": nationalities[m.eval(nationality_of_house[house_idx]).as_long()],
            "drink": drinks[m.eval(drink_of_house[house_idx]).as_long()],
            "cigarette": cigarettes[m.eval(cigarette_of_house[house_idx]).as_long()],
            "pet": pets[m.eval(pet_of_house[house_idx]).as_long()]
        }
        solution.append(house_data)
        print(f"House {house_num + 1}: {house_data}")
    
    # Find zebra owner
    zebra_owner = None
    for house_data in solution:
        if house_data["pet"] == "Zebra":
            zebra_owner = house_data["nationality"]
            break
    
    print(f"\nzebra_owner: {zebra_owner}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")