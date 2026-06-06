from z3 import *

solver = Solver()

# Variables: position (chapter) of each clue
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Each clue assigned to a chapter 1-7, all different
for c in clues:
    solver.add(c >= 1, c <= 7)
solver.add(Distinct(clues))

# Constraint 1: T cannot be in chapter 1
solver.add(T != 1)

# Constraint 2: T before W, exactly two chapters separating => W = T + 3
solver.add(W == T + 3)

# Constraint 3: S and Z not adjacent
solver.add(Abs(S - Z) != 1)

# Constraint 4: W and X not adjacent
solver.add(Abs(W - X) != 1)

# Constraint 5: U and X must be adjacent
solver.add(Abs(U - X) == 1)

# Define each option as a specific ordering
# Option A: S, T, Z, X, U, W, R  (ch1=S, ch2=T, ch3=Z, ch4=X, ch5=U, ch6=W, ch7=R)
opt_a = And(S==1, T==2, Z==3, X==4, U==5, W==6, R==7)
# Option B: T, X, U, W, S, R, Z
opt_b = And(T==1, X==2, U==3, W==4, S==5, R==6, Z==7)
# Option C: U, S, X, T, Z, R, W
opt_c = And(U==1, S==2, X==3, T==4, Z==5, R==6, W==7)
# Option D: X, U, T, Z, R, W, S
opt_d = And(X==1, U==2, T==3, Z==4, R==5, W==6, S==7)
# Option E: Z, R, T, U, X, W, S
opt_e = And(Z==1, R==2, T==3, U==4, X==5, W==6, S==7)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
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