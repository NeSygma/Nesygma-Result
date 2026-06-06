from z3 import *

# ============================================================
# DATA
# ============================================================
PEOPLE = 12
ROOMS = 12
TIMES = 7
WEAPONS = 6

MURDER_TIME = 4
MURDER_ROOM = 0  # Study
MURDER_WEAPON = 1  # Knife

# Names
person_names = ["Agatha", "Butler", "Charles", "Daisy", "Edward", "Felicity",
                "George", "Harriet", "Ian", "Julia", "Kenneth", "Lucy"]
room_names = ["Study", "Hall", "Kitchen", "Library", "Garden", "Dining",
              "Cellar", "Lounge", "Conservatory", "Bedroom", "Attic", "Garage"]

# Room adjacency (undirected)
adj = {
    0: [1, 3],          # Study: Hall, Library
    1: [0, 2, 5, 6, 7, 9],  # Hall: Study, Kitchen, Dining, Cellar, Lounge, Bedroom
    2: [1, 5, 11],      # Kitchen: Hall, Dining, Garage
    3: [0, 4, 7],       # Library: Study, Garden, Lounge
    4: [3, 8, 11],      # Garden: Library, Conservatory, Garage
    5: [1, 2, 7],       # Dining: Hall, Kitchen, Lounge
    6: [1, 11],         # Cellar: Hall, Garage
    7: [1, 3, 5, 8, 9, 10],  # Lounge: Hall, Library, Dining, Conservatory, Bedroom, Attic
    8: [4, 7],          # Conservatory: Garden, Lounge
    9: [1, 7, 10],      # Bedroom: Hall, Lounge, Attic
    10: [9, 7],         # Attic: Bedroom, Lounge
    11: [2, 6, 4]       # Garage: Kitchen, Cellar, Garden
}

# High-confidence locations at time 4
high_conf = {
    0: 0,   # Agatha: Study
    11: 0,  # Lucy: Study
    1: 6,   # Butler: Cellar
    2: 3,   # Charles: Library
    3: 1,   # Daisy: Hall
    4: 4,   # Edward: Garden
    5: 2,   # Felicity: Kitchen
    6: 5,   # George: Dining
    7: 7,   # Harriet: Lounge
    8: 8,   # Ian: Conservatory
    9: 9,   # Julia: Bedroom
    10: 10  # Kenneth: Attic
}

# Witness statements: (person, time, room)
witnesses = [
    (2, 3, 3),   # 1: Charles in Library at t3
    (1, 3, 1),   # 2: Butler in Hall at t3
    (3, 3, 5),   # 3: Daisy in Dining at t3
    (4, 5, 4),   # 4: Edward in Garden at t5
    (5, 5, 2),   # 5: Felicity in Kitchen at t5
    (6, 5, 7),   # 6: George in Lounge at t5
    (7, 3, 7),   # 7: Harriet in Lounge at t3
    (8, 5, 8),   # 8: Ian in Conservatory at t5
    (9, 5, 9),   # 9: Julia in Bedroom at t5
    (10, 5, 10), # 10: Kenneth in Attic at t5
    (11, 3, 1),  # 11: Lucy in Hall at t3
    (0, 3, 0),   # 12: Agatha in Study at t3
    (2, 5, 3),   # 13: Charles in Library at t5
    (1, 5, 6),   # 14: Butler in Cellar at t5
    (3, 5, 1),   # 15: Daisy in Hall at t5
    (4, 3, 4),   # 16: Edward in Garden at t3
    (5, 3, 2),   # 17: Felicity in Kitchen at t3
    (6, 3, 5),   # 18: George in Dining at t3
]

# ============================================================
# SYMBOLIC VARIABLES
# ============================================================
solver = Solver()

# Use Z3 Array for location to allow symbolic indexing
location = [[Int(f"loc_{p}_{t}") for t in range(TIMES)] for p in range(PEOPLE)]

# killer variable
killer = Int('killer')

# hates[p1][p2] = True if p1 hates p2
hates = [[Bool(f"hates_{p1}_{p2}") for p2 in range(PEOPLE)] for p1 in range(PEOPLE)]

# richer[p1][p2] = True if p1 is richer than p2
richer = [[Bool(f"richer_{p1}_{p2}") for p2 in range(PEOPLE)] for p1 in range(PEOPLE)]

# ============================================================
# DOMAIN CONSTRAINTS
# ============================================================

# Location domain: each location is 0..ROOMS-1
for p in range(PEOPLE):
    for t in range(TIMES):
        solver.add(And(location[p][t] >= 0, location[p][t] < ROOMS))

# Killer domain
solver.add(And(killer >= 0, killer < PEOPLE))

# ============================================================
# CONSTRAINT 12: Each person in exactly one room at each time
# (already enforced by single integer variable per person per time)

# CONSTRAINT 13: Movement is local (adjacent or stay)
for p in range(PEOPLE):
    for t in range(1, TIMES):
        prev_room = location[p][t-1]
        curr_room = location[p][t]
        constraints = []
        for r in range(ROOMS):
            allowed = [r] + adj[r]
            constraints.append(Implies(prev_room == r, Or([curr_room == a for a in allowed])))
        solver.add(And(constraints))

# CONSTRAINT 14: Murder occurred in Study at time 4
solver.add(location[0][MURDER_TIME] == MURDER_ROOM)

# CONSTRAINT 15: Killer must be in Study at time 4
# Use Or-loop pattern since killer is symbolic
solver.add(Or([And(killer == p, location[p][MURDER_TIME] == MURDER_ROOM) for p in range(PEOPLE)]))

# CONSTRAINT 16: Exactly one weapon used: Knife (weapon index 1)
# Already given as fact.

# CONSTRAINT 1: Exactly one killer (single integer variable)

# CONSTRAINT 2: The killer hates the victim
solver.add(Or([And(killer == p, hates[p][0] == True) for p in range(PEOPLE)]))

# CONSTRAINT 3: The killer is no richer than the victim (not strictly richer)
solver.add(Or([And(killer == p, Not(richer[p][0])) for p in range(PEOPLE)]))

# CONSTRAINT 4: Charles hates no one that Agatha hates
for p in range(PEOPLE):
    solver.add(Implies(hates[0][p], Not(hates[2][p])))

# CONSTRAINT 5: Agatha hates everybody except the butler
for p in range(PEOPLE):
    if p != 1:
        solver.add(hates[0][p] == True)
    else:
        solver.add(hates[0][p] == False)

# CONSTRAINT 6: The butler hates everyone not richer than Aunt Agatha
for p in range(PEOPLE):
    solver.add(Implies(Not(richer[p][0]), hates[1][p]))

# CONSTRAINT 7: The butler hates everyone whom Agatha hates
for p in range(PEOPLE):
    solver.add(Implies(hates[0][p], hates[1][p]))

# CONSTRAINT 8: No one hates everyone
for p1 in range(PEOPLE):
    solver.add(Or([Not(hates[p1][p2]) for p2 in range(PEOPLE)]))

# CONSTRAINT 9: Agatha is the victim (already encoded)

# CONSTRAINT 10: No suicides (killer != victim)
solver.add(killer != 0)

# CONSTRAINT 11: Wealth relations (richer) are irreflexive and antisymmetric
for p in range(PEOPLE):
    solver.add(Not(richer[p][p]))
for p1 in range(PEOPLE):
    for p2 in range(PEOPLE):
        if p1 != p2:
            solver.add(Implies(richer[p1][p2], Not(richer[p2][p1])))

# ============================================================
# HIGH-CONFIDENCE LOCATION FACTS AT TIME 4
# ============================================================
for p, r in high_conf.items():
    solver.add(location[p][MURDER_TIME] == r)

# ============================================================
# WITNESS STATEMENTS (at least 14 of 18 must be true)
# ============================================================
witness_vars = [Bool(f"w_{i}") for i in range(len(witnesses))]
for i, (p, t, r) in enumerate(witnesses):
    solver.add(witness_vars[i] == (location[p][t] == r))

solver.add(Sum([If(w, 1, 0) for w in witness_vars]) >= 14)

# ============================================================
# FORENSIC INDICATORS (at least 8 of 10 must be true)
# ============================================================
forensic_vars = [Bool(f"forensic_{i}") for i in range(10)]

# All are consistent with knife, so they can all be true
solver.add(forensic_vars[0] == True)  # No gunshot residue
solver.add(forensic_vars[1] == True)  # No shell casings
solver.add(forensic_vars[2] == True)  # No blunt-force trauma
solver.add(forensic_vars[3] == True)  # Wound consistent with blade
solver.add(forensic_vars[4] == True)  # No ligature marks
solver.add(forensic_vars[5] == True)  # Clean-edged cut
solver.add(forensic_vars[6] == True)  # No heavy-object blood spatter
solver.add(forensic_vars[7] == True)  # No powder burns
solver.add(forensic_vars[8] == True)  # No toxin in glass
solver.add(forensic_vars[9] == True)  # Kitchen knife missing

solver.add(Sum([If(f, 1, 0) for f in forensic_vars]) >= 8)

# ============================================================
# SOLVE
# ============================================================
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    k = m[killer].as_long()
    print("STATUS: sat")
    print(f"killer = {k}")
    print(f"killer_name = {person_names[k]}")
    # Print locations for the killer at all times
    print(f"\nKiller ({person_names[k]}) locations:")
    for t in range(TIMES):
        r = m[location[k][t]].as_long()
        print(f"  Time {t} ({['19:00','19:30','20:00','20:30','21:00','21:30','22:00'][t]}): {room_names[r]}")
    # Print all people's locations at time 4
    print(f"\nAll locations at time 4 (21:00 - murder time):")
    for p in range(PEOPLE):
        r = m[location[p][4]].as_long()
        print(f"  {person_names[p]}: {room_names[r]}")
    # Print hate relations for killer
    print(f"\nWho does {person_names[k]} hate?")
    for p in range(PEOPLE):
        if is_true(m[hates[k][p]]):
            print(f"  Hates {person_names[p]}")
    # Print richer relations for killer vs victim
    print(f"\nIs {person_names[k]} richer than Agatha? {is_true(m[richer[k][0]])}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")