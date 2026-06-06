from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare the solver
solver = Solver()

# Number of houses
N = 5

# Define symbolic constants for each attribute value
# Colors
colors = ['Red', 'Green', 'White', 'Yellow', 'Blue']
Color = Datatype('Color')
Color.declare('Red')
Color.declare('Green')
Color.declare('White')
Color.declare('Yellow')
Color.declare('Blue')
Color = Color.create()
Red, Green, White, Yellow, Blue = Color

# Nationalities
nationalities = ['Brit', 'Swede', 'Dane', 'Norwegian', 'German']
Nationality = Datatype('Nationality')
Nationality.declare('Brit')
Nationality.declare('Swede')
Nationality.declare('Dane')
Nationality.declare('Norwegian')
Nationality.declare('German')
Nationality = Nationality.create()
Brit, Swede, Dane, Norwegian, German = Nationality

# Drinks
drinks = ['Tea', 'Coffee', 'Milk', 'Beer', 'Water']
Drink = Datatype('Drink')
Drink.declare('Tea')
Drink.declare('Coffee')
Drink.declare('Milk')
Drink.declare('Beer')
Drink.declare('Water')
Drink = Drink.create()
Tea, Coffee, Milk, Beer, Water = Drink

# Cigarettes
cigarettes = ['Pall_Mall', 'Dunhill', 'Blends', 'Blue_Master', 'Prince']
Cigarette = Datatype('Cigarette')
Cigarette.declare('Pall_Mall')
Cigarette.declare('Dunhill')
Cigarette.declare('Blends')
Cigarette.declare('Blue_Master')
Cigarette.declare('Prince')
Cigarette = Cigarette.create()
Pall_Mall, Dunhill, Blends, Blue_Master, Prince = Cigarette

# Pets
pets = ['Dog', 'Birds', 'Cats', 'Horse', 'Zebra']
Pet = Datatype('Pet')
Pet.declare('Dog')
Pet.declare('Birds')
Pet.declare('Cats')
Pet.declare('Horse')
Pet.declare('Zebra')
Pet = Pet.create()
Dog, Birds, Cats, Horse, Zebra = Pet

# Create a list of houses, each house is a dictionary of attributes
houses = [{} for _ in range(N)]

# Create symbolic variables for each attribute in each house
for i in range(N):
    houses[i]['color'] = Const(f'color_{i}', Color)
    houses[i]['nationality'] = Const(f'nationality_{i}', Nationality)
    houses[i]['drink'] = Const(f'drink_{i}', Drink)
    houses[i]['cigarette'] = Const(f'cigarette_{i}', Cigarette)
    houses[i]['pet'] = Const(f'pet_{i}', Pet)

# All values for an attribute must be distinct across houses
for attr in ['color', 'nationality', 'drink', 'cigarette', 'pet']:
    solver.add(Distinct([houses[i][attr] for i in range(N)]))

# Constraint 1: The Brit lives in the red house
for i in range(N):
    solver.add(Implies(houses[i]['nationality'] == Brit, houses[i]['color'] == Red))
    solver.add(Implies(houses[i]['color'] == Red, houses[i]['nationality'] == Brit))

# Constraint 2: The Swede keeps dogs as pets
for i in range(N):
    solver.add(Implies(houses[i]['nationality'] == Swede, houses[i]['pet'] == Dog))
    solver.add(Implies(houses[i]['pet'] == Dog, houses[i]['nationality'] == Swede))

# Constraint 3: The Dane drinks tea
for i in range(N):
    solver.add(Implies(houses[i]['nationality'] == Dane, houses[i]['drink'] == Tea))
    solver.add(Implies(houses[i]['drink'] == Tea, houses[i]['nationality'] == Dane))

# Constraint 4: The green house is on the left of the white house (directly adjacent)
for i in range(N-1):
    solver.add(Implies(houses[i]['color'] == Green, houses[i+1]['color'] == White))

# Constraint 5: The green house's owner drinks coffee
for i in range(N):
    solver.add(Implies(houses[i]['color'] == Green, houses[i]['drink'] == Coffee))
    solver.add(Implies(houses[i]['drink'] == Coffee, houses[i]['color'] == Green))

# Constraint 6: The person who smokes Pall Mall rears birds
for i in range(N):
    solver.add(Implies(houses[i]['cigarette'] == Pall_Mall, houses[i]['pet'] == Birds))
    solver.add(Implies(houses[i]['pet'] == Birds, houses[i]['cigarette'] == Pall_Mall))

# Constraint 7: The owner of the yellow house smokes Dunhill
for i in range(N):
    solver.add(Implies(houses[i]['color'] == Yellow, houses[i]['cigarette'] == Dunhill))
    solver.add(Implies(houses[i]['cigarette'] == Dunhill, houses[i]['color'] == Yellow))

# Constraint 8: The person living in the center house (house 3) drinks milk
solver.add(houses[2]['drink'] == Milk)

# Constraint 9: The Norwegian lives in the first house (house 1)
solver.add(houses[0]['nationality'] == Norwegian)

# Constraint 10: The person who smokes Blends lives next to the one who keeps cats
for i in range(N):
    if i > 0:
        solver.add(Implies(houses[i]['cigarette'] == Blends, houses[i-1]['pet'] == Cats))
    if i < N-1:
        solver.add(Implies(houses[i]['cigarette'] == Blends, houses[i+1]['pet'] == Cats))

# Constraint 11: The person who keeps a horse lives next to the person who smokes Dunhill
for i in range(N):
    if i > 0:
        solver.add(Implies(houses[i]['pet'] == Horse, houses[i-1]['cigarette'] == Dunhill))
    if i < N-1:
        solver.add(Implies(houses[i]['pet'] == Horse, houses[i+1]['cigarette'] == Dunhill))

# Constraint 12: The owner who smokes Blue Master drinks beer
for i in range(N):
    solver.add(Implies(houses[i]['cigarette'] == Blue_Master, houses[i]['drink'] == Beer))
    solver.add(Implies(houses[i]['drink'] == Beer, houses[i]['cigarette'] == Blue_Master))

# Constraint 13: The German smokes Prince
for i in range(N):
    solver.add(Implies(houses[i]['nationality'] == German, houses[i]['cigarette'] == Prince))
    solver.add(Implies(houses[i]['cigarette'] == Prince, houses[i]['nationality'] == German))

# Constraint 14: The Norwegian lives next to the blue house
for i in range(N):
    if i > 0:
        solver.add(Implies(houses[i]['nationality'] == Norwegian, houses[i-1]['color'] == Blue))
    if i < N-1:
        solver.add(Implies(houses[i]['nationality'] == Norwegian, houses[i+1]['color'] == Blue))

# Constraint 15: The person who smokes Blends has a neighbor who drinks water
for i in range(N):
    if i > 0:
        solver.add(Implies(houses[i]['cigarette'] == Blends, houses[i-1]['drink'] == Water))
    if i < N-1:
        solver.add(Implies(houses[i]['cigarette'] == Blends, houses[i+1]['drink'] == Water))

# Check if the problem is satisfiable
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Extract the solution
    solution = []
    for i in range(N):
        house = {
            'house': i + 1,
            'color': str(model[houses[i]['color']]),
            'nationality': str(model[houses[i]['nationality']]),
            'drink': str(model[houses[i]['drink']]),
            'cigarette': str(model[houses[i]['cigarette']]).replace("_", " "),
            'pet': str(model[houses[i]['pet']])
        }
        solution.append(house)
    # Print the solution
    for house in solution:
        print(house)
    # Find the zebra owner
    for house in solution:
        if house['pet'] == 'Zebra':
            print(f"zebra_owner = {house['nationality']}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")