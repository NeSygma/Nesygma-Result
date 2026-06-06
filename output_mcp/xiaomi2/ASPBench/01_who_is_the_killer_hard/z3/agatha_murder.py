from z3 import *

solver = Solver()

N = 12  # people
R = 12  # rooms
T = 7   # time points (0..6)

# People
AGATHA, BUTLER, CHARLES, DAISY, EDWARD, FELICITY, GEORGE, HARRIET, IAN, JULIA, KENNETH, LUCY = range(12)
names = ["Agatha", "Butler", "Charles", "Daisy", "Edward", "Felicity",
         "George", "Harriet", "Ian", "Julia", "Kenneth", "Lucy"]

# Rooms
STUDY, HALL, KITCHEN, LIBRARY, GARDEN, DINING, CELLAR, LOUNGE, CONSERVATORY, BEDROOM, ATTIC, GARAGE = range(12)
room_names = ["Study","Hall","Kitchen","Library","Garden","Dining","Cellar","Lounge","Conservatory","Bedroom","Attic","Garage"]

# Adjacency list
adj = {
    STUDY: [HALL, LIBRARY],
    HALL: [STUDY, KITCHEN, DINING, CELLAR, LOUNGE, BEDROOM],
    KITCHEN: [HALL, DINING, GARAGE],
    LIBRARY: [STUDY, GARDEN, LOUNGE],
    GARDEN: [LIBRARY, CONSERVATORY, GARAGE],
    DINING: [HALL, KITCHEN, LOUNGE],
    CELLAR: [HALL, GARAGE],
    LOUNGE: [HALL, LIBRARY, DINING, CONSERVATORY, BEDROOM, ATTIC],
    CONSERVATORY: [GARDEN, LOUNGE],
    BEDROOM: [HALL, LOUNGE, ATTIC],
    ATTIC: [BEDROOM, LOUNGE],
    GARAGE: [KITCHEN, CELLAR, GARDEN],
}

# ============================================================
# Room variables: room[p][t] = room of person p at time t
# ============================================================
room = [[Int(f'room_{p}_{t}') for t in range(T)] for p in range(N)]

for p in range(N):
    for t in range(T):
        solver.add(room[p][t] >= 0, room[p][t] < R)

# Movement: from t-1 to t, stay or move to adjacent room
for p in range(N):
    for t in range(1, T):
        for r in range(R):
            allowed = [r] + adj[r]
            solver.add(Implies(room[p][t-1] == r, Or([room[p][t] == a for a in allowed])))

# ============================================================
# High-confidence location facts at time 4 (murder time)
# ============================================================
high_conf = {
    AGATHA: STUDY, LUCY: STUDY, BUTLER: CELLAR, CHARLES: LIBRARY,
    DAISY: HALL, EDWARD: GARDEN, FELICITY: KITCHEN, GEORGE: DINING,
    HARRIET: LOUNGE, IAN: CONSERVATORY, JULIA: BEDROOM, KENNETH: ATTIC,
}
for p, r in high_conf.items():
    solver.add(room[p][4] == r)

# ============================================================
# Hate and Richer relations
# ============================================================
hates = [[Bool(f'hates_{i}_{j}') for j in range(N)] for i in range(N)]
richer = [[Bool(f'richer_{i}_{j}') for j in range(N)] for i in range(N)]

# Constraint 11: Richer is irreflexive and antisymmetric
for i in range(N):
    solver.add(Not(richer[i][i]))
for i in range(N):
    for j in range(N):
        if i != j:
            solver.add(Implies(richer[i][j], Not(richer[j][i])))

# Constraint 5: Agatha hates everybody except the butler (not herself)
for p in range(N):
    if p == AGATHA or p == BUTLER:
        solver.add(hates[AGATHA][p] == False)
    else:
        solver.add(hates[AGATHA][p] == True)

# Constraint 6: Butler hates everyone not richer than Agatha
for p in range(N):
    solver.add(Implies(Not(richer[p][AGATHA]), hates[BUTLER][p]))

# Constraint 7: Butler hates everyone Agatha hates
for p in range(N):
    solver.add(Implies(hates[AGATHA][p], hates[BUTLER][p]))

# Constraint 4: Charles hates no one that Agatha hates
for p in range(N):
    solver.add(Implies(hates[AGATHA][p], Not(hates[CHARLES][p])))

# Constraint 8: No one hates everyone
for i in range(N):
    solver.add(Or([Not(hates[i][j]) for j in range(N)]))

# ============================================================
# Killer
# ============================================================
killer = Int('killer')
solver.add(killer >= 0, killer < N)
solver.add(killer != AGATHA)  # Constraint 10: no suicide

# Constraint 2: killer hates victim (Agatha)
solver.add(Or([And(killer == i, hates[i][AGATHA]) for i in range(N)]))

# Constraint 3: killer is not richer than victim
solver.add(Or([And(killer == i, Not(richer[i][AGATHA])) for i in range(N)]))

# Constraint 15: killer must be in Study at time 4
solver.add(Or([And(killer == i, room[i][4] == STUDY) for i in range(N)]))

# ============================================================
# Witness statements (at least 14 of 18 must be true)
# ============================================================
witness_data = [
    (CHARLES, LIBRARY, 3),      # 1
    (BUTLER, HALL, 3),          # 2
    (DAISY, DINING, 3),         # 3
    (EDWARD, GARDEN, 5),        # 4
    (FELICITY, KITCHEN, 5),     # 5
    (GEORGE, LOUNGE, 5),        # 6
    (HARRIET, LOUNGE, 3),       # 7
    (IAN, CONSERVATORY, 5),     # 8
    (JULIA, BEDROOM, 5),        # 9
    (KENNETH, ATTIC, 5),        # 10
    (LUCY, HALL, 3),            # 11
    (AGATHA, STUDY, 3),         # 12
    (CHARLES, LIBRARY, 5),      # 13
    (BUTLER, CELLAR, 5),        # 14
    (DAISY, HALL, 5),           # 15
    (EDWARD, GARDEN, 3),        # 16
    (FELICITY, KITCHEN, 3),     # 17
    (GEORGE, DINING, 3),        # 18
]

witness_bools = []
for idx, (p, r, t) in enumerate(witness_data):
    wb = Bool(f'wit_{idx}')
    solver.add(wb == (room[p][t] == r))
    witness_bools.append(wb)

solver.add(Sum([If(wb, 1, 0) for wb in witness_bools]) >= 14)

# ============================================================
# Forensic indicators (at least 8 of 10 must be true)
# All 10 are consistent with knife; model them as all true
# ============================================================
forensic_bools = [Bool(f'forensic_{i}') for i in range(10)]
for fb in forensic_bools:
    solver.add(fb == True)
solver.add(Sum([If(fb, 1, 0) for fb in forensic_bools]) >= 8)

# ============================================================
# Solve
# ============================================================
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    killer_val = m.eval(killer).as_long()
    print("STATUS: sat")
    print(f"killer = {killer_val}")
    print(f"killer_name = {names[killer_val]}")

    # Room assignments at times 3, 4, 5
    for t_label, t_val in [("3", 3), ("4 (murder)", 4), ("5", 5)]:
        print(f"\nRoom assignments at time {t_label}:")
        for p in range(N):
            r_val = m.eval(room[p][t_val]).as_long()
            print(f"  {names[p]:10s}: {room_names[r_val]}")

    # Hate relations
    print("\nHate relations:")
    for i in range(N):
        hated = [names[j] for j in range(N) if is_true(m.eval(hates[i][j]))]
        if hated:
            print(f"  {names[i]} hates: {', '.join(hated)}")

    # Richer relations
    print("\nRicher relations:")
    for i in range(N):
        for j in range(N):
            if i != j and is_true(m.eval(richer[i][j])):
                print(f"  {names[i]} is richer than {names[j]}")

    # Witness truth values
    true_count = 0
    print("\nWitness statement evaluation:")
    for idx, (p, r, t) in enumerate(witness_data):
        val = is_true(m.eval(witness_bools[idx]))
        if val:
            true_count += 1
        status = "TRUE" if val else "FALSE"
        print(f"  {idx+1:2d}. {names[p]:10s} in {room_names[r]:14s} at t={t}: {status}")
    print(f"  Total true: {true_count}/18 (need >= 14)")

    # Verify movement for killer
    print(f"\nKiller ({names[killer_val]}) movement trace:")
    for t in range(T):
        r_val = m.eval(room[killer_val][t]).as_long()
        print(f"  t={t}: {room_names[r_val]}")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")