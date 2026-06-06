from z3 import *

solver = Solver()

# People: 0=Evelyn, 1=Frank, 2=Grace, 3=Henry, 4=Iris
# Locations: 0=Library, 1=Park, 2=Cafe, 3=Museum, 4=Studio
# Hobbies: 0=Baking, 1=Coding, 2=Gardening, 3=Painting, 4=Sculpting
# Snacks: 0=Apple, 1=Muffin, 2=Nuts, 3=Tea, 4=Yogurt
# Projects: 0=A, 1=B, 2=C, 3=D, 4=E

n = 5

people_names = ["Evelyn", "Frank", "Grace", "Henry", "Iris"]
location_names = ["Library", "Park", "Cafe", "Museum", "Studio"]
hobby_names = ["Baking", "Coding", "Gardening", "Painting", "Sculpting"]
snack_names = ["Apple", "Muffin", "Nuts", "Tea", "Yogurt"]
project_names = ["A", "B", "C", "D", "E"]

loc = [Int(f'loc_{i}') for i in range(n)]
hobby = [Int(f'hobby_{i}') for i in range(n)]
snack = [Int(f'snack_{i}') for i in range(n)]
proj = [Int(f'proj_{i}') for i in range(n)]

# Domain constraints
for i in range(n):
    solver.add(0 <= loc[i], loc[i] < n)
    solver.add(0 <= hobby[i], hobby[i] < n)
    solver.add(0 <= snack[i], snack[i] < n)
    solver.add(0 <= proj[i], proj[i] < n)

# Uniqueness constraints (each attribute category is a permutation)
solver.add(Distinct(loc))
solver.add(Distinct(hobby))
solver.add(Distinct(snack))
solver.add(Distinct(proj))

# --- Constraint 1 ---
# The person who enjoys Coding (hobby=1) is in a location alphabetically
# before the person who enjoys Gardening (hobby=2).
for i in range(n):
    for j in range(n):
        solver.add(Implies(And(hobby[i]==1, hobby[j]==2), loc[i] < loc[j]))

# --- Constraint 2 ---
# For any person whose hobby is not Painting (hobby!=3), snack must not be Apple (snack!=0).
for i in range(n):
    solver.add(Implies(hobby[i] != 3, snack[i] != 0))
    # Contrapositive: if snack is Apple, hobby must be Painting
    solver.add(Implies(snack[i] == 0, hobby[i] == 3))

# --- Constraint 3 ---
# Number of people whose hobby starts with 'S' or 'C' is exactly 2.
# S: Sculpting (4), C: Coding (1)
solver.add(Sum([If(Or(hobby[i]==1, hobby[i]==4), 1, 0) for i in range(n)]) == 2)

# --- Constraint 4 ---
# Henry (index 3) works on Project D (index 3).
solver.add(proj[3] == 3)

# --- Constraint 5 ---
# The person in the Museum (loc=3) does not eat Nuts (snack!=2).
for i in range(n):
    solver.add(Implies(loc[i]==3, snack[i]!=2))

# --- Constraint 6 ---
# The person whose project is 'E' (proj=4) is in a location alphabetically
# after the person whose project is 'A' (proj=0).
for i in range(n):
    for j in range(n):
        solver.add(Implies(And(proj[i]==4, proj[j]==0), loc[i] > loc[j]))

# --- Constraint 7 ---
# The person who enjoys Baking (hobby=0) has a project alphabetically after
# the project of the person in the Park (loc=1).
for i in range(n):
    for j in range(n):
        solver.add(Implies(And(hobby[i]==0, loc[j]==1), proj[i] > proj[j]))

# --- Constraint 8 ---
# Frank (index 1) is at the Cafe (loc=2).
solver.add(loc[1] == 2)

# --- Constraint 9 ---
# Evelyn (index 0) does not enjoy Gardening (hobby!=2).
solver.add(hobby[0] != 2)

# --- Constraint 10 ---
# The alphabetical distance between the project of the person eating Muffins (snack=1)
# and the project of the person enjoying Sculpting (hobby=4) is exactly 2.
for i in range(n):
    for j in range(n):
        solver.add(Implies(And(snack[i]==1, hobby[j]==4),
                          Or(proj[i]-proj[j]==2, proj[j]-proj[i]==2)))

# --- Constraint 11 ---
# The sum of compatibility scores for all five hobby-snack assignments is exactly 15.
# Compatibility pairs:
# (Painting=3, Apple=0): 3
# (Coding=1, Muffin=1): 5
# (Gardening=2, Nuts=2): 2
# (Baking=0, Yogurt=4): 4
# (Sculpting=4, Tea=3): 1

total_score = Sum([
    If(And(hobby[i]==3, snack[i]==0), 3, 0) +   # Painting, Apple
    If(And(hobby[i]==1, snack[i]==1), 5, 0) +   # Coding, Muffin
    If(And(hobby[i]==2, snack[i]==2), 2, 0) +   # Gardening, Nuts
    If(And(hobby[i]==0, snack[i]==4), 4, 0) +   # Baking, Yogurt
    If(And(hobby[i]==4, snack[i]==3), 1, 0)     # Sculpting, Tea
    for i in range(n)
])
solver.add(total_score == 15)

# --- Solve ---
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print()
    print("Complete Assignment:")
    print("=" * 80)
    for i in range(n):
        p_name = people_names[i]
        loc_val = model[loc[i]].as_long()
        hob_val = model[hobby[i]].as_long()
        snk_val = model[snack[i]].as_long()
        prj_val = model[proj[i]].as_long()
        
        loc_name = location_names[loc_val]
        hob_name = hobby_names[hob_val]
        snk_name = snack_names[snk_val]
        prj_name = project_names[prj_val]
        
        print(f"{p_name:10s} | Location: {loc_name:10s} | Hobby: {hob_name:10s} | Snack: {snk_name:8s} | Project: {prj_name}")
    
    # Also compute the total compatibility score for verification
    total = 0
    for i in range(n):
        hv = model[hobby[i]].as_long()
        sv = model[snack[i]].as_long()
        pair_score = 0
        if hv == 3 and sv == 0:  # Painting, Apple
            pair_score = 3
        elif hv == 1 and sv == 1:  # Coding, Muffin
            pair_score = 5
        elif hv == 2 and sv == 2:  # Gardening, Nuts
            pair_score = 2
        elif hv == 0 and sv == 4:  # Baking, Yogurt
            pair_score = 4
        elif hv == 4 and sv == 3:  # Sculpting, Tea
            pair_score = 1
        total += pair_score
    print()
    print(f"Total Compatibility Score: {total}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")