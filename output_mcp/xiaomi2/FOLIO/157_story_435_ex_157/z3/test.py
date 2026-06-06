from z3 import *

# Predicates for James
W = Bool('W')  # works in the library
C = Bool('C')  # from the computer science department
P = Bool('P')  # has a part-time job offered by the university
D = Bool('D')  # taking the database course
K = Bool('K')  # taking a class with Professor David
L = Bool('L')  # working in the lab

# Universal rules (applied to James)
rules = [
    Implies(W, Not(C)),   # Premise 1: library worker -> not CS
    Implies(P, W),         # Premise 2: part-time job -> works in library
    Implies(D, C),         # Premise 3: database course -> CS
    Implies(K, D),         # Premise 4: class with David -> database
    Implies(L, K),         # Premise 5: lab -> class with David
]

# Premise 6: James works in the lab
premise6 = L

# Premise 7: "James doesn't work in the lab or have a part-time job"
# Interpretation A: Not(L) AND Not(P) — contradicts premise 6 directly
premise7a = And(Not(L), Not(P))
# Interpretation B: Not(L) OR Not(P) — consistent (reduces to Not(P) since L is true)
premise7b = Or(Not(L), Not(P))

# Check consistency of both interpretations
sa = Solver()
sa.add(rules + [premise6, premise7a])
cons_a = sa.check()
print(f"Interpretation A (Not(L) AND Not(P)) consistency: {cons_a}")

sb = Solver()
sb.add(rules + [premise6, premise7b])
cons_b = sb.check()
print(f"Interpretation B (Not(L) OR Not(P)) consistency: {cons_b}")

# Use the consistent interpretation B for theorem proving
premises = rules + [premise6, premise7b]
goal = P  # Conclusion: "James has a part-time job offered by the university"

# Theorem proving: check premises against goal and negated goal
s_neg = Solver()
s_neg.add(premises)
s_neg.add(Not(goal))
neg_res = s_neg.check()

s_pos = Solver()
s_pos.add(premises)
s_pos.add(goal)
pos_res = s_pos.check()

print(f"\nTheorem proving results:")
print(f"Premises + Not(goal): {neg_res}")
print(f"Premises + goal:     {pos_res}")

if neg_res == unsat and pos_res == sat:
    print("STATUS: proved")
    print("RESULT: True")
elif neg_res == sat and pos_res == unsat:
    print("STATUS: proved")
    print("RESULT: False")
elif neg_res == sat and pos_res == sat:
    print("STATUS: proved")
    print("RESULT: Uncertain")
elif neg_res == unsat and pos_res == unsat:
    print("STATUS: unknown")
    print("RESULT: Inconsistent")

# Verify: is P disprovable from rules + L alone (even without premise 7)?
print("\n--- Derivation check from rules + L(James) alone ---")
s_derive = Solver()
s_derive.add(rules + [L])
s_derive.add(P)
derive_res = s_derive.check()
print(f"Rules + L(James) + P(James): {derive_res}")
if derive_res == unsat:
    print("P(James) is independently disprovable from the logical chain alone.")
    m = s_neg.model()
    print(f"\nModel under Not(P):")
    for v in [L, K, D, C, W, P]:
        print(f"  {v} = {m[v]}")

print("\n--- Summary ---")
print("Chain: Lab -> Class with David -> Database -> CS Department")
print("Chain: Part-time Job -> Works in Library -> Not CS Department")
print("Since James is in CS (via lab chain), he CANNOT have a part-time job.")
print("The conclusion 'James has a part-time job' is FALSE.")
