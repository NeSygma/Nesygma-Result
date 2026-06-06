from z3 import *

# People
people = ["Evelyn", "Frank", "Grace", "Henry", "Iris"]
P = len(people)

# Locations
locations = ["Library", "Park", "Cafe", "Museum", "Studio"]
L = len(locations)

# Hobbies
hobbies = ["Painting", "Coding", "Gardening", "Baking", "Sculpting"]
H = len(hobbies)

# Snacks
snacks = ["Apple", "Muffin", "Nuts", "Yogurt", "Tea"]
S = len(snacks)

# Projects
projects = ["A", "B", "C", "D", "E"]
PR = len(projects)

# Alphabetical order of location names: Cafe(0), Library(1), Museum(2), Park(3), Studio(4)
# We'll use a Z3 function to map location index to alphabetical rank
loc_alpha_func = Function('loc_alpha_func', IntSort(), IntSort())

solver = Solver()

# Define the mapping: location index -> alphabetical rank
# locations: Library=0, Park=1, Cafe=2, Museum=3, Studio=4
# alphabetical: Cafe(0), Library(1), Museum(2), Park(3), Studio(4)
# So: loc 0(Library)->1, loc 1(Park)->3, loc 2(Cafe)->0, loc 3(Museum)->2, loc 4(Studio)->4
for loc_idx, alpha_rank in [(0, 1), (1, 3), (2, 0), (3, 2), (4, 4)]:
    solver.add(loc_alpha_func(loc_idx) == alpha_rank)

# Decision variables: each person gets a location, hobby, snack, project index
loc = [Int(f"loc_{i}") for i in range(P)]
hob = [Int(f"hob_{i}") for i in range(P)]
snk = [Int(f"snk_{i}") for i in range(P)]
prj = [Int(f"prj_{i}") for i in range(P)]

# Domain constraints: each attribute is 0..4
for i in range(P):
    solver.add(0 <= loc[i], loc[i] < L)
    solver.add(0 <= hob[i], hob[i] < H)
    solver.add(0 <= snk[i], snk[i] < S)
    solver.add(0 <= prj[i], prj[i] < PR)

# All different for each attribute
solver.add(Distinct(loc))
solver.add(Distinct(hob))
solver.add(Distinct(snk))
solver.add(Distinct(prj))

# Constraint 1: Coding (hob=1) location alphabetically before Gardening (hob=2)
coding_loc_alpha = Int('coding_loc_alpha')
gardening_loc_alpha = Int('gardening_loc_alpha')
solver.add(Or([And(hob[i] == 1, coding_loc_alpha == loc_alpha_func(loc[i])) for i in range(P)]))
solver.add(Or([And(hob[i] == 2, gardening_loc_alpha == loc_alpha_func(loc[i])) for i in range(P)]))
solver.add(coding_loc_alpha < gardening_loc_alpha)

# Constraint 2: For any person whose hobby is not Painting (hob != 0), snack must not be Apple (snk != 0)
for i in range(P):
    solver.add(Implies(hob[i] != 0, snk[i] != 0))

# Constraint 3: Number of people whose hobby starts with 'S' or 'C' is exactly 2
# Starts with S: Sculpting(4). Starts with C: Coding(1)
solver.add(Sum([If(Or(hob[i] == 1, hob[i] == 4), 1, 0) for i in range(P)]) == 2)

# Constraint 4: Henry (index 3) works on Project D (index 3)
solver.add(prj[3] == 3)

# Constraint 5: The person in the Museum (loc=3) does not eat Nuts (snk != 2)
for i in range(P):
    solver.add(Implies(loc[i] == 3, snk[i] != 2))

# Constraint 6: Project 'E' (index 4) location alphabetically after project 'A' (index 0)
prj_e_loc_alpha = Int('prj_e_loc_alpha')
prj_a_loc_alpha = Int('prj_a_loc_alpha')
solver.add(Or([And(prj[i] == 4, prj_e_loc_alpha == loc_alpha_func(loc[i])) for i in range(P)]))
solver.add(Or([And(prj[i] == 0, prj_a_loc_alpha == loc_alpha_func(loc[i])) for i in range(P)]))
solver.add(prj_a_loc_alpha < prj_e_loc_alpha)

# Constraint 7: Baking (hob=3) has a project alphabetically after the project of the person in the Park (loc=1)
baking_prj = Int('baking_prj')
park_prj = Int('park_prj')
solver.add(Or([And(hob[i] == 3, baking_prj == prj[i]) for i in range(P)]))
solver.add(Or([And(loc[i] == 1, park_prj == prj[i]) for i in range(P)]))
solver.add(baking_prj > park_prj)

# Constraint 8: Frank (index 1) is at the Cafe (loc=2)
solver.add(loc[1] == 2)

# Constraint 9: Evelyn (index 0) does not enjoy Gardening (hob != 2)
solver.add(hob[0] != 2)

# Constraint 10: Alphabetical distance between project of person eating Muffins (snk=1) 
# and project of person enjoying Sculpting (hob=4) is exactly 2
muffin_prj = Int('muffin_prj')
sculpting_prj = Int('sculpting_prj')
solver.add(Or([And(snk[i] == 1, muffin_prj == prj[i]) for i in range(P)]))
solver.add(Or([And(hob[i] == 4, sculpting_prj == prj[i]) for i in range(P)]))
solver.add(Or(muffin_prj - sculpting_prj == 2, sculpting_prj - muffin_prj == 2))

# Constraint 11: Sum of compatibility scores for all five hobby-snack assignments must be exactly 15
def get_score(i):
    return (If(And(hob[i] == 0, snk[i] == 0), 3, 0) +
            If(And(hob[i] == 1, snk[i] == 1), 5, 0) +
            If(And(hob[i] == 2, snk[i] == 2), 2, 0) +
            If(And(hob[i] == 3, snk[i] == 3), 4, 0) +
            If(And(hob[i] == 4, snk[i] == 4), 1, 0))

solver.add(Sum([get_score(i) for i in range(P)]) == 15)

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Solution found!")
    for i in range(P):
        pname = people[i]
        loc_name = locations[m[loc[i]].as_long()]
        hob_name = hobbies[m[hob[i]].as_long()]
        snk_name = snacks[m[snk[i]].as_long()]
        prj_name = projects[m[prj[i]].as_long()]
        print(f"{pname}: Location={loc_name}, Hobby={hob_name}, Snack={snk_name}, Project={prj_name}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")