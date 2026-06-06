from z3 import *

# Constants
NUM_PEOPLE = 12
NUM_ROOMS = 12
NUM_TIMES = 7

people_names = ["Agatha","Butler","Charles","Daisy","Edward","Felicity","George","Harriet","Ian","Julia","Kenneth","Lucy"]
rooms_names = ["Study","Hall","Kitchen","Library","Garden","Dining","Cellar","Lounge","Conservatory","Bedroom","Attic","Garage"]

# Adjacency list (undirected)
adj = {
    0: [1,3],          # Study
    1: [0,2,5,6,7,9],# Hall
    2: [1,5,11],      # Kitchen
    3: [0,4,7],       # Library
    4: [3,8,11],      # Garden
    5: [1,2,7],       # Dining
    6: [1,11],         # Cellar
    7: [1,3,5,8,9,10],# Lounge
    8: [4,7],          # Conservatory
    9: [1,7,10],       # Bedroom
    10:[9,7],          # Attic
    11:[2,6,4]         # Garage
}
# Allowed next rooms (including staying)
allowed_next = {r: [r] + adj[r] for r in range(NUM_ROOMS)}

solver = Solver()

# Location variables: loc[p][t]
loc = [[Int(f"loc_{p}_{t}") for t in range(NUM_TIMES)] for p in range(NUM_PEOPLE)]
for p in range(NUM_PEOPLE):
    for t in range(NUM_TIMES):
        solver.add(loc[p][t] >= 0, loc[p][t] < NUM_ROOMS)

# High-confidence facts at time 4 (index 4)
high_conf = {
    0:0,  # Agatha -> Study
    1:6,  # Butler -> Cellar
    2:3,  # Charles -> Library
    3:1,  # Daisy -> Hall
    4:4,  # Edward -> Garden
    5:2,  # Felicity -> Kitchen
    6:5,  # George -> Dining
    7:7,  # Harriet -> Lounge
    8:8,  # Ian -> Conservatory
    9:9,  # Julia -> Bedroom
    10:10,# Kenneth -> Attic
    11:0  # Lucy -> Study
}
for p,room in high_conf.items():
    solver.add(loc[p][4] == room)

# Movement constraints (local adjacency or stay)
for p in range(NUM_PEOPLE):
    for t in range(1, NUM_TIMES):
        cases = []
        for r in range(NUM_ROOMS):
            allowed = allowed_next[r]
            cases.append(And(loc[p][t-1] == r, Or([loc[p][t] == s for s in allowed])))
        solver.add(Or(cases))

# Medium reliability statements (18)
stmt_truth = []

def add_stmt(person, time_idx, room_idx):
    b = Bool(f"stmt_{person}_{time_idx}_{room_idx}")
    solver.add(b == (loc[person][time_idx] == room_idx))
    stmt_truth.append(b)

# Statements list (person indices as per problem)
add_stmt(2,3,3)   # 1 Charles Library time3
add_stmt(1,3,1)   # 2 Butler Hall time3
add_stmt(3,3,5)   # 3 Daisy Dining time3
add_stmt(4,5,4)   # 4 Edward Garden time5
add_stmt(5,5,2)   # 5 Felicity Kitchen time5
add_stmt(6,5,7)   # 6 George Lounge time5
add_stmt(7,3,7)   # 7 Harriet Lounge time3
add_stmt(8,5,8)   # 8 Ian Conservatory time5
add_stmt(9,5,9)   # 9 Julia Bedroom time5
add_stmt(10,5,10) #10 Kenneth Attic time5
add_stmt(11,3,1)  #11 Lucy Hall time3
add_stmt(0,3,0)   #12 Agatha Study time3
add_stmt(2,5,3)   #13 Charles Library time5
add_stmt(1,5,6)   #14 Butler Cellar time5
add_stmt(3,5,1)   #15 Daisy Hall time5
add_stmt(4,3,4)   #16 Edward Garden time3
add_stmt(5,3,2)   #17 Felicity Kitchen time3
add_stmt(6,3,5)   #18 George Dining time3

solver.add(Sum([If(b,1,0) for b in stmt_truth]) >= 14)

# Forensic indicators (10) – at least 8 true (no linking needed)
forensic_vars = []
for i in range(10):
    f = Bool(f"forensic_{i}")
    forensic_vars.append(f)
solver.add(Sum([If(b,1,0) for b in forensic_vars]) >= 8)

# Hate matrix H[p][q]
H = [[Bool(f"H_{p}_{q}") for q in range(NUM_PEOPLE)] for p in range(NUM_PEOPLE)]
# Agatha hates everybody except the butler (and not herself)
for q in range(NUM_PEOPLE):
    if q == 0 or q == 1:
        solver.add(H[0][q] == False)
    else:
        solver.add(H[0][q] == True)

# Richer matrix R[p][q]
R = [[Bool(f"R_{p}_{q}") for q in range(NUM_PEOPLE)] for p in range(NUM_PEOPLE)]
for p in range(NUM_PEOPLE):
    solver.add(R[p][p] == False)
    for q in range(p+1, NUM_PEOPLE):
        solver.add(Not(And(R[p][q], R[q][p])))
        # No further constraints on richness

# Butler hates everyone not richer than Agatha (person 0)
for p in range(NUM_PEOPLE):
    solver.add(Implies(Not(R[p][0]), H[1][p]))
# Butler also hates everyone whom Agatha hates
for q in range(NUM_PEOPLE):
    solver.add(Implies(H[0][q], H[1][q]))

# Charles hates no one that Agatha hates
for q in range(NUM_PEOPLE):
    solver.add(Implies(H[0][q], Not(H[2][q])))

# No one hates everyone
for p in range(NUM_PEOPLE):
    solver.add(Or([Not(H[p][q]) for q in range(NUM_PEOPLE)]))

# Killer variable
killer = Int('killer')
solver.add(killer >= 0, killer < NUM_PEOPLE)
solver.add(killer != 0)  # not the victim
# Killer must be in Study at time 4
for p in range(NUM_PEOPLE):
    solver.add(Implies(killer == p, loc[p][4] == 0))
# Killer hates victim
for p in range(NUM_PEOPLE):
    solver.add(Implies(killer == p, H[p][0] == True))
# Killer not richer than victim
for p in range(NUM_PEOPLE):
    solver.add(Implies(killer == p, Not(R[p][0])))

# Weapon used is Knife (index 1)
weapon_used = Int('weapon_used')
solver.add(weapon_used == 1)

# Check
result = solver.check()
if result == sat:
    m = solver.model()
    k = m.eval(killer).as_long()
    print("STATUS: sat")
    print(f"killer = {k}")
    print(f"killer_name = {people_names[k]}")
else:
    print("STATUS: unsat")