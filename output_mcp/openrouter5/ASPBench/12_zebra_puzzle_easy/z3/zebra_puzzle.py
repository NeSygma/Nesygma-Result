from z3 import *

solver = Solver()

# Houses are numbered 1 to 5
HOUSES = list(range(5))  # 0-indexed internally, but we'll map 0->1, 1->2, etc.

# Colors
Red, Green, White, Yellow, Blue = 0, 1, 2, 3, 4
colors = [Int(f"color_{i}") for i in range(5)]
for i in range(5):
    solver.add(colors[i] >= 0, colors[i] <= 4)
solver.add(Distinct(colors))

# Nationalities
Brit, Swede, Dane, Norwegian, German = 0, 1, 2, 3, 4
nationalities = [Int(f"nationality_{i}") for i in range(5)]
for i in range(5):
    solver.add(nationalities[i] >= 0, nationalities[i] <= 4)
solver.add(Distinct(nationalities))

# Drinks
Tea, Coffee, Milk, Beer, Water = 0, 1, 2, 3, 4
drinks = [Int(f"drink_{i}") for i in range(5)]
for i in range(5):
    solver.add(drinks[i] >= 0, drinks[i] <= 4)
solver.add(Distinct(drinks))

# Cigarettes
PallMall, Dunhill, Blends, BlueMaster, Prince = 0, 1, 2, 3, 4
cigarettes = [Int(f"cigarette_{i}") for i in range(5)]
for i in range(5):
    solver.add(cigarettes[i] >= 0, cigarettes[i] <= 4)
solver.add(Distinct(cigarettes))

# Pets
Dog, Birds, Cats, Horse, Zebra = 0, 1, 2, 3, 4
pets = [Int(f"pet_{i}") for i in range(5)]
for i in range(5):
    solver.add(pets[i] >= 0, pets[i] <= 4)
solver.add(Distinct(pets))

# Helper: position of a value in a list
def pos_of(val, lst):
    """Return the index i such that lst[i] == val"""
    return [i for i in range(5) if lst[i] == val][0]

# But we can't use Python pos_of with symbolic values. Use constraints instead.

# 1. The Brit lives in the red house
for i in range(5):
    solver.add(Implies(nationalities[i] == Brit, colors[i] == Red))
    solver.add(Implies(colors[i] == Red, nationalities[i] == Brit))

# 2. The Swede keeps dogs as pets
for i in range(5):
    solver.add(Implies(nationalities[i] == Swede, pets[i] == Dog))
    solver.add(Implies(pets[i] == Dog, nationalities[i] == Swede))

# 3. The Dane drinks tea
for i in range(5):
    solver.add(Implies(nationalities[i] == Dane, drinks[i] == Tea))
    solver.add(Implies(drinks[i] == Tea, nationalities[i] == Dane))

# 4. The green house is on the left of the white house (directly adjacent)
for i in range(4):
    solver.add(Implies(And(colors[i] == Green, colors[i+1] == White), True))
# Enforce: there exists i such that colors[i]==Green and colors[i+1]==White
solver.add(Or([And(colors[i] == Green, colors[i+1] == White) for i in range(4)]))

# 5. The green house's owner drinks coffee
for i in range(5):
    solver.add(Implies(colors[i] == Green, drinks[i] == Coffee))
    solver.add(Implies(drinks[i] == Coffee, colors[i] == Green))

# 6. The person who smokes Pall Mall rears birds
for i in range(5):
    solver.add(Implies(cigarettes[i] == PallMall, pets[i] == Birds))
    solver.add(Implies(pets[i] == Birds, cigarettes[i] == PallMall))

# 7. The owner of the yellow house smokes Dunhill
for i in range(5):
    solver.add(Implies(colors[i] == Yellow, cigarettes[i] == Dunhill))
    solver.add(Implies(cigarettes[i] == Dunhill, colors[i] == Yellow))

# 8. The person living in the center house (house 3) drinks milk
# House 3 is index 2 (0-indexed)
solver.add(drinks[2] == Milk)

# 9. The Norwegian lives in the first house (house 1)
solver.add(nationalities[0] == Norwegian)

# 10. The person who smokes Blends lives next to the one who keeps cats
solver.add(Or([
    And(cigarettes[i] == Blends, 
        Or([And(j >= 0, j < 5, abs(i-j) == 1, pets[j] == Cats) for j in range(5)]))
    for i in range(5)
]))

# 11. The person who keeps a horse lives next to the person who smokes Dunhill
solver.add(Or([
    And(pets[i] == Horse,
        Or([And(j >= 0, j < 5, abs(i-j) == 1, cigarettes[j] == Dunhill) for j in range(5)]))
    for i in range(5)
]))

# 12. The owner who smokes Blue Master drinks beer
for i in range(5):
    solver.add(Implies(cigarettes[i] == BlueMaster, drinks[i] == Beer))
    solver.add(Implies(drinks[i] == Beer, cigarettes[i] == BlueMaster))

# 13. The German smokes Prince
for i in range(5):
    solver.add(Implies(nationalities[i] == German, cigarettes[i] == Prince))
    solver.add(Implies(cigarettes[i] == Prince, nationalities[i] == German))

# 14. The Norwegian lives next to the blue house
solver.add(Or([
    And(nationalities[i] == Norwegian,
        Or([And(j >= 0, j < 5, abs(i-j) == 1, colors[j] == Blue) for j in range(5)]))
    for i in range(5)
]))

# 15. The person who smokes Blends has a neighbor who drinks water
solver.add(Or([
    And(cigarettes[i] == Blends,
        Or([And(j >= 0, j < 5, abs(i-j) == 1, drinks[j] == Water) for j in range(5)]))
    for i in range(5)
]))

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    color_names = ["Red", "Green", "White", "Yellow", "Blue"]
    nationality_names = ["Brit", "Swede", "Dane", "Norwegian", "German"]
    drink_names = ["Tea", "Coffee", "Milk", "Beer", "Water"]
    cigarette_names = ["Pall Mall", "Dunhill", "Blends", "Blue Master", "Prince"]
    pet_names = ["Dog", "Birds", "Cats", "Horse", "Zebra"]
    
    for i in range(5):
        c = m[colors[i]].as_long()
        n = m[nationalities[i]].as_long()
        d = m[drinks[i]].as_long()
        ci = m[cigarettes[i]].as_long()
        p = m[pets[i]].as_long()
        print(f"House {i+1}: Color={color_names[c]}, Nationality={nationality_names[n]}, Drink={drink_names[d]}, Cigarette={cigarette_names[ci]}, Pet={pet_names[p]}")
    
    # Find zebra owner
    for i in range(5):
        if m[pets[i]].as_long() == Zebra:
            owner_nat = m[nationalities[i]].as_long()
            print(f"\nThe {nationality_names[owner_nat]} owns the zebra.")
            print(f"answer:{nationality_names[owner_nat]}")
            break
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")