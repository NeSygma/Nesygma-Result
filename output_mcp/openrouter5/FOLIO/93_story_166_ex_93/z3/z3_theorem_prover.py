from z3 import *

# Theorem Proving / Validity Checking pattern

# Define sorts/constants
ManagedBuilding = Bool('ManagedBuilding')
PetsAllowed = Bool('PetsAllowed')
DepositRequired = Bool('DepositRequired')
DepositEqRent = Bool('DepositEqRent')
DepositMoreThanRent = Bool('DepositMoreThanRent')
SecurityDepositNoMoreThan1500 = Bool('SecurityDepositNoMoreThan1500')
MonthlyRent2000 = Bool('MonthlyRent2000')
TomRents = Bool('TomRents')
TomAllowedMoveInWithFluffy = Bool('TomAllowedMoveInWithFluffy')
FluffyIsCat = Bool('FluffyIsCat')
CatIsPet = Bool('CatIsPet')
OliveGardenManaged = Bool('OliveGardenManaged')
OliveGardenRent2000 = Bool('OliveGardenRent2000')
PetsAllowedInManaged = Bool('PetsAllowedInManaged')
MoveInWithPetAllowed = Bool('MoveInWithPetAllowed')

# Premises
premises = [
    # Pets are allowed in some managed buildings.
    # "Some" means there exists at least one managed building where pets are allowed.
    # We'll encode this as: If a building is managed, it's possible pets are allowed.
    # More precisely: There exists a managed building where pets are allowed.
    # But since we're reasoning about The Olive Garden specifically, we need to be careful.
    # Let's encode: If a building is managed and allows pets, then pets are allowed there.
    # Actually, "Pets are allowed in some managed buildings" = There exists a managed building B such that pets are allowed in B.
    # This doesn't tell us anything about The Olive Garden specifically.
    
    # A deposit is required to rent an apartment in a managed building.
    # If a building is managed, then a deposit is required.
    Implies(ManagedBuilding, DepositRequired),
    
    # The security deposit can be either equal to the monthly rent at a managed building or more.
    # If a building is managed, then deposit = rent OR deposit > rent
    Implies(ManagedBuilding, Or(DepositEqRent, DepositMoreThanRent)),
    
    # Fluffy is Tom's cat.
    # Fluffy is a cat.
    FluffyIsCat,
    
    # Cats are pets.
    Implies(FluffyIsCat, CatIsPet),
    
    # The Olive Garden is a managed building.
    OliveGardenManaged,
    
    # The monthly rent at the Olive Garden is $2000.
    OliveGardenRent2000,
    
    # $2000 is more than $1500.
    # This is a fact about numbers.
    
    # Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, 
    # and the security deposit is no more than $1500.
    # If (TomAllowedMoveInWithFluffy AND SecurityDepositNoMoreThan1500) THEN TomRents
    Implies(And(TomAllowedMoveInWithFluffy, SecurityDepositNoMoreThan1500), TomRents),
    
    # If a managed building allows pets, then people are allowed to move in with a pet.
    Implies(And(ManagedBuilding, PetsAllowed), MoveInWithPetAllowed),
    
    # Also: TomAllowedMoveInWithFluffy means he can move in with Fluffy.
    # If move in with a pet is allowed, and Fluffy is a pet, then Tom can move in with Fluffy.
    Implies(And(MoveInWithPetAllowed, CatIsPet), TomAllowedMoveInWithFluffy),
    
    # The Olive Garden is managed, so deposit is required.
    # Deposit at Olive Garden: either equal to $2000 or more than $2000.
    # $2000 > $1500, so deposit > $1500.
    # Therefore SecurityDepositNoMoreThan1500 is False.
    
    # Let's add the numerical facts:
    # Olive Garden rent = 2000
    # If deposit = rent or deposit > rent, then deposit >= 2000
    # Since 2000 > 1500, deposit > 1500, so deposit is NOT <= 1500
    
    # We need to connect the dots:
    # OliveGardenManaged -> DepositRequired
    # OliveGardenManaged -> (DepositEqRent OR DepositMoreThanRent)
    # OliveGardenRent2000 -> rent = 2000
    # If deposit = 2000 or deposit > 2000, then deposit > 1500
    # So SecurityDepositNoMoreThan1500 is False
    
    # Let's add explicit constraints about the deposit at Olive Garden
    # The deposit at Olive Garden is either equal to $2000 or more.
    # So deposit >= 2000 > 1500, so deposit is NOT <= 1500.
    Implies(OliveGardenManaged, Not(SecurityDepositNoMoreThan1500)),
    
    # Also, we don't know if The Olive Garden allows pets.
    # "Some managed buildings allow pets" doesn't tell us about this specific one.
]

# Goal: Tom will rent an apartment in The Olive Garden.
goal = TomRents

# Check Negated Goal (try to find counterexample)
s_neg = Solver()
s_neg.add(premises)
s_neg.add(Not(goal))
neg_res = s_neg.check()

# Check Positive Goal (try to find confirming model)
s_pos = Solver()
s_pos.add(premises)
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