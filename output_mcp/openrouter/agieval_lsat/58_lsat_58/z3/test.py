from z3 import *

# candidates indices
J, K, L, N, O = 0,1,2,3,4
V, Y, Z = Ints('V Y Z')
solver = Solver()
# domain constraints
solver.add(And(V >= 0, V <= 4))
solver.add(And(Y >= 0, Y <= 4))
solver.add(And(Z >= 0, Z <= 4))
# distinct
solver.add(Distinct(V, Y, Z))
# helper booleans
K_assigned = Or(V == K, Y == K, Z == K)
N_assigned = Or(V == N, Y == N, Z == N)
J_assigned = Or(V == J, Y == J, Z == J)
L_assigned = Or(V == L, Y == L, Z == L)
O_assigned = Or(V == O, Y == O, Z == O)
# constraints
solver.add(Xor(K_assigned, N_assigned))
solver.add(Implies(J_assigned, K_assigned))
solver.add(Implies(V == O, Not(Y == K)))
solver.add(Implies(L_assigned, Z == L))

options = {
    "A": Z == J,
    "B": Z == K,
    "C": Z == N,
    "D": Not(L_assigned),
    "E": Not(O_assigned)
}

for name, constr in options.items():
    s = Solver()
    s.add(solver.assertions())
    s.add(constr)
    res = s.check()
    print(name, res)