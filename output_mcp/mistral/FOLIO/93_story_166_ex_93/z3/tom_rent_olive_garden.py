from z3 import *

# Define sorts and constants
ManagedBuilding = DeclareSort('ManagedBuilding')
Pet = DeclareSort('Pet')
Person = DeclareSort('Person')

# Constants
Olive_Garden = Const('Olive_Garden', ManagedBuilding)
Tom = Const('Tom', Person)
Fluffy = Const('Fluffy', Pet)

# Predicates and functions
is_managed_building = Function('is_managed_building', ManagedBuilding, BoolSort())
allows_pets = Function('allows_pets', ManagedBuilding, BoolSort())
requires_deposit = Function('requires_deposit', ManagedBuilding, BoolSort())
monthly_rent = Function('monthly_rent', ManagedBuilding, IntSort(), BoolSort())
deposit = Function('deposit', ManagedBuilding, IntSort(), BoolSort())
is_pet = Function('is_pet', Pet, BoolSort())
is_cat = Function('is_cat', Pet, BoolSort())
owns = Function('owns', Person, Pet, BoolSort())
can_move_in_with_pet = Function('can_move_in_with_pet', Person, ManagedBuilding, Pet, BoolSort())
will_rent = Function('will_rent', Person, ManagedBuilding, BoolSort())

# Facts from premises
solver = Solver()

# 1. The Olive Garden is a managed building.
solver.add(is_managed_building(Olive_Garden))

# 2. The monthly rent at The Olive Garden is $2000.
solver.add(monthly_rent(Olive_Garden, 2000))

# 3. $2000 is more than $1500.
solver.add(2000 > 1500)

# 4. Fluffy is Tom's cat.
solver.add(is_cat(Fluffy))
solver.add(owns(Tom, Fluffy))

# 5. Cats are pets.
p = Const('p', Pet)
solver.add(ForAll([p], Implies(is_cat(p), is_pet(p))))

# 6. Pets are allowed in some managed buildings.
#    We assert that The Olive Garden allows pets.
solver.add(allows_pets(Olive_Garden))

# 7. A deposit is required to rent an apartment in a managed building.
b = Const('b', ManagedBuilding)
solver.add(ForAll([b], Implies(is_managed_building(b), requires_deposit(b))))

# 8. The security deposit can be either equal to the monthly rent at a managed building or more.
b = Const('b', ManagedBuilding)
d = Int('d')
r = Int('r')
solver.add(ForAll([b, d, r], 
                  Implies(And(is_managed_building(b), monthly_rent(b, r), deposit(b, d)), 
                         d >= r)))

# 9. If a managed building allows pets, then people are allowed to move in with a pet.
t = Const('t', Person)
p = Const('p', Pet)
b = Const('b', ManagedBuilding)
solver.add(ForAll([t, b, p], 
                  Implies(And(is_managed_building(b), allows_pets(b), is_pet(p), owns(t, p)),
                         can_move_in_with_pet(t, b, p))))

# 10. Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500.
b = Const('b', ManagedBuilding)
solver.add(ForAll([b], 
                  Implies(And(is_managed_building(b),
                             can_move_in_with_pet(Tom, b, Fluffy),
                             Exists([d], And(deposit(b, d), d <= 1500))),
                         will_rent(Tom, b))))

# Check if Tom will rent an apartment in The Olive Garden
conclusion = will_rent(Tom, Olive_Garden)

# Check the positive conclusion
solver.push()
solver.add(conclusion)
pos_result = solver.check()

# Check the negated conclusion
solver.pop()
solver.add(Not(conclusion))
neg_result = solver.check()

# Interpret results
if pos_result == unsat and neg_result == sat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif pos_result == sat and neg_result == unsat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif pos_result == sat and neg_result == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
elif pos_result == unsat and neg_result == unsat:
    print("STATUS: unknown")
    print("CONCLUSION: Inconsistent premises")
else:
    print("STATUS: unknown")
    print("CONCLUSION: Unknown due to solver limitation")