from z3 import *

solver = Solver()

# Variables
sel_Q = Bool('sel_Q')
sel_R = Bool('sel_R')
sel_S = Bool('sel_S')
sel_T = Bool('sel_T')
sel_V = Bool('sel_V')
sel_W = Bool('sel_W')
sel_X = Bool('sel_X')

leader_Q = Bool('leader_Q')
leader_R = Bool('leader_R')
leader_S = Bool('leader_S')
leader_T = Bool('leader_T')
leader_V = Bool('leader_V')
leader_W = Bool('leader_W')
leader_X = Bool('leader_X')

# Base constraints
# Leader implies selected
solver.add(Implies(leader_Q, sel_Q))
solver.add(Implies(leader_R, sel_R))
solver.add(Implies(leader_S, sel_S))
solver.add(Implies(leader_T, sel_T))
solver.add(Implies(leader_V, sel_V))
solver.add(Implies(leader_W, sel_W))
solver.add(Implies(leader_X, sel_X))

# Quinn or Ruiz can be a project member only if leading the project
solver.add(Implies(sel_Q, leader_Q))
solver.add(Implies(sel_R, leader_R))

# If Smith is a project member, Taylor must also be
solver.add(Implies(sel_S, sel_T))

# If Wells is a project member, neither Ruiz nor Verma can be
solver.add(Implies(sel_W, And(Not(sel_R), Not(sel_V))))

# Exactly 3 selected
solver.add(Sum([If(sel_Q,1,0), If(sel_R,1,0), If(sel_S,1,0), If(sel_T,1,0), If(sel_V,1,0), If(sel_W,1,0), If(sel_X,1,0)]) == 3)

# Exactly 1 leader
solver.add(Sum([If(leader_Q,1,0), If(leader_R,1,0), If(leader_S,1,0), If(leader_T,1,0), If(leader_V,1,0), If(leader_W,1,0), If(leader_X,1,0)]) == 1)

# Verma is selected and leader
solver.add(sel_V == True)
solver.add(leader_V == True)

# Option constraints
opt_a_constr = And(Not(sel_Q), Not(sel_S))
opt_b_constr = And(Not(sel_R), Not(sel_T))
opt_c_constr = And(Not(sel_S), Not(sel_T))
opt_d_constr = And(Not(sel_S), Not(sel_X))
opt_e_constr = And(Not(sel_T), Not(sel_W))

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