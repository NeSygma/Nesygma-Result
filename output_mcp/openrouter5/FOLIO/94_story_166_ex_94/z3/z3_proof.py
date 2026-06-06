from z3 import *

# We'll model this as a theorem-proving task.
# Define sorts/domains
# ManagedBuilding, Pet, Person, etc.

# Let's use symbolic booleans and integers.

# Premises:

# 1. Pets are allowed in some managed buildings.
# "Some" means there exists at least one managed building where pets are allowed.
# We'll model this as: exists b: ManagedBuilding(b) and AllowsPets(b)
# But we don't have a domain of buildings enumerated. Let's use a simpler approach:
# We'll create a boolean variable for "pets_allowed_in_some_managed" = True
# Actually, we need to be more precise. Let's use a function.

# Let's define:
# ManagedBuilding(b) - b is a managed building
# AllowsPets(b) - building b allows pets
# Deposit(b) - security deposit amount at building b
# Rent(b) - monthly rent at building b
# PetOwner(p, pet) - person p owns pet pet
# IsCat(pet) - pet is a cat
# IsPet(pet) - pet is a pet
# CanMoveIn(person, building, pet) - person can move into building with pet

# But to keep it simple and solvable, let's use propositional/quantifier-free approach.

# Let's define specific individuals:
# Tom, Fluffy, OliveGarden

# Booleans:
Tom_rents_OliveGarden = Bool('Tom_rents_OliveGarden')
OliveGarden_allows_pets = Bool('OliveGarden_allows_pets')
OliveGarden_is_managed = Bool('OliveGarden_is_managed')
Fluffy_is_cat = Bool('Fluffy_is_cat')
Fluffy_is_pet = Bool('Fluffy_is_pet')
Tom_owns_Fluffy = Bool('Tom_owns_Fluffy')
Deposit_OliveGarden = Int('Deposit_OliveGarden')
Rent_OliveGarden = Int('Rent_OliveGarden')
Deposit_no_more_than_1500 = Bool('Deposit_no_more_than_1500')
Allowed_move_in_with_pet = Bool('Allowed_move_in_with_pet')
Tom_allowed_move_in_Fluffy_OliveGarden = Bool('Tom_allowed_move_in_Fluffy_OliveGarden')

solver = Solver()

# Premise: Pets are allowed in some managed buildings.
# This means there exists at least one managed building that allows pets.
# Since we only know about Olive Garden as a managed building, this premise
# doesn't force Olive Garden to allow pets. It just says "some" (at least one).
# We'll encode this as: there exists some building b such that Managed(b) and AllowsPets(b).
# Since we don't have other buildings, we can't force Olive Garden to allow pets.
# But we can say: IF Olive Garden is the only managed building, then it must allow pets.
# However, the premise says "some" not "all". So we can't conclude Olive Garden allows pets.
# Let's just note this premise but not add a constraint that forces Olive Garden to allow pets.

# Premise: A deposit is required to rent an apartment in a managed building.
# So if a building is managed, there is a deposit.
# Deposit_OliveGarden >= 0 (exists)
solver.add(Implies(OliveGarden_is_managed, Deposit_OliveGarden >= 0))

# Premise: The security deposit can be either equal to the monthly rent at a managed building or more.
# So for any managed building: Deposit >= Rent
solver.add(Implies(OliveGarden_is_managed, Deposit_OliveGarden >= Rent_OliveGarden))

# Premise: Fluffy is Tom's cat.
solver.add(Tom_owns_Fluffy)
solver.add(Fluffy_is_cat)

# Premise: Cats are pets.
solver.add(Implies(Fluffy_is_cat, Fluffy_is_pet))

# Premise: The Olive Garden is a managed building.
solver.add(OliveGarden_is_managed)

# Premise: The monthly rent at the Olive Garden is $2000.
solver.add(Rent_OliveGarden == 2000)

# Premise: $2000 is more than $1500.
# (This is a factual statement, always true)
solver.add(2000 > 1500)

# Premise: Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy,
# and the security deposit is no more than $1500.
# Tom_will_rent <=> (Allowed_move_in_with_Fluffy AND Deposit <= 1500)
# Actually: "Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy,
# and the security deposit is no more than $1500."
# This means: IF (allowed to move in with Fluffy AND deposit <= 1500) THEN Tom will rent.
solver.add(Implies(And(Allowed_move_in_with_pet, Deposit_OliveGarden <= 1500), Tom_rents_OliveGarden))

# Premise: If a managed building allows pets, then people are allowed to move in with a pet.
# For Olive Garden specifically:
solver.add(Implies(OliveGarden_allows_pets, Allowed_move_in_with_pet))

# Now, the conclusion to evaluate: Tom is allowed to move into an apartment in The Olive Garden with Fluffy.
# This is: Allowed_move_in_with_pet (since Fluffy is a pet and Tom owns Fluffy)

# Let's check if the conclusion is provable from premises.

# First, let's check what we know about Olive Garden allowing pets.
# Premise 1 says "Pets are allowed in some managed buildings."
# This is an existential statement. It doesn't tell us Olive Garden allows pets.
# So we cannot conclude Olive Garden allows pets.

# Let's do theorem proving.

# Goal: Tom is allowed to move into an apartment in The Olive Garden with Fluffy.
goal = Allowed_move_in_with_pet

# Check negated goal
s_neg = Solver()
s_neg.add(OliveGarden_is_managed)
s_neg.add(Deposit_OliveGarden >= 0)
s_neg.add(Deposit_OliveGarden >= Rent_OliveGarden)
s_neg.add(Tom_owns_Fluffy)
s_neg.add(Fluffy_is_cat)
s_neg.add(Implies(Fluffy_is_cat, Fluffy_is_pet))
s_neg.add(Rent_OliveGarden == 2000)
s_neg.add(2000 > 1500)
s_neg.add(Implies(And(Allowed_move_in_with_pet, Deposit_OliveGarden <= 1500), Tom_rents_OliveGarden))
s_neg.add(Implies(OliveGarden_allows_pets, Allowed_move_in_with_pet))
# Also, we need to add that Fluffy is a pet (since Fluffy is a cat and cats are pets)
s_neg.add(Fluffy_is_pet)
# Negated goal
s_neg.add(Not(goal))

neg_res = s_neg.check()

# Check positive goal
s_pos = Solver()
s_pos.add(OliveGarden_is_managed)
s_pos.add(Deposit_OliveGarden >= 0)
s_pos.add(Deposit_OliveGarden >= Rent_OliveGarden)
s_pos.add(Tom_owns_Fluffy)
s_pos.add(Fluffy_is_cat)
s_pos.add(Implies(Fluffy_is_cat, Fluffy_is_pet))
s_pos.add(Rent_OliveGarden == 2000)
s_pos.add(2000 > 1500)
s_pos.add(Implies(And(Allowed_move_in_with_pet, Deposit_OliveGarden <= 1500), Tom_rents_OliveGarden))
s_pos.add(Implies(OliveGarden_allows_pets, Allowed_move_in_with_pet))
s_pos.add(Fluffy_is_pet)
s_pos.add(goal)

pos_res = s_pos.check()

print(f"Negated goal result: {neg_res}")
print(f"Positive goal result: {pos_res}")

if neg_res == unsat and pos_res == sat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif neg_res == sat and pos_res == unsat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif neg_res == sat and pos_res == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
elif neg_res == unsat and pos_res == unsat:
    print("STATUS: unknown")
    print("CONCLUSION: Inconsistent")
else:
    print("STATUS: unknown")