from z3 import *

# Declare Boolean variables representing the emotional state of events
happy = Bool('happy')
sad = Bool('sad')

solver = Solver()

# Premise 1: Each event is either happy or sad (exclusive)
#   - At least one of happy/sad holds
#   - At most one holds (they are exclusive)
solver.add(Or(happy, sad))
solver.add(Not(And(happy, sad)))

# Premise 2: At least one event is happy
solver.add(happy == True)

# Conclusion to evaluate: All events are sad
#   This is expressed as sad == True (for the single event considered)
solver.add(sad == True)

# Check the combined constraints
BENCHMARK_MODE = True  # Ensure we are in model-finding mode
result = solver.check()

if result == sat:
    print("STATUS: sat")
    # If satisfiable, we could extract a model, but we expect unsat
elif result == unsat:
    # Unsatisfiable means the premises contradict the conclusion,
    # so the conclusion is false given the premises.
    print("STATUS: proved")
    print("CONCLUSION: False")
else:
    print("STATUS: unknown")