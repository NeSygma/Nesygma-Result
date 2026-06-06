from z3 import *

# Declare boolean variables
has_F1 = Bool('has_F1')
has_J1 = Bool('has_J1')
wants_to_work = Bool('wants_to_work')
apply_CPT = Bool('apply_CPT')
apply_OPT = Bool('apply_OPT')

solver = Solver()

# Premise 1: Mike is an international student and has exactly one of F1 or J1 visa
# Exactly one: (has_F1 && !has_J1) || (!has_F1 && has_J1)
solver.add(Or(And(has_F1, Not(has_J1)), And(Not(has_F1), has_J1)))

# Premise 2: If Mike has F1 and wants to work, then he needs to apply for CPT or OPT
solver.add(Implies(And(has_F1, wants_to_work), Or(apply_CPT, apply_OPT)))

# Premise 3: Mike is an international student (given)
# Already accounted for in premise 1; no extra clause needed

# Premise 4: If Mike wants to work, then he needs to apply for CPT
solver.add(Implies(wants_to_work, apply_CPT))

# --- Check entailment of conclusion "has_F1"
# Check if there is a model where has_F1 is True
solver.push()
solver.add(has_F1)
sat1 = solver.check()
model1 = None
if sat1 == sat:
    model1 = solver.model()
solver.pop()

# Check if there is a model where has_F1 is False (i.e., not has_F1)
solver.push()
solver.add(Not(has_F1))
sat2 = solver.check()
model2 = None
if sat2 == sat:
    model2 = solver.model()
solver.pop()

# Determine status
if sat1 == sat and sat2 == sat:
    # Both possibilities exist => uncertain
    print("STATUS: unknown")
    # Optionally print model details
    if model1:
        print("Model with has_F1=True:", model1[has_F1])
    if model2:
        print("Model with has_F1=False:", model2[has_F1])
elif sat1 == sat:
    # Only true case is possible => provable
    print("STATUS: proved")
    print("Conclusion is definitely True.")
else:
    # Only false case is possible => refutable
    print("STATUS: proved")
    print("Conclusion is definitely False.")