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

# The question asks: the third project member MUST be either...
# This means: across ALL valid models, the third member is always one of the options.
# We need to find which option covers ALL possible third members.

# First, find all possible third members
possible_third = []
for i in range(N):
    s = Solver()
    # Copy all constraints
    for c in solver.assertions():
        s.add(c)
    # This worker is the third member (member but not Taylor or Wells)
    s.add(is_member[i] == True)
    if i != 3 and i != 5:  # Not Taylor or Wells
        # Ensure the other non-Taylor, non-Wells workers are NOT members
        for j in range(N):
            if j != 3 and j != 5 and j != i:
                s.add(is_member[j] == False)
    if s.check() == sat:
        possible_third.append(i)
        print(f"Worker {workers[i]} can be the third member")

print(f"\nPossible third members: {[workers[i] for i in possible_third]}")

# Now check which options cover ALL possible third members
# Option A: Quinn or Smith -> covers indices 0, 2
# Option B: Quinn or Xue -> covers indices 0, 6
# Option C: Ruiz or Verma -> covers indices 1, 4
# Option D: Smith or Xue -> covers indices 2, 6
# Option E: Verma or Xue -> covers indices 4, 6

options = {
    "A": {0, 2},
    "B": {0, 6},
    "C": {1, 4},
    "D": {2, 6},
    "E": {4, 6}
}

valid_options = []
for letter, covers in options.items():
    if set(possible_third).issubset(covers):
        valid_options.append(letter)

print(f"Options that cover all possible third members: {valid_options}")

if len(valid_options) == 1:
    print("STATUS: sat")
    print(f"answer:{valid_options[0]}")
elif len(valid_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {valid_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")