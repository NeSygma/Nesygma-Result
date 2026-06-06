from z3 import *

# Mapping students to integers
students = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']
Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio = range(6)

# Year variables: index 0->1921, 1->1922, 2->1923, 3->1924
assign = [Int(f'assign_{year}') for year in [1921, 1922, 1923, 1924]]

solver = Solver()
# Domain constraints
for a in assign:
    solver.add(a >= 0, a < 6)
# Distinct students for each year
solver.add(Distinct(assign))

# Only Louis or Tiffany can be assigned to 1923 (index 2)
solver.add(Or(assign[2] == Louis, assign[2] == Tiffany))

# Mollie, if assigned, must be in 1921 or 1922 (indices 0 or 1)
# So she cannot be in 1923 or 1924
solver.add(assign[2] != Mollie)
solver.add(assign[3] != Mollie)

# If Tiffany assigned, Ryan must be assigned somewhere
tiffany_assigned = Or([a == Tiffany for a in assign])
ryan_assigned = Or([a == Ryan for a in assign])
solver.add(Implies(tiffany_assigned, ryan_assigned))

# If Ryan assigned, then Onyx must be assigned to the year immediately prior to Ryan's
# Also Ryan cannot be in the first year (no prior year)
for i, a in enumerate(assign):
    # If Ryan is in year i, then i>0 and previous year has Onyx
    solver.add(Implies(a == Ryan, And(i > 0, assign[i-1] == Onyx)))

# Determine which students can be assigned to 1921 (index 0)
possible_students = []
for s in range(6):
    solver.push()
    solver.add(assign[0] == s)
    if solver.check() == sat:
        possible_students.append(s)
    solver.pop()

count = len(possible_students)
# Prepare option constraints as Boolean constants
opt_a_constr = BoolVal(count == 6)  # six
opt_b_constr = BoolVal(count == 5)  # five
opt_c_constr = BoolVal(count == 4)  # four
opt_d_constr = BoolVal(count == 3)  # three
opt_e_constr = BoolVal(count == 2)  # two

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