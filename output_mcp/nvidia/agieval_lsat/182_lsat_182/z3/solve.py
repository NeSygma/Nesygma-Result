from z3 import *

solver = Solver()

# Variables
k = Bool('k')
l = Bool('l')
m = Bool('m')
n = Bool('n')
o = Bool('o')
p = Bool('p')

# Base constraints
solver.add(m != p)  # M and P cannot be same season
solver.add(k == n)  # K and N same season
solver.add(Implies(k, o))  # If K fall then O fall
solver.add(Implies(m, Not(n)))  # If M fall then N spring
solver.add(n)  # N is fall

# Options constraints
opt_a_constr = k == False  # A: K is spring
opt_b_constr = l == True   # B: L is fall
opt_c_constr = m == True   # C: M is fall
opt_d_constr = o == False  # D: O is spring
opt_e_constr = p == False  # E: P is spring

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