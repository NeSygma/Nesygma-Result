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
solver.add(Implies(Or(morning_mon == nina, afternoon_mon == nina), 
                 And(Or(morning_tue == helen, afternoon_tue == helen), Or(morning_tue == irving, afternoon_tue == irving))))

# If Nina is assigned to Tuesday morning or afternoon, then Wednesday morning and afternoon must be Helen and Irving (order not specified)
solver.add(Implies(Or(morning_tue == nina, afternoon_tue == nina), 
                 And(Or(morning_wed == helen, afternoon_wed == helen), Or(morning_wed == irving, afternoon_wed == irving))))

# Constraint: Exactly two reports per day (one morning, one afternoon)
# Ensure that morning and afternoon slots are distinct for each day
solver.add(morning_mon != afternoon_mon)
solver.add(morning_tue != afternoon_tue)
solver.add(morning_wed != afternoon_wed)

# Constraint: Exactly six students give reports (Kyle and Lenore do not give reports)
# This is enforced by the fact that only six students are considered (excluding Kyle and Lenore)
# Additionally, ensure that all six students are assigned to at least one slot
solver.add(Distinct([morning_mon, afternoon_mon, morning_tue, afternoon_tue, morning_wed, afternoon_wed]))

# Now, evaluate each answer choice for the morning slots
found_options = []

# Option A: Helen, George, Nina
solver.push()
solver.add(morning_mon == helen)
solver.add(morning_tue == george)
solver.add(morning_wed == nina)
if solver.check() == sat:
    found_options.append("A")
    print("Option A is satisfiable")
else:
    print("Option A is not satisfiable")
solver.pop()

# Option B: Irving, Robert, Helen
solver.push()
solver.add(morning_mon == irving)
solver.add(morning_tue == robert)
solver.add(morning_wed == helen)
if solver.check() == sat:
    found_options.append("B")
    print("Option B is satisfiable")
else:
    print("Option B is not satisfiable")
solver.pop()

# Option C: Nina, Helen, Olivia
solver.push()
solver.add(morning_mon == nina)
solver.add(morning_tue == helen)
solver.add(morning_wed == olivia)
if solver.check() == sat:
    found_options.append("C")
    print("Option C is satisfiable")
else:
    print("Option C is not satisfiable")
solver.pop()

# Option D: Olivia, Robert, Irving
solver.push()
solver.add(morning_mon == olivia)
solver.add(morning_tue == robert)
solver.add(morning_wed == irving)
if solver.check() == sat:
    found_options.append("D")
    print("Option D is satisfiable")
else:
    print("Option D is not satisfiable")
solver.pop()

# Option E: Robert, George, Helen
solver.push()
solver.add(morning_mon == robert)
solver.add(morning_tue == george)
solver.add(morning_wed == helen)
if solver.check() == sat:
    found_options.append("E")
    print("Option E is satisfiable")
else:
    print("Option E is not satisfiable")
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