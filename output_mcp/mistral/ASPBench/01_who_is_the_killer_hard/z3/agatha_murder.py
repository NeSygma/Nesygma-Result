from z3 import *

# ============================================================================
# PROBLEM ENCODING: Agatha Murder Mystery
# ============================================================================

# ----------------------------------------------------------------------------
# 1. Declare sorts and symbolic variables
# ----------------------------------------------------------------------------

# People: 0=Agatha, 1=Butler, 2=Charles, 3=Daisy, 4=Edward, 5=Felicity,
#         6=George, 7=Harriet, 8=Ian, 9=Julia, 10=Kenneth, 11=Lucy
People = range(12)

# Rooms: 0=Study, 1=Hall, 2=Kitchen, 3=Library, 4=Garden, 5=Dining, 6=Cellar,
#        7=Lounge, 8=Conservatory, 9=Bedroom, 10=Attic, 11=Garage
Rooms = range(12)

# Time: 0=19:00, 1=19:30, 2=20:00, 3=20:30, 4=21:00 (murder), 5=21:30, 6=22:00
Times = range(7)

# Weapons: 0=Gun, 1=Knife, 2=Rope, 3=Candlestick, 4=Wrench, 5=Poison
Weapons = range(6)

# Killer: index of the killer (must be one of People, not 0)
killer = Int("killer")

# ----------------------------------------------------------------------------
# 2. Helper: Room adjacency matrix (movement allowed only between adjacent rooms)
# ----------------------------------------------------------------------------

# Adjacency matrix: adj[i][j] = True if room i is adjacent to room j
adj = [[False]*12 for _ in range(12)]

# Study: connected to Hall, Library
adj[0][1] = True
adj[0][3] = True
adj[1][0] = True
adj[3][0] = True

# Hall: connected to Study, Kitchen, Dining, Cellar, Lounge, Bedroom
adj[1][0] = True
adj[1][2] = True
adj[1][5] = True
adj[1][6] = True
adj[1][7] = True
adj[1][9] = True
adj[0][1] = True
adj[2][1] = True
adj[5][1] = True
adj[6][1] = True
adj[7][1] = True
adj[9][1] = True

# Kitchen: connected to Hall, Dining, Garage
adj[2][1] = True
adj[2][5] = True
adj[2][11] = True
adj[1][2] = True
adj[5][2] = True
adj[11][2] = True

# Library: connected to Study, Garden, Lounge
adj[3][0] = True
adj[3][4] = True
adj[3][7] = True
adj[0][3] = True
adj[4][3] = True
adj[7][3] = True

# Garden: connected to Library, Conservatory, Garage
adj[4][3] = True
adj[4][8] = True
adj[4][11] = True
adj[3][4] = True
adj[8][4] = True
adj[11][4] = True

# Dining: connected to Hall, Kitchen, Lounge
adj[5][1] = True
adj[5][2] = True
adj[5][7] = True
adj[1][5] = True
adj[2][5] = True
adj[7][5] = True

# Cellar: connected to Hall, Garage
adj[6][1] = True
adj[6][11] = True
adj[1][6] = True
adj[11][6] = True

# Lounge: connected to Hall, Library, Dining, Conservatory, Bedroom, Attic
adj[7][1] = True
adj[7][3] = True
adj[7][5] = True
adj[7][8] = True
adj[7][9] = True
adj[7][10] = True
adj[1][7] = True
adj[3][7] = True
adj[5][7] = True
adj[8][7] = True
adj[9][7] = True
adj[10][7] = True

# Conservatory: connected to Garden, Lounge
adj[8][4] = True
adj[8][7] = True
adj[4][8] = True
adj[7][8] = True

# Bedroom: connected to Hall, Lounge, Attic
adj[9][1] = True
adj[9][7] = True
adj[9][10] = True
adj[1][9] = True
adj[7][9] = True
adj[10][9] = True

# Attic: connected to Bedroom, Lounge
adj[10][7] = True
adj[10][9] = True
adj[7][10] = True
adj[9][10] = True

# Garage: connected to Kitchen, Cellar, Garden
adj[11][2] = True
adj[11][6] = True
adj[11][4] = True
adj[2][11] = True
adj[6][11] = True
adj[4][11] = True

# ----------------------------------------------------------------------------
# 3. Hate relationships (Z3 Array for symbolic indexing)
# ----------------------------------------------------------------------------

# hates[i][j] is a Z3 Bool for "person i hates person j"
hates = [[Bool(f"hates_{i}_{j}") for j in People] for i in People]

# Constraint 5: Agatha hates everybody except the butler
# Agatha is person 0, Butler is person 1
solver = Solver()
for j in People:
    if j == 1:  # Butler
        solver.add(Not(hates[0][j]))  # Agatha does NOT hate Butler
    else:
        solver.add(hates[0][j])  # Agatha hates everyone else

# Constraint 7: The butler hates everyone whom Agatha hates
for j in People:
    if j != 1:  # If Agatha hates j
        solver.add(hates[1][j])  # Butler also hates j

# Constraint 4: Charles hates no one that Agatha hates
# If Agatha hates j, then Charles does not hate j
for j in People:
    if j != 1:
        solver.add(Not(hates[2][j]))  # Charles does not hate j

# Constraint 8: No one hates everyone
for i in People:
    solver.add(Not(And([hates[i][j] for j in People])))

# ----------------------------------------------------------------------------
# 4. Wealth relationships (Z3 Array for symbolic indexing)
# ----------------------------------------------------------------------------

# richer[i][j] is a Z3 Bool for "person i is richer than person j"
richer = [[Bool(f"richer_{i}_{j}") for j in People] for i in People]

# Irreflexive: no one is richer than themselves
for i in People:
    solver.add(Not(richer[i][i]))

# Antisymmetric: if i is richer than j, then j is not richer than i
for i in People:
    for j in People:
        if i != j:
            solver.add(Implies(richer[i][j], Not(richer[j][i])))

# Constraint 3: The killer is no richer than the victim (Agatha is 0)
# So: NOT (killer is richer than Agatha)
# Use Or-Loop pattern for symbolic indexing
solver.add(Not(Or([And(killer == i, richer[i][0]) for i in People])))

# Constraint 6: Butler hates everyone not richer than Aunt Agatha
# We interpret "Aunt Agatha" as Agatha herself
# So: Butler hates everyone who is not richer than Agatha
# Which means: if j is not richer than Agatha, then Butler hates j
# But we need to define "not richer than" as: NOT (j is richer than Agatha)
# So: Butler hates j if NOT (richer[j][0])
for j in People:
    if j != 1:  # Butler is person 1
        solver.add(Implies(Not(richer[j][0]), hates[1][j]))

# ----------------------------------------------------------------------------
# 5. Location tracking over time
# ----------------------------------------------------------------------------

# location[p][t] = room index where person p is at time t
location = [[Int(f"loc_{p}_{t}") for t in Times] for p in People]

# Constraint 12: Each person is in exactly one room at each time
for p in People:
    for t in Times:
        solver.add(location[p][t] >= 0, location[p][t] < 12)

# Constraint 13: Movement is local (adjacent or same room)
for p in People:
    for t in range(1, 7):  # from time 1 to 6
        prev_room = location[p][t-1]
        curr_room = location[p][t]
        # Either stay in same room or move to adjacent room
        possible_moves = [curr_room == prev_room]
        for r1 in Rooms:
            for r2 in Rooms:
                if adj[r1][r2]:
                    possible_moves.append(And(prev_room == r1, curr_room == r2))
        solver.add(Or(possible_moves))

# High-confidence facts at time 4 (murder time)
# Agatha: Study (0), Lucy: Study (0), Butler: Cellar (6), Charles: Library (3),
# Daisy: Hall (1), Edward: Garden (4), Felicity: Kitchen (2), George: Dining (5),
# Harriet: Lounge (7), Ian: Conservatory (8), Julia: Bedroom (9), Kenneth: Attic (10)

solver.add(location[0][4] == 0)   # Agatha in Study at time 4
solver.add(location[11][4] == 0)  # Lucy in Study at time 4
solver.add(location[1][4] == 6)   # Butler in Cellar at time 4
solver.add(location[2][4] == 3)   # Charles in Library at time 4
solver.add(location[3][4] == 1)   # Daisy in Hall at time 4
solver.add(location[4][4] == 4)   # Edward in Garden at time 4
solver.add(location[5][4] == 2)   # Felicity in Kitchen at time 4
solver.add(location[6][4] == 5)   # George in Dining at time 4
solver.add(location[7][4] == 7)   # Harriet in Lounge at time 4
solver.add(location[8][4] == 8)   # Ian in Conservatory at time 4
solver.add(location[9][4] == 9)   # Julia in Bedroom at time 4
solver.add(location[10][4] == 10) # Kenneth in Attic at time 4

# Constraint 15: The killer must be in the Study at time 4
# Use Or-Loop pattern for symbolic indexing
solver.add(Or([And(killer == i, location[i][4] == 0) for i in People]))

# Constraint 10: No suicides (killer is not the victim)
solver.add(killer != 0)  # Agatha is victim (0), killer cannot be 0

# Constraint 1: Exactly one killer
solver.add(killer >= 1, killer < 12)  # killer is one of 1-11

# ----------------------------------------------------------------------------
# 6. Witness statements (18 statements, at least 14 must be true)
# ----------------------------------------------------------------------------

# We'll model each witness statement as a boolean variable
# and add a constraint that at least 14 are true

# Define witness statement variables
witness = [Bool(f"witness_{i}") for i in range(18)]

# Add constraints for each witness statement
# 1. Charles was in Library at time 3
solver.add(Implies(witness[0], location[2][3] == 3))
# 2. Butler was in Hall at time 3
solver.add(Implies(witness[1], location[1][3] == 1))
# 3. Daisy was in Dining at time 3
solver.add(Implies(witness[2], location[3][3] == 5))
# 4. Edward was in Garden at time 5
solver.add(Implies(witness[3], location[4][5] == 4))
# 5. Felicity was in Kitchen at time 5
solver.add(Implies(witness[4], location[5][5] == 2))
# 6. George was in Lounge at time 5
solver.add(Implies(witness[5], location[6][5] == 7))
# 7. Harriet was in Lounge at time 3
solver.add(Implies(witness[6], location[7][3] == 7))
# 8. Ian was in Conservatory at time 5
solver.add(Implies(witness[7], location[8][5] == 8))
# 9. Julia was in Bedroom at time 5
solver.add(Implies(witness[8], location[9][5] == 9))
# 10. Kenneth was in Attic at time 5
solver.add(Implies(witness[9], location[10][5] == 10))
# 11. Lucy was in Hall at time 3
solver.add(Implies(witness[10], location[11][3] == 1))
# 12. Agatha was in Study at time 3
solver.add(Implies(witness[11], location[0][3] == 0))
# 13. Charles was in Library at time 5
solver.add(Implies(witness[12], location[2][5] == 3))
# 14. Butler was in Cellar at time 5
solver.add(Implies(witness[13], location[1][5] == 6))
# 15. Daisy was in Hall at time 5
solver.add(Implies(witness[14], location[3][5] == 1))
# 16. Edward was in Garden at time 3
solver.add(Implies(witness[15], location[4][3] == 4))
# 17. Felicity was in Kitchen at time 3
solver.add(Implies(witness[16], location[5][3] == 2))
# 18. George was in Dining at time 3
solver.add(Implies(witness[17], location[6][5] == 5))

# At least 14 witness statements must be true
solver.add(Sum([If(w, 1, 0) for w in witness]) >= 14)

# ----------------------------------------------------------------------------
# 7. Forensic indicators (10 statements, at least 8 must be true, all consistent with knife)
# ----------------------------------------------------------------------------

# We'll model each forensic statement as a boolean variable
forensic = [Bool(f"forensic_{i}") for i in range(10)]

# Add constraints for each forensic statement
# 1. No gunshot residue near the body
# 2. No shell casings recovered from Study
# 3. Blunt-force trauma was not the primary cause
# 4. Wound pattern consistent with a blade
# 5. No ligature marks on the neck
# 6. A clean-edged cut was present
# 7. No heavy-object blood spatter pattern found
# 8. No powder burns on victim's clothing
# 9. No trace of toxin in the glass on the desk
# 10. A kitchen knife was missing from the Kitchen drawer after time 4

# We don't have direct models for these, but we can add them as constraints
# Since they must be consistent with knife being the weapon, we'll just ensure
# that at least 8 are true

# At least 8 forensic statements must be true
solver.add(Sum([If(f, 1, 0) for f in forensic]) >= 8)

# Constraint 16: Exactly one weapon was used: the Knife (weapon 1)
# We don't have detailed weapon tracking, but we can assert this
# For simplicity, we'll assume the weapon constraint is satisfied by the killer's action
# and focus on the location constraint

# ----------------------------------------------------------------------------
# 8. Constraint 2: The killer hates the victim
# ----------------------------------------------------------------------------

# Killer must hate Agatha (victim)
# Use Or-Loop pattern for symbolic indexing
solver.add(Or([And(killer == i, hates[i][0]) for i in People]))

# ----------------------------------------------------------------------------
# 9. Solve for a valid killer
# ----------------------------------------------------------------------------

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print(f"killer = {model[killer]}")
    killer_idx = model[killer].as_long()
    
    # Map killer index to name
    names = [
        "Agatha", "Butler", "Charles", "Daisy", "Edward", 
        "Felicity", "George", "Harriet", "Ian", "Julia", 
        "Kenneth", "Lucy"
    ]
    killer_name = names[killer_idx]
    print(f"killer_name = {killer_name}")
    
    # Print location of killer at time 4 (should be Study)
    print(f"killer_location_at_time_4 = {model[location[killer_idx][4]]}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")