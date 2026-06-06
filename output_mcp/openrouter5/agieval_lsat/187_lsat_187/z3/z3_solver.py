from z3 import *

# Seven workers: Quinn, Ruiz, Smith, Taylor, Verma, Wells, Xue
# We'll use indices 0-6
names = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]
Q, R, S, T, V, W, X = range(7)

solver = Solver()

# Decision variables:
# member[i] = True if worker i is a project member
member = [Bool(f"member_{i}") for i in range(7)]
# leader[i] = True if worker i is the project leader
leader = [Bool(f"leader_{i}") for i in range(7)]

# Exactly three project members
solver.add(Sum([If(member[i], 1, 0) for i in range(7)]) == 3)

# Exactly one project leader
solver.add(Sum([If(leader[i], 1, 0) for i in range(7)]) == 1)

# The leader must be a project member
for i in range(7):
    solver.add(Implies(leader[i], member[i]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project.
# If Quinn is a member, then Quinn is leader.
solver.add(Implies(member[Q], leader[Q]))
# If Ruiz is a member, then Ruiz is leader.
solver.add(Implies(member[R], leader[R]))

# Constraint 2: If Smith is a project member, Taylor must also be.
solver.add(Implies(member[S], member[T]))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be.
solver.add(Implies(member[W], Not(Or(member[R], member[V]))))

# Question: Verma could be the project leader if which one of the following is true?
# We need to test each option: under that condition, is there a model where Verma is leader?

# Option A: Neither Quinn nor Smith is selected. (i.e., not members)
opt_a = And(Not(member[Q]), Not(member[S]))

# Option B: Neither Ruiz nor Taylor is selected.
opt_b = And(Not(member[R]), Not(member[T]))

# Option C: Neither Smith nor Taylor is selected.
opt_c = And(Not(member[S]), Not(member[T]))

# Option D: Neither Smith nor Xue is selected.
opt_d = And(Not(member[S]), Not(member[X]))

# Option E: Neither Taylor nor Wells is selected.
opt_e = And(Not(member[T]), Not(member[W]))

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    # We want to check if Verma CAN be leader under this condition
    solver.add(leader[V])
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