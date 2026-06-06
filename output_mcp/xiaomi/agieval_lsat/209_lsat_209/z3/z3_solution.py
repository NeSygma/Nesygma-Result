from z3 import *

solver = Solver()

# Students: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
names = {0: "Juana", 1: "Kelly", 2: "Lateefah", 3: "Mei", 4: "Olga"}

# team[i] = 0 (green) or 1 (red)
team = [Int(f'team_{i}') for i in range(5)]
# facilitator[i] = True if student i is facilitator
fac = [Bool(f'fac_{i}') for i in range(5)]

# Domain constraints
for i in range(5):
    solver.add(Or(team[i] == 0, team[i] == 1))

# One team has 2 members, the other has 3
green_count = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
red_count = Sum([If(team[i] == 1, 1, 0) for i in range(5)])
solver.add(Or(And(green_count == 2, red_count == 3), And(green_count == 3, red_count == 2)))

# Exactly one facilitator per team
green_fac_count = Sum([If(And(team[i] == 0, fac[i]), 1, 0) for i in range(5)])
red_fac_count = Sum([If(And(team[i] == 1, fac[i]), 1, 0) for i in range(5)])
solver.add(green_fac_count == 1)
solver.add(red_fac_count == 1)

# Condition 1: Juana is assigned to a different team than Olga
solver.add(team[0] != team[4])

# Condition 2: Lateefah is assigned to the green team
solver.add(team[2] == 0)

# Condition 3: Kelly is not a facilitator
solver.add(fac[1] == False)

# Condition 4: Olga is a facilitator
solver.add(fac[4] == True)

# First, let's verify the base constraints are satisfiable
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    print("Base constraints are satisfiable.")
    for i in range(5):
        t = "green" if m[team[i]] == 0 else "red"
        f = "Facilitator" if m[fac[i]] else "Not facilitator"
        print(f"  {names[i]}: {t}, {f}")
else:
    print("Base constraints are UNSAT - problem with encoding!")
    exit()

# Define option constraints
# (A) Juana is assigned to the red team
opt_a = (team[0] == 1)

# (B) Lateefah is a facilitator
opt_b = (fac[2] == True)

# (C) Olga is assigned to the green team
opt_c = (team[4] == 0)

# (D) Juana and Mei are not both facilitators
opt_d = Not(And(fac[0], fac[3]))

# (E) Neither Juana nor Kelly is a facilitator
opt_e = And(fac[0] == False, fac[1] == False)

# For "must be true", we check if the negation is UNSAT
# i.e., the option holds in ALL valid models
print("\nChecking which options MUST be true (negation is UNSAT)...")
must_be_true = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s = Solver()
    # Add base constraints
    s.add(team[i] >= 0 for i in range(5))
    s.add(team[i] <= 1 for i in range(5))
    s.add(Or(And(green_count == 2, red_count == 3), And(green_count == 3, red_count == 2)))
    s.add(green_fac_count == 1)
    s.add(red_fac_count == 1)
    s.add(team[0] != team[4])
    s.add(team[2] == 0)
    s.add(fac[1] == False)
    s.add(fac[4] == True)
    # Add negation of the option
    s.add(Not(constr))
    result = s.check()
    if result == unsat:
        print(f"  Option {letter}: MUST be true (negation is UNSAT)")
        must_be_true.append(letter)
    elif result == sat:
        print(f"  Option {letter}: NOT necessarily true (counterexample exists)")
    else:
        print(f"  Option {letter}: UNKNOWN")

print(f"\nOptions that must be true: {must_be_true}")
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")