from z3 import *

# Photographers: Frost=0, Gonzalez=1, Heideck=2, Knutson=3, Lai=4, Mays=5
names = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]
N = 6

# Assignment: 0=unassigned, 1=Silva, 2=Thorne
assign = [Int(f'assign_{names[i]}') for i in range(N)]

# Base constraints
solver = Solver()
for i in range(N):
    solver.add(Or(assign[i] == 0, assign[i] == 1, assign[i] == 2))

# At least 2 photographers to each ceremony
solver.add(Sum([If(assign[i] == 1, 1, 0) for i in range(N)]) >= 2)
solver.add(Sum([If(assign[i] == 2, 1, 0) for i in range(N)]) >= 2)

# Constraint 1: Frost must be assigned together with Heideck to one ceremony
# Both at Silva, or both at Thorne, or neither assigned
solver.add(Or(
    And(assign[0] == 1, assign[2] == 1),  # Both Silva
    And(assign[0] == 2, assign[2] == 2),  # Both Thorne
    And(assign[0] == 0, assign[2] == 0)   # Neither assigned
))

# Constraint 2: If Lai and Mays are both assigned, different ceremonies
# If both assigned (not 0), they can't be at same ceremony
solver.add(Implies(
    And(assign[4] != 0, assign[5] != 0),
    assign[4] != assign[5]
))

# Constraint 3: If Gonzalez assigned to Silva, Lai must be assigned to Thorne
solver.add(Implies(assign[1] == 1, assign[4] == 2))

# Constraint 4: If Knutson not assigned to Thorne, both Heideck and Mays must be assigned to Thorne
solver.add(Implies(assign[3] != 2, And(assign[2] == 2, assign[5] == 2)))

# Now check each option for complete assignment to Silva
# Option A: Frost, Gonzalez, Heideck, Knutson at Silva (others not at Silva)
opt_a = And(assign[0]==1, assign[1]==1, assign[2]==1, assign[3]==1, assign[4]!=1, assign[5]!=1)
# Option B: Frost, Gonzalez, Heideck at Silva
opt_b = And(assign[0]==1, assign[1]==1, assign[2]==1, assign[3]!=1, assign[4]!=1, assign[5]!=1)
# Option C: Gonzalez, Knutson at Silva
opt_c = And(assign[0]!=1, assign[1]==1, assign[2]!=1, assign[3]==1, assign[4]!=1, assign[5]!=1)
# Option D: Heideck, Lai at Silva
opt_d = And(assign[0]!=1, assign[1]!=1, assign[2]==1, assign[3]!=1, assign[4]==1, assign[5]!=1)
# Option E: Knutson, Mays at Silva
opt_e = And(assign[0]!=1, assign[1]!=1, assign[2]!=1, assign[3]==1, assign[4]!=1, assign[5]==1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for i in range(N):
            val = m[assign[i]]
            if val is not None:
                print(f"  {names[i]} = {['unassigned','Silva','Thorne'][int(str(val))]}")
        found_options.append(letter)
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")