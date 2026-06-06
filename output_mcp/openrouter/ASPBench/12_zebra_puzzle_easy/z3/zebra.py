from z3 import *

# Enumerations
colors = ["Red", "Green", "White", "Yellow", "Blue"]
nationalities = ["Brit", "Swede", "Dane", "Norwegian", "German"]
drinks = ["Tea", "Coffee", "Milk", "Beer", "Water"]
cigarettes = ["Pall Mall", "Dunhill", "Blends", "Blue Master", "Prince"]
pets = ["Dog", "Birds", "Cats", "Horse", "Zebra"]

# Index helpers
R, G, W, Y, B = range(5)  # colors indices
Brit, Swede, Dane, Norwegian, German = range(5)
Tea, Coffee, Milk, Beer, Water = range(5)
PallMall, Dunhill, Blends, BlueMaster, Prince = range(5)
Dog, Birds, Cats, Horse, Zebra = range(5)

solver = Solver()

# Variables per house (0..4 for houses 1..5)
col = [Int(f"col_{i}") for i in range(5)]
nat = [Int(f"nat_{i}") for i in range(5)]
dr = [Int(f"dr_{i}") for i in range(5)]
cig = [Int(f"cig_{i}") for i in range(5)]
pet = [Int(f"pet_{i}") for i in range(5)]

vars_lists = [col, nat, dr, cig, pet]
for lst in vars_lists:
    for v in lst:
        solver.add(v >= 0, v < 5)
    solver.add(Distinct(lst))

# 1. Brit lives in red house
for i in range(5):
    solver.add(Implies(nat[i] == Brit, col[i] == R))
# 2. Swede keeps dogs
for i in range(5):
    solver.add(Implies(nat[i] == Swede, pet[i] == Dog))
# 3. Dane drinks tea
for i in range(5):
    solver.add(Implies(nat[i] == Dane, dr[i] == Tea))
# 4. Green house is left of white house (adjacent)
adjacent_green_white = []
for i in range(4):
    adjacent_green_white.append(And(col[i] == G, col[i+1] == W))
solver.add(Or(adjacent_green_white))
# 5. Green house's owner drinks coffee
for i in range(5):
    solver.add(Implies(col[i] == G, dr[i] == Coffee))
# 6. Pall Mall -> birds
for i in range(5):
    solver.add(Implies(cig[i] == PallMall, pet[i] == Birds))
# 7. Yellow house -> Dunhill
for i in range(5):
    solver.add(Implies(col[i] == Y, cig[i] == Dunhill))
# 8. Center house drinks milk (house 3 -> index 2)
solver.add(dr[2] == Milk)
# 9. Norwegian lives in first house (index 0)
solver.add(nat[0] == Norwegian)
# 10. Blends next to cats
for i in range(5):
    neighbor_cats = []
    if i > 0:
        neighbor_cats.append(pet[i-1] == Cats)
    if i < 4:
        neighbor_cats.append(pet[i+1] == Cats)
    solver.add(Implies(cig[i] == Blends, Or(neighbor_cats)))
# 11. Horse next to Dunhill
for i in range(5):
    neighbor_dunhill = []
    if i > 0:
        neighbor_dunhill.append(cig[i-1] == Dunhill)
    if i < 4:
        neighbor_dunhill.append(cig[i+1] == Dunhill)
    solver.add(Implies(pet[i] == Horse, Or(neighbor_dunhill)))
# 12. Blue Master drinks beer
for i in range(5):
    solver.add(Implies(cig[i] == BlueMaster, dr[i] == Beer))
# 13. German smokes Prince
for i in range(5):
    solver.add(Implies(nat[i] == German, cig[i] == Prince))
# 14. Norwegian lives next to blue house
# Norwegian is at house 0, so house 1 must be blue
solver.add(col[1] == B)
# 15. Blends neighbor drinks water
for i in range(5):
    neighbor_water = []
    if i > 0:
        neighbor_water.append(dr[i-1] == Water)
    if i < 4:
        neighbor_water.append(dr[i+1] == Water)
    solver.add(Implies(cig[i] == Blends, Or(neighbor_water)))

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Build solution list
    solution = []
    zebra_owner = None
    for i in range(5):
        house_num = i+1
        col_val = m[col[i]].as_long()
        nat_val = m[nat[i]].as_long()
        dr_val = m[dr[i]].as_long()
        cig_val = m[cig[i]].as_long()
        pet_val = m[pet[i]].as_long()
        if pet_val == Zebra:
            zebra_owner = nationalities[nat_val]
        solution.append({
            "house": house_num,
            "color": colors[col_val],
            "nationality": nationalities[nat_val],
            "drink": drinks[dr_val],
            "cigarette": cigarettes[cig_val],
            "pet": pets[pet_val]
        })
    # Print solution in order
    for house in solution:
        print(house)
    print("zebra_owner:", zebra_owner)
else:
    print("STATUS: unsat")