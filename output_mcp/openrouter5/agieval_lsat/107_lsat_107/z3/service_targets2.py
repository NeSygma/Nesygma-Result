from z3 import *

# Clients: Image (I), Solide (S), Truvest (T)
# Targets: 1, 2, or 3 days (1 = shortest, 3 = longest)
# For each client: website target and voicemail target

W_I, W_S, W_T = Ints('W_I W_S W_T')
V_I, V_S, V_T = Ints('V_I V_S V_T')

solver = Solver()

# Domain: each target is 1, 2, or 3
for var in [W_I, W_S, W_T, V_I, V_S, V_T]:
    solver.add(Or(var == 1, var == 2, var == 3))

# Condition 1: website <= voicemail for each client
solver.add(W_I <= V_I)
solver.add(W_S <= V_S)
solver.add(W_T <= V_T)

# Condition 2: V_I < V_S and V_I < V_T
solver.add(V_I < V_S)
solver.add(V_I < V_T)

# Condition 3: W_S < W_T
solver.add(W_S < W_T)

# The question asks: which target CANNOT be set for more than one of the clients?
# This means: for which target type (e.g., "1-day website") is it IMPOSSIBLE
# for two or more clients to share that same target value?

# Let's enumerate all valid solutions and see which target values appear
# for more than one client in any solution.

# First, let's find all solutions and track which target types appear for >=2 clients
# We'll use a different approach: for each option, check if it's POSSIBLE (sat)
# for that target to appear for >=2 clients. The one that's UNSAT is the answer.

# But we got multiple SATs before. Let me re-read the problem more carefully.

# "Which one of the following targets CANNOT be set for more than one of the clients?"
# This means: which of these five specific target types is impossible to assign
# to two or more different clients simultaneously?

# Let me check each one more carefully.

# Option A: a 1-day website target for more than one client
# i.e., at least two of {W_I, W_S, W_T} are 1
opt_a_constr = Sum([If(W_I == 1, 1, 0), If(W_S == 1, 1, 0), If(W_T == 1, 1, 0)]) >= 2

# Option B: a 2-day voicemail target for more than one client
opt_b_constr = Sum([If(V_I == 2, 1, 0), If(V_S == 2, 1, 0), If(V_T == 2, 1, 0)]) >= 2

# Option C: a 2-day website target for more than one client
opt_c_constr = Sum([If(W_I == 2, 1, 0), If(W_S == 2, 1, 0), If(W_T == 2, 1, 0)]) >= 2

# Option D: a 3-day voicemail target for more than one client
opt_d_constr = Sum([If(V_I == 3, 1, 0), If(V_S == 3, 1, 0), If(V_T == 3, 1, 0)]) >= 2

# Option E: a 3-day website target for more than one client
opt_e_constr = Sum([If(W_I == 3, 1, 0), If(W_S == 3, 1, 0), If(W_T == 3, 1, 0)]) >= 2

# Let me also print all valid models to understand the space
print("=== All valid assignments ===")
solver_all = Solver()
for var in [W_I, W_S, W_T, V_I, V_S, V_T]:
    solver_all.add(Or(var == 1, var == 2, var == 3))
solver_all.add(W_I <= V_I)
solver_all.add(W_S <= V_S)
solver_all.add(W_T <= V_T)
solver_all.add(V_I < V_S)
solver_all.add(V_I < V_T)
solver_all.add(W_S < W_T)

count = 0
while solver_all.check() == sat and count < 50:
    m = solver_all.model()
    print(f"W_I={m[W_I]}, W_S={m[W_S]}, W_T={m[W_T]}, V_I={m[V_I]}, V_S={m[V_S]}, V_T={m[V_T]}")
    solver_all.add(Or(W_I != m[W_I], W_S != m[W_S], W_T != m[W_T], V_I != m[V_I], V_S != m[V_S], V_T != m[V_T]))
    count += 1
print(f"Total solutions found: {count}")

# Now test each option
print("\n=== Testing each option ===")
for letter, constr, desc in [("A", opt_a_constr, "1-day website for >=2 clients"),
                               ("B", opt_b_constr, "2-day voicemail for >=2 clients"),
                               ("C", opt_c_constr, "2-day website for >=2 clients"),
                               ("D", opt_d_constr, "3-day voicemail for >=2 clients"),
                               ("E", opt_e_constr, "3-day website for >=2 clients")]:
    s = Solver()
    for var in [W_I, W_S, W_T, V_I, V_S, V_T]:
        s.add(Or(var == 1, var == 2, var == 3))
    s.add(W_I <= V_I)
    s.add(W_S <= V_S)
    s.add(W_T <= V_T)
    s.add(V_I < V_S)
    s.add(V_I < V_T)
    s.add(W_S < W_T)
    s.add(constr)
    res = s.check()
    print(f"Option {letter} ({desc}): {res}")
    if res == sat:
        m = s.model()
        print(f"  Example: W_I={m[W_I]}, W_S={m[W_S]}, W_T={m[W_T]}, V_I={m[V_I]}, V_S={m[V_S]}, V_T={m[V_T]}")

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    s = Solver()
    for var in [W_I, W_S, W_T, V_I, V_S, V_T]:
        s.add(Or(var == 1, var == 2, var == 3))
    s.add(W_I <= V_I)
    s.add(W_S <= V_S)
    s.add(W_T <= V_T)
    s.add(V_I < V_S)
    s.add(V_I < V_T)
    s.add(W_S < W_T)
    s.add(constr)
    if s.check() == sat:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")