from z3 import *

# Define Boolean variables for Hannah's properties
works_student_job = Bool('works_student_job')
needs_money = Bool('needs_money')
orders_takeout = Bool('orders_takeout')
enjoys_dining_hall = Bool('enjoys_dining_hall')
not_picky = Bool('not_picky')
spends_time_dining_hall = Bool('spends_time_dining_hall')

# Premises as constraints
premises = []

# Premise 1: If works_student_job then needs_money
premises.append(Implies(works_student_job, needs_money))

# Premise 2: If orders_takeout then works_student_job
premises.append(Implies(orders_takeout, works_student_job))

# Premise 3: orders_takeout OR enjoys_dining_hall
premises.append(Or(orders_takeout, enjoys_dining_hall))

# Premise 4: If enjoys_dining_hall then not_picky
premises.append(Implies(enjoys_dining_hall, not_picky))

# Premise 5: If enjoys_dining_hall then spends_time_dining_hall
premises.append(Implies(enjoys_dining_hall, spends_time_dining_hall))

# Premise 6: Hannah works in student jobs on campus
premises.append(works_student_job)

# Premise 7: If needs_money then (not_picky and Not(needs_money))
# This is equivalent to: needs_money => (not_picky and Not(needs_money))
# Which is only satisfiable if needs_money is False
premises.append(Implies(needs_money, And(not_picky, Not(needs_money))))

# Check if premises are consistent
solver_prem = Solver()
solver_prem.add(premises)
prem_result = solver_prem.check()

if prem_result == sat:
    print("STATUS: sat")
    print("Premises are consistent.")
    m = solver_prem.model()
    print(f"works_student_job = {m[works_student_job]}")
    print(f"needs_money = {m[needs_money]}")
    print(f"orders_takeout = {m[orders_takeout]}")
    print(f"enjoys_dining_hall = {m[enjoys_dining_hall]}")
    print(f"not_picky = {m[not_picky]}")
    print(f"spends_time_dining_hall = {m[spends_time_dining_hall]}")
elif prem_result == unsat:
    print("STATUS: unsat")
    print("Premises are inconsistent.")
else:
    print("STATUS: unknown")
    print("Premises are inconclusive.")