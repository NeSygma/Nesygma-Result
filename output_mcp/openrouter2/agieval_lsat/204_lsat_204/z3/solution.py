from z3 import *
solver = Solver()

singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
pos = {s: Int(f"{s}_pos") for s in singers}
recorded = {s: Bool(f"{s}_rec") for s in singers}

# Domain constraints
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)

# Distinct positions
solver.add(Distinct([pos[s] for s in singers]))

# Recorded status: Kammer and Lugo recorded, others not
solver.add(recorded["Kammer"] == True)
solver.add(recorded["Lugo"] == True)
for s in singers:
    if s not in ["Kammer", "Lugo"]:
        solver.add(recorded[s] == False)

# Fourth audition cannot be recorded
for s in singers:
    solver.add(Implies(pos[s] == 4, Not(recorded[s])))

# Fifth audition must be recorded
for s in singers:
    solver.add(Implies(pos[s] == 5, recorded[s]))

# Waite earlier than the two recorded auditions
solver.add(pos["Waite"] < pos["Kammer"])
solver.add(pos["Waite"] < pos["Lugo"])

# Kammer earlier than Trillo
solver.add(pos["Kammer"] < pos["Trillo"])

# Zinn earlier than Yoshida
solver.add(pos["Zinn"] < pos["Yoshida"])

# Options
opt_a_constr = pos["Kammer"] == 6
opt_b_constr = pos["Lugo"] == 6
opt_c_constr = pos["Trillo"] == 6
opt_d_constr = pos["Waite"] == 6
opt_e_constr = pos["Zinn"] == 6

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