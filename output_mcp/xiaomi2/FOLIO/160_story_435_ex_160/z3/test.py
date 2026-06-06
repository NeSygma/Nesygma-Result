from z3 import *

# Boolean propositions for James
work_library = Bool('work_library')
work_lab = Bool('work_lab')
cs_dept = Bool('cs_dept')
part_time_uni = Bool('part_time_uni')
takes_database = Bool('takes_database')
class_david = Bool('class_david')

solver = Solver()

# Premise 1: work_library -> NOT cs_dept
solver.add(Implies(work_library, Not(cs_dept)))

# Premise 2: part_time_uni -> work_library
solver.add(Implies(part_time_uni, work_library))

# Premise 3: takes_database -> cs_dept
solver.add(Implies(takes_database, cs_dept))

# Premise 4: class_david -> takes_database
solver.add(Implies(class_david, takes_database))

# Premise 5: work_lab -> class_david
solver.add(Implies(work_lab, class_david))

# Premise 6: James works in the lab
solver.add(work_lab == True)

# Premise 7: James doesn't work in the LIBRARY and doesn't have a part-time job from the university
solver.add(work_library == False)
solver.add(part_time_uni == False)

# Derivation chain: work_lab -> class_david -> takes_database -> cs_dept
# Since work_lab=True, all downstream should be True.

goal = takes_database

# Theorem proving: check premises + NOT(goal)
s_neg = Solver()
s_neg.add(Implies(work_library, Not(cs_dept)))
s_neg.add(Implies(part_time_uni, work_library))
s_neg.add(Implies(takes_database, cs_dept))
s_neg.add(Implies(class_david, takes_database))
s_neg.add(Implies(work_lab, class_david))
s_neg.add(work_lab == True)
s_neg.add(work_library == False)
s_neg.add(part_time_uni == False)
s_neg.add(Not(goal))
neg_res = s_neg.check()

# Check premises + goal
s_pos = Solver()
s_pos.add(Implies(work_library, Not(cs_dept)))
s_pos.add(Implies(part_time_uni, work_library))
s_pos.add(Implies(takes_database, cs_dept))
s_pos.add(Implies(class_david, takes_database))
s_pos.add(Implies(work_lab, class_david))
s_pos.add(work_lab == True)
s_pos.add(work_library == False)
s_pos.add(part_time_uni == False)
s_pos.add(goal)
pos_res = s_pos.check()

print(f"Negated goal check: {neg_res}")
print(f"Positive goal check: {pos_res}")

if neg_res == unsat and pos_res == sat:
    print("STATUS: proved")
    print("RESULT: True")
    print("CONCLUSION: James takes the database course is PROVED TRUE.")
    print("DERIVATION CHAIN:")
    print("  Premise 6: work_lab(James) = True")
    print("  Premise 5: work_lab -> class_david  =>  class_david(James) = True")
    print("  Premise 4: class_david -> takes_database  =>  takes_database(James) = True")
    print("  Premise 3: takes_database -> cs_dept  =>  cs_dept(James) = True")
    print("  Premise 7: work_library(James) = False, part_time_uni(James) = False (consistent)")
    print("  Premise 1: work_library -> NOT cs_dept  (vacuously true since work_library=False)")
    m = s_pos.model()
    print(f"\nModel: work_lab={m[work_lab]}, class_david={m[class_david]}, takes_database={m[takes_database]}, cs_dept={m[cs_dept]}, work_library={m[work_library]}, part_time_uni={m[part_time_uni]}")
elif neg_res == sat and pos_res == unsat:
    print("STATUS: proved")
    print("RESULT: False")
    print("CONCLUSION: James takes the database course is DISPROVED.")
elif neg_res == sat and pos_res == sat:
    print("STATUS: proved")
    print("RESULT: Uncertain")
    print("CONCLUSION: Both the conclusion and its negation are consistent with premises.")
elif neg_res == unsat and pos_res == unsat:
    print("STATUS: unknown")
    print("RESULT: Inconsistent")
    print("CONCLUSION: The premises are internally contradictory.")
else:
    print("STATUS: unknown")
