from z3 import *

solver = Solver()

# Seven accomplices: Peters, Quinn, Rovero, Stanton, Tao, Villas, White
# Positions 1-7 (1 = first recruited, 7 = last recruited)
P, Q, R, S, T, V, W = Ints('P Q R S T V W')
positions = [P, Q, R, S, T, V, W]
names = ['Peters', 'Quinn', 'Rovero', 'Stanton', 'Tao', 'Villas', 'White']

# Each position is 1-7, all distinct
for pos in positions:
    solver.add(pos >= 1, pos <= 7)
solver.add(Distinct(positions))

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao
solver.add(And(S != T + 1, S != T - 1))

# Constraint 2: Quinn was recruited earlier than Rovero
solver.add(Q < R)

# Constraint 3: Villas was recruited immediately before White
solver.add(W == V + 1)

# Constraint 4: Peters was recruited fourth
solver.add(P == 4)

# Middle five (positions 2-6) for each option
# We need to check which option is consistent with the constraints

# Option A: Quinn=2, Stanton=3, Peters=4, Tao=5, Villas=6
opt_a = And(Q == 2, S == 3, P == 4, T == 5, V == 6)

# Option B: Quinn=2, Stanton=3, Peters=4, Tao=5, White=6
opt_b = And(Q == 2, S == 3, P == 4, T == 5, W == 6)

# Option C: Villas=2, White=3, Peters=4, Quinn=5, Stanton=6
opt_c = And(V == 2, W == 3, P == 4, Q == 5, S == 6)

# Option D: Villas=2, White=3, Peters=4, Rovero=5, Stanton=6
opt_d = And(V == 2, W == 3, P == 4, R == 5, S == 6)

# Option E: Villas=2, White=3, Quinn=4, Rovero=5, Stanton=6
opt_e = And(V == 2, W == 3, Q == 4, R == 5, S == 6)

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