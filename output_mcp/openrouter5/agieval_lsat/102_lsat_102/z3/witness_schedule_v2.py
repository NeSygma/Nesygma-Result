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

# Let's first check if the base constraints are satisfiable
print("Base constraints check:")
if solver.check() == sat:
    m = solver.model()
    print(f"F={m[F]}, G={m[G]}, H={m[H]}, I={m[I]}, J={m[J]}")
else:
    print("UNSAT base")
    exit()

# Now evaluate each option
# Option A: Franco on Wednesday (F == 2)
solver.push()
solver.add(F == 2)
print(f"\nOption A (F==2): {solver.check()}")
solver.pop()

# Option B: Garcia on Monday (G == 0)
solver.push()
solver.add(G == 0)
print(f"Option B (G==0): {solver.check()}")
if solver.check() == sat:
    m = solver.model()
    print(f"  F={m[F]}, G={m[G]}, H={m[H]}, I={m[I]}, J={m[J]}")
solver.pop()

# Option C: Garcia on Wednesday (G == 2)
solver.push()
solver.add(G == 2)
print(f"Option C (G==2): {solver.check()}")
if solver.check() == sat:
    m = solver.model()
    print(f"  F={m[F]}, G={m[G]}, H={m[H]}, I={m[I]}, J={m[J]}")
solver.pop()

# Option D: Hong on Tuesday (H == 1)
solver.push()
solver.add(H == 1)
print(f"Option D (H==1): {solver.check()}")
if solver.check() == sat:
    m = solver.model()
    print(f"  F={m[F]}, G={m[G]}, H={m[H]}, I={m[I]}, J={m[J]}")
solver.pop()

# Option E: Iturbe is the only witness on Wednesday
solver.push()
solver.add(And(I == 2, F != 2, G != 2, H != 2, J != 2))
print(f"Option E (only Iturbe on Wed): {solver.check()}")
if solver.check() == sat:
    m = solver.model()
    print(f"  F={m[F]}, G={m[G]}, H={m[H]}, I={m[I]}, J={m[J]}")
solver.pop()