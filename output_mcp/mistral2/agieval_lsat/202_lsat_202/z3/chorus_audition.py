from z3 import *

# Base constraints solver
solver = Solver()

# Singers
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
# Abbreviations for brevity
singer_abbrev = {
    "Kammer": "K",
    "Lugo": "L",
    "Trillo": "T",
    "Waite": "W",
    "Yoshida": "Y",
    "Zinn": "Z"
}

# Positions: 1 to 6
positions = range(1, 7)

# Assign each singer to a position
assign = {s: Int(f"pos_{s}") for s in singers}

# Each position has exactly one singer
solver.add(Distinct(list(assign.values())))
for pos in positions:
    solver.add(Or([assign[s] == pos for s in singers]))

# Recorded auditions: only K and L are recorded
recorded = ["Kammer", "Lugo"]
non_recorded = [s for s in singers if s not in recorded]

# Constraint 1: The fourth audition cannot be recorded
solver.add(Not(Or([assign[s] == 4 for s in recorded])))

# Constraint 2: The fifth audition must be recorded
solver.add(Or([assign[s] == 5 for s in recorded]))

# Constraint 3: Waite's audition must take place earlier than the two recorded auditions
solver.add(assign["Waite"] < assign["Kammer"])
solver.add(assign["Waite"] < assign["Lugo"])

# Constraint 4: Kammer's audition must take place earlier than Trillo's audition
solver.add(assign["Kammer"] < assign["Trillo"])

# Constraint 5: Zinn's audition must take place earlier than Yoshida's audition
solver.add(assign["Zinn"] < assign["Yoshida"])

# Now evaluate each option
found_options = []

# Option A: K, T, Z, W, L, Y
solver.push()
solver.add(assign["Kammer"] == 1)
solver.add(assign["Trillo"] == 2)
solver.add(assign["Zinn"] == 3)
solver.add(assign["Waite"] == 4)
solver.add(assign["Lugo"] == 5)
solver.add(assign["Yoshida"] == 6)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: W, K, Y, Z, L, T
solver.push()
solver.add(assign["Waite"] == 1)
solver.add(assign["Kammer"] == 2)
solver.add(assign["Yoshida"] == 3)
solver.add(assign["Zinn"] == 4)
solver.add(assign["Lugo"] == 5)
solver.add(assign["Trillo"] == 6)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: W, L, K, T, Z, Y
solver.push()
solver.add(assign["Waite"] == 1)
solver.add(assign["Lugo"] == 2)
solver.add(assign["Kammer"] == 3)
solver.add(assign["Trillo"] == 4)
solver.add(assign["Zinn"] == 5)
solver.add(assign["Yoshida"] == 6)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: W, Z, K, T, L, Y
solver.push()
solver.add(assign["Waite"] == 1)
solver.add(assign["Zinn"] == 2)
solver.add(assign["Kammer"] == 3)
solver.add(assign["Trillo"] == 4)
solver.add(assign["Lugo"] == 5)
solver.add(assign["Yoshida"] == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Z, Y, W, L, K, T
solver.push()
solver.add(assign["Zinn"] == 1)
solver.add(assign["Yoshida"] == 2)
solver.add(assign["Waite"] == 3)
solver.add(assign["Lugo"] == 4)
solver.add(assign["Kammer"] == 5)
solver.add(assign["Trillo"] == 6)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")