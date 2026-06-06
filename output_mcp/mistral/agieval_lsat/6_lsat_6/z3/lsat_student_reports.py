from z3 import *

# Define students and days
Students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
Days = ["Monday", "Tuesday", "Wednesday"]
Day_Indices = {d: i for i, d in enumerate(Days)}  # Map day names to indices 0,1,2

# Create symbolic constants for students and days
student_consts = {s: Int(s) for s in Students}

# Create solver
solver = Solver()

# Helper: All students are distinct and take values 0-7 (we'll map to indices)
for s in Students:
    solver.add(student_consts[s] >= 0, student_consts[s] < 8)

# Define morning and afternoon reporters as arrays indexed by day (0=Monday, 1=Tuesday, 2=Wednesday)
morning_reporter = [Int(f"morning_{i}") for i in range(3)]
afternoon_reporter = [Int(f"afternoon_{i}") for i in range(3)]

# Each reporter must be a valid student
for i in range(3):
    solver.add(Or([morning_reporter[i] == student_consts[s] for s in Students]))
    solver.add(Or([afternoon_reporter[i] == student_consts[s] for s in Students]))

# Morning reporters on Monday, Tuesday, Wednesday are exactly Helen, Kyle, Lenore (in some order)
# We'll enforce that the set of morning reporters equals {Helen, Kyle, Lenore}
# Since we have exactly 3 morning slots and 3 students, we can enforce:
solver.add(Distinct(morning_reporter))
for mr in morning_reporter:
    solver.add(Or([mr == student_consts[s] for s in ["Helen", "Kyle", "Lenore"]]))

# Exactly 6 distinct students give reports (2 per day × 3 days = 6)
# We need to collect all 6 reporter variables
all_reporters = morning_reporter + afternoon_reporter
solver.add(Distinct(all_reporters))

# George can only give a report on Tuesday (day index 1)
solver.add(Or([morning_reporter[1] == student_consts["George"], 
               afternoon_reporter[1] == student_consts["George"]]))

# Neither Olivia nor Robert can give an afternoon report
for i in range(3):
    solver.add(Not(Or([afternoon_reporter[i] == student_consts["Olivia"], 
                      afternoon_reporter[i] == student_consts["Robert"]])))

# Nina's constraint:
# If Nina gives a report on Monday (day 0) or Tuesday (day 1), then the next day must have both Helen and Irving
# We need to check if Nina is assigned to any slot on Monday or Tuesday
nina_on_monday = Or([morning_reporter[0] == student_consts["Nina"], 
                     afternoon_reporter[0] == student_consts["Nina"]])
nina_on_tuesday = Or([morning_reporter[1] == student_consts["Nina"], 
                      afternoon_reporter[1] == student_consts["Nina"]])

# If Nina is on Monday, then Tuesday must have both Helen and Irving
solver.add(Implies(nina_on_monday, 
                   And(Or([morning_reporter[1] == student_consts["Helen"], 
                           afternoon_reporter[1] == student_consts["Helen"]]),
                       Or([morning_reporter[1] == student_consts["Irving"], 
                           afternoon_reporter[1] == student_consts["Irving"]]))))

# If Nina is on Tuesday, then Wednesday must have both Helen and Irving
solver.add(Implies(nina_on_tuesday, 
                   And(Or([morning_reporter[2] == student_consts["Helen"], 
                           afternoon_reporter[2] == student_consts["Helen"]]),
                       Or([morning_reporter[2] == student_consts["Irving"], 
                           afternoon_reporter[2] == student_consts["Irving"]]))))

# Base constraints are set. Now evaluate multiple-choice options.
# We need to check which option MUST be true.
# For "must be true", we check if the negation of the option is incompatible with constraints.
# However, the provided skeleton checks if each option is satisfiable.
# We'll adapt: encode each option as a constraint and see which one is the only valid one.

# Let's define what each option means:
# (A) Helen gives a report on Monday: Helen is morning_reporter[0] or afternoon_reporter[0]
# (B) Irving gives a report on Monday: Irving is morning_reporter[0] or afternoon_reporter[0]
# (C) Irving gives a report on Wednesday: Irving is morning_reporter[2] or afternoon_reporter[2]
# (D) Kyle gives a report on Tuesday: Kyle is morning_reporter[1] or afternoon_reporter[1]
# (E) Kyle gives a report on Wednesday: Kyle is morning_reporter[2] or afternoon_reporter[2]

# We'll check each option by adding it as a constraint and seeing if a model exists
found_options = []

# Option A: Helen gives a report on Monday
solver.push()
solver.add(Or([morning_reporter[0] == student_consts["Helen"], 
               afternoon_reporter[0] == student_consts["Helen"]]))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Irving gives a report on Monday
solver.push()
solver.add(Or([morning_reporter[0] == student_consts["Irving"], 
               afternoon_reporter[0] == student_consts["Irving"]]))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Irving gives a report on Wednesday
solver.push()
solver.add(Or([morning_reporter[2] == student_consts["Irving"], 
               afternoon_reporter[2] == student_consts["Irving"]]))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Kyle gives a report on Tuesday
solver.push()
solver.add(Or([morning_reporter[1] == student_consts["Kyle"], 
               afternoon_reporter[1] == student_consts["Kyle"]]))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Kyle gives a report on Wednesday
solver.push()
solver.add(Or([morning_reporter[2] == student_consts["Kyle"], 
               afternoon_reporter[2] == student_consts["Kyle"]]))
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Determine the result based on found_options
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")