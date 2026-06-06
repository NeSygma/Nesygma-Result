from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each student's play bitmask as BitVec to allow bitwise operations
# Plays: Sunset=1 (0b001), Tamerlane=2 (0b010), Undulation=4 (0b100)
jiang = BitVec('jiang', 3)
kramer = BitVec('kramer', 3)
lopez = BitVec('lopez', 3)
megregian = BitVec('megregian', 3)
o_neill = BitVec('o_neill', 3)

# Helper function to count the number of plays reviewed (popcount) for BitVec
# This function uses bitwise operations to count the number of 1s in the 3-bit bitmask
def popcount(x):
    return (x & 1) + ((x >> 1) & 1) + ((x >> 2) & 1)

solver = Solver()

# Each student reviews at least one play
solver.add(popcount(jiang) >= 1)
solver.add(popcount(kramer) >= 1)
solver.add(popcount(lopez) >= 1)
solver.add(popcount(megregian) >= 1)
solver.add(popcount(o_neill) >= 1)

# Kramer and Lopez each review fewer plays than Megregian
solver.add(popcount(kramer) < popcount(megregian))
solver.add(popcount(lopez) < popcount(megregian))

# Neither Lopez nor Megregian reviews any play Jiang reviews
# This means the bitwise AND of Jiang's bitmask and Lopez's bitmask should be 0
solver.add(jiang & lopez == 0)
solver.add(jiang & megregian == 0)

# Kramer and O'Neill both review Tamerlane (bitmask 2, i.e., 0b010)
solver.add(kramer & 2 == 2)
solver.add(o_neill & 2 == 2)

# Exactly two students review the same set of plays
# We need to ensure there is exactly one pair with equal bitmasks and all others are distinct
# List of all pairs
pairs = [
    (jiang, kramer), (jiang, lopez), (jiang, megregian), (jiang, o_neill),
    (kramer, lopez), (kramer, megregian), (kramer, o_neill),
    (lopez, megregian), (lopez, o_neill),
    (megregian, o_neill)
]

# We need exactly one pair to be equal and all others to be unequal
# We will enforce this by:
# 1. For each pair, create a boolean condition for equality
# 2. Ensure exactly one of these conditions is true
# 3. Ensure all other pairs are not equal

pair_equalities = [
    (jiang == kramer),
    (jiang == lopez),
    (jiang == megregian),
    (jiang == o_neill),
    (kramer == lopez),
    (kramer == megregian),
    (kramer == o_neill),
    (lopez == megregian),
    (lopez == o_neill),
    (megregian == o_neill)
]

# Exactly one pair is equal
num_equal_pairs = Sum([If(cond, 1, 0) for cond in pair_equalities])
solver.add(num_equal_pairs == 1)

# All other pairs must not be equal
for i in range(len(pairs)):
    for j in range(i + 1, len(pairs)):
        # This is a bit tricky: we want to ensure that if pair i is the equal one, all others are not equal
        # Instead, we can enforce that for all pairs except the one that is equal, they are not equal
        # To do this, we can use the fact that exactly one pair is equal, so all others must be unequal
        pass

# Instead, we can enforce that for all pairs, if they are not the equal pair, they are not equal
# We can do this by iterating over all pairs and adding a constraint that they are not equal
# unless they are the one pair that is equal. But since we don't know which pair is equal in advance,
# we can instead enforce that all pairs are not equal, and then relax the constraint for the one pair that is equal.
# However, this is not straightforward in Z3.

# Alternative approach: For each pair, assume it is the equal pair and ensure all others are not equal
# This is computationally expensive but ensures correctness for this small problem.

# We will instead enforce that all pairs are not equal, and then use the fact that exactly one pair is equal
# to ensure that the rest are not equal. This is already enforced by the num_equal_pairs == 1 constraint.

# Now, evaluate each multiple-choice option
found_options = []

# Option A: Jiang reviews more of the plays than Lopez does
solver.push()
solver.add(popcount(jiang) > popcount(lopez))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Megregian reviews more of the plays than Jiang does
solver.push()
solver.add(popcount(megregian) > popcount(jiang))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Megregian reviews more of the plays than O'Neill does
solver.push()
solver.add(popcount(megregian) > popcount(o_neill))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: O'Neill reviews more of the plays than Jiang does
solver.push()
solver.add(popcount(o_neill) > popcount(jiang))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: O'Neill reviews more of the plays than Kramer does
solver.push()
solver.add(popcount(o_neill) > popcount(kramer))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")