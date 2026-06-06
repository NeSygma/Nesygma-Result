from z3 import *

# Define student mapping
# 0: Louis, 1: Mollie, 2: Onyx, 3: Ryan, 4: Tiffany, 5: Yoshio

# Year variables: year1 for 1921, year2 for 1922, year3 for 1923, year4 for 1924
year1 = Int('year1')
year2 = Int('year2')
year3 = Int('year3')
year4 = Int('year4')

solver = Solver()
# Domain constraints
students = [0,1,2,3,4,5]
for y in [year1, year2, year3, year4]:
    solver.add(Or([y == s for s in students]))
# Distinctness (exactly 4 distinct students)
solver.add(Distinct(year1, year2, year3, year4))
# Yoshio not assigned
for y in [year1, year2, year3, year4]:
    solver.add(y != 5)
# Only Louis or Tiffany can be assigned to 1923
solver.add(Or(year3 == 0, year3 == 4))
# Conditional constraints
# If Mollie assigned, she must be in 1921 or 1922
mollie_assigned = Or(year1 == 1, year2 == 1, year3 == 1, year4 == 1)
solver.add(Implies(mollie_assigned, Or(year1 == 1, year2 == 1)))
# If Tiffany assigned, Ryan must be assigned
tiffany_assigned = Or(year1 == 4, year2 == 4, year3 == 4, year4 == 4)
ryan_assigned = Or(year1 == 3, year2 == 3, year3 == 3, year4 == 3)
solver.add(Implies(tiffany_assigned, ryan_assigned))
# If Ryan assigned, Onyx must be in the immediately prior year
# Ryan cannot be in 1921
solver.add(year1 != 3)
# If Ryan in 1922 then Onyx in 1921
solver.add(Implies(year2 == 3, year1 == 2))
# If Ryan in 1923 then Onyx in 1922
solver.add(Implies(year3 == 3, year2 == 2))
# If Ryan in 1924 then Onyx in 1923
solver.add(Implies(year4 == 3, year3 == 2))

# Define option constraints
opt_a_constr = And(year1 != 0, year2 != 0, year3 != 0, year4 != 0)  # Louis not assigned
opt_b_constr = And(year1 != 3, year2 != 3, year3 != 3, year4 != 3)  # Ryan not assigned
opt_c_constr = And(year1 != 4, year2 != 4, year3 != 4, year4 != 4)  # Tiffany not assigned
opt_d_constr = year2 == 2  # Onyx assigned to 1922
opt_e_constr = year4 == 0  # Louis assigned to 1924

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