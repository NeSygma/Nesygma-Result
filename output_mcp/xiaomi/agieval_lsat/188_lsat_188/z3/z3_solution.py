from z3 import *

solver = Solver()

# Workers: Quinn=0, Ruiz=1, Smith=2, Taylor=3, Verma=4, Wells=5, Xue=6
workers = ['Quinn', 'Ruiz', 'Smith', 'Taylor', 'Verma', 'Wells', 'Xue']
N = len(workers)

# member[i] = True if worker i is a project member
member = [Bool(f'member_{workers[i]}') for i in range(N)]

# leader[i] = True if worker i is the project leader
leader = [Bool(f'leader_{workers[i]}') for i in range(N)]

# Exactly 3 members
solver.add(Sum([If(member[i], 1, 0) for i in range(N)]) == 3)

# Exactly 1 leader
solver.add(Sum([If(leader[i], 1, 0) for i in range(N)]) == 1)

# Leader must be a member
for i in range(N):
    solver.add(Implies(leader[i], member[i]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project
solver.add(Implies(member[0], leader[0]))  # Quinn
solver.add(Implies(member[1], leader[1]))  # Ruiz

# Constraint 2: If Smith is a project member, Taylor must also be
solver.add(Implies(member[2], member[3]))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be
solver.add(Implies(member[5], And(Not(member[1]), Not(member[4]))))

# Given: Taylor is NOT a project member
solver.add(Not(member[3]))

# Since Taylor is not a member, by constraint 2, Smith cannot be a member either
# (If Smith were a member, Taylor would have to be, contradiction)
# This is already implied by constraint 2, but let's verify the solver handles it.

# Now check each option: which worker MUST be a member?
# A worker MUST be a member if adding Not(member[i]) makes it unsat

found_options = []
for letter, idx in [("A", 0), ("B", 1), ("C", 4), ("D", 5), ("E", 6)]:
    solver.push()
    solver.add(Not(member[idx]))  # Try to make this worker NOT a member
    if solver.check() == unsat:
        # This worker MUST be a member (can't exclude them)
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