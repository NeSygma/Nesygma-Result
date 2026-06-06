from z3 import *

solver = Solver()

# Declare symbolic variables for each scientist (True if selected, False otherwise)
botanists = [Bool('F'), Bool('G'), Bool('H')]
chemists = [Bool('K'), Bool('L'), Bool('M')]
zoologists = [Bool('P'), Bool('Q'), Bool('R')]

# Base constraints:
# 1. Exactly 5 scientists are selected in total
solver.add(Sum(botanists + chemists + zoologists) == 5)

# 2. At least one scientist of each type must be selected
solver.add(Sum(botanists) >= 1)
solver.add(Sum(chemists) >= 1)
solver.add(Sum(zoologists) >= 1)

# 3. If more than one botanist is selected, then at most one zoologist is selected
solver.add(Implies(Sum(botanists) > 1, Sum(zoologists) <= 1))

# 4. F and K cannot both be selected
solver.add(Not(And(botanists[0], chemists[0])))

# 5. K and M cannot both be selected
solver.add(Not(And(chemists[0], chemists[2])))

# 6. If M is selected, both P and R must be selected
solver.add(Implies(chemists[2], And(zoologists[0], zoologists[2])))

# Condition: Both G and H are selected, and F is NOT selected
condition = And(botanists[1], botanists[2], Not(botanists[0]))

# The panel must include either:
# (A) F or else K
# (B) F or else M
# (C) K or else M
# (D) M or else Q
# (E) P or else Q

found_options = []

# Option A: The panel must include either F or K (or both)
# Since F is not selected (from condition), this reduces to K must be selected.
option_a_constr = And(
    condition,
    chemists[0],  # K must be selected
    Sum(botanists + chemists + zoologists) == 5,
    Sum(botanists) >= 1,
    Sum(chemists) >= 1,
    Sum(zoologists) >= 1,
    Implies(Sum(botanists) > 1, Sum(zoologists) <= 1),
    Not(And(botanists[0], chemists[0])),
    Not(And(chemists[0], chemists[2])),
    Implies(chemists[2], And(zoologists[0], zoologists[2]))
)

# Option B: The panel must include either F or M (or both)
# Since F is not selected (from condition), this reduces to M must be selected.
option_b_constr = And(
    condition,
    chemists[2],  # M must be selected
    Sum(botanists + chemists + zoologists) == 5,
    Sum(botanists) >= 1,
    Sum(chemists) >= 1,
    Sum(zoologists) >= 1,
    Implies(Sum(botanists) > 1, Sum(zoologists) <= 1),
    Not(And(botanists[0], chemists[0])),
    Not(And(chemists[0], chemists[2])),
    Implies(chemists[2], And(zoologists[0], zoologists[2]))
)

# Option C: The panel must include either K or M (or both)
option_c_constr = And(
    condition,
    Or(chemists[0], chemists[2]),  # K or M must be selected
    Sum(botanists + chemists + zoologists) == 5,
    Sum(botanists) >= 1,
    Sum(chemists) >= 1,
    Sum(zoologists) >= 1,
    Implies(Sum(botanists) > 1, Sum(zoologists) <= 1),
    Not(And(botanists[0], chemists[0])),
    Not(And(chemists[0], chemists[2])),
    Implies(chemists[2], And(zoologists[0], zoologists[2]))
)

# Option D: The panel must include either M or Q
option_d_constr = And(
    condition,
    Or(chemists[2], zoologists[1]),  # M or Q must be selected
    Sum(botanists + chemists + zoologists) == 5,
    Sum(botanists) >= 1,
    Sum(chemists) >= 1,
    Sum(zoologists) >= 1,
    Implies(Sum(botanists) > 1, Sum(zoologists) <= 1),
    Not(And(botanists[0], chemists[0])),
    Not(And(chemists[0], chemists[2])),
    Implies(chemists[2], And(zoologists[0], zoologists[2]))
)

# Option E: The panel must include either P or Q
option_e_constr = And(
    condition,
    Or(zoologists[0], zoologists[1]),  # P or Q must be selected
    Sum(botanists + chemists + zoologists) == 5,
    Sum(botanists) >= 1,
    Sum(chemists) >= 1,
    Sum(zoologists) >= 1,
    Implies(Sum(botanists) > 1, Sum(zoologists) <= 1),
    Not(And(botanists[0], chemists[0])),
    Not(And(chemists[0], chemists[2])),
    Implies(chemists[2], And(zoologists[0], zoologists[2]))
)

# Test each option
for letter, constr in [("A", option_a_constr), ("B", option_b_constr), ("C", option_c_constr), ("D", option_d_constr), ("E", option_e_constr)]:
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