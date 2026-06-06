from z3 import *

solver = Solver()

# Workers: Quinn=0, Ruiz=1, Smith=2, Taylor=3, Verma=4, Wells=5, Xue=6
workers = ['Quinn', 'Ruiz', 'Smith', 'Taylor', 'Verma', 'Wells', 'Xue']
N = len(workers)

# Boolean variables: is_member[i] = worker i is a project member
is_member = [Bool(f'member_{w}') for w in workers]
# Boolean variables: is_leader[i] = worker i is the project leader
is_leader = [Bool(f'leader_{w}') for w in workers]

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
solver.add(Implies(is_member[5], Not(is_member[1])))
solver.add(Implies(is_member[5], Not(is_member[4])))

# Given: Taylor is the project leader
solver.add(is_leader[3] == True)
solver.add(is_member[3] == True)

# Given: Wells is a project member
solver.add(is_member[5] == True)

# Since Wells is a member, Ruiz and Verma cannot be members (from constraint 3)
# Since Taylor is leader, Quinn and Ruiz cannot be members (from constraint 1, they'd need to be leader but Taylor is leader)

# Now evaluate each answer choice for the third member
# We already know Taylor and Wells are members. The third member is the remaining one.

# Option A: Quinn or Smith
opt_a = Or(is_member[0], is_member[2])
# Option B: Quinn or Xue
opt_b = Or(is_member[0], is_member[6])
# Option C: Ruiz or Verma
opt_c = Or(is_member[1], is_member[4])
# Option D: Smith or Xue
opt_d = Or(is_member[2], is_member[6])
# Option E: Verma or Xue
opt_e = Or(is_member[4], is_member[6])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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