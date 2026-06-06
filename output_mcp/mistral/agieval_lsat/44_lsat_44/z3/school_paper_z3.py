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
# We need to ensure there is exactly one pair with equal bitmasks
# We will enforce that exactly one pair of students have equal bitmasks
# There are C(5,2)=10 possible pairs; we need exactly one pair to be equal

# List of all pairs
pairs = [
    (jiang, kramer), (jiang, lopez), (jiang, megregian), (jiang, o_neill),
    (kramer, lopez), (kramer, megregian), (kramer, o_neill),
    (lopez, megregian), (lopez, o_neill),
    (megregian, o_neill)
]

# We need exactly one pair to be equal
# We will use a counter for the number of equal pairs
# Since Z3 does not have a direct way to count equalities, we will use a trick:
# For each pair, we can assert that either they are equal or not, and count the equal ones
# We will use a sum of boolean conditions to count the number of equal pairs

# Create a list of boolean conditions for each pair being equal
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

# We need exactly one of these to be true
# We can use a sum of boolean conditions to count the number of equal pairs
# Z3's Sum can sum boolean conditions (True=1, False=0)
num_equal_pairs = Sum([If(cond, 1, 0) for cond in pair_equalities])
solver.add(num_equal_pairs == 1)

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