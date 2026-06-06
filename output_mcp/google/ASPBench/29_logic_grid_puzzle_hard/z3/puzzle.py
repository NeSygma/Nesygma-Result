from z3 import *

# People: 0:Evelyn, 1:Frank, 2:Grace, 3:Henry, 4:Iris
# Locations: 0:Cafe, 1:Library, 2:Museum, 3:Park, 4:Studio (Alphabetical)
# Hobbies: 0:Baking, 1:Coding, 2:Gardening, 3:Painting, 4:Sculpting (Alphabetical)
# Snacks: 0:Apple, 1:Muffin, 2:Nuts, 3:Tea, 4:Yogurt (Alphabetical)
# Projects: 0:A, 1:B, 2:C, 3:D, 4:E

solver = Solver()

# Variables
# Each person has a location, hobby, snack, project
loc = [Int(f'loc_{i}') for i in range(5)]
hob = [Int(f'hob_{i}') for i in range(5)]
sna = [Int(f'sna_{i}') for i in range(5)]
pro = [Int(f'pro_{i}') for i in range(5)]

# Domains
for i in range(5):
    solver.add(loc[i] >= 0, loc[i] < 5)
    solver.add(hob[i] >= 0, hob[i] < 5)
    solver.add(sna[i] >= 0, sna[i] < 5)
    solver.add(pro[i] >= 0, pro[i] < 5)

# Uniqueness
solver.add(Distinct(loc))
solver.add(Distinct(hob))
solver.add(Distinct(sna))
solver.add(Distinct(pro))

# Compatibility Scores
# (Painting, Apple): 3, (Coding, Muffin): 5, (Gardening, Nuts): 2, (Baking, Yogurt): 4, (Sculpting, Tea): 1
def get_score(h, s):
    return If(And(h == 3, s == 0), 3,
           If(And(h == 1, s == 1), 5,
           If(And(h == 2, s == 2), 2,
           If(And(h == 0, s == 4), 4,
           If(And(h == 4, s == 3), 1, 0)))))

# Constraint 1: Coding person's location < Gardening person's location
# Coding: 1, Gardening: 2
c_loc = Int('c_loc')
g_loc = Int('g_loc')
solver.add(Or([And(hob[i] == 1, c_loc == loc[i]) for i in range(5)]))
solver.add(Or([And(hob[i] == 2, g_loc == loc[i]) for i in range(5)]))
solver.add(c_loc < g_loc)

# Constraint 2: If snack == Apple, hobby == Painting
# Apple: 0, Painting: 3
for i in range(5):
    solver.add(Implies(sna[i] == 0, hob[i] == 3))

# Constraint 3: Count of (hobby starts with 'S' or 'C') == 2
# Coding: 1, Sculpting: 4
solver.add(Sum([If(Or(hob[i] == 1, hob[i] == 4), 1, 0) for i in range(5)]) == 2)

# Constraint 4: Henry works on Project D (Henry: 3, Project D: 3)
solver.add(pro[3] == 3)

# Constraint 5: Museum person's snack != Nuts (Museum: 2, Nuts: 2)
for i in range(5):
    solver.add(Implies(loc[i] == 2, sna[i] != 2))

# Constraint 6: Project E's location > Project A's location (Project E: 4, Project A: 0)
e_loc = Int('e_loc')
a_loc = Int('a_loc')
solver.add(Or([And(pro[i] == 4, e_loc == loc[i]) for i in range(5)]))
solver.add(Or([And(pro[i] == 0, a_loc == loc[i]) for i in range(5)]))
solver.add(e_loc > a_loc)

# Constraint 7: Baking person's project > Park person's project (Baking: 0, Park: 3)
b_pro = Int('b_pro')
p_pro = Int('p_pro')
solver.add(Or([And(hob[i] == 0, b_pro == pro[i]) for i in range(5)]))
solver.add(Or([And(loc[i] == 3, p_pro == pro[i]) for i in range(5)]))
solver.add(b_pro > p_pro)

# Constraint 8: Frank is at the Cafe (Frank: 1, Cafe: 0)
solver.add(loc[1] == 0)

# Constraint 9: Evelyn does not enjoy Gardening (Evelyn: 0, Gardening: 2)
solver.add(hob[0] != 2)

# Constraint 10: |Project(Muffin) - Project(Sculpting)| = 2 (Muffin: 1, Sculpting: 4)
m_pro = Int('m_pro')
s_pro = Int('s_pro')
solver.add(Or([And(sna[i] == 1, m_pro == pro[i]) for i in range(5)]))
solver.add(Or([And(hob[i] == 4, s_pro == pro[i]) for i in range(5)]))
solver.add(Or(m_pro - s_pro == 2, s_pro - m_pro == 2))

# Constraint 11: Sum of compatibility scores = 15
solver.add(Sum([get_score(hob[i], sna[i]) for i in range(5)]) == 15)

if solver.check() == sat:
    print("STATUS: sat")
    m = solver.model()
    people = ["Evelyn", "Frank", "Grace", "Henry", "Iris"]
    locations = ["Cafe", "Library", "Museum", "Park", "Studio"]
    hobbies = ["Baking", "Coding", "Gardening", "Painting", "Sculpting"]
    snacks = ["Apple", "Muffin", "Nuts", "Tea", "Yogurt"]
    projects = ["A", "B", "C", "D", "E"]
    for i in range(5):
        print(f"{people[i]}: Loc={locations[m[loc[i]].as_long()]}, Hob={hobbies[m[hob[i]].as_long()]}, Sna={snacks[m[sna[i]].as_long()]}, Pro={projects[m[pro[i]].as_long()]}")
else:
    print("STATUS: unsat")