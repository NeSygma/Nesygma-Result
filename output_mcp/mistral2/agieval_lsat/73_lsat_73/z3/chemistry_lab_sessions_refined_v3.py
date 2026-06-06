from z3 import *

solver = Solver()

# Days: Wednesday (0), Thursday (1), Friday (2)
# Sessions: Morning (0), Afternoon (1)
# Lab assistants: Julio, Kevin, Lan, Nessa, Olivia, Rebecca

# Declare symbolic variables for lab assistants assigned to each session
# sessions[day][session] = assistant
sessions = [[Int(f"sessions_{day}_{session}") for session in range(2)] for day in range(3)]

# Lab assistants as symbolic constants
Julio, Kevin, Lan, Nessa, Olivia, Rebecca = Ints('Julio Kevin Lan Nessa Olivia Rebecca')
assistants = [Julio, Kevin, Lan, Nessa, Olivia, Rebecca]

# Each assistant is assigned to exactly one session
solver.add(Distinct(assistants))

# All sessions are assigned to one of the six assistants
for day in range(3):
    for session in range(2):
        solver.add(Or([sessions[day][session] == a for a in assistants]))

# Helper function to extract the day of a given assistant
# For each assistant, determine which day they are assigned to
assistant_days = {}
for assistant in assistants:
    for day in range(3):
        for session in range(2):
            solver.add(Implies(sessions[day][session] == assistant, assistant_days.setdefault(assistant, Int(f"day_{assistant}")) == day))

# Kevin and Rebecca must lead sessions on the same day
solver.add(assistant_days[Kevin] == assistant_days[Rebecca])

# Lan and Olivia cannot lead sessions on the same day
solver.add(assistant_days[Lan] != assistant_days[Olivia])

# Nessa must lead an afternoon session
nessa_afternoon = False
for day in range(3):
    solver.add(Implies(sessions[day][1] == Nessa,essa_afternoon == True))
solver.add(essa_afternoon == True)

# Julio's session must meet on an earlier day than Olivia's
solver.add(assistant_days[Julio] < assistant_days[Olivia])

# Kevin's session meets on the day before Nessa's
solver.add(assistant_days[Kevin] + 1 == assistant_days[Nessa])

# Now evaluate the multiple choice options for Thursday afternoon session
# Thursday afternoon is sessions[1][1]

# Define constraints for each option
# Option A: Thursday afternoon is either Julio or Nessa
opt_a_constr = And(
    sessions[1][1] == Julio,
    Or(sessions[1][1] == Nessa)
)

# Option B: Thursday afternoon is either Kevin or Rebecca
opt_b_constr = And(
    sessions[1][1] == Kevin,
    Or(sessions[1][1] == Rebecca)
)

# Option C: Thursday afternoon is Kevin, Nessa, or Rebecca
opt_c_constr = Or(
    sessions[1][1] == Kevin,
    sessions[1][1] == Nessa,
    sessions[1][1] == Rebecca
)

# Option D: Thursday afternoon is Julio, Kevin, Nessa, or Rebecca
opt_d_constr = Or(
    sessions[1][1] == Julio,
    sessions[1][1] == Kevin,
    sessions[1][1] == Nessa,
    sessions[1][1] == Rebecca
)

# Option E: Thursday afternoon is Julio, Kevin, Lan, Nessa, or Rebecca
opt_e_constr = Or(
    sessions[1][1] == Julio,
    sessions[1][1] == Kevin,
    sessions[1][1] == Lan,
    sessions[1][1] == Nessa,
    sessions[1][1] == Rebecca
)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")