from z3 import *

# Define boolean variables for each person
A = Bool('Alice')
B = Bool('Bob')
C = Bool('Charlie')
D = Bool('Diana')
E = Bool('Ethan')
F = Bool('Fiona')
G = Bool('George')
H = Bool('Hannah')
I = Bool('Ian')
J = Bool('Julia')
K = Bool('Kevin')
L = Bool('Lily')
M = Bool('Mason')
N = Bool('Nina')
O = Bool('Oliver')
P = Bool('Paula')
Q = Bool('Quentin')
R = Bool('Rachel')
S = Bool('Sam')
T = Bool('Tina')
U = Bool('Ursula')
V = Bool('Victor')
W = Bool('Wendy')
X = Bool('Xavier')

# Helper: sum of bools

def sum_bools(lst):
    return Sum([If(b, 1, 0) for b in lst])

# Group A statements
alice_stmt = And(Not(H), Or(Not(B), C), sum_bools([A,B,C,D,E,F,G,H]) == 4)
bob_stmt = (D == B)
charlie_stmt = sum_bools([A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X]) == 12
diana_stmt = And(Xor(E, F), Not(H))
ethan_stmt = Iff(G, A)
fiona_stmt = And(Xor(B, C), F)
george_stmt = (A == H)
hannah_stmt = sum_bools([B,C,D]) == 1

# Group B statements
ian_stmt = And(A == P, Not(J))
julia_stmt = And(K, N)
kevin_stmt = Or(O, Not(L))
lily_stmt = And(sum_bools([I,J,K,L,M,N,O,P]) == 4, Not(O))
 mason_stmt = And(B == E, Not(J))
nina_stmt = Xor(I, P)
oliver_stmt = sum_bools([G,H,I,J]) == 2
paula_stmt = Iff(R, Not(Q))

# Group C statements
quentin_stmt = sum_bools([Q,R,S,T,U,V,W,X]) >= 5
rachel_stmt = And(C, L, Not(V))
sam_stmt = And(Not(T), Not(O), Not(U))
tina_stmt = Or(Not(R), Not(M))
ursula_stmt = And(I, J)
victor_stmt = sum_bools([Not(A), Not(B), Not(C), Not(D)]) == 2
wendy_stmt = And(Not(V), Not(U), X)
xavier_stmt = And(sum_bools([Q,R,S,T,U,V,W,X]) == 4, S)

# Create solver and add constraints
solver = Solver()

# Each person variable equals the truth of their statement
solver.add(A == alice_stmt)
solver.add(B == bob_stmt)
solver.add(C == charlie_stmt)
solver.add(D == diana_stmt)
solver.add(E == ethan_stmt)
solver.add(F == fiona_stmt)
solver.add(G == george_stmt)
solver.add(H == hannah_stmt)

solver.add(I == ian_stmt)
solver.add(J == julia_stmt)
solver.add(K == kevin_stmt)
solver.add(L == lily_stmt)
solver.add(M == mason_stmt)
solver.add(N == nina_stmt)
solver.add(O == oliver_stmt)
solver.add(P == paula_stmt)

solver.add(Q == quentin_stmt)
solver.add(R == rachel_stmt)
solver.add(S == sam_stmt)
solver.add(T == tina_stmt)
solver.add(U == ursula_stmt)
solver.add(V == victor_stmt)
solver.add(W == wendy_stmt)
solver.add(X == xavier_stmt)

# Check
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print assignments
    for name, var in [
        ('Alice', A), ('Bob', B), ('Charlie', C), ('Diana', D), ('Ethan', E), ('Fiona', F), ('George', G), ('Hannah', H),
        ('Ian', I), ('Julia', J), ('Kevin', K), ('Lily', L), ('Mason', M), ('Nina', N), ('Oliver', O), ('Paula', P),
        ('Quentin', Q), ('Rachel', R), ('Sam', S), ('Tina', T), ('Ursula', U), ('Victor', V), ('Wendy', W), ('Xavier', X)
    ]:
        val = m[var]
        print(f"{name} = {'knight' if is_true(val) else 'knave'}")
elif result == unsat:
    print("STATUS: unsat")
    if True:  # BENCHMARK_MODE
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")