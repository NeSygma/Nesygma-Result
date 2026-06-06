from z3 import *

solver = Solver()

# Declare day variables
franco = Int('franco')
garcia = Int('garcia')
hong = Int('hong')
iturbe = Int('iturbe')
jackson = Int('jackson')

# Domain constraints: each day variable between 0 (Monday) and 2 (Wednesday)
for var in [franco, garcia, hong, iturbe, jackson]:
    solver.add(var >= 0, var <= 2)

# Helper sums
sum_tue = Sum([If(v == 1, 1, 0) for v in [franco, garcia, hong, iturbe, jackson]])
sum_mon = Sum([If(v == 0, 1, 0) for v in [franco, garcia, hong, iturbe, jackson]])

# Global constraints (will be added for each option)
global_constraints = And(
    franco != garcia,
    iturbe == 2,
    sum_tue == 2,
    hong != 0,
    sum_mon >= 1
)

# Define option constraints as And of schedule + global
opt_a_constr = And(
    franco == 0,
    hong == 1,
    iturbe == 1,
    garcia == 2,
    jackson == 2,
    global_constraints
)

opt_b_constr = And(
    franco == 0,
    hong == 0,
    iturbe == 1,
    jackson == 1,
    garcia == 2,
    global_constraints
)

opt_c_constr = And(
    garcia == 0,
    franco == 1,
    iturbe == 1,
    hong == 2,
    jackson == 2,
    global_constraints
)

opt_d_constr = And(
    garcia == 0,
    jackson == 0,
    franco == 1,
    hong == 1,
    iturbe == 2,
    global_constraints
)

opt_e_constr = And(
    garcia == 0,
    jackson == 0,
    hong == 1,
    franco == 2,
    iturbe == 2,
    global_constraints
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