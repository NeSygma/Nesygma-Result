from z3 import *

solver = Solver()

# Entities and variables
lectures = range(5)  # 0: first, 1: second, 2: third, 3: fourth, 4: fifth
birds = ['oystercatchers', 'petrels', 'rails', 'sandpipers', 'terns']
locations = ['Gladwyn Hall', 'Howard Auditorium']

# Decision variables
lecture_bird = [Int(f'lecture_bird_{i}') for i in lectures]
lecture_location = [Int(f'lecture_location_{i}') for i in lectures]

# Helper: Map birds and locations to Int values for easier constraints
bird_to_int = {b: i for i, b in enumerate(birds)}
int_to_bird = {i: b for i, b in enumerate(birds)}
loc_to_int = {l: i for i, l in enumerate(locations)}
int_to_loc = {i: l for i, l in enumerate(locations)}

# Constraints from the problem statement

# 1. The first lecture is in Gladwyn Hall
solver.add(lecture_location[0] == loc_to_int['Gladwyn Hall'])

# 2. The fourth lecture is in Howard Auditorium
solver.add(lecture_location[3] == loc_to_int['Howard Auditorium'])

# 3. Exactly three of the lectures are in Gladwyn Hall
solver.add(Sum([lecture_location[i] == loc_to_int['Gladwyn Hall'] for i in lectures]) == 3)

# 4. The lecture on sandpipers is in Howard Auditorium and is given earlier than the lecture on oystercatchers
solver.add(lecture_bird[lectures[2]] == bird_to_int['sandpipers'])  # Third lecture is on sandpipers (given in Q)
solver.add(lecture_location[lectures[2]] == loc_to_int['Howard Auditorium'])
# Sandpipers earlier than oystercatchers
solver.add(Or([
    And(lecture_bird[i] == bird_to_int['sandpipers'], 
        lecture_bird[j] == bird_to_int['oystercatchers'], 
        i < j)
    for i in lectures for j in lectures if i < j
]))

# 5. The lecture on terns is given earlier than the lecture on petrels, which is in Gladwyn Hall
solver.add(Or([
    And(lecture_bird[i] == bird_to_int['terns'], 
        lecture_bird[j] == bird_to_int['petrels'], 
        i < j,
        lecture_location[j] == loc_to_int['Gladwyn Hall'])
    for i in lectures for j in lectures if i < j
]))

# All birds are assigned to exactly one lecture
solver.add(Distinct(lecture_bird))

# All lectures have a bird assigned
for i in lectures:
    solver.add(lecture_bird[i] >= 0, lecture_bird[i] < len(birds))

# All lectures have a location assigned (already covered by location constraints)

# Base constraints for the problem (third lecture is on sandpipers)
# Already added above: solver.add(lecture_bird[2] == bird_to_int['sandpipers'])

# Now evaluate the multiple choice options
found_options = []

# Option A: The second lecture is on oystercatchers and is in Gladwyn Hall
solver.push()
solver.add(lecture_bird[1] == bird_to_int['oystercatchers'])
solver.add(lecture_location[1] == loc_to_int['Gladwyn Hall'])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The fifth lecture is on oystercatchers and is in Howard Auditorium
solver.push()
solver.add(lecture_bird[4] == bird_to_int['oystercatchers'])
solver.add(lecture_location[4] == loc_to_int['Howard Auditorium'])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: The second lecture is on rails and is in Howard Auditorium
solver.push()
solver.add(lecture_bird[1] == bird_to_int['rails'])
solver.add(lecture_location[1] == loc_to_int['Howard Auditorium'])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The second lecture is on terns and is in Gladwyn Hall
solver.push()
solver.add(lecture_bird[1] == bird_to_int['terns'])
solver.add(lecture_location[1] == loc_to_int['Gladwyn Hall'])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The fourth lecture is on terns and is in Howard Auditorium
solver.push()
solver.add(lecture_bird[3] == bird_to_int['terns'])
solver.add(lecture_location[3] == loc_to_int['Howard Auditorium'])
if solver.check() == sat:
    found_options.append("E")
solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")