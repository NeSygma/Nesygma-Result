from z3 import *

solver = Solver()

# Boolean variables
has_f1 = Bool('has_f1')
has_j1 = Bool('has_j1')
wants_work = Bool('wants_work')
apply_cpt = Bool('apply_cpt')
apply_opt = Bool('apply_opt')

# Premise 1: Mike, as an international student, has either F1 or J1 visa
solver.add(Or(has_f1, has_j1))

# Premise 2: If an international student with F1 wants to work, they must apply for CPT or OPT
solver.add(Or(Not(has_f1), Not(wants_work), apply_cpt, apply_opt))

# Premise 4: Mike needs to apply for CPT if he wants to work
solver.add(Or(Not(wants_work), apply_cpt))

# Check if the negation of the conclusion (¬has_f1) is satisfiable with the premises
solver.push()
solver.add(Not(has_f1))
sat_neg = solver.check()
model_neg = solver.model() if sat_neg == sat else None
solver.pop()

# Check that the premises alone are satisfiable
solver.push()
sat_premises = solver.check()
solver.pop()

if not sat_premises:
    print("STATUS: unsat")
elif sat_neg == sat:
    print("STATUS: unknown")
    # Print a counterexample model where the conclusion is false
    print("Counterexample: has_f1 =", model_neg[has_f1])
    print("has_j1 =", model_neg[has_j1])
    print("wants_work =", model_neg[wants_work])
    print("apply_cpt =", model_neg[apply_cpt])
    print("apply_opt =", model_neg[apply_opt])
else:
    # If ¬has_f1 is unsatisfiable, the conclusion is entailed
    solver.push()
    solver.add(has_f1)
    sat_affirm = solver.check()
    model_affirm = solver.model() if sat_affirm == sat else None
    solver.pop()
    if sat_affirm == sat:
        print("STATUS: proved")
        print("Conclusion is definitely TRUE.")
    else:
        print("STATUS: proved")
        print("Conclusion is definitely FALSE.")