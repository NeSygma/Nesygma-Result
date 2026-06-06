from z3 import *

solver = Solver()

# Each composition is performed at a position 1-8
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')

# All positions are from 1 to 8
compositions = [F, H, L, O, P, R, S, T]
for c in compositions:
    solver.add(c >= 1, c <= 8)

# Each composition gets a unique position (exactly once each)
solver.add(Distinct(compositions))

# Constraint 1: T is performed either immediately before F or immediately after R
# T immediately before F: T + 1 == F
# OR T immediately after R: R + 1 == T
solver.add(Or(T + 1 == F, R + 1 == T))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F.
# |pos(F) - pos(R)| > 2 (at least 2 compositions between them means distance > 2)
# Actually "at least two compositions are performed either after F and before R, or after R and before F"
# means there are at least 2 compositions strictly between F and R.
# So |pos(F) - pos(R)| >= 3 (if position difference is 3, there are 2 compositions between)
# Let's use: Or(And(F < R, R - F - 1 >= 2), And(R < F, F - R - 1 >= 2))
# Which simplifies to: |F - R| - 1 >= 2, i.e., |F - R| >= 3
solver.add(Or(F + 3 <= R, R + 3 <= F))

# Constraint 3: O is performed either first or fifth.
solver.add(Or(O == 1, O == 5))

# Constraint 4: The eighth composition performed is either L or H.
solver.add(Or(L == 8, H == 8))

# Constraint 5: P is performed at some time before S.
solver.add(P < S)

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O.
# |pos(O) - pos(S)| >= 2 (at least 1 composition between them)
solver.add(Or(O + 2 <= S, S + 2 <= O))

# Additional condition: Exactly two compositions are performed after F but before O.
# This means there are exactly 2 compositions between F and O, with F before O.
# So F + 3 == O (positions: F, _, _, O)
solver.add(F + 3 == O)

# Now we need to find which position R must be in.
# We'll test each possible position for R.
# But first, let's just get a model to see what solutions exist.

# Let's enumerate solutions to see what positions R can take
solutions_r = set()
while solver.check() == sat:
    m = solver.model()
    r_val = m[R].as_long()
    solutions_r.add(r_val)
    # Block this solution
    solver.add(Or([c != m.eval(c) for c in compositions]))

print(f"STATUS: sat")
print(f"Possible positions for R: {sorted(solutions_r)}")

# Now test each option
solver2 = Solver()

# All positions are from 1 to 8
for c in compositions:
    solver2.add(c >= 1, c <= 8)
solver2.add(Distinct(compositions))
solver2.add(Or(T + 1 == F, R + 1 == T))
solver2.add(Or(F + 3 <= R, R + 3 <= F))
solver2.add(Or(O == 1, O == 5))
solver2.add(Or(L == 8, H == 8))
solver2.add(P < S)
solver2.add(Or(O + 2 <= S, S + 2 <= O))
solver2.add(F + 3 == O)

# The question asks: if exactly two compositions are after F but before O, then R must be...
# So we add the condition and test each possible R position as a MUST (necessary condition)
# We need to find which position R ALWAYS takes (i.e., in all valid models, R is at that position)
# Let's test each position for R

found_options = []
for letter, r_pos in [("A", 1), ("B", 3), ("C", 4), ("D", 6), ("E", 7)]:
    solver2.push()
    solver2.add(R == r_pos)
    if solver2.check() == sat:
        found_options.append(letter)
    solver2.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")