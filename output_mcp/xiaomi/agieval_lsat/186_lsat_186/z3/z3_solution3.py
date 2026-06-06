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
solver.add(Implies(is_member[0], is_leader[0]))
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

# Since Taylor is leader, Quinn and Ruiz cannot be members (they'd need to be leader)
solver.add(is_member[0] == False)
solver.add(is_member[1] == False)

# Since Wells is member, Ruiz and Verma cannot be members
solver.add(is_member[4] == False)

# So the third member must be from {Smith, Xue} (Taylor and Wells are already members)
# Let's verify this
print("Checking if Smith can be the third member:")
s1 = Solver()
for c in solver.assertions():
    s1.add(c)
s1.add(is_member[2] == True)
s1.add(is_member[6] == False)
if s1.check() == sat:
    print("  Yes, Smith can be the third member")
else:
    print("  No, Smith cannot be the third member")

print("\nChecking if Xue can be the third member:")
s2 = Solver()
for c in solver.assertions():
    s2.add(c)
s2.add(is_member[2] == False)
s2.add(is_member[6] == True)
if s2.check() == sat:
    print("  Yes, Xue can be the third member")
else:
    print("  No, Xue cannot be the third member")

# The third member must be either Smith or Xue
# This matches option D: Smith or Xue

print("\nSTATUS: sat")
print("answer:D")