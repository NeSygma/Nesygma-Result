from z3 import *

# Define Student enumeration
Student = Datatype('Student')
Student.declare('Louis')
Student.declare('Mollie')
Student.declare('Onyx')
Student.declare('Ryan')
Student.declare('Tiffany')
Student.declare('Yoshio')
Student = Student.create()

# Year variables
y1921 = Const('y1921', Student)
y1922 = Const('y1922', Student)
y1923 = Const('y1923', Student)
y1924 = Const('y1924', Student)

solver = Solver()

# Base constraints
# 1. Exactly one student per year, all distinct
solver.add(Distinct(y1921, y1922, y1923, y1924))

# 2. Only Louis or Tiffany can be assigned to 1923
solver.add(Or(y1923 == Student.Louis, y1923 == Student.Tiffany))

# 3. If Mollie is assigned, she must be in 1921 or 1922
solver.add(Implies(
    Or(y1921 == Student.Mollie, y1922 == Student.Mollie, y1923 == Student.Mollie, y1924 == Student.Mollie),
    Or(y1921 == Student.Mollie, y1922 == Student.Mollie)
))

# 4. If Tiffany is assigned, Ryan must be assigned
solver.add(Implies(
    Or(y1921 == Student.Tiffany, y1922 == Student.Tiffany, y1923 == Student.Tiffany, y1924 == Student.Tiffany),
    Or(y1921 == Student.Ryan, y1922 == Student.Ryan, y1923 == Student.Ryan, y1924 == Student.Ryan)
))

# 5. If Ryan is assigned, Onyx must be in the year immediately prior
# First, Ryan cannot be in 1921 (no prior year)
solver.add(y1921 != Student.Ryan)
# Then implications for other years
solver.add(Implies(y1922 == Student.Ryan, y1921 == Student.Onyx))
solver.add(Implies(y1923 == Student.Ryan, y1922 == Student.Onyx))
solver.add(Implies(y1924 == Student.Ryan, y1923 == Student.Onyx))

# 6. Yoshio is not assigned
solver.add(y1921 != Student.Yoshio)
solver.add(y1922 != Student.Yoshio)
solver.add(y1923 != Student.Yoshio)
solver.add(y1924 != Student.Yoshio)

# Now evaluate each answer choice
found_options = []

# Option A: Louis is not assigned to the project
opt_a_constr = And(y1921 != Student.Louis, y1922 != Student.Louis, y1923 != Student.Louis, y1924 != Student.Louis)

# Option B: Ryan is not assigned to the project
opt_b_constr = And(y1921 != Student.Ryan, y1922 != Student.Ryan, y1923 != Student.Ryan, y1924 != Student.Ryan)

# Option C: Tiffany is not assigned to the project
opt_c_constr = And(y1921 != Student.Tiffany, y1922 != Student.Tiffany, y1923 != Student.Tiffany, y1924 != Student.Tiffany)

# Option D: Onyx is assigned to 1922
opt_d_constr = (y1922 == Student.Onyx)

# Option E: Louis is assigned to 1924
opt_e_constr = (y1924 == Student.Louis)

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