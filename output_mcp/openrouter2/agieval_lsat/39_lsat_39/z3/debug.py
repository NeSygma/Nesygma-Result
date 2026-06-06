from z3 import *

solver = Solver()
# Variables
O1,O2,O3 = Ints('O1 O2 O3')
P1,P2,P3 = Ints('P1 P2 P3')
S1,S2,S3 = Ints('S1 S2 S3')

for d in [O1,O2,O3,P1,P2,P3,S1,S2,S3]:
    solver.add(d>=0,d<=4)

solver.add(Distinct(O1,O2,O3))
solver.add(Distinct(P1,P2,P3))
solver.add(Distinct(S1,S2,S3))

solver.add(O1<O2,O2<O3)
solver.add(P1<P2,P2<P3)
solver.add(S1<S2,S2<S3)

solver.add(Or(O1==0,O2==0,O3==0,P1==0,P2==0,P3==0,S1==0,S2==0,S3==0))

solver.add(O2==P1)
solver.add(S2==3)
solver.add(P1==1)

opt_a_constr = Sum([If(O1==0,1,0),If(P1==0,1,0),If(S1==0,1,0)])==2
opt_b_constr = Sum([If(O1==1,1,0),If(P1==1,1,0),If(S1==1,1,0)])==2
opt_c_constr = Sum([If(O2==2,1,0),If(P2==2,1,0),If(S2==2,1,0)])==2
opt_d_constr = Sum([If(O2==3,1,0),If(P2==3,1,0),If(S2==3,1,0)])==2
opt_e_constr = Sum([If(O3==4,1,0),If(P3==4,1,0),If(S3==4,1,0)])==2

for letter,constr in [('A',opt_a_constr),('B',opt_b_constr),('C',opt_c_constr),('D',opt_d_constr),('E',opt_e_constr)]:
    solver.push()
    solver.add(constr)
    res=solver.check()
    print(letter,res)
    if res==sat:
        m=solver.model()
        print('model',m)
    solver.pop()