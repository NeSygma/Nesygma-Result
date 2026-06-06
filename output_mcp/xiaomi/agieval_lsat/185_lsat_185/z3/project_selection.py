from z3 import *

solver = Solver()

# Workers: Quinn=0, Ruiz=1, Smith=2, Taylor=3, Verma=4, Wells=5, Xue=6
workers = ['Quinn', 'Ruiz', 'Smith', 'Taylor', 'Verma', 'Wells', 'Xue']
N = len(workers)

# Boolean variables: is_member[i] = worker i is a project member
is_member = [Bool(f'member_{workers[i]}') for i in range(N)]
# is_leader[i] = worker i is the project leader
is_leader = [Bool(f'leader_{workers[i]}') for i in range(N)]

# Exactly 3 members
solver.add(Sum([If(is_member[i], 1, 0) for i in range(N)]) == 3)

# Exactly 1 leader
solver.add(Sum([If(is_leader[i], 1, 0) for i in range(N)]) == 1)

# Leader must be a member
for i in range(N):
    solver.add(Implies(is_leader[i], is_member[i]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project
# If Quinn is a member, Quinn must be leader
solver.add(Implies(is_member[0], is_leader[0]))
# If Ruiz is a member, Ruiz must be leader
solver.add(Implies(is_member[1], is_leader[1]))

# Constraint 2: If Smith is a project member, Taylor must also be
solver.add(Implies(is_member[2], is_member[3]))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be
solver.add(Implies(is_member[5], And(Not(is_member[1]), Not(is_member[4]))))

# Define each option's constraints
# Option A: Ruiz (leader), Taylor, Wells
opt_a_constr = And(
    is_leader[1], is_member[1],  # Ruiz is leader and member
    is_member[3],                 # Taylor is member
    is_member[5],                 # Wells is member
    # Others not members
    Not(is_member[0]), Not(is_member[2]), Not(is_member[4]), Not(is_member[6]),
    # Only Ruiz is leader
    Not(is_leader[0]), Not(is_leader[2]), Not(is_leader[3]),
    Not(is_leader[4]), Not(is_leader[5]), Not(is_leader[6])
)

# Option B: Verma (leader), Quinn, Taylor
opt_b_constr = And(
    is_leader[4], is_member[4],  # Verma is leader and member
    is_member[0],                 # Quinn is member
    is_member[3],                 # Taylor is member
    # Others not members
    Not(is_member[1]), Not(is_member[2]), Not(is_member[5]), Not(is_member[6]),
    # Only Verma is leader
    Not(is_leader[0]), Not(is_leader[1]), Not(is_leader[2]),
    Not(is_leader[3]), Not(is_leader[5]), Not(is_leader[6])
)

# Option C: Verma (leader), Smith, Taylor
opt_c_constr = And(
    is_leader[4], is_member[4],  # Verma is leader and member
    is_member[2],                 # Smith is member
    is_member[3],                 # Taylor is member
    # Others not members
    Not(is_member[0]), Not(is_member[1]), Not(is_member[5]), Not(is_member[6]),
    # Only Verma is leader
    Not(is_leader[0]), Not(is_leader[1]), Not(is_leader[2]),
    Not(is_leader[3]), Not(is_leader[5]), Not(is_leader[6])
)

# Option D: Verma (leader), Smith, Xue
opt_d_constr = And(
    is_leader[4], is_member[4],  # Verma is leader and member
    is_member[2],                 # Smith is member
    is_member[6],                 # Xue is member
    # Others not members
    Not(is_member[0]), Not(is_member[1]), Not(is_member[3]), Not(is_member[5]),
    # Only Verma is leader
    Not(is_leader[0]), Not(is_leader[1]), Not(is_leader[2]),
    Not(is_leader[3]), Not(is_leader[5]), Not(is_leader[6])
)

# Option E: Xue (leader), Verma, Wells
opt_e_constr = And(
    is_leader[6], is_member[6],  # Xue is leader and member
    is_member[4],                 # Verma is member
    is_member[5],                 # Wells is member
    # Others not members
    Not(is_member[0]), Not(is_member[1]), Not(is_member[2]), Not(is_member[3]),
    # Only Xue is leader
    Not(is_leader[0]), Not(is_leader[1]), Not(is_leader[2]),
    Not(is_leader[3]), Not(is_leader[4]), Not(is_leader[5])
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