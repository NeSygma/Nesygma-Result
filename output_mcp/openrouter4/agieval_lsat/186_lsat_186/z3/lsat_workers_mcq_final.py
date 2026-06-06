from z3 import *

solver = Solver()
N = 7
m = [Bool(f'm_{i}') for i in range(N)]  # member
l = [Bool(f'l_{i}') for i in range(N)]  # leader

# Exactly 3 members
solver.add(Sum([If(m[i], 1, 0) for i in range(N)]) == 3)

# Exactly 1 leader
solver.add(Sum([If(l[i], 1, 0) for i in range(N)]) == 1)

# Leader implies member
for i in range(N):
    solver.add(Implies(l[i], m[i]))

# Constraint 1: Quinn or Ruiz can be a member only if leading
solver.add(Implies(m[0], l[0]))
solver.add(Implies(m[1], l[1]))

# Constraint 2: If Smith is a member, Taylor must also be
solver.add(Implies(m[2], m[3]))

# Constraint 3: If Wells is a member, neither Ruiz nor Verma can be
solver.add(Implies(m[5], And(Not(m[1]), Not(m[4]))))

# Given: Taylor is the project leader
solver.add(l[3] == True)

# Given: Wells is a project member
solver.add(m[5] == True)

# Third member means: there is exactly one other member besides Taylor(3) and Wells(5)
# For each answer option (pair of workers), the statement "the third member must be either X or Y"
# means that in every valid scenario, the third member is in {X, Y}.
# Equivalently: there is NO valid scenario where the third member is NOT X and NOT Y.

# Tests:
# Option A: third member is Quinn(0) or Smith(2)
# Option B: third member is Quinn(0) or Xue(6)
# Option C: third member is Ruiz(1) or Verma(4)
# Option D: third member is Smith(2) or Xue(6)
# Option E: third member is Verma(4) or Xue(6)

# For each option, we add: NOT(member of first) AND NOT(member of second)
# If unsat, that means you can't avoid both -> the third member must be one of them -> correct.
# If sat, there exists a model where neither is the third member -> option is wrong.

found_options = []
options = {
    "A": [0, 2],  # Quinn, Smith
    "B": [0, 6],  # Quinn, Xue
    "C": [1, 4],  # Ruiz, Verma
    "D": [2, 6],  # Smith, Xue
    "E": [4, 6]   # Verma, Xue
}

for letter, (idx1, idx2) in options.items():
    solver.push()
    # Add constraint: the third member is NOT idx1 AND NOT idx2
    # If this is unsat, then it's impossible for the third member to avoid {idx1, idx2}
    # => the third member must be either idx1 or idx2
    solver.add(Not(m[idx1]))
    solver.add(Not(m[idx2]))
    if solver.check() == unsat:
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