from z3 import *

solver = Solver()

# Buildings and their classes
# G=Garza(class1), F=Flores(class1)
# L=Lynch(class2), K=King(class2), M=Meyer(class2), O=Ortiz(class2)
# Y=Yates(class3), Z=Zimmer(class3)

# Companies: 0=RealProp, 1=Southco, 2=Trustcorp

# Variables: which company owns each building
G, F = Ints('G F')
L, K, M, O = Ints('L K M O')
Y, Z = Ints('Y Z')

buildings = [G, F, L, K, M, O, Y, Z]

# Domain: each building is owned by one of the three companies
for b in buildings:
    solver.add(b >= 0, b <= 2)

# Class counts per company
R1, R2, R3 = Ints('R1 R2 R3')
S1, S2, S3 = Ints('S1 S2 S3')
T1, T2, T3 = Ints('T1 T2 T3')

# Non-negative
for v in [R1, R2, R3, S1, S2, S3, T1, T2, T3]:
    solver.add(v >= 0)

# Total counts of each class are invariant
solver.add(R1 + S1 + T1 == 2)  # total class 1
solver.add(R2 + S2 + T2 == 4)  # total class 2
solver.add(R3 + S3 + T3 == 2)  # total class 3

# Link building ownership to class counts
solver.add(R1 == Sum([If(G == 0, 1, 0), If(F == 0, 1, 0)]))
solver.add(R2 == Sum([If(L == 0, 1, 0), If(K == 0, 1, 0), If(M == 0, 1, 0), If(O == 0, 1, 0)]))
solver.add(R3 == Sum([If(Y == 0, 1, 0), If(Z == 0, 1, 0)]))

solver.add(S1 == Sum([If(G == 1, 1, 0), If(F == 1, 1, 0)]))
solver.add(S2 == Sum([If(L == 1, 1, 0), If(K == 1, 1, 0), If(M == 1, 1, 0), If(O == 1, 1, 0)]))
solver.add(S3 == Sum([If(Y == 1, 1, 0), If(Z == 1, 1, 0)]))

solver.add(T1 == Sum([If(G == 2, 1, 0), If(F == 2, 1, 0)]))
solver.add(T2 == Sum([If(L == 2, 1, 0), If(K == 2, 1, 0), If(M == 2, 1, 0), If(O == 2, 1, 0)]))
solver.add(T3 == Sum([If(Y == 2, 1, 0), If(Z == 2, 1, 0)]))

# Trade reachability constraints
# Companies: 0=RealProp, 1=Southco, 2=Trustcorp
# a[i][j] = number of rule 2 trades where i gives class 1, j gives two class 2s
# b[i][j] = number of rule 3 trades where i gives class 2, j gives two class 3s

a = [[Int(f'a_{i}_{j}') for j in range(3)] for i in range(3)]
b = [[Int(f'b_{i}_{j}') for j in range(3)] for i in range(3)]

for i in range(3):
    for j in range(3):
        solver.add(a[i][j] >= 0)
        solver.add(b[i][j] >= 0)
    solver.add(a[i][i] == 0)  # can't trade with yourself
    solver.add(b[i][i] == 0)

# Changes for each company
# RealProp (index 0)
dR1 = Sum([a[j][0] - a[0][j] for j in range(3)])
dR2 = Sum([2*a[0][j] - 2*a[j][0] + b[j][0] - b[0][j] for j in range(3)])
dR3 = Sum([2*b[0][j] - 2*b[j][0] for j in range(3)])

# Southco (index 1)
dS1 = Sum([a[j][1] - a[1][j] for j in range(3)])
dS2 = Sum([2*a[1][j] - 2*a[j][1] + b[j][1] - b[1][j] for j in range(3)])
dS3 = Sum([2*b[1][j] - 2*b[j][1] for j in range(3)])

# Trustcorp (index 2)
dT1 = Sum([a[j][2] - a[2][j] for j in range(3)])
dT2 = Sum([2*a[2][j] - 2*a[j][2] + b[j][2] - b[2][j] for j in range(3)])
dT3 = Sum([2*b[2][j] - 2*b[j][2] for j in range(3)])

# Initial state: R=(1,0,2), S=(1,1,0), T=(0,3,0)
# Final state: R=(R1,R2,R3), S=(S1,S2,S3), T=(T1,T2,T3)
solver.add(R1 == 1 + dR1)
solver.add(R2 == 0 + dR2)
solver.add(R3 == 2 + dR3)

solver.add(S1 == 1 + dS1)
solver.add(S2 == 1 + dS2)
solver.add(S3 == 0 + dS3)

solver.add(T1 == 0 + dT1)
solver.add(T2 == 3 + dT2)
solver.add(T3 == 0 + dT3)

# Option A: RealProp owns Flores and Garza.
opt_a_constr = And(G == 0, F == 0,  # RealProp owns Garza and Flores
                   Y != 0, Z != 0,  # RealProp doesn't own Yates or Zimmer
                   L != 0, K != 0, M != 0, O != 0)  # RealProp doesn't own any class 2

# Option B: Southco owns Flores and Meyer.
opt_b_constr = And(F == 1, M == 1,  # Southco owns Flores and Meyer
                   G != 1, L != 1, K != 1, O != 1, Y != 1, Z != 1)  # Southco doesn't own others

# Option C: Southco owns Garza and Lynch.
opt_c_constr = And(G == 1, L == 1,  # Southco owns Garza and Lynch
                   F != 1, K != 1, M != 1, O != 1, Y != 1, Z != 1)  # Southco doesn't own others

# Option D: Trustcorp owns Flores and Ortiz.
opt_d_constr = And(F == 2, O == 2,  # Trustcorp owns Flores and Ortiz
                   G != 2, L != 2, K != 2, M != 2, Y != 2, Z != 2)  # Trustcorp doesn't own others

# Option E: Trustcorp owns Garza and Meyer.
opt_e_constr = And(G == 2, M == 2,  # Trustcorp owns Garza and Meyer
                   F != 2, L != 2, K != 2, O != 2, Y != 2, Z != 2)  # Trustcorp doesn't own others

# Check each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    print(f"Option {letter}: {result}")
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"  G={m[G]}, F={m[F]}, L={m[L]}, K={m[K]}, M={m[M]}, O={m[O]}, Y={m[Y]}, Z={m[Z]}")
        print(f"  R=({m[R1]},{m[R2]},{m[R3]}), S=({m[S1]},{m[S2]},{m[S3]}), T=({m[T1]},{m[T2]},{m[T3]})")
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