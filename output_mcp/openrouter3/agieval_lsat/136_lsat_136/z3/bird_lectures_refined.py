from z3 import *

# Create solver
solver = Solver()

# Define lectures
lectures = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]
L = {name: Int(f"L_{name}") for name in lectures}  # time slot (1-5)
V = {name: Int(f"V_{name}") for name in lectures}  # venue (0=Gladwyn, 1=Howard)

# Base constraints
# All lectures must have distinct time slots (1-5)
solver.add(Distinct([L[name] for name in lectures]))

# All time slots must be between 1 and 5
for name in lectures:
    solver.add(L[name] >= 1, L[name] <= 5)
    solver.add(V[name] >= 0, V[name] <= 1)

# 1. First lecture is in Gladwyn Hall
# Find which lecture is at time 1 and ensure it's in Gladwyn
solver.add(Or([And(L[name] == 1, V[name] == 0) for name in lectures]))

# 2. Fourth lecture is in Howard Auditorium
solver.add(Or([And(L[name] == 4, V[name] == 1) for name in lectures]))

# 3. Exactly three lectures are in Gladwyn Hall (venue 0)
solver.add(Sum([If(V[name] == 0, 1, 0) for name in lectures]) == 3)

# 4. Sandpipers lecture is in Howard and earlier than oystercatchers
solver.add(V["sandpipers"] == 1)
solver.add(L["sandpipers"] < L["oystercatchers"])

# 5. Terns lecture is earlier than petrels, and petrels is in Gladwyn Hall
solver.add(L["terns"] < L["petrels"])
solver.add(V["petrels"] == 0)

# 6. Additional constraint: terns is in Howard Auditorium (given in question)
solver.add(V["terns"] == 1)

# Now test each option for the 3rd lecture
# Option A: It is on oystercatchers and is in Gladwyn Hall
opt_a_constr = And(L["oystercatchers"] == 3, V["oystercatchers"] == 0)

# Option B: It is on rails and is in Howard Auditorium
opt_b_constr = And(L["rails"] == 3, V["rails"] == 1)

# Option C: It is on rails and is in Gladwyn Hall
opt_c_constr = And(L["rails"] == 3, V["rails"] == 0)

# Option D: It is on sandpipers and is in Howard Auditorium
opt_d_constr = And(L["sandpipers"] == 3, V["sandpipers"] == 1)

# Option E: It is on terns and is in Howard Auditorium
opt_e_constr = And(L["terns"] == 3, V["terns"] == 1)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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