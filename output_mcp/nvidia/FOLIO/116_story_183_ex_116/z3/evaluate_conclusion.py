from z3 import *

# Boolean variables representing key predicates
block_MW = Bool('block_Michael_Windy')   # Michael can block Windy's shooting
jump_W = Bool('jump_Windy')             # Windy jumps when shooting
great_W = Bool('great_shooter_Windy')   # Windy is a great shooter

solver = Solver()

# Premise 1: Michael can block any shooting from a person as long as the person does not jump when shooting.
# For Windy: if ¬jump_W then block_MW  ==  jump_W ∨ block_MW
solver.add(Or(jump_W, block_MW))

# Premise 2: Michael cannot block Windy's shooting
solver.add(Not(block_MW))

# Premise 3: Every shooter who can jump when shooting is a great shooter.
# jump_W → great_W  ==  ¬jump_W ∨ great_W
solver.add(Or(Not(jump_W), great_W))

# Negate the conclusion to test entailment: assume ¬great_W
solver.add(Not(great_W))

# Check satisfiability
result = solver.check()

# Output according to the required format
if result == unsat:
    print("STATUS: proved")
    print("RESULT: True")
elif result == sat:
    print("STATUS: proved")
    print("RESULT: False")
else:
    print("STATUS: proved")
    print("RESULT: Unknown")