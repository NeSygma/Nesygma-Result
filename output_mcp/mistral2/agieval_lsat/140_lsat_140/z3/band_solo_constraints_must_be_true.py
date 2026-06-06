from z3 import *

# Declare symbolic variables for each band member's solo position
solver = Solver()

guitarist = Int('guitarist')
keyboard = Int('keyboard')
percussionist = Int('percussionist')
saxophonist = Int('saxophonist')
trumpeter = Int('trumpeter')
violinist = Int('violinist')

# Each solo position is unique and between 1 and 6
positions = [guitarist, keyboard, percussionist, saxophonist, trumpeter, violinist]
for pos in positions:
    solver.add(And(pos >= 1, pos <= 6))

# Constraint 1: The guitarist does not perform the fourth solo.
solver.add(guitarist != 4)

# Constraint 2: The percussionist performs a solo at some time before the keyboard player does.
solver.add(percussionist < keyboard)

# Constraint 3: The keyboard player performs a solo at some time after the violinist does and at some time before the guitarist does.
solver.add(violinist < keyboard)
solver.add(keyboard < guitarist)

# Constraint 4: The saxophonist performs a solo at some time after exactly one of the percussionist or the trumpeter does.
# This means:
# - saxophonist > percussionist and saxophonist <= trumpeter, OR
# - saxophonist > trumpeter and saxophonist <= percussionist

# Option 1: saxophonist after percussionist but not after trumpeter
option1 = And(saxophonist > percussionist, saxophonist <= trumpeter)

# Option 2: saxophonist after trumpeter but not after percussionist
option2 = And(saxophonist > trumpeter, saxophonist <= percussionist)

# Exactly one of the two options must be true
solver.add(Or(option1, option2))
solver.add(Not(And(option1, option2)))

# Additional constraint from the question: The percussionist performs a solo at some time before the saxophonist does.
solver.add(percussionist < saxophonist)

# Check if the base constraints are satisfiable
base_result = solver.check()
if base_result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: base constraints are unsatisfiable")
    exit()

# Now, evaluate each answer choice to see if it MUST be true
must_be_true = []

# Choice A: The percussionist performs the first solo.
# Check if NOT A is unsatisfiable
solver.push()
solver.add(Not(percussionist == 1))
if solver.check() == unsat:
    must_be_true.append("A")
solver.pop()

# Choice B: The percussionist performs the second solo.
# Check if NOT B is unsatisfiable
solver.push()
solver.add(Not(percussionist == 2))
if solver.check() == unsat:
    must_be_true.append("B")
solver.pop()

# Choice C: The violinist performs a solo at some time before the saxophonist does.
# This is already implied by the base constraints (violinist < keyboard and percussionist < saxophonist).
# So, NOT C should be unsatisfiable.
solver.push()
solver.add(Not(violinist < saxophonist))
if solver.check() == unsat:
    must_be_true.append("C")
solver.pop()

# Choice D: The percussionist performs a solo at some time before the trumpeter does.
# Check if NOT D is unsatisfiable
solver.push()
solver.add(Not(percussionist < trumpeter))
if solver.check() == unsat:
    must_be_true.append("D")
solver.pop()

# Choice E: The saxophonist performs a solo at some time before the keyboard player does.
# Check if NOT E is unsatisfiable
solver.push()
solver.add(Not(saxophonist < keyboard))
if solver.check() == unsat:
    must_be_true.append("E")
solver.pop()

# Determine the result
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")