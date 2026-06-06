from z3 import *

# Seven workers: Quinn, Ruiz, Smith, Taylor, Verma, Wells, Xue
workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]
N = 7

# Boolean variables: member[i] = True if worker i is a project member
member = [Bool(f"member_{i}") for i in range(N)]

# leader[i] = True if worker i is the project leader
leader = [Bool(f"leader_{i}") for i in range(N)]

solver = Solver()

# Exactly three project members
solver.add(Sum([If(member[i], 1, 0) for i in range(N)]) == 3)

# Exactly one project leader
solver.add(Sum([If(leader[i], 1, 0) for i in range(N)]) == 1)

# Leader must be a project member
for i in range(N):
    solver.add(Implies(leader[i], member[i]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project.
solver.add(Implies(member[0], leader[0]))  # Quinn
solver.add(Implies(member[1], leader[1]))  # Ruiz

# Constraint 2: If Smith is a project member, Taylor must also be.
solver.add(Implies(member[2], member[3]))  # Smith -> Taylor

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be.
solver.add(Implies(member[5], Not(member[1])))  # Wells -> not Ruiz
solver.add(Implies(member[5], Not(member[4])))  # Wells -> not Verma

# Given: Taylor is the project leader
solver.add(leader[3])  # Taylor is leader

# Given: Wells is a project member
solver.add(member[5])  # Wells is a member

# Let's first check what the model looks like
print("Checking base constraints...")
result = solver.check()
if result == sat:
    m = solver.model()
    print("SAT - base model:")
    for i in range(N):
        print(f"  {workers[i]}: member={m[member[i]]}, leader={m[leader[i]]}")
else:
    print("UNSAT - no solution with given constraints")
    exit()

# Now enumerate all solutions to see which workers can be the third member
solver.push()  # save state

solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = tuple(m[member[i]] for i in range(N))
    solutions.append(sol)
    # Block this solution
    solver.add(Or([member[i] != m[member[i]] for i in range(N)]))

solver.pop()

print(f"\nTotal solutions: {len(solutions)}")
for idx, sol in enumerate(solutions):
    members = [workers[i] for i in range(N) if sol[i]]
    print(f"  Solution {idx+1}: members = {members}")

# Find which workers are members in ALL solutions
possible_third = []
for i in range(N):
    if i == 3 or i == 5:  # Taylor and Wells are already known
        continue
    # Check if this worker is a member in all solutions
    if all(sol[i] for sol in solutions):
        possible_third.append(workers[i])

print(f"\nWorkers who MUST be the third member: {possible_third}")

# Now evaluate each answer choice
# Each option says the third member must be either X or Y
# This means: in every valid solution, the third member is one of the two.

def option_holds(opt_indices):
    """Check if in every solution, the third member is one of the given indices"""
    for sol in solutions:
        third_members = [i for i in range(N) if sol[i] and i not in (3, 5)]
        if len(third_members) != 1:
            return False
        if third_members[0] not in opt_indices:
            return False
    return True

opt_a_indices = [0, 2]  # Quinn or Smith
opt_b_indices = [0, 6]  # Quinn or Xue
opt_c_indices = [1, 4]  # Ruiz or Verma
opt_d_indices = [2, 6]  # Smith or Xue
opt_e_indices = [4, 6]  # Verma or Xue

options = {
    "A": opt_a_indices,
    "B": opt_b_indices,
    "C": opt_c_indices,
    "D": opt_d_indices,
    "E": opt_e_indices
}

found_options = []
for letter, indices in options.items():
    if option_holds(indices):
        found_options.append(letter)
        print(f"Option {letter} ({[workers[i] for i in indices]}) holds in all solutions")

if len(found_options) == 1:
    print(f"\nSTATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print(f"\nSTATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print(f"\nSTATUS: unsat")
    print("Refine: No options found")