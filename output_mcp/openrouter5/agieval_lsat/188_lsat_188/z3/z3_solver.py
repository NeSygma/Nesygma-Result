from z3 import *

# Seven workers: Quinn, Ruiz, Smith, Taylor, Verma, Wells, Xue
# We'll use Boolean variables for "is a project member" and "is the project leader"
# Exactly 3 members, exactly 1 leader among those members.

workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]

member = {w: Bool(f"member_{w}") for w in workers}
leader = {w: Bool(f"leader_{w}") for w in workers}

solver = Solver()

# Exactly three project members
solver.add(Sum([If(member[w], 1, 0) for w in workers]) == 3)

# Exactly one project leader (and leader must be a member)
solver.add(Sum([If(leader[w], 1, 0) for w in workers]) == 1)
for w in workers:
    solver.add(Implies(leader[w], member[w]))

# Constraints:
# 1. Quinn or Ruiz can be a project member only if leading the project.
#    i.e., If Quinn is a member, Quinn must be leader. If Ruiz is a member, Ruiz must be leader.
solver.add(Implies(member["Quinn"], leader["Quinn"]))
solver.add(Implies(member["Ruiz"], leader["Ruiz"]))

# 2. If Smith is a project member, Taylor must also be.
solver.add(Implies(member["Smith"], member["Taylor"]))

# 3. If Wells is a project member, neither Ruiz nor Verma can be.
solver.add(Implies(member["Wells"], Not(Or(member["Ruiz"], member["Verma"]))))

# Additional condition: Taylor is NOT a project member
solver.add(Not(member["Taylor"]))

# Now evaluate each option: which worker MUST be a project member?
# We test each option by adding the constraint that the worker is NOT a member.
# If that leads to unsat, then the worker MUST be a member.

found_options = []

# Option A: Quinn must be a member?
opt_a = Not(member["Quinn"])
# Option B: Ruiz must be a member?
opt_b = Not(member["Ruiz"])
# Option C: Verma must be a member?
opt_c = Not(member["Verma"])
# Option D: Wells must be a member?
opt_d = Not(member["Wells"])
# Option E: Xue must be a member?
opt_e = Not(member["Xue"])

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        # If adding "worker is NOT a member" is unsat, then worker MUST be a member
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