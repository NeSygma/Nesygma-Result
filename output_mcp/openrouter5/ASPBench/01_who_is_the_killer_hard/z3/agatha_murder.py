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
    (2, 3, 3),   # Charles in Library at time 3
    (1, 3, 1),   # Butler in Hall at time 3
    (3, 3, 5),   # Daisy in Dining at time 3
    (4, 5, 4),   # Edward in Garden at time 5
    (5, 5, 2),   # Felicity in Kitchen at time 5
    (6, 5, 7),   # George in Lounge at time 5
    (7, 5, 7),   # Harriet in Lounge at time 5
    (8, 5, 8),   # Ian in Conservatory at time 5
    (9, 5, 9),   # Julia in Bedroom at time 5
    (10, 5, 10), # Kenneth in Attic at time 5
    (11, 3, 1),  # Lucy in Hall at time 3
    (0, 3, 0),   # Agatha in Study at time 3
    (2, 5, 3),   # Charles in Library at time 5
    (1, 5, 6),   # Butler in Cellar at time 5
    (3, 5, 1),   # Daisy in Hall at time 5
    (4, 5, 4),   # Edward in Garden at time 5 (duplicate of #4? Actually #4 is Edward Garden t5, #16 is Edward Garden t3)
    (4, 3, 4),   # Edward in Garden at time 3
    (5, 3, 2),   # Felicity in Kitchen at time 3
    (6, 3, 5),   # George in Dining at time 3
]
# Wait, let me recount. The problem says 18 witness statements.
# Let me list them carefully:
# 1. Charles in Library at time 3
# 2. Butler in Hall at time 3
# 3. Daisy in Dining at time 3
# 4. Edward in Garden at time 5
# 5. Felicity in Kitchen at time 5
# 6. George in Lounge at time 5
# 7. Harriet in Lounge at time 3
# 8. Ian in Conservatory at time 5
# 9. Julia in Bedroom at time 5
# 10. Kenneth in Attic at time 5
# 11. Lucy in Hall at time 3
# 12. Agatha in Study at time 3
# 13. Charles in Library at time 5
# 14. Butler in Cellar at time 5
# 15. Daisy in Hall at time 5
# 16. Edward in Garden at time 3
# 17. Felicity in Kitchen at time 3
# 18. George in Dining at time 3

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

# location[p][t] = room index (0..11) for person p at time t
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
        # Either same room, or adjacent
        adj_rooms = adj  # dict
        # Build constraint: curr_room == prev_room OR curr_room is adjacent to prev_room
        # Use Or-loop
        possible = [curr_room == prev_room]  # staying put
        for r in range(ROOMS):
            # If curr_room == r, then prev_room must be r or adjacent to r
            pass
        # Better: for each possible prev_room value, curr_room must be same or adjacent
        # curr_room == prev_room OR Or([And(prev_room == r, Or([curr_room == a for a in adj[r] + [r]])) for r in range(ROOMS)])
        # Simplify: just use implication
        # For each room r, if prev_room == r then curr_room must be in {r} ∪ adj[r]
        constraints = []
        for r in range(ROOMS):
            allowed = [r] + adj[r]
            constraints.append(Implies(prev_room == r, Or([curr_room == a for a in allowed])))
        solver.add(And(constraints))

# CONSTRAINT 14: Murder occurred in Study at time 4
# Agatha was in Study at time 4 (already in high_conf)
solver.add(location[0][MURDER_TIME] == MURDER_ROOM)

# CONSTRAINT 15: Killer must be in Study at time 4
solver.add(location[killer][MURDER_TIME] == MURDER_ROOM)

# CONSTRAINT 16: Exactly one weapon used: Knife (weapon index 1)
# This is already given as fact, no variable needed.

# CONSTRAINT 1: Exactly one killer
# (killer is a single integer, so it's one person by definition)

# CONSTRAINT 2: The killer hates the victim
solver.add(hates[killer][0] == True)

# CONSTRAINT 3: The killer is no richer than the victim (not strictly richer)
# i.e., NOT richer[killer][0]
solver.add(Not(richer[killer][0]))

# CONSTRAINT 4: Charles hates no one that Agatha hates
# For all p: if Agatha hates p, then Charles does NOT hate p
for p in range(PEOPLE):
    solver.add(Implies(hates[0][p], Not(hates[2][p])))

# CONSTRAINT 5: Agatha hates everybody except the butler
# Agatha hates everyone except person 1 (Butler)
for p in range(PEOPLE):
    if p != 1:
        solver.add(hates[0][p] == True)
    else:
        solver.add(hates[0][p] == False)

# CONSTRAINT 6: The butler hates everyone not richer than Aunt Agatha
# "not richer than Aunt Agatha" means NOT richer[p][0] (Agatha is person 0)
# So for all p: if NOT richer[p][0], then butler hates p
for p in range(PEOPLE):
    solver.add(Implies(Not(richer[p][0]), hates[1][p]))

# CONSTRAINT 7: The butler hates everyone whom Agatha hates
# For all p: if Agatha hates p, then butler hates p
for p in range(PEOPLE):
    solver.add(Implies(hates[0][p], hates[1][p]))

# CONSTRAINT 8: No one hates everyone
# For each person p1, there exists at least one person p2 such that p1 does NOT hate p2
for p1 in range(PEOPLE):
    solver.add(Or([Not(hates[p1][p2]) for p2 in range(PEOPLE)]))

# CONSTRAINT 9: Agatha is the victim (already encoded, person 0)

# CONSTRAINT 10: No suicides (killer != victim)
solver.add(killer != 0)

# CONSTRAINT 11: Wealth relations (richer) are irreflexive and antisymmetric
# Irreflexive: no one is richer than themselves
for p in range(PEOPLE):
    solver.add(Not(richer[p][p]))
# Antisymmetric: if p1 is richer than p2, then p2 is NOT richer than p1
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
# All consistent with knife (weapon 1)
# ============================================================
# These are all facts that should be true given knife was used.
# We encode them as constraints that must be true (since they're "consistent with knife")
# But the problem says "at least 8 of 10 must be true"
# Let's encode them as boolean variables too.

forensic_vars = [Bool(f"forensic_{i}") for i in range(10)]

# 1. No gunshot residue near the body
solver.add(forensic_vars[0] == True)  # consistent with knife

# 2. No shell casings recovered from Study
solver.add(forensic_vars[1] == True)  # consistent with knife

# 3. Blunt-force trauma was not the primary cause
solver.add(forensic_vars[2] == True)  # consistent with knife

# 4. Wound pattern consistent with a blade
solver.add(forensic_vars[3] == True)  # consistent with knife

# 5. No ligature marks on the neck
solver.add(forensic_vars[4] == True)  # consistent with knife

# 6. A clean-edged cut was present
solver.add(forensic_vars[5] == True)  # consistent with knife

# 7. No heavy-object blood spatter pattern found
solver.add(forensic_vars[6] == True)  # consistent with knife

# 8. No powder burns on victim's clothing
solver.add(forensic_vars[7] == True)  # consistent with knife

# 9. No trace of toxin in the glass on the desk
solver.add(forensic_vars[8] == True)  # consistent with knife

# 10. A kitchen knife was missing from the Kitchen drawer after time 4
solver.add(forensic_vars[9] == True)  # consistent with knife

# At least 8 of 10 must be true
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