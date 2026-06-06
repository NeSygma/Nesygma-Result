from z3 import *

# Initialize solver
solver = Solver()

# Constants
NUM_PEOPLE = 12
NUM_ROOMS = 12
NUM_TIMES = 7
NUM_WEAPONS = 6

# Person indices
AGATHA = 0
BUTLER = 1
CHARLES = 2
DAISY = 3
EDWARD = 4
FELICITY = 5
GEORGE = 6
HARRIET = 7
IAN = 8
JULIA = 9
KENNETH = 10
LUCY = 11

# Room indices
STUDY = 0
HALL = 1
KITCHEN = 2
LIBRARY = 3
GARDEN = 4
DINING = 5
CELLAR = 6
LOUNGE = 7
CONSERVATORY = 8
BEDROOM = 9
ATTIC = 10
GARAGE = 11

# Weapon indices
GUN = 0
KNIFE = 1
ROPE = 2
CANDLESTICK = 3
WRENCH = 4
POISON = 5

# Declare variables
killer = Int('killer')
location = [[Int(f'loc_{p}_{t}') for t in range(NUM_TIMES)] for p in range(NUM_PEOPLE)]
hates = [[Bool(f'hates_{p}_{q}') for q in range(NUM_PEOPLE)] for p in range(NUM_PEOPLE)]
richer = [[Bool(f'richer_{p}_{q}') for q in range(NUM_PEOPLE)] for p in range(NUM_PEOPLE)]

# Weapon used (exactly one weapon used: Knife)
weapon_used = Int('weapon_used')
solver.add(weapon_used == KNIFE)

# 1. Exactly one killer (not Agatha)
solver.add(killer >= 0, killer < NUM_PEOPLE)
solver.add(killer != AGATHA)

# 2. Killer hates victim (Agatha)
solver.add(hates[killer][AGATHA])

# 3. Killer is not richer than victim
solver.add(Not(richer[killer][AGATHA]))

# 4. Charles hates no one that Agatha hates
for p in range(NUM_PEOPLE):
    solver.add(Implies(hates[AGATHA][p], Not(hates[CHARLES][p])))

# 5. Agatha hates everybody except the butler
for p in range(NUM_PEOPLE):
    if p != BUTLER:
        solver.add(hates[AGATHA][p])
    else:
        solver.add(Not(hates[AGATHA][BUTLER]))

# 6. Butler hates everyone not richer than Agatha
for p in range(NUM_PEOPLE):
    solver.add(Implies(Not(richer[p][AGATHA]), hates[BUTLER][p]))

# 7. Butler hates everyone Agatha hates
for p in range(NUM_PEOPLE):
    solver.add(Implies(hates[AGATHA][p], hates[BUTLER][p]))

# 8. No one hates everyone
for p in range(NUM_PEOPLE):
    solver.add(Or([Not(hates[p][q]) for q in range(NUM_PEOPLE)]))

# 9. Agatha is the victim (already implied by killer != AGATHA, but explicit)
solver.add(killer != AGATHA)

# 10. No suicides (already covered by killer != AGATHA)

# 11. Wealth relations are irreflexive and antisymmetric
for p in range(NUM_PEOPLE):
    solver.add(Not(richer[p][p]))  # irreflexive
    for q in range(NUM_PEOPLE):
        if p != q:
            solver.add(Implies(richer[p][q], Not(richer[q][p])))  # antisymmetric

# 12. Each person in exactly one room at each time
for p in range(NUM_PEOPLE):
    for t in range(NUM_TIMES):
        solver.add(location[p][t] >= 0)
        solver.add(location[p][t] < NUM_ROOMS)
        # All people in different rooms at same time (not required, but each person in exactly one room)
        # Actually, multiple people can be in same room

# 13. Movement constraints
# Define adjacency matrix
adjacency = [[False] * NUM_ROOMS for _ in range(NUM_ROOMS)]
adjacency[STUDY][HALL] = adjacency[STUDY][LIBRARY] = True
adjacency[HALL][STUDY] = adjacency[HALL][KITCHEN] = adjacency[HALL][DINING] = adjacency[HALL][CELLAR] = adjacency[HALL][LOUNGE] = adjacency[HALL][BEDROOM] = True
adjacency[KITCHEN][HALL] = adjacency[KITCHEN][DINING] = adjacency[KITCHEN][GARAGE] = True
adjacency[LIBRARY][STUDY] = adjacency[LIBRARY][GARDEN] = adjacency[LIBRARY][LOUNGE] = True
adjacency[GARDEN][LIBRARY] = adjacency[GARDEN][CONSERVATORY] = adjacency[GARDEN][GARAGE] = True
adjacency[DINING][HALL] = adjacency[DINING][KITCHEN] = adjacency[DINING][LOUNGE] = True
adjacency[CELLAR][HALL] = adjacency[CELLAR][GARAGE] = True
adjacency[LOUNGE][HALL] = adjacency[LOUNGE][LIBRARY] = adjacency[LOUNGE][DINING] = adjacency[LOUNGE][CONSERVATORY] = adjacency[LOUNGE][BEDROOM] = adjacency[LOUNGE][ATTIC] = True
adjacency[CONSERVATORY][GARDEN] = adjacency[CONSERVATORY][LOUNGE] = True
adjacency[BEDROOM][HALL] = adjacency[BEDROOM][LOUNGE] = adjacency[BEDROOM][ATTIC] = True
adjacency[ATTIC][BEDROOM] = adjacency[ATTIC][LOUNGE] = True
adjacency[GARAGE][KITCHEN] = adjacency[GARAGE][CELLAR] = adjacency[GARAGE][GARDEN] = True

# Movement constraint: from time T-1 to T, person either stays or moves to adjacent room
for p in range(NUM_PEOPLE):
    for t in range(1, NUM_TIMES):
        # Stay in same room OR move to adjacent room
        stay = location[p][t] == location[p][t-1]
        move_adjacent = Or([And(location[p][t-1] == r1, location[p][t] == r2) 
                           for r1 in range(NUM_ROOMS) for r2 in range(NUM_ROOMS) 
                           if adjacency[r1][r2]])
        solver.add(Or(stay, move_adjacent))

# 14. Murder occurred in Study at time 4
solver.add(location[AGATHA][4] == STUDY)

# 15. Killer must be in Study at time 4
solver.add(location[killer][4] == STUDY)

# 16. Exactly one weapon used: Knife (already set)

# High-confidence location facts at time 4
facts_time4 = [
    (AGATHA, STUDY),
    (LUCY, STUDY),
    (BUTLER, CELLAR),
    (CHARLES, LIBRARY),
    (DAISY, HALL),
    (EDWARD, GARDEN),
    (FELICITY, KITCHEN),
    (GEORGE, DINING),
    (HARRIET, LOUNGE),
    (IAN, CONSERVATORY),
    (JULIA, BEDROOM),
    (KENNETH, ATTIC)
]
for person, room in facts_time4:
    solver.add(location[person][4] == room)

# Witness statements (at least 14 of 18 must be true)
witness_statements = [
    (CHARLES, LIBRARY, 3),   # 1
    (BUTLER, HALL, 3),       # 2
    (DAISY, DINING, 3),      # 3
    (EDWARD, GARDEN, 5),     # 4
    (FELICITY, KITCHEN, 5),  # 5
    (GEORGE, LOUNGE, 5),     # 6
    (HARRIET, LOUNGE, 3),    # 7
    (IAN, CONSERVATORY, 5),  # 8
    (JULIA, BEDROOM, 5),     # 9
    (KENNETH, ATTIC, 5),     # 10
    (LUCY, HALL, 3),         # 11
    (AGATHA, STUDY, 3),      # 12
    (CHARLES, LIBRARY, 5),   # 13
    (BUTLER, CELLAR, 5),     # 14
    (DAISY, HALL, 5),        # 15
    (EDWARD, GARDEN, 3),     # 16
    (FELICITY, KITCHEN, 3),  # 17
    (GEORGE, DINING, 3)      # 18
]

# Create boolean variables for each witness statement being true
witness_true = [Bool(f'witness_{i}') for i in range(len(witness_statements))]
for i, (person, room, time) in enumerate(witness_statements):
    solver.add(Implies(witness_true[i], location[person][time] == room))
    solver.add(Implies(Not(witness_true[i]), location[person][time] != room))

# At least 14 of 18 witness statements must be true
solver.add(Sum([If(witness_true[i], 1, 0) for i in range(len(witness_statements))]) >= 14)

# Forensic indicators (at least 8 of 10 must be true, all consistent with knife)
# We'll model these as boolean constraints
forensic_indicators = [
    Bool('forensic_0'),  # No gunshot residue near the body
    Bool('forensic_1'),  # No shell casings recovered from Study
    Bool('forensic_2'),  # Blunt-force trauma was not the primary cause
    Bool('forensic_3'),  # Wound pattern consistent with a blade
    Bool('forensic_4'),  # No ligature marks on the neck
    Bool('forensic_5'),  # A clean-edged cut was present
    Bool('forensic_6'),  # No heavy-object blood spatter pattern found
    Bool('forensic_7'),  # No powder burns on victim's clothing
    Bool('forensic_8'),  # No trace of toxin in the glass on the desk
    Bool('forensic_9')   # A kitchen knife was missing from the Kitchen drawer after time 4
]

# All forensic indicators must be consistent with knife (KNIFE = 1)
# For simplicity, we'll assume all forensic indicators are true if weapon is knife
# In a more detailed model, we'd have specific constraints for each indicator
# Here we just require at least 8 of 10 to be true
solver.add(Sum([If(forensic_indicators[i], 1, 0) for i in range(10)]) >= 8)

# Additional constraint: Weapon used is knife (already set)
# The missing knife indicator (forensic_9) should be true if weapon is knife
solver.add(forensic_9 == True)  # Kitchen knife missing

# Check solver
result = solver.check()

if result == sat:
    model = solver.model()
    killer_val = model.eval(killer)
    killer_name = ["Agatha", "Butler", "Charles", "Daisy", "Edward", "Felicity", 
                   "George", "Harriet", "Ian", "Julia", "Kenneth", "Lucy"][killer_val.as_long()]
    
    print("STATUS: sat")
    print(f"killer: {killer_val.as_long()}")
    print(f"killer_name: {killer_name}")
    
    # Print location of killer at time 4
    killer_loc = model.eval(location[killer_val.as_long()][4])
    print(f"Killer location at time 4: Room {killer_loc.as_long()}")
    
    # Print some witness statement results
    print("\nWitness statements (true/false):")
    for i, (person, room, time) in enumerate(witness_statements):
        stmt_val = model.eval(witness_true[i])
        person_names = ["Agatha", "Butler", "Charles", "Daisy", "Edward", "Felicity", 
                       "George", "Harriet", "Ian", "Julia", "Kenneth", "Lucy"]
        room_names = ["Study", "Hall", "Kitchen", "Library", "Garden", "Dining", 
                     "Cellar", "Lounge", "Conservatory", "Bedroom", "Attic", "Garage"]
        print(f"  {i+1}. {person_names[person]} in {room_names[room]} at time {time}: {stmt_val}")
    
    # Count true witness statements
    true_count = sum(1 for i in range(len(witness_statements)) if model.eval(witness_true[i]))
    print(f"\nTrue witness statements: {true_count}/18 (need >= 14)")
    
    # Print forensic indicators
    print("\nForensic indicators:")
    for i in range(10):
        print(f"  {i+1}. {model.eval(forensic_indicators[i])}")
    
    true_forensic = sum(1 for i in range(10) if model.eval(forensic_indicators[i]))
    print(f"\nTrue forensic indicators: {true_forensic}/10 (need >= 8)")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found - constraints are inconsistent")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")