from z3 import *

solver = Solver()

# Define session indices: 0=Wed AM, 1=Wed PM, 2=Thu AM, 3=Thu PM, 4=Fri AM, 5=Fri PM
# Assistants
julio = Int('julio')
kevin = Int('kevin')
lan = Int('lan')
nessa = Int('nessa')
olivia = Int('olivia')
rebecca = Int('rebecca')

# Helper functions for day and time
def day(s):
    return s / 2   # integer division

def time(s):
    return Mod(s, 2)   # 0 for morning, 1 for afternoon

# Base constraints
# All assistants assigned to different sessions
solver.add(Distinct([julio, kevin, lan, nessa, olivia, rebecca]))

# Each session index between 0 and 5
for var in [julio, kevin, lan, nessa, olivia, rebecca]:
    solver.add(And(0 <= var, var <= 5))

# Kevin and Rebecca same day
solver.add(day(kevin) == day(rebecca))

# Lan and Olivia different day
solver.add(day(lan) != day(olivia))

# Nessa afternoon
solver.add(time(nessa) == 1)

# Julio earlier day than Olivia
solver.add(day(julio) < day(olivia))

# Additional condition: Julio and Kevin both lead morning sessions
solver.add(time(julio) == 0)
solver.add(time(kevin) == 0)

# Define options
options = [
    ("A", lan == 0),                     # Lan Wednesday morning
    ("B", lan == 3),                     # Lan Thursday afternoon
    ("C", nessa == 5),                   # Nessa Friday afternoon
    ("D", olivia == 2),                  # Olivia Thursday morning
    ("E", olivia == 4)                   # Olivia Friday morning
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
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