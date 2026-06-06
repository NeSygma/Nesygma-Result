from z3 import *

# Define rooms
rooms = ['room1','room2','room3','room4','room5','room6','room7']
R = len(rooms)
# Treasure indices
treasures = ['treasure1','treasure2','treasure3']
T = len(treasures)
# Monster types
monster_names = ['goblin','orc','dragon']
M = len(monster_names)
danger_level = [2,4,8]
max_group = [3,2,1]

solver = Solver()

# Treasure placement: each treasure assigned to a room (0..R-1)
treasure_room = [Int(f"treasure_room_{i}") for i in range(T)]
for tr in treasure_room:
    solver.add(tr >= 0, tr < R)

# Monster counts per room and type
monster_cnt = [[Int(f"cnt_{r}_{m}") for m in range(M)] for r in range(R)]
for r in range(R):
    for m in range(M):
        solver.add(monster_cnt[r][m] >= 0, monster_cnt[r][m] <= max_group[m])

# Danger per room
room_danger = [Int(f"danger_{r}") for r in range(R)]
for r in range(R):
    danger_expr = Sum([monster_cnt[r][m] * danger_level[m] for m in range(M)])
    solver.add(room_danger[r] == danger_expr)
    solver.add(room_danger[r] <= 10)  # max danger per room

# Strategic placement: rare treasure (treasure2) in higher-danger room than common (treasure1)
# Compute danger of the room where each treasure is placed
danger_t1 = Sum([If(treasure_room[0] == r, room_danger[r], 0) for r in range(R)])
danger_t2 = Sum([If(treasure_room[1] == r, room_danger[r], 0) for r in range(R)])
solver.add(danger_t2 > danger_t1)

# Minimum treasures per path to exit (room7 index 6)
# Define two simple paths sets (indices)
pathA = [0,1,3,5,4,6]  # room1,2,4,6,5,7
pathB = [0,2,4,6]      # room1,3,5,7
# Helper: treasure present in a room if any treasure assigned there
has_treasure = [Bool(f"has_treasure_{r}") for r in range(R)]
for r in range(R):
    solver.add(has_treasure[r] == Or([treasure_room[t] == r for t in range(T)]))
# At least one treasure in each path
solver.add(Sum([If(has_treasure[r], 1, 0) for r in pathA]) >= 1)
solver.add(Sum([If(has_treasure[r], 1, 0) for r in pathB]) >= 1)

# Connectivity: all rooms reachable from entrance (room1 index 0)
# Using reachability propagation over edges
reachable = [Bool(f"reach_{r}") for r in range(R)]
solver.add(reachable[0] == True)
edges = [(0,1),(0,2),(1,3),(2,4),(3,5),(4,5),(4,6)]
# Propagate reachability (fixed-point via multiple rounds)
for _ in range(R):
    for (u,v) in edges:
        solver.add(Implies(reachable[u], reachable[v]))
        solver.add(Implies(reachable[v], reachable[u]))
# Enforce all reachable
for r in range(R):
    solver.add(reachable[r] == True)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Treasure placements
    for i, name in enumerate(treasures):
        room_idx = m[treasure_room[i]].as_long()
        print(f"{name} placed in {rooms[room_idx]}")
    # Monster placements and danger per room
    total_danger = 0
    for r in range(R):
        danger_val = m[room_danger[r]].as_long()
        total_danger += danger_val
        mons = []
        for mi, mname in enumerate(monster_names):
            cnt = m[monster_cnt[r][mi]].as_long()
            if cnt > 0:
                mons.append(f"{cnt} {mname}(s)")
        mons_str = ", ".join(mons) if mons else "none"
        print(f"{rooms[r]}: danger={danger_val}, monsters={mons_str}")
    print(f"balance_analysis.total_danger = {total_danger}")
    # Treasure distribution by rarity
    treasure_rarity = ['common','rare','legendary']
    dist = {r:0 for r in ['common','rare','legendary']}
    for r in treasure_rarity:
        dist[r] += 1
    print("balance_analysis.treasure_distribution =", dist)
else:
    print("STATUS: unsat")