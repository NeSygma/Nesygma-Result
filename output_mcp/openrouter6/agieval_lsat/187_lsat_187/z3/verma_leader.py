from z3 import *

# Define worker names and indices
names = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]
# Create boolean variables for membership and leadership
members = [Bool(f"member_{name}") for name in names]
leaders = [Bool(f"leader_{name}") for name in names]

# Base constraints
solver = Solver()

# Exactly three members
solver.add(Sum([If(m, 1, 0) for m in members]) == 3)

# Exactly one leader
solver.add(Sum([If(l, 1, 0) for l in leaders]) == 1)

# Leader must be a member (for all)
for i in range(7):
    solver.add(Implies(leaders[i], members[i]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project.
# That is: if member then leader for Quinn and Ruiz.
idx_quinn = names.index("Quinn")
idx_ruiz = names.index("Ruiz")
solver.add(Implies(members[idx_quinn], leaders[idx_quinn]))
solver.add(Implies(members[idx_ruiz], leaders[idx_ruiz]))

# Constraint 2: If Smith is a project member, Taylor must also be.
idx_smith = names.index("Smith")
idx_taylor = names.index("Taylor")
solver.add(Implies(members[idx_smith], members[idx_taylor]))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be.
idx_wells = names.index("Wells")
idx_verma = names.index("Verma")
solver.add(Implies(members[idx_wells], And(Not(members[idx_ruiz]), Not(members[idx_verma]))))

# Now evaluate each answer choice
# Option constraints (each is a conjunction of two "not member" statements)
opt_a_constr = And(Not(members[idx_quinn]), Not(members[idx_smith]))
opt_b_constr = And(Not(members[idx_ruiz]), Not(members[idx_taylor]))
opt_c_constr = And(Not(members[idx_smith]), Not(members[idx_taylor]))
opt_d_constr = And(Not(members[idx_smith]), Not(members[idx_xue]))  # need idx_xue
idx_xue = names.index("Xue")
opt_d_constr = And(Not(members[idx_smith]), Not(members[idx_xue]))
opt_e_constr = And(Not(members[idx_taylor]), Not(members[idx_wells]))

# Ensure Verma is the leader (and thus a member)
verma_leader_constraint = And(leaders[idx_verma], members[idx_verma])

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    solver.add(verma_leader_constraint)
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