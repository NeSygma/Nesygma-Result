from z3 import *

# People
people = ["Evelyn", "Frank", "Grace", "Henry", "Iris"]
# Locations
locations = ["Library", "Park", "Cafe", "Museum", "Studio"]
# Hobbies
hobbies = ["Painting", "Coding", "Gardening", "Baking", "Sculpting"]
# Snacks
snacks = ["Apple", "Muffin", "Nuts", "Yogurt", "Tea"]
# Projects
projects = ["A", "B", "C", "D", "E"]

# Create integer variables for each attribute per person
loc = {p: Int(f"loc_{p}") for p in people}
hob = {p: Int(f"hob_{p}") for p in people}
snk = {p: Int(f"snk_{p}") for p in people}
proj = {p: Int(f"proj_{p}") for p in people}

# Index mappings
loc_idx = {l: i for i, l in enumerate(locations)}
hob_idx = {h: i for i, h in enumerate(hobbies)}
snk_idx = {s: i for i, s in enumerate(snacks)}
proj_idx = {pr: i for i, pr in enumerate(projects)}

solver = Solver()

# Each attribute is in range [0, 4]
for p in people:
    solver.add(And(loc[p] >= 0, loc[p] < 5))
    solver.add(And(hob[p] >= 0, hob[p] < 5))
    solver.add(And(snk[p] >= 0, snk[p] < 5))
    solver.add(And(proj[p] >= 0, proj[p] < 5))

# All attributes are distinct (each person has unique values)
solver.add(Distinct([loc[p] for p in people]))
solver.add(Distinct([hob[p] for p in people]))
solver.add(Distinct([snk[p] for p in people]))
solver.add(Distinct([proj[p] for p in people]))

# Constraint 1: Coding person's location is alphabetically before Gardening person's location
# Find who has Coding and who has Gardening
for p1 in people:
    for p2 in people:
        solver.add(Implies(And(hob[p1] == hob_idx["Coding"], hob[p2] == hob_idx["Gardening"]),
                           loc[p1] < loc[p2]))

# Constraint 2: If hobby != Painting, then snack != Apple
for p in people:
    solver.add(Implies(hob[p] != hob_idx["Painting"], snk[p] != snk_idx["Apple"]))

# Constraint 3: Exactly 2 people have hobby starting with 'S' or 'C'
# Hobbies starting with S or C: Sculpting (S), Coding (C)
solver.add(Sum([If(Or(hob[p] == hob_idx["Sculpting"], hob[p] == hob_idx["Coding"]), 1, 0) for p in people]) == 2)

# Constraint 4: Henry works on Project D
solver.add(proj["Henry"] == proj_idx["D"])

# Constraint 5: Museum person does not eat Nuts
for p in people:
    solver.add(Implies(loc[p] == loc_idx["Museum"], snk[p] != snk_idx["Nuts"]))

# Constraint 6: Project E person's location is alphabetically after Project A person's location
for p1 in people:
    for p2 in people:
        solver.add(Implies(And(proj[p1] == proj_idx["E"], proj[p2] == proj_idx["A"]),
                           loc[p1] > loc[p2]))

# Constraint 7: Baking person's project is alphabetically after Park person's project
for p1 in people:
    for p2 in people:
        solver.add(Implies(And(hob[p1] == hob_idx["Baking"], loc[p2] == loc_idx["Park"]),
                           proj[p1] > proj[p2]))

# Constraint 8: Frank is at the Cafe
solver.add(loc["Frank"] == loc_idx["Cafe"])

# Constraint 9: Evelyn does not enjoy Gardening
solver.add(hob["Evelyn"] != hob_idx["Gardening"])

# Constraint 10: Alphabetical distance between Muffin person's project and Sculpting person's project is exactly 2
for p1 in people:
    for p2 in people:
        solver.add(Implies(And(snk[p1] == snk_idx["Muffin"], hob[p2] == hob_idx["Sculpting"]),
                           Or(proj[p1] - proj[p2] == 2, proj[p2] - proj[p1] == 2)))

# Constraint 11: Sum of compatibility scores is exactly 15
# Compatibility scores: (Painting, Apple): 3, (Coding, Muffin): 5, (Gardening, Nuts): 2, (Baking, Yogurt): 4, (Sculpting, Tea): 1
compat = []
for p in people:
    compat.append(If(And(hob[p] == hob_idx["Painting"], snk[p] == snk_idx["Apple"]), 3, 0))
    compat.append(If(And(hob[p] == hob_idx["Coding"], snk[p] == snk_idx["Muffin"]), 5, 0))
    compat.append(If(And(hob[p] == hob_idx["Gardening"], snk[p] == snk_idx["Nuts"]), 2, 0))
    compat.append(If(And(hob[p] == hob_idx["Baking"], snk[p] == snk_idx["Yogurt"]), 4, 0))
    compat.append(If(And(hob[p] == hob_idx["Sculpting"], snk[p] == snk_idx["Tea"]), 1, 0))
solver.add(Sum(compat) == 15)

# Solve
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Solution found!")
    for p in people:
        l = locations[m[loc[p]].as_long()]
        h = hobbies[m[hob[p]].as_long()]
        s = snacks[m[snk[p]].as_long()]
        pr = projects[m[proj[p]].as_long()]
        print(f"  {p}: Location={l}, Hobby={h}, Snack={s}, Project={pr}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")