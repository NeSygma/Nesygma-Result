from z3 import *

# Witnesses: Franco, Garcia, Hong, Iturbe, Jackson
# Days: Monday=0, Tuesday=1, Wednesday=2

solver = Solver()

F, G, H, I, J = Ints('F G H I J')
witnesses = [F, G, H, I, J]

for w in witnesses:
    solver.add(And(w >= 0, w <= 2))

# Franco != Garcia
solver.add(F != G)

# Iturbe on Wednesday
solver.add(I == 2)

# Exactly two on Tuesday
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)

# Hong not on Monday
solver.add(H != 0)

# At least one on Monday
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Franco same day as Hong
solver.add(F == H)

# Let's first see what models exist to understand the constraints better
print("All possible schedules with F == H:")
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {w: m.eval(w, model_completion=True) for w in witnesses}
    solutions.append(sol)
    solver.add(Or([w != m.eval(w, model_completion=True) for w in witnesses]))

print(f"Found {len(solutions)} solutions:")
for s in solutions:
    print(f"  F={s[F]}, G={s[G]}, H={s[H]}, I={s[I]}, J={s[J]}")

# Now let's check each option more carefully
# The problem asks: which MUST be true? So we need to check if an option is true in ALL solutions.

# Reset solver
solver2 = Solver()
for w in witnesses:
    solver2.add(And(w >= 0, w <= 2))
solver2.add(F != G)
solver2.add(I == 2)
solver2.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)
solver2.add(H != 0)
solver2.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)
solver2.add(F == H)

# For "must be true", we check if the negation of the option is UNSAT
# (i.e., the option holds in every valid model)

def must_be_true(constr):
    s = Solver()
    # Copy all constraints
    for w in witnesses:
        s.add(And(w >= 0, w <= 2))
    s.add(F != G)
    s.add(I == 2)
    s.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)
    s.add(H != 0)
    s.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)
    s.add(F == H)
    s.add(Not(constr))
    return s.check() == unsat

print("\nChecking which options MUST be true:")
print(f"A (F==2): {must_be_true(F == 2)}")
print(f"B (G==0): {must_be_true(G == 0)}")
print(f"C (G==2): {must_be_true(G == 2)}")
print(f"D (H==1): {must_be_true(H == 1)}")

# E: Iturbe is the only witness on Wednesday
opt_e_constrs = [I == 2]
for w in [F, G, H, J]:
    opt_e_constrs.append(w != 2)
opt_e = And(opt_e_constrs)
print(f"E (only Iturbe on Wed): {must_be_true(opt_e)}")