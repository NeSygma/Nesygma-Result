from z3 import *

# Students: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
names = {0: "Juana", 1: "Kelly", 2: "Lateefah", 3: "Mei", 4: "Olga"}
N = 5

def make_solver():
    solver = Solver()
    team = [Int(f'team_{i}') for i in range(N)]
    fac = [Bool(f'fac_{i}') for i in range(N)]
    
    for i in range(N):
        solver.add(Or(team[i] == 0, team[i] == 1))
    
    green_count = Sum([If(team[i] == 0, 1, 0) for i in range(N)])
    solver.add(Or(green_count == 2, green_count == 3))
    
    green_fac_count = Sum([If(And(team[i] == 0, fac[i]), 1, 0) for i in range(N)])
    red_fac_count = Sum([If(And(team[i] == 1, fac[i]), 1, 0) for i in range(N)])
    solver.add(green_fac_count == 1)
    solver.add(red_fac_count == 1)
    
    # Constraints
    solver.add(team[0] != team[4])  # Juana != Olga
    solver.add(team[2] == 0)        # Lateefah on green
    solver.add(fac[1] == False)      # Kelly not facilitator
    solver.add(fac[4] == True)       # Olga is facilitator
    solver.add(team[3] == 0)         # Mei on green (given condition)
    
    return solver, team, fac

# For "must be true" questions: check if negation of each option is UNSAT
# If negation is UNSAT, the option MUST be true

options = {
    "A": lambda team, fac: team[0] == 0,       # Juana on green
    "B": lambda team, fac: team[1] == 1,        # Kelly on red
    "C": lambda team, fac: team[4] == 0,        # Olga on green
    "D": lambda team, fac: fac[2] == True,      # Lateefah is facilitator
    "E": lambda team, fac: fac[3] == True,      # Mei is facilitator
}

must_be_true = []

for letter, opt_fn in options.items():
    s, team, fac = make_solver()
    # Add negation of the option
    s.add(Not(opt_fn(team, fac)))
    result = s.check()
    if result == unsat:
        must_be_true.append(letter)
        print(f"Option {letter}: MUST be true (negation is UNSAT)")
    else:
        print(f"Option {letter}: NOT necessarily true (negation is SAT)")
        m = s.model()
        for i in range(N):
            print(f"  {names[i]}: team={'Green' if m[team[i]]==0 else 'Red'}, fac={m.evaluate(fac[i])}")

print()
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")