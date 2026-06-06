from z3 import *

# Students
L, M, O, R, T, Y = range(6)
student_names = {L: "Louis", M: "Mollie", O: "Onyx", R: "Ryan", T: "Tiffany", Y: "Yoshio"}

# Years
years = [1921, 1922, 1923, 1924]
# Map years to indices 0, 1, 2, 3
year_to_idx = {1921: 0, 1922: 1, 1923: 2, 1924: 3}

# Variables: assigned[i] is the student assigned to year years[i]
assigned = [Int(f"assigned_{y}") for y in years]

solver = Solver()

# Each year has exactly one student
for a in assigned:
    solver.add(a >= 0, a <= 5)
solver.add(Distinct(assigned))

# Helper: is_assigned[s]
def is_assigned(s):
    return Or([assigned[i] == s for i in range(4)])

# Constraint 1: Only Louis or Tiffany can be assigned to 1923
solver.add(Or(assigned[year_to_idx[1923]] == L, assigned[year_to_idx[1923]] == T))

# Constraint 2: If Mollie is assigned, she must be in 1921 or 1922
solver.add(Implies(is_assigned(M), Or(assigned[year_to_idx[1921]] == M, assigned[year_to_idx[1922]] == M)))

# Constraint 3: If Tiffany is assigned, Ryan must be assigned
solver.add(Implies(is_assigned(T), is_assigned(R)))

# Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior
# Ryan cannot be in 1921
solver.add(Implies(is_assigned(R), assigned[year_to_idx[1921]] != R))
# If R in 1922, O in 1921
solver.add(Implies(assigned[year_to_idx[1922]] == R, assigned[year_to_idx[1921]] == O))
# If R in 1923, O in 1922
solver.add(Implies(assigned[year_to_idx[1923]] == R, assigned[year_to_idx[1922]] == O))
# If R in 1924, O in 1923
solver.add(Implies(assigned[year_to_idx[1924]] == R, assigned[year_to_idx[1923]] == O))

# Question: Which student CANNOT be assigned to 1922?
# Test each student for 1922
options = [("A", L), ("B", M), ("C", O), ("D", R), ("E", Y)]
valid_options = []

for label, student in options:
    solver.push()
    solver.add(assigned[year_to_idx[1922]] == student)
    if solver.check() == sat:
        # This student CAN be assigned to 1922
        pass
    else:
        # This student CANNOT be assigned to 1922
        valid_options.append(label)
    solver.pop()

if len(valid_options) == 1:
    print("STATUS: sat")
    print(f"answer:{valid_options[0]}")
elif len(valid_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {valid_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")