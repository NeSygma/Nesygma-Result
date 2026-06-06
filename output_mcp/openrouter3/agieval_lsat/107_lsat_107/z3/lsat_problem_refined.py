from z3 import *

solver = Solver()

# Declare variables for each client's targets
I_W, I_V = Ints('I_W I_V')
S_W, S_V = Ints('S_W S_V')
T_W, T_V = Ints('T_W T_V')

# All targets must be 1, 2, or 3
solver.add(Or([I_W == 1, I_W == 2, I_W == 3]))
solver.add(Or([I_V == 1, I_V == 2, I_V == 3]))
solver.add(Or([S_W == 1, S_W == 2, S_W == 3]))
solver.add(Or([S_V == 1, S_V == 2, S_V == 3]))
solver.add(Or([T_W == 1, T_W == 2, T_W == 3]))
solver.add(Or([T_V == 1, T_V == 2, T_V == 3]))

# Constraint 1: For each client, website target ≤ voicemail target
solver.add(I_W <= I_V)
solver.add(S_W <= S_V)
solver.add(T_W <= T_V)

# Constraint 2: Image's voicemail target < other clients' voicemail targets
solver.add(I_V < S_V)
solver.add(I_V < T_V)

# Constraint 3: Solide's website target < Truvest's website target
solver.add(S_W < T_W)

# Now we need to check each option to see if it CANNOT appear more than once
# For each option, we check if it's IMPOSSIBLE for that target to appear more than once
# If it's impossible (unsat), then that's the answer

found_options = []

# Option A: a 1-day website target CANNOT appear more than once?
# Check if it's impossible for at least 2 website targets to be 1
opt_a_constr = Or(
    And(I_W == 1, S_W == 1),
    And(I_W == 1, T_W == 1),
    And(S_W == 1, T_W == 1)
)

# Option B: a 2-day voicemail target CANNOT appear more than once?
opt_b_constr = Or(
    And(I_V == 2, S_V == 2),
    And(I_V == 2, T_V == 2),
    And(S_V == 2, T_V == 2)
)

# Option C: a 2-day website target CANNOT appear more than once?
opt_c_constr = Or(
    And(I_W == 2, S_W == 2),
    And(I_W == 2, T_W == 2),
    And(S_W == 2, T_W == 2)
)

# Option D: a 3-day voicemail target CANNOT appear more than once?
opt_d_constr = Or(
    And(I_V == 3, S_V == 3),
    And(I_V == 3, T_V == 3),
    And(S_V == 3, T_V == 3)
)

# Option E: a 3-day website target CANNOT appear more than once?
opt_e_constr = Or(
    And(I_W == 3, S_W == 3),
    And(I_W == 3, T_W == 3),
    And(S_W == 3, T_W == 3)
)

# For each option, check if adding the constraint that it CAN appear more than once
# leads to unsat (meaning it CANNOT appear more than once)
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), 
                       ("C", opt_c_constr), ("D", opt_d_constr), 
                       ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
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