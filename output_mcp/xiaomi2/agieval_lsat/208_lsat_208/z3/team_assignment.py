from z3 import *

# Students: Juana(0), Kelly(1), Lateefah(2), Mei(3), Olga(4)
names = ["Juana", "Kelly", "Lateefah", "Mei", "Olga"]
N = 5

# team[i] = True means Green, False means Red
# fac[i] = True means student i is a facilitator

solver = Solver()

# Base constraints (always apply)
# Constraint 1: Juana and Olga on different teams
# Constraint 2: Lateefah on green team
# Constraint 3: Kelly is not a facilitator
# Constraint 4: Olga is a facilitator
# Constraint 5: One team has 2, other has 3 members
# Constraint 6: Exactly one facilitator per team

# We'll encode each option explicitly and check it

def make_option_constraints(opt_team, opt_fac):
    """Given team assignments and facilitator assignments for an option,
    return constraints that encode exactly those assignments plus all base constraints."""
    constraints = []
    
    # Encode the specific team and facilitator assignments
    for i in range(N):
        constraints.append(team[i] == opt_team[i])
        constraints.append(fac[i] == opt_fac[i])
    
    return constraints

# Define variables
team = [Bool(f'team_{names[i]}') for i in range(N)]  # True=Green, False=Red
fac = [Bool(f'fac_{names[i]}') for i in range(N)]     # True=facilitator

# Option A: green: Juana, Lateefah, Olga(fac); red: Kelly, Mei(fac)
opt_a_team = [True, False, True, False, True]   # J=G, K=R, L=G, M=R, O=G
opt_a_fac  = [False, False, False, True, True]   # M=fac, O=fac

# Option B: green: Kelly, Lateefah(fac), Olga; red: Juana, Mei(fac)
opt_b_team = [False, True, True, False, True]   # J=R, K=G, L=G, M=R, O=G
opt_b_fac  = [False, False, True, True, False]   # L=fac, M=fac

# Option C: green: Kelly, Lateefah, Olga(fac); red: Juana(fac), Mei
opt_c_team = [False, True, True, False, True]   # J=R, K=G, L=G, M=R, O=G
opt_c_fac  = [True, False, False, False, True]   # J=fac, O=fac

# Option D: green: Kelly, Mei, Olga(fac); red: Juana(fac), Lateefah
opt_d_team = [False, True, False, True, True]   # J=R, K=G, L=R, M=G, O=G
opt_d_fac  = [True, False, False, False, True]   # J=fac, O=fac

# Option E: green: Lateefah, Olga(fac); red: Juana, Kelly(fac), Mei
opt_e_team = [False, False, True, False, True]   # J=R, K=R, L=G, M=R, O=G
opt_e_fac  = [False, True, False, False, True]   # K=fac, O=fac

options = [
    ("A", opt_a_team, opt_a_fac),
    ("B", opt_b_team, opt_b_fac),
    ("C", opt_c_team, opt_c_fac),
    ("D", opt_d_team, opt_d_fac),
    ("E", opt_e_team, opt_e_fac),
]

found_options = []

for letter, opt_team, opt_fac in options:
    solver.push()
    
    # Add the option's specific assignments
    for i in range(N):
        solver.add(team[i] == opt_team[i])
        solver.add(fac[i] == opt_fac[i])
    
    # Base constraint 1: Juana and Olga on different teams
    solver.add(team[0] != team[4])
    
    # Base constraint 2: Lateefah on green team
    solver.add(team[2] == True)
    
    # Base constraint 3: Kelly is not a facilitator
    solver.add(fac[1] == False)
    
    # Base constraint 4: Olga is a facilitator
    solver.add(fac[4] == True)
    
    # Base constraint 5: One team has 2 members, other has 3
    green_count = Sum([If(team[i], 1, 0) for i in range(N)])
    solver.add(Or(green_count == 2, green_count == 3))
    
    # Base constraint 6: Exactly one facilitator per team
    green_fac_count = Sum([If(And(team[i], fac[i]), 1, 0) for i in range(N)])
    red_fac_count = Sum([If(And(Not(team[i]), fac[i]), 1, 0) for i in range(N)])
    solver.add(green_fac_count == 1)
    solver.add(red_fac_count == 1)
    
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter}: SAT")
        for i in range(N):
            t = "Green" if is_true(m[team[i]]) else "Red"
            f = " (facilitator)" if is_true(m[fac[i]]) else ""
            print(f"  {names[i]}: {t}{f}")
    else:
        print(f"Option {letter}: UNSAT")
    
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