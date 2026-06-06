from z3 import *

# Define the invariant
def get_V(n1, n2, n3):
    return 4 * n1 + 2 * n2 + 1 * n3

# Initial values
V_R_init = get_V(1, 0, 2)
V_S_init = get_V(1, 1, 0)
V_T_init = get_V(0, 3, 0)

# Options:
# (A) R owns {F, G} -> n_R1=2, n_R2=0, n_R3=0. V_R = 8.
# (B) S owns {F, M} -> n_S1=1, n_S2=1, n_S3=0. V_S = 6.
# (C) S owns {G, L} -> n_S1=1, n_S2=1, n_S3=0. V_S = 6.
# (D) T owns {F, O} -> n_T1=1, n_T2=1, n_T3=0. V_T = 6.
# (E) T owns {G, M} -> n_T1=1, n_T2=1, n_T3=0. V_T = 6.

# We need to check which of these CANNOT be true.
# An option CANNOT be true if its V_i != V_i_init.

solver = Solver()

# Define the options as constraints on the final state
# Let n_i1, n_i2, n_i3 be the final counts for company i.
# We want to see which option is impossible.

# Option A: R owns {F, G}
# n_R1 = 2, n_R2 = 0, n_R3 = 0
opt_a_constr = (get_V(2, 0, 0) != V_R_init)

# Option B: S owns {F, M}
# n_S1 = 1, n_S2 = 1, n_S3 = 0
opt_b_constr = (get_V(1, 1, 0) != V_S_init)

# Option C: S owns {G, L}
# n_S1 = 1, n_S2 = 1, n_S3 = 0
opt_c_constr = (get_V(1, 1, 0) != V_S_init)

# Option D: T owns {F, O}
# n_T1 = 1, n_T2 = 1, n_T3 = 0
opt_d_constr = (get_V(1, 1, 0) != V_T_init)

# Option E: T owns {G, M}
# n_T1 = 1, n_T2 = 1, n_T3 = 0
opt_e_constr = (get_V(1, 1, 0) != V_T_init)

# The question asks which one CANNOT be true.
# So we are looking for the option that is TRUE (i.e., the constraint is satisfied).
# Wait, the question is "Which one CANNOT be true".
# So we want to find the option where the invariant is violated.
# Let's rephrase:
# An option is "CANNOT be true" if the invariant is violated.
# So we want to find the option where the invariant is violated.

# Let's test each option:
# If an option violates the invariant, it CANNOT be true.
# If an option satisfies the invariant, it MIGHT be true.

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    # If constr is True, it means the invariant is violated, so it CANNOT be true.
    if constr:
        found_options.append(letter)

print(f"Options that cannot be true: {found_options}")