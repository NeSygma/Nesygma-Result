from z3 import *

# Define constants
people = ['Evelyn', 'Frank', 'Grace', 'Henry', 'Iris']
locations = ['Cafe', 'Library', 'Museum', 'Park', 'Studio']  # alphabetical order
hobbies = ['Painting', 'Coding', 'Gardening', 'Baking', 'Sculpting']
projects = ['A', 'B', 'C', 'D', 'E']
# snack mapping based on hobby
snack_map = {
    'Painting': 'Apple',
    'Coding': 'Muffin',
    'Gardening': 'Nuts',
    'Baking': 'Yogurt',
    'Sculpting': 'Tea'
}

# Create Z3 variables for each person
loc = {p: Int(f'loc_{p}') for p in people}
hob = {p: Int(f'hob_{p}') for p in people}
proj = {p: Int(f'proj_{p}') for p in people}

solver = Solver()

# Domains 0..4
for p in people:
    solver.add(And(loc[p] >= 0, loc[p] < 5))
    solver.add(And(hob[p] >= 0, hob[p] < 5))
    solver.add(And(proj[p] >= 0, proj[p] < 5))

# All-different constraints per category
solver.add(Distinct([loc[p] for p in people]))
solver.add(Distinct([hob[p] for p in people]))
solver.add(Distinct([proj[p] for p in people]))

# Helper to get index of a name in list
def idx(name, lst):
    return lst.index(name)

# Constraint 1: Coding location before Gardening location
coding_person = [p for p in people]
# We'll encode using existential: find person with hobby Coding and Gardening
# Use expressions
coding_loc = Int('coding_loc')
gardening_loc = Int('gardening_loc')
solver.add(coding_loc == Sum([If(hob[p] == idx('Coding', hobbies), loc[p], 0) for p in people]))
solver.add(gardening_loc == Sum([If(hob[p] == idx('Gardening', hobbies), loc[p], 0) for p in people]))
solver.add(coding_loc < gardening_loc)

# Constraint 2: if hobby != Painting then snack != Apple
# Since snack is determined by hobby, this means hobby != Painting -> snack != Apple, which holds automatically because only Painting maps to Apple.
# So no extra constraint needed.

# Constraint 3: number of hobbies starting with S or C is exactly 2 (already true by uniqueness)
# No extra constraint.

# Constraint 4: Henry works on Project D
solver.add(proj['Henry'] == idx('D', projects))

# Constraint 5: person in Museum does not eat Nuts -> hobby not Gardening (since Nuts only with Gardening)
# So location Museum cannot have hobby Gardening.
for p in people:
    solver.add(Implies(loc[p] == idx('Museum', locations), hob[p] != idx('Gardening', hobbies)))

# Constraint 6: project E location after project A location
projE_loc = Int('projE_loc')
projA_loc = Int('projA_loc')
solver.add(projE_loc == Sum([If(proj[p] == idx('E', projects), loc[p], 0) for p in people]))
solver.add(projA_loc == Sum([If(proj[p] == idx('A', projects), loc[p], 0) for p in people]))
solver.add(projE_loc > projA_loc)

# Constraint 7: Baking hobby's project after project of person in Park
baking_proj = Int('baking_proj')
park_proj = Int('park_proj')
solver.add(baking_proj == Sum([If(hob[p] == idx('Baking', hobbies), proj[p], 0) for p in people]))
solver.add(park_proj == Sum([If(loc[p] == idx('Park', locations), proj[p], 0) for p in people]))
solver.add(baking_proj > park_proj)

# Constraint 8: Frank is at Cafe
solver.add(loc['Frank'] == idx('Cafe', locations))

# Constraint 9: Evelyn does not enjoy Gardening
solver.add(hob['Evelyn'] != idx('Gardening', hobbies))

# Constraint 10: alphabetical distance between project of Muffin eater and project of Sculpting hobby is 2
# Muffin eater is the person whose hobby is Coding (since snack mapping). So project of person with hobby Coding.
proj_muffin = Int('proj_muffin')
proj_sculpt = Int('proj_sculpt')
solver.add(proj_muffin == Sum([If(hob[p] == idx('Coding', hobbies), proj[p], 0) for p in people]))
solver.add(proj_sculpt == Sum([If(hob[p] == idx('Sculpting', hobbies), proj[p], 0) for p in people]))
solver.add(Or(proj_muffin - proj_sculpt == 2, proj_sculpt - proj_muffin == 2))

# Constraint 11: sum of compatibility scores =15. Since each hobby must pair with its specific snack, we just ensure each hobby appears once (already) -> sum will be 15 automatically.
# No extra constraint needed.

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print('STATUS: sat')
    for p in people:
        loc_name = locations[m[loc[p]].as_long()]
        hob_name = hobbies[m[hob[p]].as_long()]
        snack_name = snack_map[hob_name]
        proj_name = projects[m[proj[p]].as_long()]
        print(f'{p}: location={loc_name}, hobby={hob_name}, snack={snack_name}, project={proj_name}')
else:
    print('STATUS: unsat')