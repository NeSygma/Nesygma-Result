from z3 import *

solver = Solver()

# Days: Wednesday, Thursday, Friday
# Sessions: Morning, Afternoon
# Assistants: Julio, Kevin, Lan, Nessa, Olivia, Rebecca

# Declare symbolic variables for each assistant's session day and time
# We represent each assistant's session as a tuple (day, time)
# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Times: 0=Morning, 1=Afternoon

# Variables for each assistant's session
Julio_day = Int('Julio_day')
Julio_time = Int('Julio_time')

Kevin_day = Int('Kevin_day')
Kevin_time = Int('Kevin_time')

Lan_day = Int('Lan_day')
Lan_time = Int('Lan_time')

Nessa_day = Int('Nessa_day')
Nessa_time = Int('Nessa_time')

Olivia_day = Int('Olivia_day')
Olivia_time = Int('Olivia_time')

Rebecca_day = Int('Rebecca_day')
Rebecca_time = Int('Rebecca_time')

# Helper function to ensure all days and times are within bounds
def in_bounds(day, time):
    return And(day >= 0, day <= 2, time >= 0, time <= 1)

# Add bounds for all variables
solver.add(in_bounds(Julio_day, Julio_time))
solver.add(in_bounds(Kevin_day, Kevin_time))
solver.add(in_bounds(Lan_day, Lan_time))
solver.add(in_bounds(Nessa_day, Nessa_time))
solver.add(in_bounds(Olivia_day, Olivia_time))
solver.add(in_bounds(Rebecca_day, Rebecca_time))

# Each assistant leads exactly one session
# All sessions are distinct (no two assistants share the same (day, time))
all_sessions = [
    (Julio_day, Julio_time),
    (Kevin_day, Kevin_time),
    (Lan_day, Lan_time),
    (Nessa_day, Nessa_time),
    (Olivia_day, Olivia_time),
    (Rebecca_day, Rebecca_time)
]

# Ensure all sessions are distinct
for i in range(len(all_sessions)):
    for j in range(i + 1, len(all_sessions)):
        solver.add(Not(And(all_sessions[i][0] == all_sessions[j][0], all_sessions[i][1] == all_sessions[j][1])))

# Constraints from the problem statement

# 1. Kevin and Rebecca must lead sessions on the same day
solver.add(Kevin_day == Rebecca_day)

# 2. Lan and Olivia cannot lead sessions on the same day
solver.add(Lan_day != Olivia_day)

# 3. Nessa must lead an afternoon session
solver.add(Nessa_time == 1)

# 4. Julio's session must meet on an earlier day than Olivia's
solver.add(Julio_day < Olivia_day)

# Additional constraint from the question:
# If Julio and Kevin both lead morning sessions, then any of the following could be true EXCEPT:
# We will test this scenario by adding these constraints in the multiple-choice evaluation.

# Base scenario: Julio and Kevin both lead morning sessions
base_constraints = And(
    Julio_time == 0,
    Kevin_time == 0
)

# Now evaluate each option under the base scenario

# Option A: Lan's session meets Wednesday morning
opt_a_constr = And(
    base_constraints,
    Lan_day == 0,
    Lan_time == 0
)

# Option B: Lan's session meets Thursday afternoon
opt_b_constr = And(
    base_constraints,
    Lan_day == 1,
    Lan_time == 1
)

# Option C: Nessa's session meets Friday afternoon
opt_c_constr = And(
    base_constraints,
    Nessa_day == 2,
    Nessa_time == 1
)

# Option D: Olivia's session meets Thursday morning
opt_d_constr = And(
    base_constraints,
    Olivia_day == 1,
    Olivia_time == 0
)

# Option E: Olivia's session meets Friday morning
opt_e_constr = And(
    base_constraints,
    Olivia_day == 2,
    Olivia_time == 0
)

# Evaluate each option
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