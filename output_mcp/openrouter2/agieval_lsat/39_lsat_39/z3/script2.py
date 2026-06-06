from z3 import *

solver = Solver()

# Variables
# We'll use 0=Mon,1=Tue,2=Wed,3=Thu,4=Fri
# For each kind, we enforce ordering: first < second < third
# Oatmeal
O1, O2, O3 = Ints('O1 O2 O3')
# Peanut butter
P1, P2, P3 = Ints('P1 P2 P3')
# Sugar
S1, S2, S3 = Ints('S1 S2 S3')

# Domain
for d in [O1,O2,O3,P1,P2,P3,S1,S2,S3]:
    solver.add(d >= 0, d <= 4)

# Distinctness per kind
solver.add(Distinct(O1,O2,O3))
solver.add(Distinct(P1,P2,P3))
solver.add(Distinct(S1,S2,S3))

# Ordering per kind
solver.add(O1 < O2, O2 < O3)
solver.add(P1 < P2, P2 < P3)
solver.add(S1 < S2, S2 < S3)

# At least one batch on Monday
solver.add(Or(O1==0, O2==0, O3==0, P1==0, P2==0, P3==0, S1==0, S2==0, S3==0))

# Second batch of oatmeal same day as first batch of peanut butter
solver.add(O2 == P1)

# Second batch of sugar on Thursday
solver.add(S2 == 3)

# First batch of peanut butter on Tuesday
solver.add(P1 == 1)

# Option constraints
opt_a_constr = Sum([If(O1 == 0,1,0), If(P1 == 0,1,0), If(S1 == 0,1,0)]) >= 2
opt_b_constr = Sum([If(O1 == 1,1,0), If(P1 == 1,1,0), If(S1 == 1,1,0)]) >= 2
opt_c_constr = Sum([If(O2 == 2,1,0), If(P2 == 2,1,0), If(S2 == 2,1,0)]) >= 2
opt_d_constr = Sum([If(O2 == 3,1,0), If(P2 == 3,1,0), If(S2 == 3,1,0)]) >= 2
opt_e_constr = Sum([If(O3 == 4,1,0), If(P3 == 4,1,0), If(S3 == 4,1,0)]) >= 2

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