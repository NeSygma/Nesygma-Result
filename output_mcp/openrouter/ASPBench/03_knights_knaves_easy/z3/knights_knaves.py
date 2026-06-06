from z3 import *

# Bool variables: True = knight, False = knave
alice = Bool('alice')
bob = Bool('bob')
charlie = Bool('charlie')

solver = Solver()

# Constraints based on statements
# Alice says: "Bob is a knave" -> statement = Not(bob)
# If alice is knight then statement true, if knave then statement false
solver.add(alice == Not(bob))

# Bob says: "Alice and Charlie are of the same type" -> statement = (alice == charlie)
solver.add(bob == (alice == charlie))

# Charlie says: "Alice is a knight" -> statement = alice
solver.add(charlie == alice)

# Solve
result = solver.check()
if result == sat:
    m = solver.model()
    def typ(val):
        return "knight" if is_true(m.eval(val)) else "knave"
    print("STATUS: sat")
    print(f"alice = {typ(alice)}")
    print(f"bob = {typ(bob)}")
    print(f"charlie = {typ(charlie)}")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")