from z3 import *

# Clients: Image (I), Solide (S), Truvest (T)
# Targets: 1, 2, or 3 days (1 = shortest, 3 = longest)
# For each client: website target and voicemail target

# Variables: W_I, W_S, W_T = website targets; V_I, V_S, V_T = voicemail targets
W_I, W_S, W_T = Ints('W_I W_S W_T')
V_I, V_S, V_T = Ints('V_I V_S V_T')

solver = Solver()

# Domain: each target is 1, 2, or 3
for var in [W_I, W_S, W_T, V_I, V_S, V_T]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Condition 1: None of the clients can have a website target that is longer than its voicemail target.
# i.e., website <= voicemail for each client
solver.add(W_I <= V_I)
solver.add(W_S <= V_S)
solver.add(W_T <= V_T)

# Condition 2: Image's voicemail target must be shorter than the other clients' voicemail targets.
# i.e., V_I < V_S and V_I < V_T
solver.add(V_I < V_S)
solver.add(V_I < V_T)

# Condition 3: Solide's website target must be shorter than Truvest's website target.
# i.e., W_S < W_T
solver.add(W_S < W_T)

# Now evaluate each option: which target type CANNOT be set for more than one client?
# We need to check if it's possible for that target value to appear for more than one client.
# For each option, we check if there exists a solution where at least two clients share that target.

# Option A: a 1-day website target (W_I=1, W_S=1, or W_T=1) for more than one client
# i.e., at least two of {W_I, W_S, W_T} are 1
opt_a_constr = Sum([If(W_I == 1, 1, 0), If(W_S == 1, 1, 0), If(W_T == 1, 1, 0)]) >= 2

# Option B: a 2-day voicemail target (V_I=2, V_S=2, or V_T=2) for more than one client
opt_b_constr = Sum([If(V_I == 2, 1, 0), If(V_S == 2, 1, 0), If(V_T == 2, 1, 0)]) >= 2

# Option C: a 2-day website target (W_I=2, W_S=2, or W_T=2) for more than one client
opt_c_constr = Sum([If(W_I == 2, 1, 0), If(W_S == 2, 1, 0), If(W_T == 2, 1, 0)]) >= 2

# Option D: a 3-day voicemail target (V_I=3, V_S=3, or V_T=3) for more than one client
opt_d_constr = Sum([If(V_I == 3, 1, 0), If(V_S == 3, 1, 0), If(V_T == 3, 1, 0)]) >= 2

# Option E: a 3-day website target (W_I=3, W_S=3, or W_T=3) for more than one client
opt_e_constr = Sum([If(W_I == 3, 1, 0), If(W_S == 3, 1, 0), If(W_T == 3, 1, 0)]) >= 2

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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