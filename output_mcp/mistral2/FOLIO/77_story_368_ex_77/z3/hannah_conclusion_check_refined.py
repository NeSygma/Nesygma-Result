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
# This is equivalent to: needs_money implies (not_picky and False) when needs_money is True
# Which simplifies to: needs_money implies False
# So needs_money must be False
premises.append(Implies(needs_money, False))

# Conclusion: not_picky and spends_time_dining_hall
conclusion = And(not_picky, spends_time_dining_hall)

# Check consistency of premises
solver_consistency = Solver()
solver_consistency.add(premises)
consistency_result = solver_consistency.check()

# If premises are consistent, check if they entail the conclusion
if consistency_result == sat:
    # Check if premises entail the conclusion
    solver_pos = Solver()
    solver_pos.add(premises)
    solver_pos.add(Not(conclusion))
    pos_result = solver_pos.check()

    # Check if premises entail the negation of the conclusion
    solver_neg = Solver()
    solver_neg.add(premises)
    solver_neg.add(conclusion)
    neg_result = solver_neg.check()

    # Interpret results
    if pos_result == unsat and neg_result == sat:
        print("STATUS: proved")
        print("CONCLUSION: True")
    elif pos_result == sat and neg_result == unsat:
        print("STATUS: proved")
        print("CONCLUSION: False")
    elif pos_result == sat and neg_result == sat:
        print("STATUS: proved")
        print("CONCLUSION: Uncertain")
    else:
        print("STATUS: unknown")
        print("CONCLUSION: Inconclusive")
else:
    print("STATUS: unknown")
    print("CONCLUSION: Inconsistent premises")