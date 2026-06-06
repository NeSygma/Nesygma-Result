from z3 import *

# Declare symbolic variables for each sales representative's zone
# We represent zones as integers: 1, 2, 3
kim, mahr, parra, quinn, stuckey, tiao, udall = Ints('kim mahr parra quinn stuckey tiao udall')

# Base constraints
solver = Solver()

# Each representative is assigned to exactly one zone
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

# Constraint 3: Parra and Quinn work in the same zone
solver.add(parra == quinn)

# Constraint 4: Stuckey and Udall work in the same zone
solver.add(stuckey == udall)

# Constraint 5: More representatives in Zone 3 than in Zone 2
# We will count the number of representatives in each zone and enforce this constraint

# Define the options as constraints
# Option A: Zone 1: Kim, Parra; Zone 2: Stuckey, Udall; Zone 3: Mahr, Quinn, Tiao
opt_a_constr = And(
    kim == 1,
    parra == 1,
    stuckey == 2,
    udall == 2,
    mahr == 3,
    quinn == 3,
    tiao == 3,
    # Ensure no other assignments (since each rep is assigned to exactly one zone)
    mahr != 1, mahr != 2,
    quinn != 1, quinn != 2,
    tiao != 1, tiao != 2,
)

# Option B: Zone 1: Kim, Tiao; Zone 2: Stuckey, Udall; Zone 3: Mahr, Parra, Quinn
opt_b_constr = And(
    kim == 1,
    tiao == 1,
    stuckey == 2,
    udall == 2,
    mahr == 3,
    parra == 3,
    quinn == 3,
    # Ensure no other assignments
    mahr != 1, mahr != 2,
    parra != 1, parra != 2,
    quinn != 1, quinn != 2,
)

# Option C: Zone 1: Parra, Quinn; Zone 2: Kim, Udall; Zone 3: Mahr, Stuckey, Tiao
opt_c_constr = And(
    parra == 1,
    quinn == 1,
    kim == 2,
    udall == 2,
    mahr == 3,
    stuckey == 3,
    tiao == 3,
    # Ensure no other assignments
    mahr != 1, mahr != 2,
    stuckey != 1, stuckey != 2,
    tiao != 1, tiao != 2,
)

# Option D: Zone 1: Stuckey, Udall; Zone 2: Kim, Tiao; Zone 3: Mahr, Parra, Quinn
opt_d_constr = And(
    stuckey == 1,
    udall == 1,
    kim == 2,
    tiao == 2,
    mahr == 3,
    parra == 3,
    quinn == 3,
    # Ensure no other assignments
    mahr != 1, mahr != 2,
    parra != 1, parra != 2,
    quinn != 1, quinn != 2,
)

# Option E: Zone 1: Tiao; Zone 2: Kim, Parra, Quinn; Zone 3: Stuckey, Udall
opt_e_constr = And(
    tiao == 1,
    kim == 2,
    parra == 2,
    quinn == 2,
    stuckey == 3,
    udall == 3,
    # Ensure no other assignments
    mahr != 1, mahr != 2,
    mahr == 3,  # Mahr must be in Zone 3
)

# Now, evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    # Check if the option satisfies all base constraints
    result = solver.check()
    if result == sat:
        # Verify the "more in Zone 3 than Zone 2" constraint for this option
        model = solver.model()
        zone_counts = {1: 0, 2: 0, 3: 0}
        for rep in [kim, mahr, parra, quinn, stuckey, tiao, udall]:
            zone = model[rep].as_long()
            zone_counts[zone] += 1
        if zone_counts[3] > zone_counts[2]:
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