from z3 import *

# Declare sorts and constants
Person = DeclareSort('Person')
michael = Const('michael', Person)
peter = Const('peter', Person)
windy = Const('windy', Person)

# Declare predicates and relations
taller = Function('taller', Person, Person, BoolSort())
can_block = Function('can_block', Person, Person, BoolSort())
jumps_when_shooting = Function('jumps_when_shooting', Person, BoolSort())
great_shooter = Function('great_shooter', Person, BoolSort())

# Premises
premises = []

# 1. If a man is taller than another man, the taller one can block the other's shooting.
# Grounded for michael and peter (since they are the only ones mentioned in blocking context)
premises.append(Implies(taller(michael, peter), can_block(michael, peter)))
premises.append(Implies(taller(peter, michael), can_block(peter, michael)))

# 2. Michael is taller than everyone else in his class.
# Grounded: michael > peter, michael > windy
premises.append(taller(michael, peter))
premises.append(taller(michael, windy))

# 3. Transitivity: if x > y and y > z, then x > z
# We only need the relevant instances:
# michael > peter and peter > michael would be a contradiction, but we have michael > peter and michael > windy
# So we add peter > michael -> michael > windy (but we don't have peter > michael)
# Actually, we have michael > peter and michael > windy, so no contradiction here
premises.append(Implies(And(taller(peter, michael), taller(michael, windy)), taller(peter, windy)))

# 4. Peter is taller than Michael
premises.append(taller(peter, michael))

# 5. Michael can block any shooting from a person as long as the person does not jump when shooting.
# Grounded for peter and windy
premises.append(can_block(michael, peter) == Not(jumps_when_shooting(peter)))
premises.append(can_block(michael, windy) == Not(jumps_when_shooting(windy)))

# 6. Michael cannot block Windy's shooting
premises.append(Not(can_block(michael, windy)))

# 7. Every shooter who can jump when shooting is a great shooter.
premises.append(Implies(jumps_when_shooting(peter), great_shooter(peter)))
premises.append(Implies(jumps_when_shooting(windy), great_shooter(windy)))

# Conclusion to evaluate: Windy is a great shooter
goal = great_shooter(windy)

# Theorem proving: Check if premises entail the goal
# We check both the positive and negative cases

# Case 1: Check if premises + not(goal) is unsatisfiable (entailment holds)
s_neg = Solver()
s_neg.add(premises)
s_neg.add(Not(goal))
neg_res = s_neg.check()

# Case 2: Check if premises + goal is unsatisfiable (contradiction)
s_pos = Solver()
s_pos.add(premises)
s_pos.add(goal)
pos_res = s_pos.check()

# Interpret results
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
    print("CONCLUSION: Inconsistent premises")
else:
    print("STATUS: unknown")
    print("CONCLUSION: Inconclusive")