from z3 import *

# Seven positions 1..7
optom = Int('optom')
pharm = Int('pharm')
rest1 = Int('rest1')
rest2 = Int('rest2')
shoe = Int('shoe')
toy = Int('toy')
vet = Int('vet')
all_vars = [optom, pharm, rest1, rest2, shoe, toy, vet]

# Base constraints
solver = Solver()
for v in all_vars:
    solver.add(v >= 1, v <= 7)
solver.add(Distinct(all_vars))

# C1: Pharmacy at one end, one restaurant at the other
solver.add(Or(
    And(pharm == 1, Or(rest1 == 7, rest2 == 7)),
    And(pharm == 7, Or(rest1 == 1, rest2 == 1))
))

# C2: Two restaurants separated by at least 2 other businesses
solver.add(Or(rest1 - rest2 >= 3, rest2 - rest1 >= 3))

# C3: Pharmacy next to optometrist or veterinarian
solver.add(Or(
    Or(pharm - optom == 1, optom - pharm == 1),
    Or(pharm - vet == 1, vet - pharm == 1)
))

# C4: Toy store not next to veterinarian
solver.add(Not(Or(toy - vet == 1, vet - toy == 1)))

# Additional: optometrist is next to shoe store
solver.add(Or(optom - shoe == 1, shoe - optom == 1))

# The O-S pair. Let left_pos = min(pos(O), pos(S)), right_pos = max(pos(O), pos(S))
# The flanking businesses are at left_pos-1 and right_pos+1.
# They must exist (pair not at edges).
left_os = If(optom < shoe, optom, shoe)
right_os = If(optom < shoe, shoe, optom)

left_flank_pos = left_os - 1
right_flank_pos = right_os + 1

solver.add(left_os > 1)  # left flank exists
solver.add(right_os < 7)  # right flank exists

# Now define each answer choice as a constraint about what the two flanking businesses are.
# A business is "at position p" means one of the 7 variables equals p.

def at_position(p, var):
    return var == p

# Option A: pharmacy and a restaurant
# One flank is pharmacy, the other is either rest1 or rest2
opt_A = Or(
    # pharmacy at left_flank, restaurant at right_flank
    And(pharm == left_flank_pos, Or(rest1 == right_flank_pos, rest2 == right_flank_pos)),
    # pharmacy at right_flank, restaurant at left_flank
    And(pharm == right_flank_pos, Or(rest1 == left_flank_pos, rest2 == left_flank_pos))
)

# Option B: pharmacy and the toy store
opt_B = Or(
    And(pharm == left_flank_pos, toy == right_flank_pos),
    And(pharm == right_flank_pos, toy == left_flank_pos)
)

# Option C: the two restaurants
opt_C = Or(
    And(rest1 == left_flank_pos, rest2 == right_flank_pos),
    And(rest1 == right_flank_pos, rest2 == left_flank_pos)
)

# Option D: a restaurant and the toy store
opt_D = Or(
    And(Or(rest1 == left_flank_pos, rest2 == left_flank_pos), toy == right_flank_pos),
    And(Or(rest1 == right_flank_pos, rest2 == right_flank_pos), toy == left_flank_pos)
)

# Option E: a restaurant and the veterinarian
opt_E = Or(
    And(Or(rest1 == left_flank_pos, rest2 == left_flank_pos), vet == right_flank_pos),
    And(Or(rest1 == right_flank_pos, rest2 == right_flank_pos), vet == left_flank_pos)
)

# Now test each option using the LSAT skeleton
found_options = []
for letter, constr in [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]:
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