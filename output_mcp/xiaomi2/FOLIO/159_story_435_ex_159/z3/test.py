from z3 import *

# Boolean predicates for James
works_in_lab = Bool('works_in_lab')
takes_david = Bool('takes_david')
takes_database = Bool('takes_database')
is_cs = Bool('is_cs')
works_in_library = Bool('works_in_library')
has_pt_job = Bool('has_pt_job')

# ---- Consistent premises (1-6) ----
core_premises = [
    Implies(works_in_library, Not(is_cs)),       # P1: library → ¬CS
    Implies(has_pt_job, works_in_library),        # P2: ptjob → library
    Implies(takes_database, is_cs),               # P3: database → CS
    Implies(takes_david, takes_database),         # P4: david → database
    Implies(works_in_lab, takes_david),           # P5: lab → david
    works_in_lab == True,                          # P6: James works in lab
]

# P7 non-contradictory component: James doesn't have a part-time job
p7_ptjob = (has_pt_job == False)

# Conclusion: takes_database OR has_pt_job
conclusion = Or(takes_database, has_pt_job)

# ============================
# Theorem proving: does the conclusion follow from the premises?
# ============================

# Check: premises + ¬conclusion (try to find counterexample)
s_neg = Solver()
for p in core_premises:
    s_neg.add(p)
s_neg.add(p7_ptjob)
s_neg.add(Not(conclusion))
neg_res = s_neg.check()

# Check: premises + conclusion (try to find confirming model)
s_pos = Solver()
for p in core_premises:
    s_pos.add(p)
s_pos.add(p7_ptjob)
s_pos.add(conclusion)
pos_res = s_pos.check()

# Print results
print("=== Theorem Proving ===")
print(f"Premises + NOT(conclusion): {neg_res}")
print(f"Premises + conclusion:     {pos_res}")

if neg_res == unsat and pos_res == sat:
    print("\nSTATUS: proved")
    print("RESULT: True")
    print("The conclusion is PROVED TRUE.")
    m = s_pos.model()
    print(f"\nConfirming model:")
    print(f"  works_in_lab     = {m[works_in_lab]}")
    print(f"  takes_david      = {m[takes_david]}")
    print(f"  takes_database   = {m[takes_database]}")
    print(f"  is_cs            = {m[is_cs]}")
    print(f"  works_in_library = {m[works_in_library]}")
    print(f"  has_pt_job       = {m[has_pt_job]}")
    print(f"\nReasoning chain:")
    print(f"  P6: James works in the lab → works_in_lab = True")
    print(f"  P5: lab → takes Prof David's class → takes_david = True")
    print(f"  P4: David's class → database course → takes_database = True")
    print(f"  P3: database → CS department → is_cs = True")
    print(f"  P7: James has no part-time job → has_pt_job = False")
    print(f"  Conclusion: database ∨ pt_job = True ∨ False = True")
elif neg_res == sat and pos_res == unsat:
    print("\nSTATUS: proved")
    print("RESULT: False")
    print("The conclusion is PROVED FALSE.")
elif neg_res == sat and pos_res == sat:
    print("\nSTATUS: proved")
    print("RESULT: Uncertain")
    print("The conclusion is UNCERTAIN (contingent).")
elif neg_res == unsat and pos_res == unsat:
    print("\nSTATUS: unknown")
    print("INCONSISTENT: Premises are contradictory.")
else:
    print("\nSTATUS: unknown")
