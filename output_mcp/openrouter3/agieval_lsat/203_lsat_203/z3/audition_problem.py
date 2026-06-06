from z3 import *

# Create solver
solver = Solver()

# Define singers
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
# Map names to indices for easier reference
name_to_idx = {name: i for i, name in enumerate(singers)}

# Position variables: position[i] = position of singer i (1-6)
position = [Int(f"pos_{name}") for name in singers]

# Recorded status: recorded[i] = True if singer i is recorded
# Kammer and Lugo are recorded, others are not
recorded = [Bool(f"rec_{name}") for name in singers]

# Add base constraints
# 1. All positions are distinct and in range 1-6
for i in range(6):
    solver.add(position[i] >= 1)
    solver.add(position[i] <= 6)
solver.add(Distinct(position))

# 2. Recorded status: Kammer and Lugo are recorded, others are not
solver.add(recorded[name_to_idx["Kammer"]] == True)
solver.add(recorded[name_to_idx["Lugo"]] == True)
solver.add(recorded[name_to_idx["Trillo"]] == False)
solver.add(recorded[name_to_idx["Waite"]] == False)
solver.add(recorded[name_to_idx["Yoshida"]] == False)
solver.add(recorded[name_to_idx["Zinn"]] == False)

# 3. Fourth audition cannot be recorded
# Find which singer is at position 4, and ensure they are not recorded
for i in range(6):
    solver.add(Implies(position[i] == 4, Not(recorded[i])))

# 4. Fifth audition must be recorded
for i in range(6):
    solver.add(Implies(position[i] == 5, recorded[i]))

# 5. Waite's audition must be earlier than the two recorded auditions
# The two recorded auditions are Kammer and Lugo
waite_idx = name_to_idx["Waite"]
kammer_idx = name_to_idx["Kammer"]
lugo_idx = name_to_idx["Lugo"]
solver.add(position[waite_idx] < position[kammer_idx])
solver.add(position[waite_idx] < position[lugo_idx])

# 6. Kammer's audition must be earlier than Trillo's audition
trillo_idx = name_to_idx["Trillo"]
solver.add(position[kammer_idx] < position[trillo_idx])

# 7. Zinn's audition must be earlier than Yoshida's audition
zinn_idx = name_to_idx["Zinn"]
yoshida_idx = name_to_idx["Yoshida"]
solver.add(position[zinn_idx] < position[yoshida_idx])

# Now test each option: which one CANNOT be the second audition?
# We'll test each option by adding the constraint that the singer is at position 2
# If the solver becomes unsatisfiable, that singer CANNOT be at position 2

found_options = []
for letter, singer in [("A", "Kammer"), ("B", "Lugo"), ("C", "Trillo"), ("D", "Waite"), ("E", "Zinn")]:
    solver.push()
    # Add constraint: this singer is at position 2
    solver.add(position[name_to_idx[singer]] == 2)
    if solver.check() == sat:
        # This singer CAN be at position 2
        pass
    else:
        # This singer CANNOT be at position 2
        found_options.append(letter)
    solver.pop()

# According to the problem, exactly one option should be impossible
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")