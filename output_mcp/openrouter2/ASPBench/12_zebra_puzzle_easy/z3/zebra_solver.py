from z3 import *

# Domain size
N = 5

# Enumerations
colors = ["Red","Green","White","Yellow","Blue"]
nationalities = ["Brit","Swede","Dane","Norwegian","German"]
drinks = ["Tea","Coffee","Milk","Beer","Water"]
cigarettes = ["Pall Mall","Dunhill","Blends","Blue Master","Prince"]
pets = ["Dog","Birds","Cats","Horse","Zebra"]

# Indices
Brit, Swede, Dane, Norwegian, German = 0,1,2,3,4
Red, Green, White, Yellow, Blue = 0,1,2,3,4
Tea, Coffee, Milk, Beer, Water = 0,1,2,3,4
PallMall, Dunhill, Blends, BlueMaster, Prince = 0,1,2,3,4
Dog, Birds, Cats, Horse, Zebra = 0,1,2,3,4

# Solver
solver = Solver()

# Variables per house
color = [Int(f"color_{i}") for i in range(N)]
nat = [Int(f"nat_{i}") for i in range(N)]
drink = [Int(f"drink_{i}") for i in range(N)]
cig = [Int(f"cig_{i}") for i in range(N)]
pet = [Int(f"pet_{i}") for i in range(N)]

# Domain constraints
for var in color + nat + drink + cig + pet:
    solver.add(var >= 0, var < N)

# Distinctness
solver.add(Distinct(color))
solver.add(Distinct(nat))
solver.add(Distinct(drink))
solver.add(Distinct(cig))
solver.add(Distinct(pet))

# 1. Brit lives in the red house
for i in range(N):
    solver.add(Implies(nat[i] == Brit, color[i] == Red))
    solver.add(Implies(color[i] == Red, nat[i] == Brit))

# 2. Swede keeps dogs
for i in range(N):
    solver.add(Implies(nat[i] == Swede, pet[i] == Dog))
    solver.add(Implies(pet[i] == Dog, nat[i] == Swede))

# 3. Dane drinks tea
for i in range(N):
    solver.add(Implies(nat[i] == Dane, drink[i] == Tea))
    solver.add(Implies(drink[i] == Tea, nat[i] == Dane))

# 4. Green house is on the left of the white house (adjacent)
for i in range(N-1):
    solver.add(Implies(color[i] == Green, color[i+1] == White))
    solver.add(Implies(color[i+1] == White, color[i] == Green))

# 5. Green house's owner drinks coffee
for i in range(N):
    solver.add(Implies(color[i] == Green, drink[i] == Coffee))
    solver.add(Implies(drink[i] == Coffee, color[i] == Green))

# 6. Pall Mall rears birds
for i in range(N):
    solver.add(Implies(cig[i] == PallMall, pet[i] == Birds))
    solver.add(Implies(pet[i] == Birds, cig[i] == PallMall))

# 7. Yellow house smokes Dunhill
for i in range(N):
    solver.add(Implies(color[i] == Yellow, cig[i] == Dunhill))
    solver.add(Implies(cig[i] == Dunhill, color[i] == Yellow))

# 8. Center house drinks milk
solver.add(drink[2] == Milk)

# 9. Norwegian lives in the first house
solver.add(nat[0] == Norwegian)

# 10. Blends lives next to cats
for i in range(N):
    neighbors = [j for j in [i-1, i+1] if 0 <= j < N]
    solver.add(Implies(cig[i] == Blends, Or([pet[j] == Cats for j in neighbors])))

# 11. Horse lives next to Dunhill
for i in range(N):
    neighbors = [j for j in [i-1, i+1] if 0 <= j < N]
    solver.add(Implies(pet[i] == Horse, Or([cig[j] == Dunhill for j in neighbors])))

# 12. Blue Master drinks beer
for i in range(N):
    solver.add(Implies(cig[i] == BlueMaster, drink[i] == Beer))
    solver.add(Implies(drink[i] == Beer, cig[i] == BlueMaster))

# 13. German smokes Prince
for i in range(N):
    solver.add(Implies(nat[i] == German, cig[i] == Prince))
    solver.add(Implies(cig[i] == Prince, nat[i] == German))

# 14. Norwegian lives next to blue house
for i in range(N):
    neighbors = [j for j in [i-1, i+1] if 0 <= j < N]
    solver.add(Implies(nat[i] == Norwegian, Or([color[j] == Blue for j in neighbors])))

# 15. Blends has neighbor who drinks water
for i in range(N):
    neighbors = [j for j in [i-1, i+1] if 0 <= j < N]
    solver.add(Implies(cig[i] == Blends, Or([drink[j] == Water for j in neighbors])))

# Solve
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("solution:")
    for i in range(N):
        h = i+1
        c = colors[m[color[i]].as_long()]
        n = nationalities[m[nat[i]].as_long()]
        d = drinks[m[drink[i]].as_long()]
        ci = cigarettes[m[cig[i]].as_long()]
        p = pets[m[pet[i]].as_long()]
        print(f"{{house: {h}, color: {c}, nationality: {n}, drink: {d}, cigarette: {ci}, pet: {p}}}")
    # Zebra owner
    zebra_house = None
    for i in range(N):
        if m[pet[i]].as_long() == Zebra:
            zebra_house = i
            break
    zebra_owner = nationalities[m[nat[zebra_house]].as_long()]
    print(f"zebra_owner: {zebra_owner}")
else:
    print("STATUS: unsat")
    if result == unsat:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")