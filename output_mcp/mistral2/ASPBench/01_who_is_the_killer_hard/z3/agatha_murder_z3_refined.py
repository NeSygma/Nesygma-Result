from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# --- Declare symbolic variables ---
# People: 0=Agatha, 1=Butler, 2=Charles, 3=Daisy, 4=Edward, 5=Felicity, 6=George, 7=Harriet, 8=Ian, 9=Julia, 10=Kenneth, 11=Lucy
# Rooms: 0=Study, 1=Hall, 2=Kitchen, 3=Library, 4=Garden, 5=Dining, 6=Cellar, 7=Lounge, 8=Conservatory, 9=Bedroom, 10=Attic, 11=Garage
# Times: 0=19:00, 1=19:30, 2=20:00, 3=20:30, 4=21:00 (murder time), 5=21:30, 6=22:00
# Weapons: 0=Gun, 1=Knife, 2=Rope, 3=Candlestick, 4=Wrench, 5=Poison

# Killer
killer = Int('killer')

# Location: location[p][t] = room index for person p at time t
location = [[Int(f"location_{p}_{t}") for t in range(7)] for p in range(12)]

# Weapon used (must be 1 for Knife)
weapon = Int('weapon')

# Hate relations: hates[p1][p2] = True if p1 hates p2
hates = [[Bool(f"hates_{p1}_{p2}") for p2 in range(12)] for p1 in range(12)]

# Richer relations: richer[p1][p2] = True if p1 is richer than p2
richer = [[Bool(f"richer_{p1}_{p2}") for p2 in range(12)] for p1 in range(12)]

# --- Helper: Room adjacency ---
adjacent = {}
adjacent[0] = [1, 3]  # Study: Hall, Library
adjacent[1] = [0, 2, 5, 6, 7, 9]  # Hall: Study, Kitchen, Dining, Cellar, Lounge, Bedroom
adjacent[2] = [1, 5, 11]  # Kitchen: Hall, Dining, Garage
adjacent[3] = [0, 4, 7]  # Library: Study, Garden, Lounge
adjacent[4] = [3, 8, 11]  # Garden: Library, Conservatory, Garage
adjacent[5] = [1, 2, 7]  # Dining: Hall, Kitchen, Lounge
adjacent[6] = [1, 11]  # Cellar: Hall, Garage
adjacent[7] = [1, 3, 5, 8, 9, 10]  # Lounge: Hall, Library, Dining, Conservatory, Bedroom, Attic
adjacent[8] = [4, 7]  # Conservatory: Garden, Lounge
adjacent[9] = [1, 7, 10]  # Bedroom: Hall, Lounge, Attic
adjacent[10] = [7, 9]  # Attic: Lounge, Bedroom
adjacent[11] = [2, 4, 6]  # Garage: Kitchen, Cellar, Garden

# --- Constraints ---
solver = Solver()

# 1. Exactly one killer (not Agatha, not suicide)
solver.add(killer != 0)  # Not Agatha
solver.add(killer >= 1, killer <= 11)  # Killer is one of the 12 people

# 2. Killer must be in Study at time 4 (murder time)
for p in range(12):
    solver.add(Implies(killer == p, location[p][4] == 0))

# 3. Exactly one weapon: Knife (1)
solver.add(weapon == 1)

# 4. Each person is in exactly one room at each time
for p in range(12):
    for t in range(7):
        solver.add(location[p][t] >= 0, location[p][t] <= 11)

# 5. Movement constraints: from time T-1 to T, a person either stays or moves to an adjacent room
for p in range(12):
    for t in range(1, 7):
        possible_moves = [location[p][t] == location[p][t-1]]
        for r1 in range(12):
            for r2 in adjacent[r1]:
                possible_moves.append(And(location[p][t-1] == r1, location[p][t] == r2))
        solver.add(Or(possible_moves))

# 6. High-confidence location facts at time 4 (murder time)
high_confidence = [
    (0, 0),  # Agatha: Study
    (11, 0), # Lucy: Study
    (1, 6),  # Butler: Cellar
    (2, 3),  # Charles: Library
    (3, 1),  # Daisy: Hall
    (4, 4),  # Edward: Garden
    (5, 2),  # Felicity: Kitchen
    (6, 5),  # George: Dining
    (7, 7),  # Harriet: Lounge
    (8, 8),  # Ian: Conservatory
    (9, 9),  # Julia: Bedroom
    (10, 10) # Kenneth: Attic
]
for p, r in high_confidence:
    solver.add(location[p][4] == r)

# 7. Medium-reliability witness statements (at least 14 of 18 must be true)
witness_statements = [
    (2, 3, 3),  # Charles was in Library at time 3
    (1, 1, 3),  # Butler was in Hall at time 3
    (3, 5, 3),  # Daisy was in Dining at time 3
    (4, 4, 5),  # Edward was in Garden at time 5
    (5, 2, 5),  # Felicity was in Kitchen at time 5
    (6, 7, 5),  # George was in Lounge at time 5
    (7, 7, 3),  # Harriet was in Lounge at time 3
    (8, 8, 5),  # Ian was in Conservatory at time 5
    (9, 9, 5),  # Julia was in Bedroom at time 5
    (10, 10, 5), # Kenneth was in Attic at time 5
    (11, 1, 3), # Lucy was in Hall at time 3
    (0, 0, 3),  # Agatha was in Study at time 3
    (2, 3, 5),  # Charles was in Library at time 5
    (1, 6, 5),  # Butler was in Cellar at time 5
    (3, 1, 5),  # Daisy was in Hall at time 5
    (4, 4, 3),  # Edward was in Garden at time 3
    (5, 2, 3),  # Felicity was in Kitchen at time 3
    (6, 5, 3)   # George was in Dining at time 3
]

# At least 14 of 18 witness statements must be true
witness_true = [Bool(f"witness_true_{i}") for i in range(18)]
for i, (p, r, t) in enumerate(witness_statements):
    solver.add(Implies(witness_true[i], location[p][t] == r))
    solver.add(Implies(Not(witness_true[i]), location[p][t] != r))

solver.add(Sum(witness_true) >= 14)

# 8. Forensic indicators (at least 8 of 10 must be true, all consistent with knife)
forensic_true = [Bool(f"forensic_true_{i}") for i in range(10)]

# 1. No gunshot residue near the body -> not Gun
solver.add(Implies(forensic_true[0], weapon != 0))
# 2. No shell casings recovered from Study -> not Gun
solver.add(Implies(forensic_true[1], weapon != 0))
# 3. Blunt-force trauma was not the primary cause -> not Rope
solver.add(Implies(forensic_true[2], weapon != 2))
# 4. Wound pattern consistent with a blade -> Knife
solver.add(Implies(forensic_true[3], weapon == 1))
# 5. No ligature marks on the neck -> not Rope
solver.add(Implies(forensic_true[4], weapon != 2))
# 6. A clean-edged cut was present -> Knife
solver.add(Implies(forensic_true[5], weapon == 1))
# 7. No heavy-object blood spatter pattern found -> not Candlestick
solver.add(Implies(forensic_true[6], weapon != 3))
# 8. No powder burns on victim's clothing -> not Gun
solver.add(Implies(forensic_true[7], weapon != 0))
# 9. No trace of toxin in the glass on the desk -> not Poison
solver.add(Implies(forensic_true[8], weapon != 5))
# 10. A kitchen knife was missing from the Kitchen drawer after time 4 -> Knife
solver.add(Implies(forensic_true[9], weapon == 1))

solver.add(Sum(forensic_true) >= 8)

# 9. Hate relations constraints
# Agatha hates everybody except the Butler
solver.add(hates[0][0] == False)  # Agatha does not hate herself
solver.add(hates[0][1] == False)  # Agatha does not hate Butler
for p in range(2, 12):
    solver.add(hates[0][p] == True)  # Agatha hates everyone else

# Butler hates everyone not richer than Aunt Agatha and everyone Agatha hates
# (Note: "Aunt Agatha" is not defined; assuming it means Agatha)
for p in range(12):
    # Butler hates everyone Agatha hates
    solver.add(hates[1][p] == hates[0][p])
    # Butler hates everyone not richer than Agatha
    solver.add(Implies(Not(richer[p][0]), hates[1][p]))  # If p is not richer than Agatha, Butler hates p

# Charles hates no one that Agatha hates
for p in range(12):
    solver.add(Implies(hates[0][p], Not(hates[2][p])))

# No one hates everyone
for p in range(12):
    solver.add(Not(And([hates[p][q] for q in range(12)])))

# 10. Wealth relations: irreflexive and antisymmetric
for p in range(12):
    solver.add(Not(richer[p][p]))  # Irreflexive
for p in range(12):
    for q in range(12):
        solver.add(Implies(And(richer[p][q], richer[q][p]), False))  # Antisymmetric

# 11. Killer hates the victim (Agatha)
for p in range(12):
    solver.add(Implies(killer == p, hates[p][0] == True))

# 12. Killer is no richer than the victim (Agatha)
for p in range(12):
    solver.add(Implies(killer == p, Not(richer[p][0])))

# --- Check and print result ---
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("Killer index:", model[killer])
    killer_idx = model[killer].as_long()
    names = ["Agatha", "Butler", "Charles", "Daisy", "Edward", "Felicity", "George", "Harriet", "Ian", "Julia", "Kenneth", "Lucy"]
    print("Killer name:", names[killer_idx])
    print("Weapon used:", model[weapon])
    print("Forensic indicators true:", [is_true(model[forensic_true[i]]) for i in range(10)])
    print("Witness statements true:", [is_true(model[witness_true[i]]) for i in range(18)])
    print("Hate matrix (first 3 people):")
    for p in range(3):
        print(["T" if is_true(model[hates[p][q]]) else "F" for q in range(12)])
    print("Richer matrix (first 3 people):")
    for p in range(3):
        print(["T" if is_true(model[richer[p][q]]) else "F" for q in range(12)])
    print("Location of killer at time 4:", model[location[killer_idx][4]])
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")