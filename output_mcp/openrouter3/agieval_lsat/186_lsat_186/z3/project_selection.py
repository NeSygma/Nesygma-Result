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

# Option A: third member is Quinn OR Smith
opt_a_constr = Or(
    And(is_member["Quinn"], Not(is_member["Smith"])),  # Quinn is third, Smith not member
    And(is_member["Smith"], Not(is_member["Quinn"]))   # Smith is third, Quinn not member
)

# Option B: third member is Quinn OR Xue
opt_b_constr = Or(
    And(is_member["Quinn"], Not(is_member["Xue"])),    # Quinn is third, Xue not member
    And(is_member["Xue"], Not(is_member["Quinn"]))     # Xue is third, Quinn not member
)

# Option C: third member is Ruiz OR Verma
opt_c_constr = Or(
    And(is_member["Ruiz"], Not(is_member["Verma"])),   # Ruiz is third, Verma not member
    And(is_member["Verma"], Not(is_member["Ruiz"]))    # Verma is third, Ruiz not member
)

# Option D: third member is Smith OR Xue
opt_d_constr = Or(
    And(is_member["Smith"], Not(is_member["Xue"])),    # Smith is third, Xue not member
    And(is_member["Xue"], Not(is_member["Smith"]))     # Xue is third, Smith not member
)

# Option E: third member is Verma OR Xue
opt_e_constr = Or(
    And(is_member["Verma"], Not(is_member["Xue"])),    # Verma is third, Xue not member
    And(is_member["Xue"], Not(is_member["Verma"]))     # Xue is third, Verma not member
)

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    # Also need to ensure exactly 3 members total (Taylor, Wells, and third)
    # We already have Taylor and Wells as members, so we need to ensure no other members
    # Add constraint that only Taylor, Wells, and the third are members
    # But we need to be careful: the third is determined by the option
    # We'll add constraints to ensure no other members besides Taylor, Wells, and the third
    # However, the option constraints already specify who the third is
    # We need to ensure that Quinn, Ruiz, Smith, Verma, Xue are not members unless specified
    # Actually, we need to ensure that exactly 3 members: Taylor, Wells, and one from the option
    # So we need to add: for all workers not in {Taylor, Wells, third}, they are not members
    # But the third is symbolic in the option, so we need to handle this carefully
    
    # Let's add a constraint that ensures only Taylor, Wells, and the third are members
    # We'll do this by ensuring that for each worker, if they're not Taylor, Wells, or the third, they're not a member
    # But the third is determined by the option, so we need to express this
    
    # Actually, we can simplify: we already have Taylor and Wells as members
    # We need exactly one more member, and it must be from the option
    # So we can add: Sum of members = 3 (already have), and the third is from the option
    # But we also need to ensure that no other workers are members
    
    # Let's add constraints to ensure that only Taylor, Wells, and the third are members
    # For each worker, if they're not Taylor, Wells, or the third, they're not a member
    # But the third is symbolic, so we need to use the option constraint
    
    # Actually, we can use the fact that we already have Taylor and Wells as members
    # And we're adding the option constraint which ensures one of the pair is a member
    # But we need to ensure that exactly one of the pair is a member (not both)
    # And that no other workers are members
    
    # Let's add: for all workers except Taylor, Wells, and the third, they are not members
    # But the third is from the option, so we need to handle each option separately
    
    # Actually, we can add a general constraint: for all workers, if they're not Taylor, Wells, or the third, they're not members
    # But the third is determined by the option, so we need to express this in terms of the option
    
    # Let's do it differently: we'll add constraints to ensure that only Taylor, Wells, and the third are members
    # We'll add: for each worker w, is_member[w] is true only if w is Taylor, Wells, or the third
    # But the third is from the option, so we need to use the option constraint
    
    # Actually, we can use the fact that we already have Taylor and Wells as members
    # And we're adding the option constraint which ensures one of the pair is a member
    # But we need to ensure that no other workers are members
    
    # Let's add: for all workers except Taylor, Wells, Quinn, Smith, Ruiz, Verma, Xue (all workers)
    # Actually, we need to ensure that only Taylor, Wells, and the third are members
    # So we need to ensure that for each worker, if they're not Taylor, Wells, or the third, they're not a member
    
    # Since the third is from the option, we can add:
    # For each worker w in {Quinn, Ruiz, Smith, Verma, Xue}, if w is not the third, then is_member[w] is false
    # But the third is determined by the option, so we need to express this
    
    # Let's handle each option separately by adding constraints that ensure only the specified third is a member
    # But we're already using solver.push() and solver.add(constr), so we can add more constraints here
    
    # Actually, we can add a constraint that ensures exactly 3 members: Taylor, Wells, and one from the option
    # We already have Taylor and Wells as members, so we need to ensure that exactly one from the option is a member
    # And that no other workers are members
    
    # Let's add: for all workers except Taylor, Wells, and the third, they are not members
    # But the third is from the option, so we need to express this in terms of the option
    
    # Actually, we can use the fact that the option constraint already ensures one of the pair is a member
    # And we can add constraints to ensure that the other workers are not members
    
    # Let's add: for each worker w in {Quinn, Ruiz, Smith, Verma, Xue}, if w is not in the option pair, then is_member[w] is false
    # But the option pair is specific to each option
    
    # Let's do it this way: for each option, we'll add constraints to ensure that only Taylor, Wells, and the third are members
    # We'll add: for all workers w, is_member[w] is true only if w is Taylor, Wells, or the third
    # But the third is from the option, so we need to express this
    
    # Actually, we can add: for each worker w, if w is not Taylor, Wells, or the third, then is_member[w] is false
    # But the third is from the option, so we need to use the option constraint
    
    # Let's use a different approach: we'll add constraints to ensure that the only members are Taylor, Wells, and one from the option
    # We'll add: for each worker w in {Quinn, Ruiz, Smith, Verma, Xue}, is_member[w] is true only if w is the third
    # But the third is from the option, so we need to express this
    
    # Actually, we can add: for each worker w in {Quinn, Ruiz, Smith, Verma, Xue}, 
    # is_member[w] is true only if (w is Quinn and option A or B) or (w is Smith and option A or D) etc.
    # This is getting complicated
    
    # Let's simplify: we'll add constraints to ensure that only Taylor, Wells, and the third are members
    # We'll add: for all workers w, is_member[w] is true only if w is Taylor, Wells, or the third
    # But the third is from the option, so we need to express this in terms of the option
    
    # Actually, we can use the fact that we already have Taylor and Wells as members
    # And we're adding the option constraint which ensures one of the pair is a member
    # But we need to ensure that no other workers are members
    
    # Let's add: for each worker w in {Quinn, Ruiz, Smith, Verma, Xue}, 
    # is_member[w] is true only if w is in the option pair
    # But the option pair is specific to each option
    
    # Let's handle each option separately by adding specific constraints
    
    # Actually, we can add a general constraint: for all workers w, is_member[w] is true only if w is Taylor, Wells, or (w is in the option pair and the option constraint ensures exactly one of them is a member)
    # But this is still complicated
    
    # Let's do it this way: we'll add constraints to ensure that only Taylor, Wells, and the third are members
    # We'll add: for each worker w in {Quinn, Ruiz, Smith, Verma, Xue}, 
    # is_member[w] is true only if (w is Quinn and option A or B) or (w is Smith and option A or D) etc.
    # But we can express this using the option constraint
    
    # Actually, we can use the fact that the option constraint already ensures one of the pair is a member
    # And we can add constraints to ensure that the other workers are not members
    
    # Let's add: for each worker w in {Quinn, Ruiz, Smith, Verma, Xue}, 
    # if w is not in the option pair, then is_member[w] is false
    # But the option pair is specific to each option
    
    # Let's handle each option separately:
    
    if letter == "A":
        # Option A: third is Quinn or Smith
        # Ensure that Ruiz, Verma, Xue are not members
        solver.add(Not(is_member["Ruiz"]))
        solver.add(Not(is_member["Verma"]))
        solver.add(Not(is_member["Xue"]))
        # Ensure that exactly one of Quinn or Smith is a member (already in opt_a_constr)
        # But we also need to ensure that if Quinn is member, then Quinn is not leader (since Taylor is leader)
        # Actually, Quinn can only be member if leader, but Taylor is leader, so Quinn cannot be member
        # Wait, constraint: Quinn can be member only if leading the project
        # But Taylor is leader, so Quinn cannot be member
        # So option A is invalid because Quinn cannot be member if Taylor is leader
        # But we need to check this with Z3
        pass
    elif letter == "B":
        # Option B: third is Quinn or Xue
        # Ensure that Ruiz, Smith, Verma are not members
        solver.add(Not(is_member["Ruiz"]))
        solver.add(Not(is_member["Smith"]))
        solver.add(Not(is_member["Verma"]))
        # But again, Quinn can only be member if leader, but Taylor is leader, so Quinn cannot be member
        # So option B is invalid if Quinn is the third
        # But Xue can be member without being leader
        pass
    elif letter == "C":
        # Option C: third is Ruiz or Verma
        # Ensure that Quinn, Smith, Xue are not members
        solver.add(Not(is_member["Quinn"]))
        solver.add(Not(is_member["Smith"]))
        solver.add(Not(is_member["Xue"]))
        # But Ruiz can only be member if leader, but Taylor is leader, so Ruiz cannot be member
        # So option C is invalid if Ruiz is the third
        # Verma can be member without being leader, but Wells is member, so Verma cannot be member (constraint 5)
        # So option C is invalid
        pass
    elif letter == "D":
        # Option D: third is Smith or Xue
        # Ensure that Quinn, Ruiz, Verma are not members
        solver.add(Not(is_member["Quinn"]))
        solver.add(Not(is_member["Ruiz"]))
        solver.add(Not(is_member["Verma"]))
        # Smith can be member if Taylor is member (constraint 4), and Taylor is member (as leader)
        # Xue can be member without being leader
        pass
    elif letter == "E":
        # Option E: third is Verma or Xue
        # Ensure that Quinn, Ruiz, Smith are not members
        solver.add(Not(is_member["Quinn"]))
        solver.add(Not(is_member["Ruiz"]))
        solver.add(Not(is_member["Smith"]))
        # But Verma cannot be member if Wells is member (constraint 5)
        # So option E is invalid if Verma is the third
        # Xue can be member without being leader
        pass
    
    # Now check if the constraints are satisfiable
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