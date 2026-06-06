from z3 import *

# Students: 0:L, 1:M, 2:O, 3:R, 4:T, 5:Y
# Years: 0:1921, 1:1922, 2:1923, 3:1924
students = range(6)
years = range(4)

solver = Solver()

# assigned[year] = student_id
assigned = [Int(f'assigned_{y}') for y in years]

# Each year has exactly one student (already implied by the structure)
# Each student is assigned to at most one year
for y in years:
    solver.add(assigned[y] >= 0, assigned[y] < 6)
solver.add(Distinct(assigned))

# C1: Only Louis (0) or Tiffany (4) can be assigned to 1923 (year 2)
solver.add(Or(assigned[2] == 0, assigned[2] == 4))

# C2: If Mollie (1) is assigned, she must be assigned to 1921 (0) or 1922 (1)
mollie_assigned = Or([assigned[y] == 1 for y in years])
solver.add(Implies(mollie_assigned, Or(assigned[0] == 1, assigned[1] == 1)))

# C3: If Tiffany (4) is assigned, then Ryan (3) must be assigned
tiffany_assigned = Or([assigned[y] == 4 for y in years])
ryan_assigned = Or([assigned[y] == 3 for y in years])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# C4: If Ryan (3) is assigned, then Onyx (2) must be assigned to the year immediately prior to Ryan's
# Ryan's year can be 1922 (1), 1923 (2), or 1924 (3). 1921 (0) is not possible because Onyx would need to be in 1920.
ryan_in_1922 = (assigned[1] == 3)
ryan_in_1923 = (assigned[2] == 3)
ryan_in_1924 = (assigned[3] == 3)

solver.add(Implies(ryan_in_1922, assigned[0] == 2))
solver.add(Implies(ryan_in_1923, assigned[1] == 2))
solver.add(Implies(ryan_in_1924, assigned[2] == 2))

# Check which students can be in 1921 (assigned[0])
possible_students_for_1921 = []
for s in students:
    solver.push()
    solver.add(assigned[0] == s)
    if solver.check() == sat:
        possible_students_for_1921.append(s)
    solver.pop()

print(f"Possible students for 1921: {possible_students_for_1921}")
print(f"Count: {len(possible_students_for_1921)}")

# Now map to the answer choices
# (A)six (B)five (C)four (D)three (E)two
# The count is 3. So the answer is (D).

# Verify the answer choice logic
opt_a_constr = (len(possible_students_for_1921) == 6)
opt_b_constr = (len(possible_students_for_1921) == 5)
opt_c_constr = (len(possible_students_for_1921) == 4)
opt_d_constr = (len(possible_students_for_1921) == 3)
opt_e_constr = (len(possible_students_for_1921) == 2)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    if constr:
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