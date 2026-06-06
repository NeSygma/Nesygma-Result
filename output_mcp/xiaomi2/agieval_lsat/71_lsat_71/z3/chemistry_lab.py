from z3 import *

solver = Solver()

# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Session: 0=morning, 1=afternoon
# Assistants: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5

# For each option, encode the assignment as (day, session) for each assistant
# Option A: Wed: Rebecca(morn), Kevin(aft); Thu: Julio(morn), Lan(aft); Fri: Nessa(morn), Olivia(aft)
# Option B: Wed: Olivia(morn), Nessa(aft); Thu: Julio(morn), Lan(aft); Fri: Kevin(morn), Rebecca(aft)
# Option C: Wed: Lan(morn), Kevin(aft); Thu: Rebecca(morn), Julio(aft); Fri: Olivia(morn), Nessa(aft)
# Option D: Wed: Kevin(morn), Rebecca(aft); Thu: Julio(morn), Nessa(aft); Fri: Olivia(morn), Lan(aft)
# Option E: Wed: Julio(morn), Lan(aft); Thu: Olivia(morn), Nessa(aft); Fri: Rebecca(morn), Kevin(aft)

options = {
    "A": {"Julio": (1, 0), "Kevin": (0, 1), "Lan": (1, 1), "Nessa": (2, 0), "Olivia": (2, 1), "Rebecca": (0, 0)},
    "B": {"Julio": (1, 0), "Kevin": (2, 0), "Lan": (1, 1), "Nessa": (0, 1), "Olivia": (0, 0), "Rebecca": (2, 1)},
    "C": {"Julio": (1, 1), "Kevin": (0, 1), "Lan": (0, 0), "Nessa": (2, 1), "Olivia": (2, 0), "Rebecca": (1, 0)},
    "D": {"Julio": (1, 0), "Kevin": (0, 0), "Lan": (2, 1), "Nessa": (1, 1), "Olivia": (2, 0), "Rebecca": (0, 1)},
    "E": {"Julio": (0, 0), "Kevin": (2, 1), "Lan": (0, 1), "Nessa": (1, 1), "Olivia": (1, 0), "Rebecca": (2, 0)},
}

def check_constraints(assign):
    """Check all constraints for a given assignment."""
    julio_day = assign["Julio"][0]
    kevin_day = assign["Kevin"][0]
    lan_day = assign["Lan"][0]
    nessa_day = assign["Nessa"][0]
    olivia_day = assign["Olivia"][0]
    rebecca_day = assign["Rebecca"][0]
    
    nessa_session = assign["Nessa"][1]
    lan_session = assign["Lan"][1]
    olivia_session = assign["Olivia"][1]
    
    # Constraint 1: Kevin and Rebecca same day
    c1 = (kevin_day == rebecca_day)
    
    # Constraint 2: Lan and Olivia different days
    c2 = (lan_day != olivia_day)
    
    # Constraint 3: Nessa must lead afternoon session
    c3 = (nessa_session == 1)
    
    # Constraint 4: Julio's day < Olivia's day
    c4 = (julio_day < olivia_day)
    
    return And(c1, c2, c3, c4)

found_options = []
for letter in ["A", "B", "C", "D", "E"]:
    solver.push()
    solver.add(check_constraints(options[letter]))
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