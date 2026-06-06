from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Define the people, locations, hobbies, snacks, and projects
people = ["Evelyn", "Frank", "Grace", "Henry", "Iris"]
locations = ["Library", "Park", "Cafe", "Museum", "Studio"]
hobbies = ["Painting", "Coding", "Gardening", "Baking", "Sculpting"]
snacks = ["Apple", "Muffin", "Nuts", "Yogurt", "Tea"]
projects = ["A", "B", "C", "D", "E"]

# Create a solver
solver = Solver()

# Create symbolic variables for assignments
# We'll use arrays where the index corresponds to a person
person_index = {p: i for i, p in enumerate(people)}
location = [Int(f"location_{i}") for i in range(5)]
hobby = [Int(f"hobby_{i}") for i in range(5)]
snack = [Int(f"snack_{i}") for i in range(5)]
project = [Int(f"project_{i}") for i in range(5)]

# Helper: All values in an array are distinct
solver.add([Distinct(location), Distinct(hobby), Distinct(snack), Distinct(project)])

# Constraint 4: Henry works on Project D
solver.add(project[person_index["Henry"]] == projects.index("D"))

# Constraint 8: Frank is at the Cafe
solver.add(location[person_index["Frank"]] == locations.index("Cafe"))

# Constraint 9: Evelyn does not enjoy Gardening
solver.add(hobby[person_index["Evelyn"]] != hobbies.index("Gardening"))

# Constraint 1: The person who enjoys Coding is in a location alphabetically before the person who enjoys Gardening
# Find the indices of the people with Coding and Gardening hobbies
coding_person = [hobby[i] == hobbies.index("Coding") for i in range(5)]
gardening_person = [hobby[i] == hobbies.index("Gardening") for i in range(5)]

# For all i, j: if person i has Coding and person j has Gardening, then location[i] < location[j]
for i in range(5):
    for j in range(5):
        solver.add(Implies(And(coding_person[i], gardening_person[j]), location[i] < location[j]))

# Constraint 2: For any person whose hobby is not Painting, their snack must not be Apple
for i in range(5):
    solver.add(Implies(hobby[i] != hobbies.index("Painting"), snack[i] != snacks.index("Apple")))

# Constraint 3: The number of people whose hobby starts with 'S' or 'C' is exactly 2
# Count hobbies starting with 'S' or 'C'
# Hobbies starting with 'S' or 'C': Sculpting (index 4), Coding (index 1)
hobby_starts_with_sc = [
    Or(hobby[i] == hobbies.index("Sculpting"), hobby[i] == hobbies.index("Coding")) for i in range(5)
]
count_sc = Sum([If(hobby_starts_with_sc[i], 1, 0) for i in range(5)])
solver.add(count_sc == 2)

# Constraint 5: The person in the Museum does not eat Nuts
for i in range(5):
    solver.add(Implies(location[i] == locations.index("Museum"), snack[i] != snacks.index("Nuts")))

# Constraint 6: The person whose project is 'E' is in a location alphabetically after the person whose project is 'A'
# Find the indices of the people with projects A and E
project_a_person = [project[i] == projects.index("A") for i in range(5)]
project_e_person = [project[i] == projects.index("E") for i in range(5)]

for i in range(5):
    for j in range(5):
        solver.add(Implies(And(project_a_person[i], project_e_person[j]), location[i] < location[j]))

# Constraint 7: The person who enjoys Baking has a project alphabetically after the project of the person in the Park
# Find the person in the Park
park_person = [location[i] == locations.index("Park") for i in range(5)]
# Find the person who enjoys Baking
baking_person = [hobby[i] == hobbies.index("Baking") for i in range(5)]

for i in range(5):
    for j in range(5):
        solver.add(Implies(And(park_person[i], baking_person[j]), project[i] < project[j]))

# Constraint 10: The alphabetical distance between the project of the person eating Muffins and the project of the person enjoying Sculpting is exactly 2
muffin_person = [snack[i] == snacks.index("Muffin") for i in range(5)]
sculpting_person = [hobby[i] == hobbies.index("Sculpting") for i in range(5)]

for i in range(5):
    for j in range(5):
        solver.add(Implies(And(muffin_person[i], sculpting_person[j]), 
                           Or(project[i] - project[j] == 2, project[j] - project[i] == 2)))

# Constraint 11: The sum of compatibility scores for all five hobby-snack assignments must be exactly 15
# Precompute compatibility scores: (hobby, snack) -> score
compatibility = {
    (hobbies.index("Painting"), snacks.index("Apple")): 3,
    (hobbies.index("Coding"), snacks.index("Muffin")): 5,
    (hobbies.index("Gardening"), snacks.index("Nuts")): 2,
    (hobbies.index("Baking"), snacks.index("Yogurt")): 4,
    (hobbies.index("Sculpting"), snacks.index("Tea")): 1,
}

# Sum the scores for each person's hobby-snack pair
total_score = 0
for i in range(5):
    h = hobby[i]
    s = snack[i]
    # If the pair is not in the compatibility dict, score is 0
    score = If(
        And(h == hobbies.index("Painting"), s == snacks.index("Apple")),
        3,
        If(
            And(h == hobbies.index("Coding"), s == snacks.index("Muffin")),
            5,
            If(
                And(h == hobbies.index("Gardening"), s == snacks.index("Nuts")),
                2,
                If(
                    And(h == hobbies.index("Baking"), s == snacks.index("Yogurt")),
                    4,
                    If(
                        And(h == hobbies.index("Sculpting"), s == snacks.index("Tea")),
                        1,
                        0
                    )
                )
            )
        )
    )
    total_score += score

solver.add(total_score == 15)

# Check the solver
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print the assignments for each person
    for i, person in enumerate(people):
        print(f"{person}:")
        print(f"  location = {locations[model.eval(location[i], model_completion=True).as_long()]}")
        print(f"  hobby = {hobbies[model.eval(hobby[i], model_completion=True).as_long()]}")
        print(f"  snack = {snacks[model.eval(snack[i], model_completion=True).as_long()]}")
        print(f"  project = {projects[model.eval(project[i], model_completion=True).as_long()]}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")