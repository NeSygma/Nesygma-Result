from z3 import *

# Declare sorts and predicates
Animal = DeclareSort('Animal')

# Predicates
spotted = Function('spotted', Animal, BoolSort())
rabbit = Function('rabbit', Animal, BoolSort())
turtle = Function('turtle', Animal, BoolSort())
squirrel = Function('squirrel', Animal, BoolSort())
cute = Function('cute', Animal, BoolSort())
skittish = Function('skittish', Animal, BoolSort())
calm = Function('calm', Animal, BoolSort())

# Constants
Rockie = Const('Rockie', Animal)

# Premises
premises = []

# 1. All rabbits that can be spotted near the campus are cute.
# ∀x: (spotted(x) ∧ rabbit(x)) → cute(x)
x = Const('x', Animal)
premises.append(ForAll([x], Implies(And(spotted(x), rabbit(x)), cute(x))))

# 2. Some turtles can be spotted near the campus.
# ∃x: (spotted(x) ∧ turtle(x))
y = Const('y', Animal)
premises.append(Exists([y], And(spotted(y), turtle(y))))

# 3. The only animals that can be spotted near the campus are rabbits and squirrels.
# ∀x: spotted(x) → (rabbit(x) ∨ squirrel(x))
premises.append(ForAll([x], Implies(spotted(x), Or(rabbit(x), squirrel(x)))))

# 4. If something is skittish, then it is not calm.
# ∀x: skittish(x) → ¬calm(x)
premises.append(ForAll([x], Implies(skittish(x), Not(calm(x)))))

# 5. All the squirrels that can be spotted near the campus are skittish.
# ∀x: (spotted(x) ∧ squirrel(x)) → skittish(x)
premises.append(ForAll([x], Implies(And(spotted(x), squirrel(x)), skittish(x))))

# 6. Rockie can be spotted near the campus, and it is calm.
premises.append(spotted(Rockie))
premises.append(calm(Rockie))

# Conclusion to evaluate
# ¬(turtle(Rockie) ∧ squirrel(Rockie)) → (cute(Rockie) ∨ skittish(Rockie))
conclusion = Implies(Not(And(turtle(Rockie), squirrel(Rockie))), Or(cute(Rockie), skittish(Rockie)))

# Theorem proving: check both positive and negated goal
print("=== Theorem Proving Mode ===")
print("Premises:", premises)
print("Conclusion:", conclusion)
print()

# Check negated goal (try to find counterexample)
s_neg = Solver()
s_neg.add(premises)
s_neg.add(Not(conclusion))
neg_res = s_neg.check()

# Check positive goal (try to find confirming model)
s_pos = Solver()
s_pos.add(premises)
s_pos.add(conclusion)
pos_res = s_pos.check()

print(f"Negated goal check: {neg_res}")
print(f"Positive goal check: {pos_res}")
print()

# Interpret result
if neg_res == unsat and pos_res == sat:
    print("STATUS: proved")
    print("CONCLUSION: True")
    print("REASON: The conclusion follows logically from the premises.")
elif neg_res == sat and pos_res == unsat:
    print("STATUS: proved")
    print("CONCLUSION: False")
    print("REASON: The conclusion is contradicted by the premises.")
elif neg_res == sat and pos_res == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
    print("REASON: The conclusion can be either true or false given the premises.")
elif neg_res == unsat and pos_res == unsat:
    print("STATUS: unknown")
    print("CONCLUSION: Inconsistent")
    print("REASON: The premises themselves are contradictory.")
else:
    print("STATUS: unknown")
    print("CONCLUSION: Unknown")
    print("REASON: Z3 returned unknown result.")