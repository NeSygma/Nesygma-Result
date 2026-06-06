from z3 import *

# We have 7 positions (1-indexed: 1..7)
# Accomplices: Peters, Quinn, Rovero, Stanton, Tao, Villas, White
P, Q, R, S, T, V, W = Ints('P Q R S T V W')

solver = Solver()

# Domain: each position is between 1 and 7
persons = [P, Q, R, S, T, V, W]
for p in persons:
    solver.add(p >= 1, p <= 7)

# All distinct positions
solver.add(Distinct(persons))

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao.
solver.add(Not(Or(S - T == 1, T - S == 1)))

# Constraint 2: Quinn was recruited earlier than Rovero.
solver.add(Q < R)

# Constraint 3: Villas was recruited immediately before White.
solver.add(V + 1 == W)

# Constraint 4: Peters was recruited fourth.
solver.add(P == 4)

# Additional condition: Quinn was recruited immediately before Rovero.
solver.add(Q + 1 == R)

# The question: "Stanton CANNOT have been recruited" at which position?
# This means: which position for Stanton is impossible given all constraints?
# We test each option: if adding "Stanton is at position X" makes the problem UNSAT,
# then Stanton cannot be at that position.

# Let's first check what positions are possible for Stanton by enumerating all solutions
# and seeing which positions Stanton takes.

solutions = set()
while solver.check() == sat:
    m = solver.model()
    pos = m.eval(S, model_completion=True).as_long()
    solutions.add(pos)
    # Block this specific position for Stanton
    solver.add(S != pos)

print(f"Possible positions for Stanton: {sorted(solutions)}")

# Now check each option
# The question asks: Stanton CANNOT have been recruited at which position?
# So the answer is the position NOT in the possible set.

all_options = {1: "A", 2: "B", 3: "C", 5: "D", 7: "E"}
impossible = [all_options[pos] for pos in all_options if pos not in solutions]

if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: Impossible options found {impossible}, possible positions: {sorted(solutions)}")