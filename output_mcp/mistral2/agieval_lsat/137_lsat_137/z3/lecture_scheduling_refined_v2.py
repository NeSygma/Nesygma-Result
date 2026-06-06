from z3 import *

solver = Solver()

# Entities and variables
lectures = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]
halls = ["Gladwyn", "Howard"]
lecture_order = [Int(f"lecture_{i}") for i in range(5)]  # lecture_order[i] = index of bird type for position i
lecture_hall = [Int(f"hall_{i}") for i in range(5)]      # lecture_hall[i] = 0 for Gladwyn, 1 for Howard

# Helper: Map bird type to its index
bird_to_idx = {bird: idx for idx, bird in enumerate(lectures)}

# Constraints

# 1. The first lecture is in Gladwyn Hall
solver.add(lecture_hall[0] == 0)

# 2. The fourth lecture is in Howard Auditorium
solver.add(lecture_hall[3] == 1)

# 3. Exactly three of the lectures are in Gladwyn Hall
solver.add(Sum([If(lecture_hall[i] == 0, 1, 0) for i in range(5)]) == 3)

# 4. The lecture on sandpipers is in Howard Auditorium and is given earlier than the lecture on oystercatchers
solver.add(lecture_hall[bird_to_idx["sandpipers"]] == 1)
solver.add(lecture_order[bird_to_idx["sandpipers"]] < lecture_order[bird_to_idx["oystercatchers"]])

# 5. The lecture on terns is given earlier than the lecture on petrels, which is in Gladwyn Hall
solver.add(lecture_order[bird_to_idx["terns"]] < lecture_order[bird_to_idx["petrels"]])
solver.add(lecture_hall[bird_to_idx["petrels"]] == 0)

# 6. All lectures are in some order (permutation of bird types)
solver.add(Distinct(lecture_order))

# 7. Hall assignments are 0 or 1
for i in range(5):
    solver.add(Or(lecture_hall[i] == 0, lecture_hall[i] == 1))

# 8. Lecture order is a permutation of 0..4
for i in range(5):
    solver.add(lecture_order[i] >= 0, lecture_order[i] < 5)

# 9. Ensure no two lectures have the same bird type in the same position
for i in range(5):
    for j in range(i+1, 5):
        solver.add(lecture_order[i] != lecture_order[j])

# Additional constraint: The lecture on sandpipers must be in one of the first three positions
# because it is in Howard and must be earlier than oystercatchers, and oystercatchers cannot be in position 4 if sandpipers is in position 4.
solver.add(lecture_order[bird_to_idx["sandpipers"]] < 3)

# Additional constraint: The lecture on oystercatchers must be after sandpipers and cannot be in position 0 or 1 if sandpipers is in position 2.
# This is implicitly handled by the earlier constraints.

# Base constraints are set. Now evaluate each option for the fifth lecture.

# Option A: It is on oystercatchers and is in Gladwyn Hall
opt_a_constr = And(
    lecture_order[bird_to_idx["oystercatchers"]] == 4,
    lecture_hall[4] == 0
)

# Option B: It is on petrels and is in Howard Auditorium
opt_b_constr = And(
    lecture_order[bird_to_idx["petrels"]] == 4,
    lecture_hall[4] == 1
)

# Option C: It is on rails and is in Howard Auditorium
opt_c_constr = And(
    lecture_order[bird_to_idx["rails"]] == 4,
    lecture_hall[4] == 1
)

# Option D: It is on sandpipers and is in Howard Auditorium
opt_d_constr = And(
    lecture_order[bird_to_idx["sandpipers"]] == 4,
    lecture_hall[4] == 1
)

# Option E: It is on terns and is in Gladwyn Hall
opt_e_constr = And(
    lecture_order[bird_to_idx["terns"]] == 4,
    lecture_hall[4] == 0
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
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