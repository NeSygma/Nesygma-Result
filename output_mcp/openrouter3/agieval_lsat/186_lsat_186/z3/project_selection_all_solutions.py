from z3 import *

# Create solver
solver = Solver()

# Workers: Quinn, Ruiz, Smith, Taylor, Verma, Wells, Xue
workers = ["Quinn", "Ruiz", "Smith", "Taylor", "Verma", "Wells", "Xue"]
# Boolean variables: is_member[w] and is_leader[w]
is_member = {w: Bool(f"member_{w}") for w in workers}
is_leader = {w: Bool(f"leader_{w}") for w in workers}

# Base constraints from problem statement
# 1. Exactly 3 members
solver.add(Sum([If(is_member[w], 1, 0) for w in workers]) == 3)

# 2. Exactly 1 leader (and leader must be a member)
solver.add(Sum([If(is_leader[w], 1, 0) for w in workers]) == 1)
for w in workers:
    solver.add(Implies(is_leader[w], is_member[w]))

# 3. Quinn or Ruiz can be a project member only if leading the project
for w in ["Quinn", "Ruiz"]:
    solver.add(Implies(is_member[w], is_leader[w]))

# 4. If Smith is a project member, Taylor must also be
solver.add(Implies(is_member["Smith"], is_member["Taylor"]))

# 5. If Wells is a project member, neither Ruiz nor Verma can be
solver.add(Implies(is_member["Wells"], And(Not(is_member["Ruiz"]), Not(is_member["Verma"]))))

# Additional given: Taylor is the project leader and Wells is a project member
solver.add(is_leader["Taylor"])
solver.add(is_member["Wells"])

# Now find all valid solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    # Get the members for this solution
    members = [w for w in workers if is_true(m[is_member[w]])]
    # Get the leader
    leader = [w for w in workers if is_true(m[is_leader[w]])]
    
    # Find the third member (besides Taylor and Wells)
    third = [w for w in members if w not in ["Taylor", "Wells"]]
    if len(third) == 1:
        solutions.append(third[0])
    
    # Block this solution to find the next one
    # Add constraint that at least one member variable must differ
    solver.add(Or([is_member[w] != is_true(m[is_member[w]]) for w in workers]))

print(f"STATUS: sat")
print(f"Found {len(solutions)} valid solutions")
print(f"Third members: {solutions}")

# Now check which options are always true
# Option A: Quinn or Smith
opt_a = all(s in ["Quinn", "Smith"] for s in solutions)
# Option B: Quinn or Xue
opt_b = all(s in ["Quinn", "Xue"] for s in solutions)
# Option C: Ruiz or Verma
opt_c = all(s in ["Ruiz", "Verma"] for s in solutions)
# Option D: Smith or Xue
opt_d = all(s in ["Smith", "Xue"] for s in solutions)
# Option E: Verma or Xue
opt_e = all(s in ["Verma", "Xue"] for s in solutions)

print(f"Option A (Quinn or Smith): {opt_a}")
print(f"Option B (Quinn or Xue): {opt_b}")
print(f"Option C (Ruiz or Verma): {opt_c}")
print(f"Option D (Smith or Xue): {opt_d}")
print(f"Option E (Verma or Xue): {opt_e}")

# Find which option is always true
always_true = []
if opt_a: always_true.append("A")
if opt_b: always_true.append("B")
if opt_c: always_true.append("C")
if opt_d: always_true.append("D")
if opt_e: always_true.append("E")

if len(always_true) == 1:
    print(f"answer:{always_true[0]}")
else:
    print(f"Refine: Multiple options always true: {always_true}")