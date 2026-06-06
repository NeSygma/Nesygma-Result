from z3 import *

# Define predicates as boolean functions
P = Function('P', BoolSort(), BoolSort())  # Actually, we need P(x) as a predicate on individuals
A = Function('A', BoolSort(), BoolSort())
J = Function('J', BoolSort(), BoolSort())
L = Function('L', BoolSort(), BoolSort())
M = Function('M', BoolSort(), BoolSort())

# Actually, better to use individual constants and predicates
# Let's use a different approach: define Yuri as a constant and predicates as functions of individuals
yuri = Const('yuri', IntSort())  # Using IntSort for individuals, but we'll treat as constant

# Define predicates as functions from individuals to Bool
P = Function('P', IntSort(), BoolSort())
A = Function('A', IntSort(), BoolSort())
J = Function('J', IntSort(), BoolSort())
L = Function('L', IntSort(), BoolSort())
M = Function('M', IntSort(), BoolSort())

# Premises
premises = []

# 1. Some professional basketball players are not American nationals
# ∃x (P(x) ∧ ¬A(x))
x = Int('x')
premises.append(And(P(x), Not(A(x))))

# 2. All professional basketball players can do jump shots
# ∀x (P(x) → J(x))
premises.append(ForAll([x], Implies(P(x), J(x))))

# 3. If someone can jump shots, they leap straight into the air
# ∀x (J(x) → L(x))
premises.append(ForAll([x], Implies(J(x), L(x))))

# 4. If someone leaps straight into the air, they activate their leg muscles
# ∀x (L(x) → M(x))
premises.append(ForAll([x], Implies(L(x), M(x))))

# 5. Yuri does not activate his leg muscles
premises.append(Not(M(yuri)))

# Conclusion: If Yuri is not an American professional basketball player, then Yuri is a professional basketball player
# (¬(P(yuri) ∧ A(yuri))) → P(yuri)
# This is equivalent to: (¬P(yuri) ∨ ¬A(yuri)) → P(yuri)
# Which simplifies to: P(yuri) ∨ ¬P(yuri) ∨ ¬A(yuri) → P(yuri)
# Actually, let's keep it as the original form
conclusion = Implies(Not(And(P(yuri), A(yuri))), P(yuri))

# Theorem proving: check if premises entail conclusion
# We need to check if premises ∧ ¬conclusion is unsatisfiable
# If it is unsatisfiable, then conclusion follows (is true)
# If it is satisfiable, then conclusion does not necessarily follow

# Check 1: Premises + ¬conclusion
s_neg = Solver()
s_neg.add(premises)
s_neg.add(Not(conclusion))
neg_res = s_neg.check()

# Check 2: Premises + conclusion
s_pos = Solver()
s_pos.add(premises)
s_pos.add(conclusion)
pos_res = s_pos.check()

print("Premises:", premises)
print("Conclusion:", conclusion)
print("Check 1 (Premises + ¬conclusion):", neg_res)
print("Check 2 (Premises + conclusion):", pos_res)

# Interpret result
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
    print("CONCLUSION: Unknown case")