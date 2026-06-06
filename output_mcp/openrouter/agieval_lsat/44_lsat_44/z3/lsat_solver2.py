from z3 import *

# Students: J, K, L, M, O
plays = ['S', 'T', 'U']
# Bool vars
J = {p: Bool('J_' + p) for p in plays}
K = {p: Bool('K_' + p) for p in plays}
L = {p: Bool('L_' + p) for p in plays}
M = {p: Bool('M_' + p) for p in plays}
O = {p: Bool('O_' + p) for p in plays}

solver = Solver()
# each student at least one play
for student in [J, K, L, M, O]:
    solver.add(Or([student[p] for p in plays]))

def cnt(st):
    return Sum([If(st[p],1,0) for p in plays])
# Kramer and Lopez fewer than Megregian
solver.add(cnt(K) < cnt(M))
solver.add(cnt(L) < cnt(M))
# Lopez and Megregian do not review any play Jiang reviews
for p in plays:
    solver.add(Implies(J[p], Not(L[p])))
    solver.add(Implies(J[p], Not(M[p])))
# Kramer and O'Neill both review Tamerlane
solver.add(K['T'] == True)
solver.add(O['T'] == True)
# Exactly one pair identical
students = {'J':J,'K':K,'L':L,'M':M,'O':O}
pair_eq = []
names = list(students.keys())
for i in range(len(names)):
    for j in range(i+1, len(names)):
        si = students[names[i]]
        sj = students[names[j]]
        eq = And([si[p]==sj[p] for p in plays])
        pair_eq.append(If(eq,1,0))
solver.add(Sum(pair_eq) == 1)

# Options definitions
opt_a = cnt(J) > cnt(L)  # A
opt_b = cnt(M) > cnt(J)  # B
opt_c = cnt(M) > cnt(O)  # C
opt_d = cnt(O) > cnt(J)  # D
opt_e = cnt(O) > cnt(K)  # E
options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

must = []
for letter, constr in options:
    solver.push()
    # add negation of option; if unsat then option must be true
    solver.add(Not(constr))
    res = solver.check()
    if res == unsat:
        must.append(letter)
    solver.pop()

if len(must) == 1:
    print("STATUS: sat")
    print(f"answer:{must[0]}")
elif len(must) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true option found")