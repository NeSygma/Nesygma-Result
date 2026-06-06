from z3 import *

# Days: 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday
# Cookie types: O=oatmeal, P=peanut butter, S=sugar
# Batches: 1, 2, 3

# Declare variables
O1, O2, O3 = Ints('O1 O2 O3')
P1, P2, P3 = Ints('P1 P2 P3')
S1, S2, S3 = Ints('S1 S2 S3')

solver = Solver()

# Domain constraints: all days between 1 and 5
for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]:
    solver.add(var >= 1, var <= 5)

# Constraint 1: No two batches of same kind on same day
solver.add(O1 != O2, O1 != O3, O2 != O3)
solver.add(P1 != P2, P1 != P3, P2 != P3)
solver.add(S1 != S2, S1 != S3, S2 != S3)

# Constraint 2: At least one batch on Monday (day 1)
solver.add(Or([var == 1 for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]]))

# Constraint 3: Second batch of oatmeal on same day as first batch of peanut butter
solver.add(O2 == P1)

# Constraint 4: Second batch of sugar on Thursday (day 4)
solver.add(S2 == 4)

# Additional constraint from question: "one kind of cookie's first batch is made on the same day as another kind of cookie's third batch"
# We need to consider this as a premise. Let's add it as a constraint that must be true.
# We'll create a variable to represent which pair satisfies this, but actually we need to ensure at least one such pair exists.
# Let's add: There exists at least one pair (type1, type2) where type1's first batch = type2's third batch
# We'll model this by adding constraints for each possible pair and using Or
first_batches = [O1, P1, S1]
third_batches = [O3, P3, S3]
# We need at least one equality between a first batch and a third batch (from different types)
# But careful: "one kind of cookie's first batch" and "another kind of cookie's third batch" - different kinds
# So we need: (O1 == P3) OR (O1 == S3) OR (P1 == O3) OR (P1 == S3) OR (S1 == O3) OR (S1 == P3)
solver.add(Or(
    O1 == P3,
    O1 == S3,
    P1 == O3,
    P1 == S3,
    S1 == O3,
    S1 == P3
))

# Now we need to evaluate the answer choices
# The question: "which one of the following could be false?"
# This means: find which statement is NOT necessarily true (i.e., there exists a model where it's false)
# So we need to check for each option: can it be false while all constraints hold?
# If exactly one option can be false (i.e., the others must be true), that's our answer.

# Let's define the options as constraints that would make them true
# We want to see which ones can be false, so we'll check the negation of each option

# Option A: "At least one batch of cookies is made on each of the five days."
# This means: for each day 1-5, at least one batch is on that day
# Negation: There exists at least one day with NO batches
# We'll check if the negation is satisfiable

# Option B: "At least two batches of cookies are made on Wednesday."
# Negation: Fewer than 2 batches on Wednesday (i.e., 0 or 1 batch on Wednesday)

# Option C: "Exactly one batch of cookies is made on Monday."
# Negation: Not exactly one batch on Monday (i.e., 0 or 2+ batches on Monday)

# Option D: "Exactly two batches of cookies are made on Tuesday."
# Negation: Not exactly two batches on Tuesday

# Option E: "Exactly one batch of cookies is made on Friday."
# Negation: Not exactly one batch on Friday

# We'll test each option's negation to see if it's satisfiable
# If an option's negation is satisfiable, then that option could be false

# First, let's check if the base constraints are satisfiable
print("Checking base constraints...")
if solver.check() != sat:
    print("Base constraints unsatisfiable!")
    exit()

# Now test each option's negation
found_options = []  # Options that could be false (i.e., their negation is satisfiable)

# Option A negation: Not (at least one batch on each day)
# i.e., There exists a day with 0 batches
# We'll check each day separately
for day in [1, 2, 3, 4, 5]:
    solver.push()
    # Add constraint that NO batch is on this day
    solver.add(And([var != day for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]]))
    if solver.check() == sat:
        found_options.append("A")
        solver.pop()
        break
    solver.pop()

# Option B negation: Fewer than 2 batches on Wednesday (day 3)
# Count batches on Wednesday: sum of indicators for each batch being on day 3
# We need: count < 2, i.e., count <= 1
# We'll check if count = 0 or count = 1 is possible
solver.push()
# Add constraint: count of batches on Wednesday <= 1
count_wed = Sum([If(var == 3, 1, 0) for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]])
solver.add(count_wed <= 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C negation: Not exactly one batch on Monday
# i.e., count of batches on Monday != 1
# We'll check if count = 0 or count >= 2 is possible
# First check count = 0
solver.push()
count_mon = Sum([If(var == 1, 1, 0) for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]])
solver.add(count_mon == 0)
if solver.check() == sat:
    found_options.append("C")
    solver.pop()
else:
    solver.pop()
    # Check count >= 2
    solver.push()
    solver.add(count_mon >= 2)
    if solver.check() == sat:
        found_options.append("C")
    solver.pop()

# Option D negation: Not exactly two batches on Tuesday
# i.e., count of batches on Tuesday != 2
# Check count = 0, 1, 3, 4, 5, 6, 7, 8, 9
# We'll check if count <= 1 or count >= 3 is possible
solver.push()
count_tue = Sum([If(var == 2, 1, 0) for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]])
solver.add(Or(count_tue <= 1, count_tue >= 3))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E negation: Not exactly one batch on Friday
# i.e., count of batches on Friday != 1
# Check count = 0 or count >= 2
solver.push()
count_fri = Sum([If(var == 5, 1, 0) for var in [O1, O2, O3, P1, P2, P3, S1, S2, S3]])
solver.add(Or(count_fri == 0, count_fri >= 2))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Now determine the answer
print(f"Options that could be false: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")