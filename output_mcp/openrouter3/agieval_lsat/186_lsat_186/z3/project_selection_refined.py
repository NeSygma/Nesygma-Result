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

# Now we need to find the third member (the one besides Taylor and Wells)
# We'll test each answer choice as the third member

# Answer choices:
# (A) Quinn or Smith
# (B) Quinn or Xue
# (C) Ruiz or Verma
# (D) Smith or Xue
# (E) Verma or Xue

# For each option, we need to check if there exists a valid assignment where:
# - Taylor is leader, Wells is member
# - The third member is from the option
# - All constraints are satisfied

# We'll use the exact skeleton provided
found_options = []

# For each option, we need to ensure:
# 1. Exactly 3 members: Taylor, Wells, and one from the option
# 2. The option constraint (one of the pair is the third member)
# 3. No other workers are members

# Let's define the options more carefully:
# Option A: third member is Quinn OR Smith
# Option B: third member is Quinn OR Xue
# Option C: third member is Ruiz OR Verma
# Option D: third member is Smith OR Xue
# Option E: third member is Verma OR Xue

# For each option, we'll add constraints to ensure only Taylor, Wells, and the third are members
# We'll also ensure that the third is from the option

for letter in ["A", "B", "C", "D", "E"]:
    solver.push()
    
    # Add constraint that ensures exactly 3 members: Taylor, Wells, and one from the option
    # We already have Taylor and Wells as members
    # We need to ensure that exactly one from the option is a member, and no others
    
    if letter == "A":
        # Option A: third is Quinn or Smith
        # Ensure that Ruiz, Verma, Xue are not members
        solver.add(Not(is_member["Ruiz"]))
        solver.add(Not(is_member["Verma"]))
        solver.add(Not(is_member["Xue"]))
        # Ensure that exactly one of Quinn or Smith is a member
        solver.add(Or(is_member["Quinn"], is_member["Smith"]))
        solver.add(Not(And(is_member["Quinn"], is_member["Smith"])))
        # But Quinn can only be member if leader, and Taylor is leader, so Quinn cannot be member
        # So we need to add: if Quinn is member, then Quinn is leader, but Taylor is leader, so Quinn cannot be member
        # Actually, we can add: Not(is_member["Quinn"]) because Taylor is leader
        solver.add(Not(is_member["Quinn"]))
        # So the third must be Smith
        # But we need to check if Smith can be member: yes, because Taylor is member (constraint 4)
        
    elif letter == "B":
        # Option B: third is Quinn or Xue
        # Ensure that Ruiz, Smith, Verma are not members
        solver.add(Not(is_member["Ruiz"]))
        solver.add(Not(is_member["Smith"]))
        solver.add(Not(is_member["Verma"]))
        # Ensure that exactly one of Quinn or Xue is a member
        solver.add(Or(is_member["Quinn"], is_member["Xue"]))
        solver.add(Not(And(is_member["Quinn"], is_member["Xue"])))
        # But Quinn can only be member if leader, and Taylor is leader, so Quinn cannot be member
        solver.add(Not(is_member["Quinn"]))
        # So the third must be Xue
        
    elif letter == "C":
        # Option C: third is Ruiz or Verma
        # Ensure that Quinn, Smith, Xue are not members
        solver.add(Not(is_member["Quinn"]))
        solver.add(Not(is_member["Smith"]))
        solver.add(Not(is_member["Xue"]))
        # Ensure that exactly one of Ruiz or Verma is a member
        solver.add(Or(is_member["Ruiz"], is_member["Verma"]))
        solver.add(Not(And(is_member["Ruiz"], is_member["Verma"])))
        # But Ruiz can only be member if leader, and Taylor is leader, so Ruiz cannot be member
        solver.add(Not(is_member["Ruiz"]))
        # And Verma cannot be member if Wells is member (constraint 5)
        solver.add(Not(is_member["Verma"]))
        # So this option is invalid
        
    elif letter == "D":
        # Option D: third is Smith or Xue
        # Ensure that Quinn, Ruiz, Verma are not members
        solver.add(Not(is_member["Quinn"]))
        solver.add(Not(is_member["Ruiz"]))
        solver.add(Not(is_member["Verma"]))
        # Ensure that exactly one of Smith or Xue is a member
        solver.add(Or(is_member["Smith"], is_member["Xue"]))
        solver.add(Not(And(is_member["Smith"], is_member["Xue"])))
        # Both Smith and Xue can be members without being leader
        # Smith can be member because Taylor is member (constraint 4)
        # Xue can be member without any constraints
        
    elif letter == "E":
        # Option E: third is Verma or Xue
        # Ensure that Quinn, Ruiz, Smith are not members
        solver.add(Not(is_member["Quinn"]))
        solver.add(Not(is_member["Ruiz"]))
        solver.add(Not(is_member["Smith"]))
        # Ensure that exactly one of Verma or Xue is a member
        solver.add(Or(is_member["Verma"], is_member["Xue"]))
        solver.add(Not(And(is_member["Verma"], is_member["Xue"])))
        # But Verma cannot be member if Wells is member (constraint 5)
        solver.add(Not(is_member["Verma"]))
        # So the third must be Xue
    
    # Check if the constraints are satisfiable
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")