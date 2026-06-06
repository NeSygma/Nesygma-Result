from z3 import *

# Define trade variables for each pair and trade type
# For pair (R,S):
u = Int('u_RS2')  # R gives to S type2
v = Int('v_RS2')  # S gives to R type2
w = Int('w_RS3')  # R gives to S type3
x = Int('x_RS3')  # S gives to R type3

# For pair (R,T):
a = Int('a_RT2')  # R gives to T type2
b = Int('b_RT2')  # T gives to R type2
c = Int('c_RT3')  # R gives to T type3
d = Int('d_RT3')  # T gives to R type3

# For pair (S,T):
e = Int('e_ST2')  # S gives to T type2
f = Int('f_ST2')  # T gives to S type2
g = Int('g_ST3')  # S gives to T type3
h = Int('h_ST3')  # T gives to S type3

# All trade variables are non-negative integers
trade_vars = [u, v, w, x, a, b, c, d, e, f, g, h]
solver = Solver()
for var in trade_vars:
    solver.add(var >= 0)
    solver.add(var <= 4)  # Bound to make search finite

# Initial counts
R1_i, R2_i, R3_i = 1, 0, 2
S1_i, S2_i, S3_i = 1, 1, 0
T1_i, T2_i, T3_i = 0, 3, 0

# Final counts
R1 = R1_i + v - u + b - a
R2 = R2_i + 2*u - 2*v - w + x + 2*a - 2*b - c + d
R3 = R3_i + 2*w - 2*x + 2*c - 2*d

S1 = S1_i + u - v + e - f
S2 = S2_i + 2*v - 2*u + w - x + 2*f - 2*e - g + h
S3 = S3_i + 2*x - 2*w + 2*g - 2*h

T1 = T1_i + a - b + e - f
T2 = T2_i + 2*b - 2*a + 2*f - 2*e + c - d + g - h
T3 = T3_i + 2*d - 2*c + 2*h - 2*g

# Constraints: all counts non-negative
solver.add(R1 >= 0, R2 >= 0, R3 >= 0)
solver.add(S1 >= 0, S2 >= 0, S3 >= 0)
solver.add(T1 >= 0, T2 >= 0, T3 >= 0)

# Condition: Trustcorp owns no class 2 buildings
solver.add(T2 == 0)

# Check that base constraints are satisfiable
if solver.check() != sat:
    print("STATUS: unsat")
    print("Base constraints unsatisfiable - refine")
else:
    # Now test each answer choice for necessity
    # We'll check if the negation of each statement is unsatisfiable
    options = []
    
    # (A) RealProp owns a class 1 building. (R1 >= 1)
    sA = Solver()
    sA.add(solver.assertions())
    sA.add(R1 == 0)  # Negation: RealProp does NOT own a class 1 building
    if sA.check() == unsat:
        options.append('A')
    
    # (B) Southco owns only class 2 buildings. (S1 == 0 and S3 == 0)
    sB = Solver()
    sB.add(solver.assertions())
    sB.add(Or(S1 > 0, S3 > 0))  # Negation: Southco owns at least one non-class2 building
    if sB.check() == unsat:
        options.append('B')
    
    # (C) Southco has made at least one trade with Trustcorp.
    # This means at least one of e,f,g,h > 0
    sC = Solver()
    sC.add(solver.assertions())
    sC.add(e == 0, f == 0, g == 0, h == 0)  # Negation: no trades between S and T
    if sC.check() == unsat:
        options.append('C')
    
    # (D) Trustcorp owns the Garza Tower. (Garza is class1, so T1 >= 1 and specifically Garza)
    # Since buildings are indistinguishable by class, we interpret as T1 >= 1
    sD = Solver()
    sD.add(solver.assertions())
    sD.add(T1 == 0)  # Negation: Trustcorp owns no class1 building
    if sD.check() == unsat:
        options.append('D')
    
    # (E) Trustcorp owns the Zimmer House. (Zimmer is class3, so T3 >= 1)
    sE = Solver()
    sE.add(solver.assertions())
    sE.add(T3 == 0)  # Negation: Trustcorp owns no class3 building
    if sE.check() == unsat:
        options.append('E')
    
    # Determine the answer
    if len(options) == 1:
        print("STATUS: sat")
        print(f"answer:{options[0]}")
    elif len(options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")