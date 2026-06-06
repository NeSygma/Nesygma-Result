from z3 import *

# Seven workers: Quinn, Ruiz, Smith, Taylor, Verma, Wells, Xue
# We'll use indices 0-6
# 0: Quinn, 1: Ruiz, 2: Smith, 3: Taylor, 4: Verma, 5: Wells, 6: Xue
names = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]
Q, R, S, T, V, W, X = 0, 1, 2, 3, 4, 5, 6

solver = Solver()

# member[i] = True if worker i is a project member
member = [Bool(f"member_{i}") for i in range(7)]

# leader[i] = True if worker i is the project leader
leader = [Bool(f"leader_{i}") for i in range(7)]

# Exactly three members
solver.add(Sum([If(member[i], 1, 0) for i in range(7)]) == 3)

# Exactly one leader
solver.add(Sum([If(leader[i], 1, 0) for i in range(7)]) == 1)

# Leader must be a member
for i in range(7):
    solver.add(Implies(leader[i], member[i]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project.
# If Quinn is a member, Quinn must be leader.
solver.add(Implies(member[Q], leader[Q]))
# If Ruiz is a member, Ruiz must be leader.
solver.add(Implies(member[R], leader[R]))

# Constraint 2: If Smith is a project member, Taylor must also be.
solver.add(Implies(member[S], member[T]))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be.
solver.add(Implies(member[W], Not(Or(member[R], member[V]))))

# Now evaluate each option
# Option A: Ruiz (leader), Taylor, Wells
opt_a_constr = And(
    leader[R], member[R],
    member[T],
    member[W],
    # Exactly these three members (and no others)
    Sum([If(member[i], 1, 0) for i in range(7)]) == 3,
    # Ensure only Ruiz, Taylor, Wells are members
    member[Q] == False,
    member[S] == False,
    member[V] == False,
    member[X] == False,
    # Ruiz is leader
    Sum([If(leader[i], 1, 0) for i in range(7)]) == 1,
    leader[R] == True,
    leader[Q] == False, leader[S] == False, leader[T] == False,
    leader[V] == False, leader[W] == False, leader[X] == False
)

# Option B: Verma (leader), Quinn, Taylor
opt_b_constr = And(
    leader[V], member[V],
    member[Q],
    member[T],
    Sum([If(member[i], 1, 0) for i in range(7)]) == 3,
    member[R] == False,
    member[S] == False,
    member[W] == False,
    member[X] == False,
    Sum([If(leader[i], 1, 0) for i in range(7)]) == 1,
    leader[V] == True,
    leader[Q] == False, leader[R] == False, leader[S] == False,
    leader[T] == False, leader[W] == False, leader[X] == False
)

# Option C: Verma (leader), Smith, Taylor
opt_c_constr = And(
    leader[V], member[V],
    member[S],
    member[T],
    Sum([If(member[i], 1, 0) for i in range(7)]) == 3,
    member[Q] == False,
    member[R] == False,
    member[W] == False,
    member[X] == False,
    Sum([If(leader[i], 1, 0) for i in range(7)]) == 1,
    leader[V] == True,
    leader[Q] == False, leader[R] == False, leader[S] == False,
    leader[T] == False, leader[W] == False, leader[X] == False
)

# Option D: Verma (leader), Smith, Xue
opt_d_constr = And(
    leader[V], member[V],
    member[S],
    member[X],
    Sum([If(member[i], 1, 0) for i in range(7)]) == 3,
    member[Q] == False,
    member[R] == False,
    member[T] == False,
    member[W] == False,
    Sum([If(leader[i], 1, 0) for i in range(7)]) == 1,
    leader[V] == True,
    leader[Q] == False, leader[R] == False, leader[S] == False,
    leader[T] == False, leader[W] == False, leader[X] == False
)

# Option E: Xue (leader), Verma, Wells
opt_e_constr = And(
    leader[X], member[X],
    member[V],
    member[W],
    Sum([If(member[i], 1, 0) for i in range(7)]) == 3,
    member[Q] == False,
    member[R] == False,
    member[S] == False,
    member[T] == False,
    Sum([If(leader[i], 1, 0) for i in range(7)]) == 1,
    leader[X] == True,
    leader[Q] == False, leader[R] == False, leader[S] == False,
    leader[T] == False, leader[V] == False, leader[W] == False
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