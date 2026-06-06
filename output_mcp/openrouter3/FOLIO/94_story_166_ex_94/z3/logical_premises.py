from z3 import *

# Create solver
solver = Solver()

# Define entities and properties
# Buildings
Olive_Garden = Int('Olive_Garden')  # 1 for Olive Garden, 0 for others
# Pets
Fluffy = Int('Fluffy')  # 1 for Fluffy, 0 for others
# People
Tom = Int('Tom')  # 1 for Tom, 0 for others

# Properties as Boolean variables
is_managed = Bool('is_managed')  # True if building is managed
allows_pets = Bool('allows_pets')  # True if building allows pets
requires_deposit = Bool('requires_deposit')  # True if deposit required
deposit_equal_or_more = Bool('deposit_equal_or_more')  # True if deposit >= rent
is_cat = Bool('is_cat')  # True if Fluffy is a cat
is_pet = Bool('is_pet')  # True if Fluffy is a pet
rent_amount = Int('rent_amount')  # Monthly rent amount
deposit_amount = Int('deposit_amount')  # Security deposit amount
can_move_in = Bool('can_move_in')  # True if Tom can move in with Fluffy

# Premise 1: Pets are allowed in some managed buildings
# This means there exists at least one managed building that allows pets
# We'll model this as: Olive Garden is managed AND allows pets
solver.add(is_managed)  # Olive Garden is managed (from premise 6)
solver.add(allows_pets)  # Olive Garden allows pets (from premise 1 and 7)

# Premise 2: A deposit is required to rent an apartment in a managed building
solver.add(Implies(is_managed, requires_deposit))

# Premise 3: The security deposit can be either equal to the monthly rent at a managed building or more
# This means deposit >= rent for managed buildings
solver.add(Implies(is_managed, deposit_equal_or_more))

# Premise 4: Fluffy is Tom's cat
# We'll model this as: Fluffy is a cat
solver.add(is_cat)

# Premise 5: Cats are pets
solver.add(Implies(is_cat, is_pet))

# Premise 6: The Olive Garden is a managed building
solver.add(is_managed)

# Premise 7: The monthly rent at the Olive Garden is $2000
solver.add(rent_amount == 2000)

# Premise 8: $2000 is more than $1500
# This is a fact, not a constraint to add

# Premise 9: Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, 
# and the security deposit is no more than $1500
# This means: can_move_in AND deposit <= 1500 → Tom rents
# We'll model the condition for Tom to rent
tom_rents = Bool('tom_rents')
solver.add(Implies(And(can_move_in, deposit_amount <= 1500), tom_rents))

# Premise 10: If a managed building allows pets, then people are allowed to move in with a pet
solver.add(Implies(And(is_managed, allows_pets), can_move_in))

# Additional constraints from premises
# From premise 3: deposit >= rent for managed buildings
solver.add(Implies(is_managed, deposit_amount >= rent_amount))

# From premise 2: deposit required for managed buildings
solver.add(Implies(is_managed, deposit_amount > 0))

# From premise 7: rent is 2000
solver.add(rent_amount == 2000)

# From premise 3 and 7: deposit >= 2000 for Olive Garden
solver.add(Implies(is_managed, deposit_amount >= 2000))

# Now check the conclusion: Tom is allowed to move into an apartment in The Olive Garden with Fluffy
# This means can_move_in should be True for Olive Garden
# From premise 10: If Olive Garden allows pets (which it does), then can_move_in is True
# So the conclusion should be True

# Let's check if can_move_in is forced to be True
solver.push()
solver.add(Not(can_move_in))  # Try to find a model where Tom cannot move in
result_neg = solver.check()
solver.pop()

# Check if can_move_in is forced to be False
solver.push()
solver.add(can_move_in)  # Try to find a model where Tom can move in
result_pos = solver.check()
solver.pop()

# Print results
print("Checking conclusion: Tom is allowed to move into an apartment in The Olive Garden with Fluffy")
print(f"Result when assuming Tom CANNOT move in: {result_neg}")
print(f"Result when assuming Tom CAN move in: {result_pos}")

if result_neg == unsat and result_pos == sat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif result_neg == sat and result_pos == unsat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif result_neg == sat and result_pos == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
elif result_neg == unsat and result_pos == unsat:
    print("STATUS: unknown")
    print("CONCLUSION: Inconsistent premises")
else:
    print("STATUS: unknown")
    print("CONCLUSION: Cannot determine")