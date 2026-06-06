from z3 import *

solver = Solver()

# Variables
I_w, I_v = Ints('I_w I_v')
S_w, S_v = Ints('S_w S_v')
T_w, T_v = Ints('T_w T_v')

# Domain: 1, 2, or 3
for var in [I_w, I_v, S_w, S_v, T_w, T_v]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Condition 1: website <= voicemail for each client
solver.add(I_w <= I_v)
solver.add(S_w <= S_v)
solver.add(T_w <= T_v)

# Condition 2: Image's voicemail shorter than others' voicemail
solver.add(I_v < S_v)
solver.add(I_v < T_v)

# Condition 3: Solide's website shorter than Truvest's website
solver.add(S_w < T_w)

# Now evaluate each option
# Each option: "X target" (e.g., a 1-day website target) cannot be set for MORE THAN ONE client.
# So we test: can more than one client have that target?
# If UNSAT, then that option is the answer.

found_options = []

# Option A: a 1-day website target
solver.push()
solver.add(
    Or(
        And(I_w == 1, S_w == 1),
        And(I_w == 1, T_w == 1),
        And(S_w == 1, T_w == 1)
    )
)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: a 2-day voicemail target
solver.push()
solver.add(
    Or(
        And(I_v == 2, S_v == 2),
        And(I_v == 2, T_v == 2),
        And(S_v == 2, T_v == 2)
    )
)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: a 2-day website target
solver.push()
solver.add(
    Or(
        And(I_w == 2, S_w == 2),
        And(I_w == 2, T_w == 2),
        And(S_w == 2, T_w == 2)
    )
)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: a 3-day voicemail target
solver.push()
solver.add(
    Or(
        And(I_v == 3, S_v == 3),
        And(I_v == 3, T_v == 3),
        And(S_v == 3, T_v == 3)
    )
)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: a 3-day website target
solver.push()
solver.add(
    Or(
        And(I_w == 3, S_w == 3),
        And(I_w == 3, T_w == 3),
        And(S_w == 3, T_w == 3)
    )
)
if solver.check() == sat:
    found_options.append('E')
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