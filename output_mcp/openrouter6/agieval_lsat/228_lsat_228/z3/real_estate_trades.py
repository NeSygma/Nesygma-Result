from z3 import *

# Define trade variables
a_RS, a_RT, a_SR, a_ST, a_TR, a_TS = Ints('a_RS a_RT a_SR a_ST a_TR a_TS')
b_RS, b_RT, b_SR, b_ST, b_TR, b_TS = Ints('b_RS b_RT b_SR b_ST b_TR b_TS')

# All trade counts must be non-negative
solver = Solver()
solver.add(a_RS >= 0, a_RT >= 0, a_SR >= 0, a_ST >= 0, a_TR >= 0, a_TS >= 0)
solver.add(b_RS >= 0, b_RT >= 0, b_SR >= 0, b_ST >= 0, b_TR >= 0, b_TS >= 0)

# Initial counts
# RealProp: class1=1, class2=0, class3=2
# Southco: class1=1, class2=1, class3=0
# Trustcorp: class1=0, class2=3, class3=0

# Net changes from trades
delta_R1 = - (a_RS + a_RT) + (a_SR + a_TR)
delta_R2 = 2*(a_RS + a_RT) - 2*(a_SR + a_TR) + ( - (b_RS + b_RT) + (b_SR + b_TR) )
delta_R3 = 2*(b_RS + b_RT) - 2*(b_SR + b_TR)

delta_S1 = - (a_SR + a_ST) + (a_RS + a_TS)
delta_S2 = 2*(a_SR + a_ST) - 2*(a_RS + a_TS) + ( - (b_SR + b_ST) + (b_RS + b_TS) )
delta_S3 = 2*(b_SR + b_ST) - 2*(b_RS + b_TS)

delta_T1 = - (a_TR + a_TS) + (a_RT + a_ST)
delta_T2 = 2*(a_TR + a_TS) - 2*(a_RT + a_ST) + ( - (b_TR + b_TS) + (b_RT + b_ST) )
delta_T3 = 2*(b_TR + b_TS) - 2*(b_RT + b_ST)

# Final counts
R1 = 1 + delta_R1
R2 = 0 + delta_R2
R3 = 2 + delta_R3

S1 = 1 + delta_S1
S2 = 1 + delta_S2
S3 = 0 + delta_S3

T1 = 0 + delta_T1
T2 = 3 + delta_T2
T3 = 0 + delta_T3

# Condition: RealProp owns only class 2 buildings
solver.add(R1 == 0)
solver.add(R3 == 0)
# Also, counts must be non-negative
solver.add(R2 >= 0)
solver.add(S1 >= 0, S2 >= 0, S3 >= 0)
solver.add(T1 >= 0, T2 >= 0, T3 >= 0)

# Total class counts must be preserved (should be automatically satisfied, but we add for clarity)
solver.add(S1 + T1 == 2)  # class 1 total
solver.add(S2 + T2 + R2 == 4)  # class 2 total
solver.add(S3 + T3 == 2)  # class 3 total

# Now, we check each answer choice by seeing if its negation is satisfiable.
# If negation is unsatisfiable, then the choice must be true.

# We'll use a loop to test each option.
options = [
    ("A", T1 >= 1),  # Trustcorp owns a class 1 building
    ("B", None),     # We'll handle separately (specific building)
    ("C", S2 >= 1),  # Southco owns a class 2 building
    ("D", S3 == 2),  # Southco owns both class 3 buildings
    ("E", None)      # We'll handle separately (specific building)
]

# For options B and E, we need to model specific buildings.
# Let's define variables for the owners of specific buildings.
# We'll use integers 0=R, 1=S, 2=T.
G_owner = Int('G_owner')  # Garza Tower (class 1)
F_owner = Int('F_owner')  # Flores Tower (class 1)
Y_owner = Int('Y_owner')  # Yates House (class 3)
Z_owner = Int('Z_owner')  # Zimmer House (class 3)
M_owner = Int('M_owner')  # Meyer Building (class 2)

# Constraints on owners: must be 0,1,2
solver.add(Or([G_owner == i for i in range(3)]))
solver.add(Or([F_owner == i for i in range(3)]))
solver.add(Or([Y_owner == i for i in range(3)]))
solver.add(Or([Z_owner == i for i in range(3)]))
solver.add(Or([M_owner == i for i in range(3)]))

# Since RealProp owns only class 2, it cannot own class 1 or class 3 buildings.
solver.add(G_owner != 0)
solver.add(F_owner != 0)
solver.add(Y_owner != 0)
solver.add(Z_owner != 0)

# The final class counts must match the ownership of specific buildings.
# For class 1: R1=0, so G_owner and F_owner are not 0.
# For class 3: R3=0, so Y_owner and Z_owner are not 0.
# For class 2: R2 is the number of class 2 buildings owned by R.
# We have four class 2 buildings: Lynch, King, Meyer, Ortiz.
# We'll define variables for their owners, but we can use the counts.
# Let's define L_owner, K_owner, O_owner similarly.
L_owner = Int('L_owner')
K_owner = Int('K_owner')
O_owner = Int('O_owner')
solver.add(Or([L_owner == i for i in range(3)]))
solver.add(Or([K_owner == i for i in range(3)]))
solver.add(Or([O_owner == i for i in range(3)]))

# Now, the number of class 2 buildings owned by each company must match R2, S2, T2.
# We'll add constraints that count the number of class 2 buildings owned by each.
# For R: count of class 2 buildings owned by R equals R2.
# We'll use If expressions to count.
class2_owners = [L_owner, K_owner, M_owner, O_owner]
R2_count = Sum([If(o == 0, 1, 0) for o in class2_owners])
S2_count = Sum([If(o == 1, 1, 0) for o in class2_owners])
T2_count = Sum([If(o == 2, 1, 0) for o in class2_owners])

solver.add(R2_count == R2)
solver.add(S2_count == S2)
solver.add(T2_count == T2)

# Similarly for class 1 and class 3, but we already have R1=0, R3=0.
# For class 1: two buildings, owners G_owner and F_owner.
# The number of class 1 buildings owned by S is S1, by T is T1.
S1_count = If(G_owner == 1, 1, 0) + If(F_owner == 1, 1, 0)
T1_count = If(G_owner == 2, 1, 0) + If(F_owner == 2, 1, 0)
solver.add(S1_count == S1)
solver.add(T1_count == T1)

# For class 3: two buildings, owners Y_owner and Z_owner.
S3_count = If(Y_owner == 1, 1, 0) + If(Z_owner == 1, 1, 0)
T3_count = If(Y_owner == 2, 1, 0) + If(Z_owner == 2, 1, 0)
solver.add(S3_count == S3)
solver.add(T3_count == T3)

# Now, we test each option by checking if its negation is satisfiable.
# We'll create a list of (letter, constraint) for options that are not specific buildings.
# For specific buildings, we'll add the constraint directly.

found_options = []

# Option A: Trustcorp owns a class 1 building (T1 >= 1)
# Negation: T1 == 0
solver.push()
solver.add(T1 == 0)
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: Trustcorp owns the Meyer Building (M_owner == 2)
solver.push()
solver.add(M_owner != 2)  # negation
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: Southco owns a class 2 building (S2 >= 1)
solver.push()
solver.add(S2 == 0)  # negation
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: Southco owns both class 3 buildings (S3 == 2)
solver.push()
solver.add(S3 != 2)  # negation
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: Southco owns the Flores Tower (F_owner == 1)
solver.push()
solver.add(F_owner != 1)  # negation
if solver.check() == unsat:
    found_options.append("E")
solver.pop()

# Now, according to the problem, exactly one option must be true.
# If found_options has exactly one element, that is the answer.
# If more than one, then the model is under-constrained (should not happen).
# If none, then no option is forced (should not happen).

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")