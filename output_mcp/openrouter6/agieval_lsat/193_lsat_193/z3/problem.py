from z3 import *

# Map students to integers
Louis = 0
Mollie = 1
Onyx = 2
Ryan = 3
Tiffany = 4
Yoshio = 5

# Declare variables for each year
year1921 = Int('year1921')
year1922 = Int('year1922')
year1923 = Int('year1923')
year1924 = Int('year1924')

solver = Solver()

# Base constraints
# Each year must be one of the students (0..5)
solver.add(year1921 >= 0, year1921 <= 5)
solver.add(year1922 >= 0, year1922 <= 5)
solver.add(year1923 >= 0, year1923 <= 5)
solver.add(year1924 >= 0, year1924 <= 5)

# All years must have distinct students
solver.add(Distinct(year1921, year1922, year1923, year1924))

# Constraint 1: Only Louis or Tiffany can be assigned to 1923
solver.add(Or(year1923 == Louis, year1923 == Tiffany))

# Constraint 2: If Mollie is assigned, she must be in 1921 or 1922
# So Mollie cannot be in 1923 or 1924
solver.add(year1923 != Mollie)
solver.add(year1924 != Mollie)

# Constraint 3: If Tiffany is assigned, then Ryan must be assigned
# We'll handle this with an implication
tiffany_assigned = Or(year1921 == Tiffany, year1922 == Tiffany, year1923 == Tiffany, year1924 == Tiffany)
ryan_assigned = Or(year1921 == Ryan, year1922 == Ryan, year1923 == Ryan, year1924 == Ryan)
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Constraint 4: If Ryan is assigned, then Onyx must be assigned to the year immediately prior
# Ryan cannot be in 1921 (no prior year)
solver.add(year1921 != Ryan)
# If Ryan is in 1922, then Onyx must be in 1921
solver.add(Implies(year1922 == Ryan, year1921 == Onyx))
# If Ryan is in 1923, then Onyx must be in 1922 (but 1923 must be Louis or Tiffany, so Ryan cannot be in 1923)
solver.add(Implies(year1923 == Ryan, year1922 == Onyx))
# If Ryan is in 1924, then Onyx must be in 1923 (but 1923 must be Louis or Tiffany, so Onyx cannot be in 1923)
solver.add(Implies(year1924 == Ryan, year1923 == Onyx))

# Additionally, we can add constraints to prevent impossible assignments:
# Ryan cannot be in 1923 because 1923 must be Louis or Tiffany
solver.add(year1923 != Ryan)
# Ryan cannot be in 1924 because then Onyx would be in 1923, which must be Louis or Tiffany
solver.add(year1924 != Ryan)

# Now, we want to find which students can be assigned to 1921.
# We'll check each student individually.
students = [Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio]
student_names = ["Louis", "Mollie", "Onyx", "Ryan", "Tiffany", "Yoshio"]
can_be_in_1921 = []

for student in students:
    s = Solver()
    s.add(solver.assertions())  # Copy all base constraints
    s.add(year1921 == student)
    if s.check() == sat:
        can_be_in_1921.append(student)

# Count how many students can be in 1921
count = len(can_be_in_1921)

# Map count to answer choice
# Choices: (A)six (B)five (C)four (D)three (E)two
if count == 6:
    answer = "A"
elif count == 5:
    answer = "B"
elif count == 4:
    answer = "C"
elif count == 3:
    answer = "D"
elif count == 2:
    answer = "E"
else:
    answer = "Unknown"

# Print results
print("STATUS: sat")
print(f"Students who can be assigned to 1921: {[student_names[i] for i in can_be_in_1921]}")
print(f"Count: {count}")
print(f"answer:{answer}")