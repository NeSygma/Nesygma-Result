from z3 import *

# Students: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
names = {0: "Juana", 1: "Kelly", 2: "Lateefah", 3: "Mei", 4: "Olga"}

def make_base():
    solver = Solver()
    team = [Int(f'team_{i}') for i in range(5)]
    fac = [Bool(f'fac_{i}') for i in range(5)]
    
    for i in range(5):
        solver.add(Or(team[i] == 0, team[i] == 1))
    
    green_count = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
    red_count = Sum([If(team[i] == 1, 1, 0) for i in range(5)])
    solver.add(Or(And(green_count == 2, red_count == 3), And(green_count == 3, red_count == 2)))
    
    fac_green = Sum([If(And(fac[i], team[i] == 0), 1, 0) for i in range(5)])
    fac_red = Sum([If(And(fac[i], team[i] == 1), 1, 0) for i in range(5)])
    solver.add(fac_green == 1)
    solver.add(fac_red == 1)
    
    solver.add(team[0] != team[4])  # Juana != Olga
    solver.add(team[2] == 0)        # Lateefah on green
    solver.add(fac[1] == False)     # Kelly not facilitator
    solver.add(fac[4] == True)      # Olga is facilitator
    
    return solver, team, fac

# Option constraints
opt_a = lambda team, fac: And(fac[2] == True, team[2] == team[1])
opt_b = lambda team, fac: And(fac[3] == True, team[3] == team[1])
opt_c = lambda team, fac: And(fac[4] == True, team[4] == team[3])
opt_d = lambda team, fac: And(fac[2] == True, team[2] != team[0])
opt_e = lambda team, fac: And(fac[3] == True, team[3] != team[4])

must_be_false = []
for letter, constr_fn in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver, team, fac = make_base()
    solver.add(constr_fn(team, fac))
    result = solver.check()
    if result == unsat:
        must_be_false.append(letter)
        print(f"Option {letter}: UNSAT (must be false)")
    elif result == sat:
        print(f"Option {letter}: SAT (can be true)")
    else:
        print(f"Option {letter}: UNKNOWN")

print()
if len(must_be_false) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_false[0]}")
elif len(must_be_false) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-false options {must_be_false}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-false options found")