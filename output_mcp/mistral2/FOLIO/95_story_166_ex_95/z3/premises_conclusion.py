from z3 import *

# Define sorts and constants
ManagedBuilding = DeclareSort('ManagedBuilding')
Pet = DeclareSort('Pet')
Person = DeclareSort('Person')

# Constants
olive_garden = Const('olive_garden', ManagedBuilding)
fluffy = Const('fluffy', Pet)
tom = Const('tom', Person)

# Declare quantified variables for use in constraints
b = Const('b', ManagedBuilding)
p = Const('p', Pet)
person = Const('person', Person)
d = Int('d')

# Predicates and functions
AllowsPets = Function('AllowsPets', ManagedBuilding, BoolSort())
IsPet = Function('IsPet', Pet, BoolSort())
IsCat = Function('IsCat', Pet, BoolSort())
OwnsPet = Function('OwnsPet', Person, Pet, BoolSort())
Rent = Function('Rent', ManagedBuilding, IntSort())
Deposit = Function('Deposit', ManagedBuilding, IntSort())
CanMoveInWithPet = Function('CanMoveInWithPet', Person, ManagedBuilding, BoolSort())
WillRent_pred = Function('WillRent_pred', Person, ManagedBuilding, IntSort(), BoolSort())

# Premises as constraints
solver = Solver()

# 1. Pets are allowed in some managed buildings
solver.add(Exists([b], AllowsPets(b)))

# 2. A deposit is required to rent an apartment in a managed building
# (Implicit in the Deposit function being defined for all managed buildings)

# 3. The security deposit can be either equal to the monthly rent at a managed building or more
# For all managed buildings, deposit >= rent
solver.add(ForAll([b], Deposit(b) >= Rent(b)))

# 4. Fluffy is Tom's cat
solver.add(IsCat(fluffy))
solver.add(OwnsPet(tom, fluffy))

# 5. Cats are pets
solver.add(ForAll([p], Implies(IsCat(p), IsPet(p))))

# 6. The Olive Garden is a managed building
# (Already defined as a constant of type ManagedBuilding)

# 7. The monthly rent at the Olive Garden is $2000
solver.add(Rent(olive_garden) == 2000)

# 8. $2000 is more than $1500 (fact, not a constraint)

# 9. Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500
# WillRent_pred(tom, b, d) iff CanMoveInWithPet(tom, b) and d <= 1500
solver.add(ForAll([b, d], WillRent_pred(tom, b, d) == And(CanMoveInWithPet(tom, b), d <= 1500)))

# 10. If a managed building allows pets, then people are allowed to move in with a pet
solver.add(ForAll([b, person], Implies(AllowsPets(b), CanMoveInWithPet(person, b))))

# Additional constraint: Fluffy is a cat, so Fluffy is a pet
solver.add(IsPet(fluffy))

# Check if the premises entail that the deposit at the Olive Garden is >= 2000
# Conclusion: Deposit(olive_garden) >= 2000

# Check if premises + conclusion is satisfiable
solver.push()
solver.add(Deposit(olive_garden) >= 2000)
result_pos = solver.check()

# Check if premises + not(conclusion) is satisfiable
solver.pop()
solver.push()
solver.add(Deposit(olive_garden) < 2000)
result_neg = solver.check()

# Analyze results
print("Premises + Conclusion (Deposit >= 2000):", result_pos)
print("Premises + Not Conclusion (Deposit < 2000):", result_neg)

if result_pos == sat and result_neg == unsat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif result_pos == unsat and result_neg == sat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif result_pos == sat and result_neg == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
elif result_pos == unsat and result_neg == unsat:
    print("STATUS: unknown")
    print("CONCLUSION: Inconsistent premises")
else:
    print("STATUS: unknown")
    print("CONCLUSION: Unexpected solver result")