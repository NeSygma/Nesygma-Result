from z3 import *

# Create solver
solver = Solver()

# Define singers
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
# Create position variables for each singer (1-6)
pos = {s: Int(f"pos_{s}") for s in singers}

# Add domain constraints: each position is between 1 and 6
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)

# All positions must be distinct (each singer in a unique position)
solver.add(Distinct([pos[s] for s in singers]))

# Recorded singers: Kammer and Lugo
recorded = ["Kammer", "Lugo"]
non_recorded = ["Trillo", "Waite", "Yoshida", "Zinn"]

# Condition 1: Fourth audition cannot be recorded
# So position 4 cannot be Kammer or Lugo
solver.add(pos["Kammer"] != 4)
solver.add(pos["Lugo"] != 4)

# Condition 2: Fifth audition must be recorded
# So position 5 must be either Kammer or Lugo
solver.add(Or(pos["Kammer"] == 5, pos["Lugo"] == 5))

# Condition 3: Waite's audition must take place earlier than the two recorded auditions
# So Waite's position < Kammer's position AND Waite's position < Lugo's position
solver.add(pos["Waite"] < pos["Kammer"])
solver.add(pos["Waite"] < pos["Lugo"])

# Condition 4: Kammer's audition must take place earlier than Trillo's audition
solver.add(pos["Kammer"] < pos["Trillo"])

# Condition 5: Zinn's audition must take place earlier than Yoshida's audition
solver.add(pos["Zinn"] < pos["Yoshida"])

# Now define the options as constraints
# Each option specifies the exact order from first to last
# We need to encode that the positions match the given order

# Option A: Kammer, Trillo, Zinn, Waite, Lugo, Yoshida
opt_a = And(
    pos["Kammer"] == 1,
    pos["Trillo"] == 2,
    pos["Zinn"] == 3,
    pos["Waite"] == 4,
    pos["Lugo"] == 5,
    pos["Yoshida"] == 6
)

# Option B: Waite, Kammer, Yoshida, Zinn, Lugo, Trillo
opt_b = And(
    pos["Waite"] == 1,
    pos["Kammer"] == 2,
    pos["Yoshida"] == 3,
    pos["Zinn"] == 4,
    pos["Lugo"] == 5,
    pos["Trillo"] == 6
)

# Option C: Waite, Lugo, Kammer, Trillo, Zinn, Yoshida
opt_c = And(
    pos["Waite"] == 1,
    pos["Lugo"] == 2,
    pos["Kammer"] == 3,
    pos["Trillo"] == 4,
    pos["Zinn"] == 5,
    pos["Yoshida"] == 6
)

# Option D: Waite, Zinn, Kammer, Trillo, Lugo, Yoshida
opt_d = And(
    pos["Waite"] == 1,
    pos["Zinn"] == 2,
    pos["Kammer"] == 3,
    pos["Trillo"] == 4,
    pos["Lugo"] == 5,
    pos["Yoshida"] == 6
)

# Option E: Zinn, Yoshida, Waite, Lugo, Kammer, Trillo
opt_e = And(
    pos["Zinn"] == 1,
    pos["Yoshida"] == 2,
    pos["Waite"] == 3,
    pos["Lugo"] == 4,
    pos["Kammer"] == 5,
    pos["Trillo"] == 6
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
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