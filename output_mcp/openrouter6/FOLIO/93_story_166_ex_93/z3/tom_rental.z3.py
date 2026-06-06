from z3 import *

# Define sorts - using a single universal sort for all entities
Entity = DeclareSort('Entity')

# Constants
Tom = Const('Tom', Entity)
Fluffy = Const('Fluffy', Entity)
OliveGarden = Const('OliveGarden', Entity)

# Predicates
ManagedBuilding = Function('ManagedBuilding', Entity, BoolSort())
AllowsPets = Function('AllowsPets', Entity, BoolSort())
DepositRequired = Function('DepositRequired', Entity, BoolSort())
Cat = Function('Cat', Entity, BoolSort())
Pet = Function('Pet', Entity, BoolSort())
Rent = Function('Rent', Entity, Entity, BoolSort())  # Rent(person, building)

# Functions for amounts
MonthlyRent = Function('MonthlyRent', Entity, IntSort())
SecurityDeposit = Function('SecurityDeposit', Entity, IntSort())

# Relations
Owns = Function('Owns', Entity, Entity, BoolSort())  # Owns(person, pet)
AllowedToMoveInWithPet = Function('AllowedToMoveInWithPet', Entity, Entity, Entity, BoolSort())  # AllowedToMoveInWithPet(person, pet, building)

# Helper predicate for Tom moving in with Fluffy at a building
def AllowedToMoveInWithFluffy(building):
    return AllowedToMoveInWithPet(Tom, Fluffy, building)

# Create solver for checking positive goal
s_pos = Solver()
# Create solver for checking negated goal  
s_neg = Solver()

# ===== PREMISES =====

# 1. Pets are allowed in some managed buildings.
# ∃b (ManagedBuilding(b) ∧ AllowsPets(b))
# We'll create a fresh variable for this existential
b1 = Const('b1', Entity)
s_pos.add(ManagedBuilding(b1), AllowsPets(b1))
s_neg.add(ManagedBuilding(b1), AllowsPets(b1))

# 2. A deposit is required to rent an apartment in a managed building.
# ∀b (ManagedBuilding(b) → DepositRequired(b))
b2 = Const('b2', Entity)
s_pos.add(Implies(ManagedBuilding(b2), DepositRequired(b2)))
s_neg.add(Implies(ManagedBuilding(b2), DepositRequired(b2)))

# 3. The security deposit can be either equal to the monthly rent at a managed building or more.
# ∀b (ManagedBuilding(b) → (SecurityDeposit(b) == MonthlyRent(b) ∨ SecurityDeposit(b) > MonthlyRent(b)))
b3 = Const('b3', Entity)
s_pos.add(Implies(ManagedBuilding(b3), 
                  Or(SecurityDeposit(b3) == MonthlyRent(b3), 
                     SecurityDeposit(b3) > MonthlyRent(b3))))
s_neg.add(Implies(ManagedBuilding(b3), 
                  Or(SecurityDeposit(b3) == MonthlyRent(b3), 
                     SecurityDeposit(b3) > MonthlyRent(b3))))

# 4. Fluffy is Tom's cat.
# Cat(Fluffy) ∧ Owns(Tom, Fluffy)
s_pos.add(Cat(Fluffy), Owns(Tom, Fluffy))
s_neg.add(Cat(Fluffy), Owns(Tom, Fluffy))

# 5. Cats are pets.
# ∀c (Cat(c) → Pet(c))
c5 = Const('c5', Entity)
s_pos.add(Implies(Cat(c5), Pet(c5)))
s_neg.add(Implies(Cat(c5), Pet(c5)))

# 6. The Olive Garden is a managed building.
s_pos.add(ManagedBuilding(OliveGarden))
s_neg.add(ManagedBuilding(OliveGarden))

# 7. The monthly rent at the Olive Garden is $2000.
s_pos.add(MonthlyRent(OliveGarden) == 2000)
s_neg.add(MonthlyRent(OliveGarden) == 2000)

# 8. $2000 is more than $1500.
s_pos.add(2000 > 1500)
s_neg.add(2000 > 1500)

# 9. Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, 
#    and the security deposit is no more than $1500.
# ∀b (ManagedBuilding(b) → ((AllowedToMoveInWithFluffy(b) ∧ SecurityDeposit(b) ≤ 1500) → Rent(Tom, b)))
b9 = Const('b9', Entity)
s_pos.add(Implies(ManagedBuilding(b9),
                  Implies(And(AllowedToMoveInWithFluffy(b9), SecurityDeposit(b9) <= 1500),
                          Rent(Tom, b9))))
s_neg.add(Implies(ManagedBuilding(b9),
                  Implies(And(AllowedToMoveInWithFluffy(b9), SecurityDeposit(b9) <= 1500),
                          Rent(Tom, b9))))

# 10. If a managed building allows pets, then people are allowed to move in with a pet.
# ∀b (ManagedBuilding(b) ∧ AllowsPets(b) → ∀p ∀pet (AllowedToMoveInWithPet(p, pet, b)))
b10 = Const('b10', Entity)
p10 = Const('p10', Entity)
pet10 = Const('pet10', Entity)
s_pos.add(Implies(And(ManagedBuilding(b10), AllowsPets(b10)),
                  AllowedToMoveInWithPet(p10, pet10, b10)))
s_neg.add(Implies(And(ManagedBuilding(b10), AllowsPets(b10)),
                  AllowedToMoveInWithPet(p10, pet10, b10)))

# Additional derived constraints from premises:
# From 4, 5: Fluffy is a pet
s_pos.add(Pet(Fluffy))
s_neg.add(Pet(Fluffy))

# From 6, 7: Olive Garden's monthly rent is 2000
# Already added

# From 3 applied to Olive Garden:
s_pos.add(Or(SecurityDeposit(OliveGarden) == MonthlyRent(OliveGarden),
             SecurityDeposit(OliveGarden) > MonthlyRent(OliveGarden)))
s_neg.add(Or(SecurityDeposit(OliveGarden) == MonthlyRent(OliveGarden),
             SecurityDeposit(OliveGarden) > MonthlyRent(OliveGarden)))

# From 10 applied to Olive Garden (if it allows pets):
# We don't know if Olive Garden allows pets yet. But from premise 1, some managed building allows pets.
# We need to consider whether Olive Garden could be that building or not.

# ===== CONCLUSION TO EVALUATE =====
# Tom will rent an apartment in The Olive Garden.
conclusion = Rent(Tom, OliveGarden)

# Check positive goal: premises + conclusion
s_pos.add(conclusion)

# Check negated goal: premises + NOT conclusion
s_neg.add(Not(conclusion))

# ===== CHECK BOTH =====
print("Checking positive goal (premises + conclusion)...")
result_pos = s_pos.check()
print(f"Positive goal result: {result_pos}")

print("\nChecking negated goal (premises + NOT conclusion)...")
result_neg = s_neg.check()
print(f"Negated goal result: {result_neg}")

# ===== INTERPRET RESULTS =====
if result_pos == sat and result_neg == unsat:
    # Conclusion is necessarily true
    print("\nSTATUS: proved")
    print("CONCLUSION: True")
elif result_pos == unsat and result_neg == sat:
    # Conclusion is necessarily false
    print("\nSTATUS: proved")
    print("CONCLUSION: False")
elif result_pos == sat and result_neg == sat:
    # Conclusion can be true or false (contingent)
    print("\nSTATUS: proved")
    print("CONCLUSION: Uncertain")
elif result_pos == unsat and result_neg == unsat:
    # Premises are inconsistent
    print("\nSTATUS: unknown")
    print("CONCLUSION: Inconsistent premises")
else:
    # Should not happen with proper encoding
    print("\nSTATUS: unknown")
    print("CONCLUSION: Unknown result")