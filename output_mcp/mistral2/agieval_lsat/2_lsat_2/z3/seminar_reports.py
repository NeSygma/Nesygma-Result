from z3 import *

# Define students as symbolic constants
george = Int('george')
helen = Int('helen')
irving = Int('irving')
nina = Int('nina')
olivia = Int('olivia')
robert = Int('robert')

# Define slots
morning_mon = Int('morning_mon')
afternoon_mon = Int('afternoon_mon')
morning_tue = Int('morning_tue')
afternoon_tue = Int('afternoon_tue')
morning_wed = Int('morning_wed')
afternoon_wed = Int('afternoon_wed')

# All possible students (excluding Kyle and Lenore as per the question)
students = [george, helen, irving, nina, olivia, robert]

# Create solver
solver = Solver()

# Constraint: All slots must be assigned to one of the students
solver.add(Or([morning_mon == s for s in students]))
solver.add(Or([afternoon_mon == s for s in students]))
solver.add(Or([morning_tue == s for s in students]))
solver.add(Or([afternoon_tue == s for s in students]))
solver.add(Or([morning_wed == s for s in students]))
solver.add(Or([afternoon_wed == s for s in students]))

# Constraint: Tuesday is the only day George can give a report
solver.add(Or([morning_tue == george, afternoon_tue == george]))
solver.add(Not(Or([morning_mon == george, afternoon_mon == george, morning_wed == george, afternoon_wed == george])))

# Constraint: Olivia and Robert cannot give afternoon reports
solver.add(Not(Or([afternoon_mon == olivia, afternoon_tue == olivia, afternoon_wed == olivia])))
solver.add(Not(Or([afternoon_mon == robert, afternoon_tue == robert, afternoon_wed == robert])))

# Constraint: Nina's report constraint
# If Nina is assigned to Monday morning or afternoon, then Tuesday morning and afternoon must be Helen and Irving (order not specified)
solver.add(Implies(morning_mon == nina, And(Or([morning_tue == helen, afternoon_tue == helen]), Or([morning_tue == irving, afternoon_tue == irving]))))
solver.add(Implies(afternoon_mon == nina, And(Or([morning_tue == helen, afternoon_tue == helen]), Or([morning_tue == irving, afternoon_tue == irving]))))

# If Nina is assigned to Tuesday morning or afternoon, then Wednesday morning and afternoon must be Helen and Irving (order not specified)
solver.add(Implies(morning_tue == nina, And(Or([morning_wed == helen, afternoon_wed == helen]), Or([morning_wed == irving, afternoon_wed == irving]))))
solver.add(Implies(afternoon_tue == nina, And(Or([morning_wed == helen, afternoon_wed == helen]), Or([morning_wed == irving, afternoon_wed == irving]))))

# Now, evaluate each answer choice for the morning slots
found_options = []

# Option A: Helen, George, Nina
solver.push()
solver.add(morning_mon == helen)
solver.add(morning_tue == george)
solver.add(morning_wed == nina)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Irving, Robert, Helen
solver.push()
solver.add(morning_mon == irving)
solver.add(morning_tue == robert)
solver.add(morning_wed == helen)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Nina, Helen, Olivia
solver.push()
solver.add(morning_mon == nina)
solver.add(morning_tue == helen)
solver.add(morning_wed == olivia)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Olivia, Robert, Irving
solver.push()
solver.add(morning_mon == olivia)
solver.add(morning_tue == robert)
solver.add(morning_wed == irving)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Robert, George, Helen
solver.push()
solver.add(morning_mon == robert)
solver.add(morning_tue == george)
solver.add(morning_wed == helen)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")