from z3 import *

# BENCHMARK_MODE: ON (for model-finding)
BENCHMARK_MODE = True

# Declare symbolic variables for each sales representative's zone assignment
# 1 = Zone 1, 2 = Zone 2, 3 = Zone 3
kim = Int('kim')
mahr = Int('mahr')
parra = Int('parra')
quinn = Int('quinn')
stuckey = Int('stuckey')
tiao = Int('tiao')
udall = Int('udall')

# Create solver
solver = Solver()

# Each representative works in exactly one zone (1, 2, or 3)
solver.add(kim >= 1, kim <= 3)
solver.add(mahr >= 1, mahr <= 3)
solver.add(parra >= 1, parra <= 3)
solver.add(quinn >= 1, quinn <= 3)
solver.add(stuckey >= 1, stuckey <= 3)
solver.add(tiao >= 1, tiao <= 3)
solver.add(udall >= 1, udall <= 3)

# Constraint 1: Either Parra or Tiao (but not both) works in Zone 1
solver.add(Or(And(parra == 1, tiao != 1), And(tiao == 1, parra != 1)))

# Constraint 2: Either Tiao or Udall (but not both) works in Zone 2
solver.add(Or(And(tiao == 2, udall != 2), And(udall == 2, tiao != 2)))

# Constraint 3: Parra and Quinn work in the same sales zone
solver.add(parra == quinn)

# Constraint 4: Stuckey and Udall work in the same sales zone
solver.add(stuckey == udall)

# Constraint 5: There are more representatives in Zone 3 than in Zone 2
# Count the number of representatives in Zone 2 and Zone 3
zone2_count = Sum([If(v == 2, 1, 0) for v in [kim, mahr, parra, quinn, stuckey, tiao, udall]])
zone3_count = Sum([If(v == 3, 1, 0) for v in [kim, mahr, parra, quinn, stuckey, tiao, udall]])
solver.add(zone3_count > zone2_count)

# Base constraints are set. Now evaluate each option for Zone 3.

# Option A: Kim, Mahr in Zone 3 (complete and accurate list)
# So, Parra, Quinn, Stuckey, Tiao, Udall must NOT be in Zone 3
opt_a_constr = And(
    kim == 3,
    mahr == 3,
    parra != 3,
    quinn != 3,
    stuckey != 3,
    tiao != 3,
    udall != 3
)

# Option B: Kim, Tiao in Zone 3 (complete and accurate list)
# So, Mahr, Parra, Quinn, Stuckey, Udall must NOT be in Zone 3
opt_b_constr = And(
    kim == 3,
    tiao == 3,
    mahr != 3,
    parra != 3,
    quinn != 3,
    stuckey != 3,
    udall != 3
)

# Option C: Parra, Quinn in Zone 3 (complete and accurate list)
# So, Kim, Mahr, Stuckey, Tiao, Udall must NOT be in Zone 3
opt_c_constr = And(
    parra == 3,
    quinn == 3,
    kim != 3,
    mahr != 3,
    stuckey != 3,
    tiao != 3,
    udall != 3
)

# Option D: Stuckey, Tiao, Udall in Zone 3 (complete and accurate list)
# So, Kim, Mahr, Parra, Quinn must NOT be in Zone 3
opt_d_constr = And(
    stuckey == 3,
    tiao == 3,
    udall == 3,
    kim != 3,
    mahr != 3,
    parra != 3,
    quinn != 3
)

# Option E: Parra, Quinn, Stuckey, Udall in Zone 3 (complete and accurate list)
# So, Kim, Mahr, Tiao must NOT be in Zone 3
opt_e_constr = And(
    parra == 3,
    quinn == 3,
    stuckey == 3,
    udall == 3,
    kim != 3,
    mahr != 3,
    tiao != 3
)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        model = solver.model()
        print(f"Option {letter} is SAT with model:")
        print(f"kim = {model[kim]}, mahr = {model[mahr]}, parra = {model[parra]}, quinn = {model[quinn]}, stuckey = {model[stuckey]}, tiao = {model[tiao]}, udall = {model[udall]}")
        print(f"Zone 2 count: {model.eval(zone2_count)}, Zone 3 count: {model.eval(zone3_count)}")
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