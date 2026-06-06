from z3 import *

solver = Solver()

# ============================================================
# Constants
# ============================================================
NUM_PEOPLE = 12
NUM_ROOMS = 12
NUM_TIMES = 7
NUM_WEAPONS = 6

# Names for output
people_names = ["Agatha", "Butler", "Charles", "Daisy", "Edward", "Felicity",
                "George", "Harriet", "Ian", "Julia", "Kenneth", "Lucy"]
room_names = ["Study", "Hall", "Kitchen", "Library", "Garden", "Dining",
              "Cellar", "Lounge", "Conservatory", "Bedroom", "Attic", "Garage"]

# ============================================================
# Adjacency (bidirectional + self)
# ============================================================
adj = {i: set() for i in range(NUM_ROOMS)}
edges = [
    (0,1),(0,3),       # Study: Hall, Library
    (1,0),(1,2),(1,5),(1,6),(1,7),(1,9),  # Hall: Study, Kitchen, Dining, Cellar, Lounge, Bedroom
    (2,1),(2,5),(2,11), # Kitchen: Hall, Dining, Garage
    (3,0),(3,4),(3,7),  # Library: Study, Garden, Lounge
    (4,3),(4,8),(4,11), # Garden: Library, Conservatory, Garage
    (5,1),(5,2),(5,7),  # Dining: Hall, Kitchen, Lounge
    (6,1),(6,11),       # Cellar: Hall, Garage
    (7,1),(7,3),(7,5),(7,8),(7,9),(7,10),  # Lounge: Hall, Library, Dining, Conservatory, Bedroom, Attic
    (8,4),(8,7),        # Conservatory: Garden, Lounge
    (9,1),(9,7),(9,10), # Bedroom: Hall, Lounge, Attic
    (10,9),(10,7),      # Attic: Bedroom, Lounge
    (11,2),(11,6),(11,4) # Garage: Kitchen, Cellar, Garden
]
for u, v in edges:
    adj[u].add(v)
    adj[v].add(u)
# Add self-loops (staying put)
for i in range(NUM_ROOMS):
    adj[i].add(i)

# ============================================================
# Decision Variables
# ============================================================

# Location: loc[p][t] = room index for person p at time t
loc = [[Int(f"loc_{p}_{t}") for t in range(NUM_TIMES)] for p in range(NUM_PEOPLE)]

# Killer
killer = Int("killer")

# Hate relation: hates[a][b] means person a hates person b
hates = [[Bool(f"hates_{a}_{b}") for b in range(NUM_PEOPLE)] for a in range(NUM_PEOPLE)]

# Richer relation: richer[a][b] means person a is richer than person b
richer = [[Bool(f"richer_{a}_{b}") for b in range(NUM_PEOPLE)] for a in range(NUM_PEOPLE)]

# ============================================================
# Domain constraints for locations
# ============================================================
for p in range(NUM_PEOPLE):
    for t in range(NUM_TIMES):
        solver.add(loc[p][t] >= 0, loc[p][t] < NUM_ROOMS)

# ============================================================
# Killer domain
# ============================================================
solver.add(killer >= 0, killer < NUM_PEOPLE)
solver.add(killer != 0)  # No suicide (constraint 10)

# ============================================================
# High-confidence location facts at time 4 (murder time)
# ============================================================
# Agatha: Study(0), Lucy: Study(0), Butler: Cellar(6), Charles: Library(3),
# Daisy: Hall(1), Edward: Garden(4), Felicity: Kitchen(2), George: Dining(5),
# Harriet: Lounge(7), Ian: Conservatory(8), Julia: Bedroom(9), Kenneth: Attic(10)
time4_locs = [0, 6, 3, 1, 4, 2, 5, 7, 8, 9, 10, 0]
for p in range(NUM_PEOPLE):
    solver.add(loc[p][4] == time4_locs[p])

# Constraint 15: Killer must be in Study at time 4
# Only people in Study at time 4 are Agatha(0) and Lucy(11)
# Since killer != 0, killer must be 11 (Lucy)
# But let's encode it symbolically first
for p in range(NUM_PEOPLE):
    solver.add(Implies(killer == p, loc[p][4] == 0))  # Study

# ============================================================
# Movement constraints (constraint 13)
# ============================================================
for p in range(NUM_PEOPLE):
    for t in range(1, NUM_TIMES):
        # Person must stay or move to adjacent room
        # Build Or over all allowed rooms
        allowed = []
        for r in range(NUM_ROOMS):
            # If person was in room r at t-1, they can be in any room in adj[r] at t
            allowed.append(And(loc[p][t-1] == r,
                               Or([loc[p][t] == a for a in adj[r]])))
        solver.add(Or(allowed))

# ============================================================
# Richer relation: irreflexive and antisymmetric (constraint 11)
# ============================================================
for a in range(NUM_PEOPLE):
    solver.add(richer[a][a] == False)  # irreflexive
    for b in range(NUM_PEOPLE):
        if a != b:
            solver.add(Implies(richer[a][b], Not(richer[b][a])))  # antisymmetric

# ============================================================
# Constraint 5: Agatha hates everybody except the butler
# ============================================================
for b in range(NUM_PEOPLE):
    if b == 1:  # Butler
        solver.add(hates[0][b] == False)
    elif b == 0:  # Agatha doesn't hate herself
        solver.add(hates[0][b] == False)
    else:
        solver.add(hates[0][b] == True)

# ============================================================
# Constraint 6: Butler hates everyone not richer than Agatha
# ============================================================
for b in range(NUM_PEOPLE):
    if b == 1:  # Butler doesn't hate himself
        solver.add(hates[1][b] == False)
    else:
        # Butler hates b iff b is NOT richer than Agatha
        solver.add(hates[1][b] == Not(richer[b][0]))

# ============================================================
# Constraint 7: Butler hates everyone whom Agatha hates
# ============================================================
for b in range(NUM_PEOPLE):
    solver.add(Implies(hates[0][b], hates[1][b]))

# ============================================================
# Constraint 4: Charles hates no one that Agatha hates
# ============================================================
for b in range(NUM_PEOPLE):
    solver.add(Implies(hates[0][b], Not(hates[2][b])))

# ============================================================
# Constraint 8: No one hates everyone
# ============================================================
for a in range(NUM_PEOPLE):
    solver.add(Not(And([hates[a][b] for b in range(NUM_PEOPLE)])))

# ============================================================
# Constraint 2: The killer hates the victim (Agatha)
# ============================================================
for p in range(NUM_PEOPLE):
    solver.add(Implies(killer == p, hates[p][0]))

# ============================================================
# Constraint 3: The killer is no richer than the victim
# ============================================================
for p in range(NUM_PEOPLE):
    solver.add(Implies(killer == p, Not(richer[p][0])))

# ============================================================
# Witness Statements (at least 14 of 18 must be true)
# ============================================================
witness_statements = [
    (2, 3, 3),   # 1. Charles in Library at time 3
    (1, 1, 3),   # 2. Butler in Hall at time 3
    (3, 5, 3),   # 3. Daisy in Dining at time 3
    (4, 4, 5),   # 4. Edward in Garden at time 5
    (5, 2, 5),   # 5. Felicity in Kitchen at time 5
    (6, 7, 5),   # 6. George in Lounge at time 5
    (7, 7, 3),   # 7. Harriet in Lounge at time 3
    (8, 8, 5),   # 8. Ian in Conservatory at time 5
    (9, 9, 5),   # 9. Julia in Bedroom at time 5
    (10, 10, 5), # 10. Kenneth in Attic at time 5
    (11, 1, 3),  # 11. Lucy in Hall at time 3
    (0, 0, 3),   # 12. Agatha in Study at time 3
    (2, 3, 5),   # 13. Charles in Library at time 5
    (1, 6, 5),   # 14. Butler in Cellar at time 5
    (3, 1, 5),   # 15. Daisy in Hall at time 5
    (4, 4, 3),   # 16. Edward in Garden at time 3
    (5, 2, 3),   # 17. Felicity in Kitchen at time 3
    (6, 5, 3),   # 18. George in Dining at time 3
]

witness_bools = []
for i, (p, r, t) in enumerate(witness_statements):
    wb = Bool(f"witness_{i}")
    solver.add(wb == (loc[p][t] == r))
    witness_bools.append(wb)

solver.add(Sum([If(wb, 1, 0) for wb in witness_bools]) >= 14)

# ============================================================
# Forensic Indicators (at least 8 of 10 must be true)
# These are about the murder weapon being a knife.
# Since constraint 16 says exactly the knife was used,
# all forensic indicators consistent with knife should be true.
# But we model them as soft constraints (at least 8/10).
# ============================================================
# The forensic indicators are facts about the crime scene, not person-dependent.
# They are all consistent with knife being the weapon.
# We model them as boolean variables that must be mostly true.
forensic_bools = [Bool(f"forensic_{i}") for i in range(10)]
solver.add(Sum([If(fb, 1, 0) for fb in forensic_bools]) >= 8)

# All forensic indicators are consistent with knife - we can assert them all true
# since the problem says they're all consistent with knife and knife IS the weapon.
# But the constraint says "at least 8 of 10 must be true", so let's keep it as >= 8.
# Actually, let's assert all true since they're all consistent with knife.
for fb in forensic_bools:
    solver.add(fb == True)

# ============================================================
# Check and output
# ============================================================
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    killer_idx = m[killer].as_long()
    print("STATUS: sat")
    print(f"killer: {killer_idx}")
    print(f"killer_name: {people_names[killer_idx]}")
    
    # Print location details
    print("\n--- Location Timeline ---")
    for p in range(NUM_PEOPLE):
        locs = [room_names[m[loc[p][t]].as_long()] for t in range(NUM_TIMES)]
        print(f"{people_names[p]}: {locs}")
    
    # Print hate relations
    print("\n--- Hate Relations ---")
    for a in range(NUM_PEOPLE):
        hated = [people_names[b] for b in range(NUM_PEOPLE) if is_true(m[hates[a][b]])]
        if hated:
            print(f"{people_names[a]} hates: {hated}")
    
    # Print richer relations
    print("\n--- Richer Relations ---")
    for a in range(NUM_PEOPLE):
        richer_than = [people_names[b] for b in range(NUM_PEOPLE) if is_true(m[richer[a][b]])]
        if richer_than:
            print(f"{people_names[a]} richer than: {richer_than}")
    
    # Print witness statement truth values
    print("\n--- Witness Statements ---")
    true_count = 0
    for i, (p, r, t) in enumerate(witness_statements):
        val = is_true(m[witness_bools[i]])
        true_count += 1 if val else 0
        status = "TRUE" if val else "FALSE"
        print(f"  {i+1}. {people_names[p]} in {room_names[r]} at t={t}: {status}")
    print(f"  Total true: {true_count}/18")
    
    # Print forensic indicators
    print("\n--- Forensic Indicators ---")
    foren_true = sum(1 for fb in forensic_bools if is_true(m[fb]))
    print(f"  Total true: {foren_true}/10")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")