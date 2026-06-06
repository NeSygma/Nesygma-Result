from z3 import *

# Define EnumSorts for each attribute domain
Person = EnumSort('Person', ['Evelyn', 'Frank', 'Grace', 'Henry', 'Iris'])
Location = EnumSort('Location', ['Library', 'Park', 'Cafe', 'Museum', 'Studio'])
Hobby = EnumSort('Hobby', ['Painting', 'Coding', 'Gardening', 'Baking', 'Sculpting'])
Snack = EnumSort('Snack', ['Apple', 'Muffin', 'Nuts', 'Yogurt', 'Tea'])
Project = EnumSort('Project', ['A', 'B', 'C', 'D', 'E'])

# Extract the constructors for each enum
Person_Evelyn, Person_Frank, Person_Grace, Person_Henry, Person_Iris = Person
Location_Library, Location_Park, Location_Cafe, Location_Museum, Location_Studio = Location
Hobby_Painting, Hobby_Coding, Hobby_Gardening, Hobby_Baking, Hobby_Sculpting = Hobby
Snack_Apple, Snack_Muffin, Snack_Nuts, Snack_Yogurt, Snack_Tea = Snack
Project_A, Project_B, Project_C, Project_D, Project_E = Project

# Create a list of people
people = [Person_Evelyn, Person_Frank, Person_Grace, Person_Henry, Person_Iris]

# Create symbolic variables for each person's attributes
locations = [Const(f"loc_{i}", Location) for i in range(5)]
hobbies = [Const(f"hobby_{i}", Hobby) for i in range(5)]
snacks = [Const(f"snack_{i}", Snack) for i in range(5)]
projects = [Const(f"proj_{i}", Project) for i in range(5)]

# Helper function to get the index of a person in the list
def person_index(p):
    return IndexOf(people, p)

# Helper function to get the location of a person
def get_location(p):
    idx = person_index(p)
    return locations[idx]

# Helper function to get the hobby of a person
def get_hobby(p):
    idx = person_index(p)
    return hobbies[idx]

# Helper function to get the snack of a person
def get_snack(p):
    idx = person_index(p)
    return snacks[idx]

# Helper function to get the project of a person
def get_project(p):
    idx = person_index(p)
    return projects[idx]

# Create solver
solver = Solver()

# Constraint: All locations are distinct
solver.add(Distinct(locations))

# Constraint: All hobbies are distinct
solver.add(Distinct(hobbies))

# Constraint: All snacks are distinct
solver.add(Distinct(snacks))

# Constraint: All projects are distinct
solver.add(Distinct(projects))

# Constraint 4: Henry works on Project D
solver.add(get_project(Person_Henry) == Project_D)

# Constraint 8: Frank is at the Cafe
solver.add(get_location(Person_Frank) == Location_Cafe)

# Constraint 9: Evelyn does not enjoy Gardening
solver.add(get_hobby(Person_Evelyn) != Hobby_Gardening)

# Constraint 1: The person who enjoys Coding is in a location alphabetically before the person who enjoys Gardening
# Find the indices of the Coding and Gardening people
coding_idx = [i for i in range(5) if hobbies[i] == Hobby_Coding][0]
gardening_idx = [i for i in range(5) if hobbies[i] == Hobby_Gardening][0]

# Get their locations
coding_loc = locations[coding_idx]
gardening_loc = locations[gardening_idx]

# Constraint: coding_loc < gardening_loc (alphabetical order)
solver.add(coding_loc < gardening_loc)

# Constraint 2: For any person whose hobby is not Painting, their snack must not be Apple
for i in range(5):
    solver.add(Implies(hobbies[i] != Hobby_Painting, snacks[i] != Snack_Apple))

# Constraint 3: The number of people whose hobby starts with 'S' or 'C' is exactly 2
# Hobbies starting with 'S' or 'C': Sculpting, Coding
sculpting_count = Sum([hobbies[i] == Hobby_Sculpting for i in range(5)])
coding_count = Sum([hobbies[i] == Hobby_Coding for i in range(5)])
solver.add(sculpting_count + coding_count == 2)

# Constraint 5: The person in the Museum does not eat Nuts
museum_idx = [i for i in range(5) if locations[i] == Location_Museum][0]
solver.add(snacks[museum_idx] != Snack_Nuts)

# Constraint 6: The person whose project is 'E' is in a location alphabetically after the person whose project is 'A'
project_a_idx = [i for i in range(5) if projects[i] == Project_A][0]
project_e_idx = [i for i in range(5) if projects[i] == Project_E][0]
project_a_loc = locations[project_a_idx]
project_e_loc = locations[project_e_idx]
solver.add(project_e_loc > project_a_loc)

# Constraint 7: The person who enjoys Baking has a project alphabetically after the project of the person in the Park
park_idx = [i for i in range(5) if locations[i] == Location_Park][0]
baking_idx = [i for i in range(5) if hobbies[i] == Hobby_Baking][0]
park_project = projects[park_idx]
baking_project = projects[baking_idx]
solver.add(baking_project > park_project)

# Constraint 10: The alphabetical distance between the project of the person eating Muffins and the project of the person enjoying Sculpting is exactly 2
muffin_idx = [i for i in range(5) if snacks[i] == Snack_Muffin][0]
sculpting_idx = [i for i in range(5) if hobbies[i] == Hobby_Sculpting][0]
muffin_project = projects[muffin_idx]
sculpting_project = projects[sculpting_idx]

# Add constraint: (muffin_project, sculpting_project) must be one of the pairs with distance 2
solver.add(Or(
    And(muffin_project == Project_A, sculpting_project == Project_C),
    And(muffin_project == Project_B, sculpting_project == Project_D),
    And(muffin_project == Project_C, sculpting_project == Project_E),
    And(muffin_project == Project_C, sculpting_project == Project_A),
    And(muffin_project == Project_D, sculpting_project == Project_B),
    And(muffin_project == Project_E, sculpting_project == Project_C),
))

# Constraint 11: The sum of compatibility scores for all five hobby-snack assignments must be exactly 15
# Compatibility scores:
# (Painting, Apple): 3
# (Coding, Muffin): 5
# (Gardening, Nuts): 2
# (Baking, Yogurt): 4
# (Sculpting, Tea): 1

# Create a list of compatibility scores for each person
compatibility_scores = [
    If(And(hobbies[i] == Hobby_Painting, snacks[i] == Snack_Apple), 3,
        If(And(hobbies[i] == Hobby_Coding, snacks[i] == Snack_Muffin), 5,
            If(And(hobbies[i] == Hobby_Gardening, snacks[i] == Snack_Nuts), 2,
                If(And(hobbies[i] == Hobby_Baking, snacks[i] == Snack_Yogurt), 4,
                    If(And(hobbies[i] == Hobby_Sculpting, snacks[i] == Snack_Tea), 1, 0)
                )
            )
        )
    )
    for i in range(5)
]

# Sum the compatibility scores and assert it equals 15
total_score = Sum(compatibility_scores)
solver.add(total_score == 15)

# Check satisfiability
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    for i, person in enumerate(people):
        print(f"Person: {person}")
        print(f"  Location: {model[locations[i]]}")
        print(f"  Hobby: {model[hobbies[i]]}")
        print(f"  Snack: {model[snacks[i]]}")
        print(f"  Project: {model[projects[i]]}")
        print()
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")