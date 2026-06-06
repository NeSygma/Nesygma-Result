from z3 import *

solver = Solver()

# Declare variables for each witness (0=Monday, 1=Tuesday, 2=Wednesday)
F = Int('Franco')
G = Int('Garcia')
H = Int('Hong')
I = Int('Iturbe')
J = Int('Jackson')

# Base constraints
solver.add(F >= 0, F <= 2)
solver.add(G >= 0, G <= 2)
solver.add(H >= 0, H <= 2)
solver.add(I >= 0, I <= 2)
solver.add(J >= 0, J <= 2)

# Iturbe testifies on Wednesday
solver.add(I == 2)

# Hong does not testify on Monday
solver.add(H != 0)

# Franco and Garcia not same day
solver.add(F != G)

# Exactly two witnesses on Tuesday
solver.add(Sum([If(F == 1, 1, 0),
                If(G == 1, 1, 0),
                If(H == 1, 1, 0),
                If(I == 1, 1, 0),
                If(J == 1, 1, 0)]) == 2)

# At least one witness on Monday
solver.add(Sum([If(F == 0, 1, 0),
                If(G == 0, 1, 0),
                If(H == 0, 1, 0),
                If(I == 0, 1, 0),
                If(J == 0, 1, 0)]) >= 1)

# Define option constraints
opt_a_constr = And(F == 0, H == 1, I == 1, G == 2, J == 2)
opt_b_constr = And(F == 0, H == 0, I == 1, J == 1, G == 2)
opt_c_constr = And(G == 0, F == 1, I == 1, H == 2, J == 2)
opt_d_constr = And(G == 0, J == 0, F == 1, H == 1, I == 2)
opt_e_constr = And(G == 0, J == 0, H == 1, F == 2, I == 2)

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