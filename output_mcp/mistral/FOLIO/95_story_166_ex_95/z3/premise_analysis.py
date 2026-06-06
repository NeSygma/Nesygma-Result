from z3 import *

# Declare entities
olive_garden = Const('olive_garden', StringSort())
tom = Const('tom', StringSort())
fluffy = Const('fluffy', StringSort())

# Declare sorts and functions
ManagedBuilding = Function('ManagedBuilding', StringSort(), BoolSort())
AllowsPets = Function('AllowsPets', StringSort(), BoolSort())
RequiresDeposit = Function('RequiresDeposit', StringSort(), BoolSort())
Deposit = Function('Deposit', StringSort(), IntSort())  # Maps building to deposit amount
Rent = Function('Rent', StringSort(), IntSort())         # Maps building to rent amount
IsPet = Function('IsPet', StringSort(), BoolSort())
IsCat = Function('IsCat', StringSort(), BoolSort())
Owner = Function('Owner', StringSort(), StringSort(), BoolSort())
CanMoveInWithPet = Function('CanMoveInWithPet', StringSort(), StringSort(), BoolSort())
WillRent = Function('WillRent', StringSort(), StringSort(), BoolSort())

# Declare quantified variables
b = Const('b', StringSort())
p = Const('p', StringSort())
o = Const('o', StringSort())

# Initialize solver
solver = Solver()

# Premise 1: Pets are allowed in some managed buildings
# We will encode this as: The Olive Garden allows pets (since it is a managed building and we need a concrete example)
solver.add(AllowsPets(olive_garden))

# Premise 2: A deposit is required to rent an apartment in a managed building
solver.add(RequiresDeposit(olive_garden))

# Premise 3: The security deposit can be either equal to the monthly rent at a managed building or more
# We will encode this as: Deposit >= Rent for the Olive Garden
solver.add(Deposit(olive_garden) >= Rent(olive_garden))

# Premise 4: Fluffy is Tom's cat
solver.add(IsCat(fluffy))
solver.add(Owner(fluffy, tom))

# Premise 5: Cats are pets
x = Const('x', StringSort())
solver.add(ForAll([x], Implies(IsCat(x), IsPet(x))))

# Premise 6: The Olive Garden is a managed building
solver.add(ManagedBuilding(olive_garden))

# Premise 7: The monthly rent at the Olive Garden is $2000
solver.add(Rent(olive_garden) == 2000)

# Premise 8: $2000 is more than $1500
solver.add(2000 > 1500)

# Premise 9: Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500
# We will encode this as: If CanMoveInWithPet(olive_garden, tom) and Deposit(olive_garden) <= 1500, then WillRent(tom, olive_garden)
solver.add(ForAll([b], Implies(And(CanMoveInWithPet(b, tom), Deposit(b) <= 1500), WillRent(tom, b))))

# Premise 10: If a managed building allows pets, then people are allowed to move in with a pet
solver.add(ForAll([b, p, o], Implies(And(ManagedBuilding(b), IsPet(p), Owner(p, o), AllowsPets(b)), CanMoveInWithPet(b, o))))

# Apply premises to the Olive Garden and Fluffy/Tom
solver.add(CanMoveInWithPet(olive_garden, tom))  # Because Fluffy is Tom's cat and the Olive Garden allows pets

# Conclusion: The security deposit at the Olive Garden is either $2000 or more
conclusion_cond = Deposit(olive_garden) >= 2000

# Check if the premises entail the conclusion
# We will check if the premises + Not(conclusion) are unsatisfiable
solver.push()
solver.add(Not(conclusion_cond))
neg_result = solver.check()
solver.pop()

# Check if the premises + conclusion are satisfiable
solver.push()
solver.add(conclusion_cond)
pos_result = solver.check()
solver.pop()

# Interpret results
if neg_result == unsat and pos_result == sat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif neg_result == sat and pos_result == unsat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif neg_result == sat and pos_result == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
elif neg_result == unsat and pos_result == unsat:
    print("STATUS: unknown")
    print("CONCLUSION: Inconsistent premises")
else:
    print("STATUS: unknown")
    print("CONCLUSION: Inconclusive")