from z3 import *

# Student mapping: 0 Louis, 1 Mollie, 2 Onyx, 3 Ryan, 4 Tiffany, 5 Yoshio
y1921 = Int('y1921')
y1922 = Int('y1922')
y1923 = Int('y1923')
y1924 = Int('y1924')
solver = Solver()
# domain constraints
for v in [y1921, y1922, y1923, y1924]:
    solver.add(v >= 0, v <= 5)
# distinct students
solver.add(Distinct(y1921, y1922, y1923, y1924))
# Only Louis or Tiffany can be assigned to 1923
solver.add(Or(y1923 == 0, y1923 == 4))
# Mollie (1) must be in 1921 or 1922 if present -> disallow 1923,1924
solver.add(y1923 != 1, y1924 != 1)
# Tiffany (4) implies Ryan (3) present somewhere
tiffany_assigned = Or(y1921 == 4, y1922 == 4, y1923 == 4, y1924 == 4)
ryan_assigned = Or(y1921 == 3, y1922 == 3, y1923 == 3, y1924 == 3)
solver.add(Implies(tiffany_assigned, ryan_assigned))
# Ryan cannot be in 1921 (no prior year)
solver.add(y1921 != 3)
# If Ryan assigned, Onyx (2) must be in the immediately prior year
# For each possible year index >0
solver.add(Implies(y1922 == 3, y1921 == 2))
solver.add(Implies(y1923 == 3, y1922 == 2))
solver.add(Implies(y1924 == 3, y1923 == 2))

# Option constraints
opt_a_constr = And(y1921 == 0, y1922 == 2, y1923 == 3, y1924 == 5)  # A: Louis, Onyx, Ryan, Yoshio
opt_b_constr = And(y1921 == 1, y1922 == 5, y1923 == 4, y1924 == 2)  # B: Mollie, Yoshio, Tiffany, Onyx
opt_c_constr = And(y1921 == 2, y1922 == 3, y1923 == 0, y1924 == 4)  # C: Onyx, Ryan, Louis, Tiffany
opt_d_constr = And(y1921 == 4, y1922 == 2, y1923 == 0, y1924 == 3)  # D: Tiffany, Onyx, Louis, Ryan
opt_e_constr = And(y1921 == 5, y1922 == 2, y1923 == 0, y1924 == 1)  # E: Yoshio, Onyx, Louis, Mollie

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