from z3 import *

# Buildings and their classes
# G:1, Y:3, Z:3, F:1, L:2, K:2, M:2, O:2
# Classes: 1: {G, F}, 2: {L, K, M, O}, 3: {Y, Z}

# Initial ownership:
# R: {G, Y, Z} -> n_R1=1, n_R2=0, n_R3=2
# S: {F, L}    -> n_S1=1, n_S2=1, n_S3=0
# T: {K, M, O} -> n_T1=0, n_T2=3, n_T3=0

# Invariant: V_i = 4*n_i1 + 2*n_i2 + 1*n_i3
# V_R = 4(1) + 2(0) + 1(2) = 6
# V_S = 4(1) + 2(1) + 1(0) = 6
# V_T = 4(0) + 2(3) + 1(0) = 6

# Total buildings:
# Class 1: 2 (G, F)
# Class 2: 4 (L, K, M, O)
# Class 3: 2 (Y, Z)

def get_V(n1, n2, n3):
    return 4 * n1 + 2 * n2 + 1 * n3

# Check each option:
# (A) R owns {F, G} -> n_R1=2, n_R2=0, n_R3=0. V_R = 4(2) + 2(0) + 1(0) = 8. (Initial V_R=6)
# (B) S owns {F, M} -> n_S1=1, n_S2=1, n_S3=0. V_S = 4(1) + 2(1) + 1(0) = 6. (Initial V_S=6)
# (C) S owns {G, L} -> n_S1=1, n_S2=1, n_S3=0. V_S = 4(1) + 2(1) + 1(0) = 6. (Initial V_S=6)
# (D) T owns {F, O} -> n_T1=1, n_T2=1, n_T3=0. V_T = 4(1) + 2(1) + 1(0) = 6. (Initial V_T=6)
# (E) T owns {G, M} -> n_T1=1, n_T2=1, n_T3=0. V_T = 4(1) + 2(1) + 1(0) = 6. (Initial V_T=6)

# Wait, the invariant only says V_i must be 6. It doesn't guarantee reachability.
# Let's re-check the options.
# (A) R owns {F, G}. V_R = 8. Since V_R must be 6, this is impossible.
# (B) S owns {F, M}. V_S = 6. Possible?
# (C) S owns {G, L}. V_S = 6. Possible?
# (D) T owns {F, O}. V_T = 6. Possible?
# (E) T owns {G, M}. V_T = 6. Possible?

# Let's verify the invariant again.
# Trade 1: (1,1), (2,2), (3,3). V_i change: 0.
# Trade 2: (1, 2+2). A gives 1, gets 2. V_A change: -4 + 2(2) = 0.
# Trade 3: (2, 3+3). A gives 2, gets 3. V_A change: -2 + 2(1) = 0.
# Yes, the invariant is correct.

# Let's check if (A) is the only one that violates the invariant.
# If (A) is the only one that violates it, then (A) is the answer.

print(f"V_R_initial = {get_V(1, 0, 2)}")
print(f"V_S_initial = {get_V(1, 1, 0)}")
print(f"V_T_initial = {get_V(0, 3, 0)}")

print(f"V_A = {get_V(2, 0, 0)}") # R owns {F, G}
print(f"V_B = {get_V(1, 1, 0)}") # S owns {F, M}
print(f"V_C = {get_V(1, 1, 0)}") # S owns {G, L}
print(f"V_D = {get_V(1, 1, 0)}") # T owns {F, O}
print(f"V_E = {get_V(1, 1, 0)}") # T owns {G, M}