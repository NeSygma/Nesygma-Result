from z3 import *

# Boolean variables: True = knight, False = knave
alice = Bool('alice')
bob = Bool('bob')
charlie = Bool('charlie')

solver = Solver()

# Alice says: "Bob is a knave" -> Bob is knave means bob == False
# If Alice is knight, statement is true: bob == False
# If Alice is knave, statement is false: Not(bob == False) i.e. bob == True
# So: alice == (bob == False)
solver.add(alice == (bob == False))

# Bob says: "Alice and Charlie are of the same type"
# If Bob is knight, statement is true: alice == charlie
# If Bob is knave, statement is false: alice != charlie
# So: bob == (alice == charlie)
solver.add(bob == (alice == charlie))

# Charlie says: "Alice is a knight"
# If Charlie is knight, statement is true: alice == True
# If Charlie is knave, statement is false: alice == False
# So: charlie == alice
solver.add(charlie == alice)

BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print(f"alice = {'knight' if m[alice] else 'knave'}")
    print(f"bob = {'knight' if m[bob] else 'knave'}")
    print(f"charlie = {'knight' if m[charlie] else 'knave'}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")