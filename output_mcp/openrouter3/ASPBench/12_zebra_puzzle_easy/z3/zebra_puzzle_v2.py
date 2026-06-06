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

# Helper function to find house with given attribute value
def find_house_with_attribute(attr_list, attr_value_idx):
    """Return house index where attr_list[house] == attr_value_idx"""
    # We'll use a symbolic approach: create a variable for the house
    house_var = Int(f"house_for_{attr_list[0].ctx}_{attr_value_idx}")
    solver.add(Or([house_var == i for i in houses]))
    solver.add(Or([attr_list[i] == attr_value_idx for i in houses]))
    # Ensure exactly one house has this attribute value
    solver.add(Sum([If(attr_list[i] == attr_value_idx, 1, 0) for i in houses]) == 1)
    return house_var

# Actually, let's use a simpler approach: directly constrain based on known indices
# Constraint 1: The Brit lives in the red house
# Brit index = 0, Red index = 0
# We need: nationality_of_house[house_with_red] == 0
# And: color_of_house[house_with_red] == 0
# We can express this as: For some house i, color_of_house[i] == 0 AND nationality_of_house[i] == 0
solver.add(Or([And(color_of_house[i] == 0, nationality_of_house[i] == 0) for i in houses]))

# Constraint 2: The Swede keeps dogs as pets
# Swede index = 1, Dog index = 0
solver.add(Or([And(nationality_of_house[i] == 1, pet_of_house[i] == 0) for i in houses]))

# Constraint 3: The Dane drinks tea
# Dane index = 2, Tea index = 0
solver.add(Or([And(nationality_of_house[i] == 2, drink_of_house[i] == 0) for i in houses]))

# Constraint 4: The green house is on the left of the white house (directly adjacent)
# Green index = 1, White index = 2
# Find house with green, house with white, ensure white = green + 1
for i in range(4):  # green can be in houses 0-3
    solver.add(Implies(color_of_house[i] == 1, color_of_house[i+1] == 2))

# Constraint 5: The green house's owner drinks coffee
# Green index = 1, Coffee index = 1
solver.add(Or([And(color_of_house[i] == 1, drink_of_house[i] == 1) for i in houses]))

# Constraint 6: The person who smokes Pall Mall rears birds
# Pall Mall index = 0, Birds index = 1
solver.add(Or([And(cigarette_of_house[i] == 0, pet_of_house[i] == 1) for i in houses]))

# Constraint 7: The owner of the yellow house smokes Dunhill
# Yellow index = 3, Dunhill index = 1
solver.add(Or([And(color_of_house[i] == 3, cigarette_of_house[i] == 1) for i in houses]))

# Constraint 8: The person living in the center house (house 3) drinks milk
# House index 2 (since 0-based), Milk index = 2
solver.add(drink_of_house[2] == 2)

# Constraint 9: The Norwegian lives in the first house (house 1)
# House index 0, Norwegian index = 3
solver.add(nationality_of_house[0] == 3)

# Constraint 10: The person who smokes Blends lives next to the one who keeps cats
# Blends index = 2, Cats index = 2
# Find house with Blends, ensure cats in house+1 or house-1
for i in houses:
    solver.add(Implies(cigarette_of_house[i] == 2,
                       Or([pet_of_house[j] == 2 for j in houses if abs(j-i) == 1])))

# Constraint 11: The person who keeps a horse lives next to the person who smokes Dunhill
# Horse index = 3, Dunhill index = 1
for i in houses:
    solver.add(Implies(pet_of_house[i] == 3,
                       Or([cigarette_of_house[j] == 1 for j in houses if abs(j-i) == 1])))

# Constraint 12: The owner who smokes Blue Master drinks beer
# Blue Master index = 3, Beer index = 3
solver.add(Or([And(cigarette_of_house[i] == 3, drink_of_house[i] == 3) for i in houses]))

# Constraint 13: The German smokes Prince
# German index = 4, Prince index = 4
solver.add(Or([And(nationality_of_house[i] == 4, cigarette_of_house[i] == 4) for i in houses]))

# Constraint 14: The Norwegian lives next to the blue house
# Norwegian index = 3, Blue index = 4
for i in houses:
    solver.add(Implies(nationality_of_house[i] == 3,
                       Or([color_of_house[j] == 4 for j in houses if abs(j-i) == 1])))

# Constraint 15: The person who smokes Blends has a neighbor who drinks water
# Blends index = 2, Water index = 4
for i in houses:
    solver.add(Implies(cigarette_of_house[i] == 2,
                       Or([drink_of_house[j] == 4 for j in houses if abs(j-i) == 1])))

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