from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each assistant's day and time
# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Times: True=Morning, False=Afternoon

# Assistants: Julio, Kevin, Lan, Nessa, Olivia, Rebecca
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
days = {a: Int(f"{a}_day") for a in assistants}
times = {a: Bool(f"{a}_morning") for a in assistants}

# Helper: All (day, time) pairs must be unique
# Represent each (day, time) pair as a single integer: day * 2 + (1 if morning else 0)
pair_vals = [
    days[a] * 2 + If(times[a], 1, 0) for a in assistants
]

# Base constraints
solver = Solver()

# 1. All (day, time) pairs are unique
solver.add(Distinct(pair_vals))

# 2. Days are in {0,1,2} (Wednesday, Thursday, Friday)
for a in assistants:
    solver.add(days[a] >= 0, days[a] <= 2)

# 3. Kevin and Rebecca must lead sessions on the same day
solver.add(days["Kevin"] == days["Rebecca"])

# 4. Lan and Olivia cannot lead sessions on the same day
solver.add(days["Lan"] != days["Olivia"])

# 5. Nessa must lead an afternoon session
solver.add(times["Nessa"] == False)

# 6. Julio's session must meet on an earlier day than Olivia's
solver.add(days["Julio"] < days["Olivia"])

# Additional condition from the question:
# Julio and Kevin both lead morning sessions
solver.add(times["Julio"] == True)
solver.add(times["Kevin"] == True)

# Now evaluate each option to see which one CANNOT be true
# We will check each option by adding its constraint and seeing if it is satisfiable

# Option A: Lan's session meets Wednesday morning
# => days["Lan"] == 0 and times["Lan"] == True
opt_a_constr = And(days["Lan"] == 0, times["Lan"] == True)

# Option B: Lan's session meets Thursday afternoon
# => days["Lan"] == 1 and times["Lan"] == False
opt_b_constr = And(days["Lan"] == 1, times["Lan"] == False)

# Option C: Nessa's session meets Friday afternoon
# => days["Nessa"] == 2 and times["Nessa"] == False
# Note: Nessa must be afternoon, so only day is constrained
opt_c_constr = (days["Nessa"] == 2)

# Option D: Olivia's session meets Thursday morning
# => days["Olivia"] == 1 and times["Olivia"] == True
opt_d_constr = And(days["Olivia"] == 1, times["Olivia"] == True)

# Option E: Olivia's session meets Friday morning
# => days["Olivia"] == 2 and times["Olivia"] == True
opt_e_constr = And(days["Olivia"] == 2, times["Olivia"] == True)

# Evaluate each option
satisfiable_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        satisfiable_options.append(letter)
    solver.pop()

# The answer is the option that is NOT satisfiable
unsatisfiable_options = [letter for letter in ["A", "B", "C", "D", "E"] if letter not in satisfiable_options]

if len(unsatisfiable_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsatisfiable_options[0]}")
elif len(unsatisfiable_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple unsatisfiable options found {unsatisfiable_options}")
else:
    print("STATUS: unsat")
    print("Refine: No unsatisfiable options found (all options are satisfiable)")