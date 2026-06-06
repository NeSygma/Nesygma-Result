from z3 import *

solver = Solver()

# Declare integer variables for each witness (day assignment)
# 0 = Monday, 1 = Tuesday, 2 = Wednesday
F, G, H, I, J = Ints('F G H I J')
days = [F, G, H, I, J]

# Domain constraints: each testifies on exactly one of the three days
for d in days:
    solver.add(And(d >= 0, d <= 2))

# Constraint 1: Franco and Garcia do NOT testify on the same day
solver.add(F != G)

# Constraint 2: Iturbe testifies on Wednesday
solver.add(I == 2)

# Constraint 3: Exactly two witnesses testify on Tuesday
solver.add(Sum([If(v == 1, 1, 0) for v in days]) == 2)

# Constraint 4: Hong does NOT testify on Monday
solver.add(H != 0)

# Constraint 5: At least one witness testifies on Monday
solver.add(Sum([If(v == 0, 1, 0) for v in days]) >= 1)

# Additional condition from the question: Jackson testifies on Wednesday
solver.add(J == 2)

# ---- Evaluate each answer choice using entailment ----
# An option "must be true" iff its negation makes the problem unsatisfiable.

found_options = []

# (A) Franco is scheduled to testify on Monday.
opt_a = (F == 0)
solver.push()
solver.add(Not(opt_a))
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# (B) Garcia is scheduled to testify on Monday.
opt_b = (G == 0)
solver.push()
solver.add(Not(opt_b))
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# (C) Exactly one witness is scheduled to testify on Monday.
opt_c = (Sum([If(v == 0, 1, 0) for v in days]) == 1)
solver.push()
solver.add(Not(opt_c))
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# (D) Exactly two witnesses are scheduled to testify on Monday.
opt_d = (Sum([If(v == 0, 1, 0) for v in days]) == 2)
solver.push()
solver.add(Not(opt_d))
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# (E) Garcia is scheduled to testify on the same day as Hong.
opt_e = (G == H)
solver.push()
solver.add(Not(opt_e))
if solver.check() == unsat:
    found_options.append("E")
solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")