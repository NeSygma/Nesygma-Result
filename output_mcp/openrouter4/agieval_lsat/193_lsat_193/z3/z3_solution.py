from z3 import *

# Student indices
Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio = 0, 1, 2, 3, 4, 5
student_names = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]

solver = Solver()

# year[i] = student assigned to year (1921 + i), i in {0,1,2,3}
year = [Int(f"year_{i}") for i in range(4)]

# Domain: each year gets a student index 0-5
for i in range(4):
    solver.add(year[i] >= 0, year[i] <= 5)

# Each year gets a different student (exactly 4 distinct students assigned)
solver.add(Distinct(year))

# Only Louis (0) or Tiffany (4) can be assigned to 1923 (year index 2)
solver.add(Or(year[2] == Louis, year[2] == Tiffany))

# If Mollie (1) is assigned, she must be in 1921 or 1922 (year index 0 or 1)
solver.add(Implies(
    Or([year[i] == Mollie for i in range(4)]),
    Or(year[0] == Mollie, year[1] == Mollie)
))

# If Tiffany (4) is assigned, Ryan (3) must be assigned
solver.add(Implies(
    Or([year[i] == Tiffany for i in range(4)]),
    Or([year[i] == Ryan for i in range(4)])
))

# If Ryan (3) is assigned, Onyx (2) must be assigned to the year immediately prior to Ryan's
solver.add(Implies(
    Or([year[i] == Ryan for i in range(4)]),
    Or([And(year[i] == Ryan, year[i-1] == Onyx) for i in range(1, 4)])
))

# Count how many students could be assigned to 1921 (year index 0)
count = 0
possible_students = []
for s in range(6):
    solver.push()
    solver.add(year[0] == s)
    if solver.check() == sat:
        count += 1
        possible_students.append(student_names[s])
        print(f"  {student_names[s]} CAN be assigned to 1921. Model: {solver.model()}")
    else:
        print(f"  {student_names[s]} CANNOT be assigned to 1921.")
    solver.pop()

print(f"\nCount of possible students for 1921: {count}")
print(f"Possible students: {possible_students}")

# Match to answer choices
options_list = [("A", 6), ("B", 5), ("C", 4), ("D", 3), ("E", 2)]

found_options = []
for letter, expected_count in options_list:
    if count == expected_count:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")