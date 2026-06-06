from z3 import *

# Student constants
Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio = range(6)
students = [Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio]

# Year variables: student assigned to each year
y1921 = Int('y1921')
y1922 = Int('y1922')
y1923 = Int('y1923')
y1924 = Int('y1924')

solver = Solver()
# Domain constraints: each year assigned a student from the list
for var in [y1921, y1922, y1923, y1924]:
    solver.add(Or([var == s for s in students]))
# Distinctness: each year has a different student
solver.add(Distinct(y1921, y1922, y1923, y1924))

# Constraint: 1923 must be Louis or Tiffany
solver.add(Or(y1923 == Louis, y1923 == Tiffany))

# Mollie, if assigned, must be 1921 or 1922 -> enforce she cannot be in 1923 or 1924
solver.add(y1923 != Mollie)
solver.add(y1924 != Mollie)

# Tiffany implies Ryan assigned somewhere
tiffany_assigned = Or(y1921 == Tiffany, y1922 == Tiffany, y1923 == Tiffany, y1924 == Tiffany)
ryan_assigned = Or(y1921 == Ryan, y1922 == Ryan, y1923 == Ryan, y1924 == Ryan)
solver.add(Implies(tiffany_assigned, ryan_assigned))

# Ryan assigned constraints: prior year must be Onyx, and Ryan cannot be 1921
solver.add(y1921 != Ryan)
solver.add(Implies(y1922 == Ryan, y1921 == Onyx))
solver.add(Implies(y1923 == Ryan, y1922 == Onyx))
solver.add(Implies(y1924 == Ryan, y1923 == Onyx))

# Prepare option constraints: each option asserts that the student is assigned to 1922
opt_a_constr = (y1922 == Louis)   # A: Louis
opt_b_constr = (y1922 == Mollie)  # B: Mollie
opt_c_constr = (y1922 == Onyx)    # C: Onyx
opt_d_constr = (y1922 == Ryan)    # D: Ryan
opt_e_constr = (y1922 == Yoshio) # E: Yoshio

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine which option is NOT possible (i.e., unsat)
all_options = {"A", "B", "C", "D", "E"}
unsat_options = all_options - set(found_options)
if len(unsat_options) == 1:
    ans = unsat_options.pop()
    print("STATUS: sat")
    print(f"answer:{ans}")
elif len(found_options) == 1:
    # fallback if exactly one possible assignment
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: found_options={found_options}, unsat_options={unsat_options}")