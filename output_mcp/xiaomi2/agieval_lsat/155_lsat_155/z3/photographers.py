from z3 import *

solver = Solver()

# Photographers: Frost=0, Gonzalez=1, Heideck=2, Knutson=3, Lai=4, Mays=5
# Assignment: 0=not assigned, 1=Silva, 2=Thorne
names = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]
assign = [Int(f'assign_{names[i]}') for i in range(6)]

# Domain: each photographer is 0 (unassigned), 1 (Silva), or 2 (Thorne)
for a in assign:
    solver.add(Or(a == 0, a == 1, a == 2))

# Each ceremony must have at least 2 photographers
# Count Silva assignments >= 2
solver.add(Sum([If(assign[i] == 1, 1, 0) for i in range(6)]) >= 2)
# Count Thorne assignments >= 2
solver.add(Sum([If(assign[i] == 2, 1, 0) for i in range(6)]) >= 2)

# Constraint 1: Frost must be assigned together with Heideck to one ceremony
# Either both assigned to same ceremony, or both unassigned
solver.add(Or(
    And(assign[0] == 1, assign[2] == 1),  # Both Silva
    And(assign[0] == 2, assign[2] == 2),  # Both Thorne
    And(assign[0] == 0, assign[2] == 0)   # Both unassigned
))

# Constraint 2: If Lai and Mays are both assigned, they must be to different ceremonies
solver.add(Implies(
    And(assign[4] != 0, assign[5] != 0),
    assign[4] != assign[5]
))

# Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
solver.add(Implies(assign[1] == 1, assign[4] == 2))

# Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
solver.add(Implies(assign[3] != 2, And(assign[2] == 2, assign[5] == 2)))

# Now evaluate each option
# Option A: Silva: Gonzalez, Lai | Thorne: Frost, Heideck, Mays
opt_a_constr = And(
    assign[1] == 1, assign[4] == 1,  # Gonzalez, Lai -> Silva
    assign[0] == 2, assign[2] == 2, assign[5] == 2,  # Frost, Heideck, Mays -> Thorne
    assign[3] == 0  # Knutson unassigned
)

# Option B: Silva: Gonzalez, Mays | Thorne: Knutson, Lai
opt_b_constr = And(
    assign[1] == 1, assign[5] == 1,  # Gonzalez, Mays -> Silva
    assign[3] == 2, assign[4] == 2,  # Knutson, Lai -> Thorne
    assign[0] == 0, assign[2] == 0  # Frost, Heideck unassigned
)

# Option C: Silva: Frost, Gonzalez, Heideck | Thorne: Knutson, Lai, Mays
opt_c_constr = And(
    assign[0] == 1, assign[1] == 1, assign[2] == 1,  # Frost, Gonzalez, Heideck -> Silva
    assign[3] == 2, assign[4] == 2, assign[5] == 2   # Knutson, Lai, Mays -> Thorne
)

# Option D: Silva: Frost, Heideck, Mays | Thorne: Gonzalez, Lai
opt_d_constr = And(
    assign[0] == 1, assign[2] == 1, assign[5] == 1,  # Frost, Heideck, Mays -> Silva
    assign[1] == 2, assign[4] == 2,  # Gonzalez, Lai -> Thorne
    assign[3] == 0  # Knutson unassigned
)

# Option E: Silva: Frost, Heideck, Mays | Thorne: Gonzalez, Knutson, Lai
opt_e_constr = And(
    assign[0] == 1, assign[2] == 1, assign[5] == 1,  # Frost, Heideck, Mays -> Silva
    assign[1] == 2, assign[3] == 2, assign[4] == 2   # Gonzalez, Knutson, Lai -> Thorne
)

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