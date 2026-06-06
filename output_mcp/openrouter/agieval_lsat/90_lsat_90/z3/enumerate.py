from z3 import *
solver = Solver()
P = [Int(f'p{i}') for i in range(1,6)]
T = [Int(f't{i}') for i in range(1,6)]
for i in range(5):
    solver.add(Or(P[i]==0, P[i]==1))
    solver.add(Or(T[i]==0, T[i]==1))
# constraints
solver.add(T[2]==1)
cond_pair_2_3 = And(T[1]==1, T[2]==1, T[0]==0, T[3]==0, T[4]==0)
cond_pair_3_4 = And(T[2]==1, T[3]==1, T[0]==0, T[1]==0, T[4]==0)
solver.add(Or(cond_pair_2_3, cond_pair_3_4))
solver.add(Or(And(P[3]==0, T[3]==1), And(P[3]==1, T[3]==0))
solver.add(P[1] != P[4])
# no traditional until Wayne modern before first traditional
first_T_cond = If(T[1]==1,
                  And(P[0]==0, T[0]==0),
                  Or(And(P[0]==0, T[0]==0), And(P[1]==0, T[1]==0)))
solver.add(first_T_cond)
# premise
solver.add(P[0]==P[1])

solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {
        'P': [m.eval(P[i]).as_long() for i in range(5)],
        'T': [m.eval(T[i]).as_long() for i in range(5)]
    }
    solutions.append(sol)
    # block
    solver.add(Or([P[i] != m.eval(P[i]) for i in range(5)] + [T[i] != m.eval(T[i]) for i in range(5)]))
print('total', len(solutions))
for s in solutions:
    print(s)