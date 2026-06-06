from z3 import *

# Variables for letters
D, O, N, A, L, G, E, R, B, T = Ints('D O N A L G E R B T')
letters = [D, O, N, A, L, G, E, R, B, T]

# Carry variables c0..c4 (c0 from units to tens, etc.)
c0, c1, c2, c3, c4 = Ints('c0 c1 c2 c3 c4')

s = Solver()
# Domain for letters 0-9
for v in letters:
    s.add(v >= 0, v <= 9)
# Distinct letters
s.add(Distinct(letters))
# Leading non-zero
s.add(D != 0, G != 0, R != 0)
# Domain for carries
s.add(c0 >= 0, c0 <= 1)
for c in [c1, c2, c3]:
    s.add(c >= 0, c <= 2)
# c4 must be 1 (as derived)
s.add(c4 == 1)

# Column constraints
# Units: D + D = T + 10*c0
s.add(2*D == T + 10*c0)
# Tens: L + L + c0 = R + 10*c1
s.add(2*L + c0 == R + 10*c1)
# Hundreds: A + A + c1 = E + 10*c2
s.add(2*A + c1 == E + 10*c2)
# Thousands: N + R + c2 = B + 10*c3
s.add(N + R + c2 == B + 10*c3)
# Ten-thousands: O + E + c3 = O + 10*c4  => simplifies to E + c3 == 10*c4
s.add(E + c3 == 10*c4)
# Hundred-thousands: D + G + c4 = R (no further carry)
s.add(D + G + c4 == R)

# Solve
res = s.check()
if res == sat:
    m = s.model()
    print("STATUS: sat")
    for name, var in [('D', D), ('O', O), ('N', N), ('A', A), ('L', L), ('G', G), ('E', E), ('R', R), ('B', B), ('T', T)]:
        print(f"{name} = {m[var]}")
    # compute numbers
    DONALD = m.evaluate(D*10**5 + O*10**4 + N*10**3 + A*10**2 + L*10 + D).as_long()
    GERALD = m.evaluate(G*10**5 + E*10**4 + R*10**3 + A*10**2 + L*10 + D).as_long()
    ROBERT = m.evaluate(R*10**5 + O*10**4 + B*10**3 + E*10**2 + R*10 + T).as_long()
    print(f"{DONALD} + {GERALD} = {ROBERT}")
else:
    print("STATUS: unsat")