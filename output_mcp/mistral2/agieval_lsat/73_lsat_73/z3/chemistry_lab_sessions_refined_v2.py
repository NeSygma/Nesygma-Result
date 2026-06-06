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

# Kevin and Rebecca must lead sessions on the same day
kevin_day = Int('kevin_day')
rebecca_day = Int('rebecca_day')

# Constrain Kevin's day
solver.add(Or([And(
    Or(sessions[day][0] == Kevin, sessions[day][1] == Kevin),
    kevin_day == day
) for day in range(3)]))

# Constrain Rebecca's day
solver.add(Or([And(
    Or(sessions[day][0] == Rebecca, sessions[day][1] == Rebecca),
    rebecca_day == day
) for day in range(3)]))

solver.add(kevin_day == rebecca_day)

# Lan and Olivia cannot lead sessions on the same day
for day in range(3):
    solver.add(Not(And(
        Or(sessions[day][0] == Lan, sessions[day][1] == Lan),
        Or(sessions[day][0] == Olivia, sessions[day][1] == Olivia)
    )))

# Nessa must lead an afternoon session
solver.add(Or([sessions[day][1] == Nessa for day in range(3)]))

# Julio's session must meet on an earlier day than Olivia's
julio_day = Int('julio_day')
olivia_day = Int('olivia_day')

# Constrain Julio's day
solver.add(Or([And(
    Or(sessions[day][0] == Julio, sessions[day][1] == Julio),
    julio_day == day
) for day in range(3)]))

# Constrain Olivia's day
solver.add(Or([And(
    Or(sessions[day][0] == Olivia, sessions[day][1] == Olivia),
    olivia_day == day
) for day in range(3)]))

solver.add(julio_day < olivia_day)

# Kevin's session meets on the day before Nessa's
nessa_day = Int('nessa_day')

# Constrain Nessa's day
solver.add(Or([And(
    Or(sessions[day][0] == Nessa, sessions[day][1] == Nessa),
    nessa_day == day
) for day in range(3)]))

solver.add(kevin_day + 1 == nessa_day)

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