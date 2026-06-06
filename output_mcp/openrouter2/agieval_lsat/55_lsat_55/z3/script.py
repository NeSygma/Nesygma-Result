from z3 import *

solver = Solver()
# Candidate indices: 0:Jaramillo, 1:Kayne, 2:Landon, 3:Novetzke, 4:Ong
assign_V = Int('assign_V')
assign_Y = Int('assign_Y')
assign_Z = Int('assign_Z')
# Domain constraints
solver.add(assign_V >= 0, assign_V <= 4)
solver.add(assign_Y >= 0, assign_Y <= 4)
solver.add(assign_Z >= 0, assign_Z <= 4)
# Distinct ambassadors
solver.add(Distinct(assign_V, assign_Y, assign_Z))
# Kayne or Novetzke, but not both, is assigned to one of the ambassadorships
count_kayne_nov = Sum([If(Or(assign_V==1, assign_V==3), 1, 0),
                       If(Or(assign_Y==1, assign_Y==3), 1, 0),
                       If(Or(assign_Z==1, assign_Z==3), 1, 0)])
solver.add(count_kayne_nov == 1)
# If Jaramillo is assigned, then Kayne is also assigned
solver.add(Implies(Or(assign_V==0, assign_Y==0, assign_Z==0),
                   Or(assign_V==1, assign_Y==1, assign_Z==1)))
# If Ong is assigned to Venezuela, Kayne is not assigned to Yemen
solver.add(Implies(assign_V==4, assign_Y != 1))
# If Landon is assigned, it is to Zambia
solver.add(Implies(Or(assign_V==2, assign_Y==2, assign_Z==2), assign_Z==2))

# Define option constraints
opt_a_constr = And(
    Not(Or(assign_V==0, assign_Y==0, assign_Z==0)),
    Not(Or(assign_V==3, assign_Y==3, assign_Z==3)),
    Or(assign_V==1, assign_Y==1, assign_Z==1),
    Or(assign_V==2, assign_Y==2, assign_Z==2),
    Or(assign_V==4, assign_Y==4, assign_Z==4)
)
opt_b_constr = And(
    Not(Or(assign_V==0, assign_Y==0, assign_Z==0)),
    Not(Or(assign_V==4, assign_Y==4, assign_Z==4)),
    Or(assign_V==1, assign_Y==1, assign_Z==1),
    Or(assign_V==2, assign_Y==2, assign_Z==2),
    Or(assign_V==3, assign_Y==3, assign_Z==3)
)
opt_c_constr = And(
    Not(Or(assign_V==1, assign_Y==1, assign_Z==1)),
    Not(Or(assign_V==2, assign_Y==2, assign_Z==2)),
    Or(assign_V==0, assign_Y==0, assign_Z==0),
    Or(assign_V==3, assign_Y==3, assign_Z==3),
    Or(assign_V==4, assign_Y==4, assign_Z==4)
)
opt_d_constr = And(
    Not(Or(assign_V==1, assign_Y==1, assign_Z==1)),
    Not(Or(assign_V==3, assign_Y==3, assign_Z==3)),
    Or(assign_V==0, assign_Y==0, assign_Z==0),
    Or(assign_V==2, assign_Y==2, assign_Z==2),
    Or(assign_V==4, assign_Y==4, assign_Z==4)
)
opt_e_constr = And(
    Not(Or(assign_V==2, assign_Y==2, assign_Z==2)),
    Not(Or(assign_V==4, assign_Y==4, assign_Z==4)),
    Or(assign_V==0, assign_Y==0, assign_Z==0),
    Or(assign_V==1, assign_Y==1, assign_Z==1),
    Or(assign_V==3, assign_Y==3, assign_Z==3)
)

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