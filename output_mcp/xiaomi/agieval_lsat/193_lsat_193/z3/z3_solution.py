from z3 import *

# Students: Louis=0, Mollie=1, Onyx=2, Ryan=3, Tiffany=4, Yoshio=5
# Years: 1921=0, 1922=1, 1923=2, 1924=3
# We need to find which students COULD be assigned to 1921

students = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']
years = [1921, 1922, 1923, 1924]

# For each student, check if there exists a valid assignment where that student is assigned to 1921
could_be_1921 = []

for target_student in range(6):
    solver = Solver()
    
    # Assignment: assign[s] = year assigned to student s, or -1 if not assigned
    assign = [Int(f'assign_{s}') for s in range(6)]
    
    # Each student is either assigned to a year (0-3) or not assigned (-1)
    for s in range(6):
        solver.add(Or(assign[s] == -1, assign[s] == 0, assign[s] == 1, assign[s] == 2, assign[s] == 3))
    
    # Exactly 4 students are assigned (exactly 4 have assign[s] != -1)
    solver.add(Sum([If(assign[s] != -1, 1, 0) for s in range(6)]) == 4)
    
    # Each year has exactly one student assigned
    for y in range(4):
        solver.add(Sum([If(assign[s] == y, 1, 0) for s in range(6)]) == 1)
    
    # Condition 1: Only Louis (0) or Tiffany (4) can be assigned to 1923 (year index 2)
    for s in range(6):
        if s != 0 and s != 4:
            solver.add(assign[s] != 2)
    
    # Condition 2: If Mollie (1) is assigned, she must be assigned to 1921 (0) or 1922 (1)
    solver.add(Implies(assign[1] != -1, Or(assign[1] == 0, assign[1] == 1)))
    
    # Condition 3: If Tiffany (4) is assigned, then Ryan (3) must be assigned
    solver.add(Implies(assign[4] != -1, assign[3] != -1))
    
    # Condition 4: If Ryan (3) is assigned, then Onyx (2) must be assigned to the year immediately prior
    # "immediately prior" means Ryan's year - 1
    solver.add(Implies(assign[3] != -1, And(assign[2] != -1, assign[2] == assign[3] - 1)))
    
    # Target: this student is assigned to 1921 (year index 0)
    solver.add(assign[target_student] == 0)
    
    result = solver.check()
    if result == sat:
        could_be_1921.append(students[target_student])

print(f"Students who could be assigned to 1921: {could_be_1921}")
print(f"Count: {len(could_be_1921)}")

# Now evaluate the answer choices
# (A) six = 6, (B) five = 5, (C) four = 4, (D) three = 3, (E) two = 2
count = len(could_be_1921)

found_options = []
for letter, target_count in [("A", 6), ("B", 5), ("C", 4), ("D", 3), ("E", 2)]:
    if count == target_count:
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