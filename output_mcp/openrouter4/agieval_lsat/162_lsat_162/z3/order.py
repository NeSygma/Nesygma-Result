from z3 import *

# Define persons
persons = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]

# Options as sequences from first to last
options = {
    "A": ["Quinn", "Tao", "Stanton", "Peters", "Villas", "White", "Rovero"],
    "B": ["Quinn", "White", "Rovero", "Peters", "Stanton", "Villas", "Tao"],
    "C": ["Villas", "White", "Quinn", "Stanton", "Peters", "Tao", "Rovero"],
    "D": ["Villas", "White", "Stanton", "Peters", "Quinn", "Tao", "Rovero"],
    "E": ["Villas", "White", "Stanton", "Peters", "Rovero", "Tao", "Quinn"]
}

found_options = []

for letter, seq in options.items():
    solver = Solver()
    
    # Position variables for each person (1-indexed positions)
    pos = {p: Int(f"pos_{p}") for p in persons}
    
    # Domain: positions 1 to 7
    for p in persons:
        solver.add(pos[p] >= 1, pos[p] <= 7)
    
    # All positions distinct
    solver.add(Distinct([pos[p] for p in persons]))
    
    # Constraint 1: Stanton neither immediately before nor immediately after Tao
    solver.add(Not(Or(pos["Stanton"] + 1 == pos["Tao"], pos["Stanton"] - 1 == pos["Tao"])))
    
    # Constraint 2: Quinn earlier than Rovero
    solver.add(pos["Quinn"] < pos["Rovero"])
    
    # Constraint 3: Villas immediately before White
    solver.add(pos["Villas"] + 1 == pos["White"])
    
    # Constraint 4: Peters was recruited fourth
    solver.add(pos["Peters"] == 4)
    
    # Enforce the specific order for this option
    for i, person in enumerate(seq):
        solver.add(pos[person] == i + 1)
    
    if solver.check() == sat:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")