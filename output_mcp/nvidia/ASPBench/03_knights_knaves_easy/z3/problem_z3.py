from z3 import *

# Boolean variables: True means the person is a knight
alice_k = Bool('alice_k')
bob_k   = Bool('bob_k')
charlie_k = Bool('charlie_k')

solver = Solver()

# 1. Alice says: "Bob is a knave"
#    Statement truth = (bob_k == False)
#    So alice_k == (bob_k == False)  <=> alice_k == Not(bob_k)
solver.add(alice_k == Not(bob_k))

# 2. Bob says: "Alice and Charlie are of the same type"
#    Statement truth = (alice_k == charlie_k)
#    So bob_k == (alice_k == charlie_k)
solver.add(bob_k == (alice_k == charlie_k))

# 3. Charlie says: "Alice is a knight"
#    Statement truth = (alice_k == True)
#    So charlie_k == alice_k
solver.add(charlie_k == alice_k)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("alice =", m[alice_k])
    print("bob   =", m[bob_k])
    print("charlie =", m[charlie_k])
else:
    print("STATUS: unsat")