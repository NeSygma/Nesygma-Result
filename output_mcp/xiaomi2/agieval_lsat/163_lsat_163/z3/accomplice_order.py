from z3 import *

solver = Solver()

# Positions 1-7 for each accomplice
P, Q, R, S, T, V, W = Ints('P Q R S T V W')
positions = [P, Q, R, S, T, V, W]
names = ['Peters', 'Quinn', 'Rovero', 'Stanton', 'Tao', 'Villas', 'White']

# Each position is 1-7, all distinct
for pos in positions:
    solver.add(pos >= 1, pos <= 7)
solver.add(Distinct(positions))

# Constraint 1: Stanton not immediately before or after Tao
solver.add(Abs(S - T) != 1)

# Constraint 2: Quinn earlier than Rovero
solver.add(Q < R)

# Constraint 3: Villas immediately before White
solver.add(V + 1 == W)

# Constraint 4: Peters recruited fourth
solver.add(P == 4)

# Now evaluate each option for positions 2-6
# Option A: Quinn=2, Stanton=3, Peters=4, Tao=5, Villas=6
opt_a_constr = And(Q == 2, S == 3, P == 4, T == 5, V == 6)
# Option B: Quinn=2, Stanton=3, Peters=4, Tao=5, White=6
opt_b_constr = And(Q == 2, S == 3, P == 4, T == 5, W == 6)
# Option C: Villas=2, White=3, Peters=4, Quinn=5, Stanton=6
opt_c_constr = And(V == 2, W == 3, P == 4, Q == 5, S == 6)
# Option D: Villas=2, White=3, Peters=4, Rovero=5, Stanton=6
opt_d_constr = And(V == 2, W == 3, P == 4, R == 5, S == 6)
# Option E: Villas=2, White=3, Quinn=4, Rovero=5, Stanton=6
opt_e_constr = And(V == 2, W == 3, Q == 4, R == 5, S == 6)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: " + ", ".join(f"{n}={m[p]}" for n, p in zip(names, positions)))
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