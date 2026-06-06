from z3 import *

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

# Now define the options as constraints on the third member
# The third member is the one that is a member but not Taylor or Wells
# We need to express: "the third member is Quinn or Smith" etc.

# For each option, we need to check if it's possible that the third member satisfies that option
# But we need to check if the option MUST be true (i.e., in all valid scenarios)

# Let's find all possible third members first
# We'll use a different approach: for each possible third member, check if it's valid

# First, let's find all valid third members
third_members = []
for w in workers:
    if w not in ["Taylor", "Wells"]:
        solver.push()
        # Add constraint that w is the third member
        solver.add(is_member[w])
        # Ensure no other members besides Taylor, Wells, and w
        for other in workers:
            if other not in ["Taylor", "Wells", w]:
                solver.add(Not(is_member[other]))
        
        if solver.check() == sat:
            third_members.append(w)
        solver.pop()

print(f"Possible third members: {third_members}")

# Now define the options
# Option A: third member is Quinn or Smith
opt_a_constr = Or([And(is_member[w], w not in ["Taylor", "Wells"]) for w in ["Quinn", "Smith"]])
# But we need to ensure that the third member is exactly one of these
# Actually, we need to check if the third member MUST be Quinn or Smith
# This means: in all valid scenarios, the third member is in {Quinn, Smith}

# Let's check each option by seeing if it's possible that the third member is NOT in that option
# If it's impossible for the third member to be outside the option, then the option must be true

found_options = []

# Option A: Quinn or Smith
solver.push()
# Add constraint that the third member is NOT Quinn and NOT Smith
third_not_A = Or([And(is_member[w], w not in ["Taylor", "Wells"]) for w in workers if w not in ["Quinn", "Smith", "Taylor", "Wells"]])
solver.add(third_not_A)
# Also ensure exactly 3 members
solver.add(Sum([If(is_member[w], 1, 0) for w in workers]) == 3)
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: Quinn or Xue
solver.push()
third_not_B = Or([And(is_member[w], w not in ["Taylor", "Wells"]) for w in workers if w not in ["Quinn", "Xue", "Taylor", "Wells"]])
solver.add(third_not_B)
solver.add(Sum([If(is_member[w], 1, 0) for w in workers]) == 3)
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: Ruiz or Verma
solver.push()
third_not_C = Or([And(is_member[w], w not in ["Taylor", "Wells"]) for w in workers if w not in ["Ruiz", "Verma", "Taylor", "Wells"]])
solver.add(third_not_C)
solver.add(Sum([If(is_member[w], 1, 0) for w in workers]) == 3)
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: Smith or Xue
solver.push()
third_not_D = Or([And(is_member[w], w not in ["Taylor", "Wells"]) for w in workers if w not in ["Smith", "Xue", "Taylor", "Wells"]])
solver.add(third_not_D)
solver.add(Sum([If(is_member[w], 1, 0) for w in workers]) == 3)
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: Verma or Xue
solver.push()
third_not_E = Or([And(is_member[w], w not in ["Taylor", "Wells"]) for w in workers if w not in ["Verma", "Xue", "Taylor", "Wells"]])
solver.add(third_not_E)
solver.add(Sum([If(is_member[w], 1, 0) for w in workers]) == 3)
if solver.check() == unsat:
    found_options.append("E")
solver.pop()

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")