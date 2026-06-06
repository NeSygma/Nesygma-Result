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

# Premise 7: If needs_money then (not_picky AND Not(needs_money))
# This is equivalent to: needs_money => (not_picky and Not(needs_money))
# Which simplifies to: Not(needs_money) OR (not_picky and Not(needs_money))
# Which further simplifies to: Not(needs_money) OR (not_picky and False) if needs_money is True
# So effectively: Not(needs_money) OR False => Not(needs_money)
# Thus, the premise implies that needs_money must be False.
premises.append(Not(needs_money))

# Conclusion to evaluate:
# Hannah is not a picky eater and spends a lot of her time eating and catching up with friends in the campus dining halls.
conclusion = And(not_picky, spends_time_dining_hall)

# Check if premises + not conclusion is satisfiable (counterexample search)
solver_neg = Solver()
solver_neg.add(premises)
solver_neg.add(Not(conclusion))
neg_result = solver_neg.check()

# Check if premises + conclusion is satisfiable (confirming model search)
solver_pos = Solver()
solver_pos.add(premises)
solver_pos.add(conclusion)
pos_result = solver_pos.check()

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