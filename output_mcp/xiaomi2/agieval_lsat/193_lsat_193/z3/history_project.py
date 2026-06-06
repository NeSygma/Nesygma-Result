from z3 import *

# Students: 0=Louis, 1=Mollie, 2=Onyx, 3=Ryan, 4=Tiffany, 5=Yoshio
LOUIS, MOLLIE, ONYX, RYAN, TIFFANY, YOSHIO = 0, 1, 2, 3, 4, 5
student_names = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]

def check_student_can_be_1921(s):
    """Check if student s can be assigned to 1921 in some valid configuration."""
    solver = Solver()
    
    # Variables: which student is assigned to each year
    y21 = Int('y21')
    y22 = Int('y22')
    y23 = Int('y23')
    y24 = Int('y24')
    years = [y21, y22, y23, y24]
    
    # Domain: each year assigned to one of 6 students
    for y in years:
        solver.add(y >= 0, y <= 5)
    
    # All four years have different students
    solver.add(Distinct(y21, y22, y23, y24))
    
    # Condition 1: Only Louis or Tiffany can be assigned to 1923
    solver.add(Or(y23 == LOUIS, y23 == TIFFANY))
    
    # Condition 2: If Mollie is assigned to the project, she must be in 1921 or 1922
    mollie_assigned = Or(y21 == MOLLIE, y22 == MOLLIE, y23 == MOLLIE, y24 == MOLLIE)
    solver.add(Implies(mollie_assigned, Or(y21 == MOLLIE, y22 == MOLLIE)))
    
    # Condition 3: If Tiffany is assigned, then Ryan must be assigned
    tiffany_assigned = Or(y21 == TIFFANY, y22 == TIFFANY, y23 == TIFFANY, y24 == TIFFANY)
    ryan_assigned = Or(y21 == RYAN, y22 == RYAN, y23 == RYAN, y24 == RYAN)
    solver.add(Implies(tiffany_assigned, ryan_assigned))
    
    # Condition 4: If Ryan is assigned, then Onyx must be in the year immediately prior
    # Ryan in 1922 -> Onyx in 1921
    # Ryan in 1923 -> Onyx in 1922
    # Ryan in 1924 -> Onyx in 1923
    # Ryan in 1921 -> impossible (no prior year)
    solver.add(Implies(ryan_assigned, 
        Or(
            And(y22 == RYAN, y21 == ONYX),
            And(y23 == RYAN, y22 == ONYX),
            And(y24 == RYAN, y23 == ONYX)
        )
    ))
    
    # This student is assigned to 1921
    solver.add(y21 == s)
    
    result = solver.check()
    if result == sat:
        m = solver.model()
        print(f"  {student_names[s]} -> 1921: SAT (e.g., y21={m[y21]}, y22={m[y22]}, y23={m[y23]}, y24={m[y24]})")
        return True
    else:
        print(f"  {student_names[s]} -> 1921: UNSAT")
        return False

# Check each student
could_be_1921 = []
for s in range(6):
    if check_student_can_be_1921(s):
        could_be_1921.append(s)

count = len(could_be_1921)
print(f"\nStudents who could be assigned to 1921: {[student_names[s] for s in could_be_1921]}")
print(f"Count: {count}")

# Now evaluate answer choices
# (A) six=6, (B) five=5, (C) four=4, (D) three=3, (E) two=2
answer_map = {"A": 6, "B": 5, "C": 4, "D": 3, "E": 2}

found_options = []
for letter, target_count in answer_map.items():
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