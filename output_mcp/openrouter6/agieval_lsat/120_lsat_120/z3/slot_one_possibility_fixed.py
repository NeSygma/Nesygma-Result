from z3 import *

# Define bands
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]
slot = {b: Int(f"slot_{b}") for b in bands}

# Base constraints
base_constraints = []
for b in bands:
    base_constraints.append(slot[b] >= 1)
    base_constraints.append(slot[b] <= 6)
base_constraints.append(Distinct([slot[b] for b in bands]))
base_constraints.append(slot["Vegemite"] < slot["Zircon"])
base_constraints.append(slot["Wellspring"] < slot["Xpert"])
base_constraints.append(slot["Zircon"] < slot["Xpert"])
base_constraints.append(Or(slot["Uneasy"] == 4, slot["Uneasy"] == 5, slot["Uneasy"] == 6))
base_constraints.append(Or(slot["Yardsign"] == 1, slot["Yardsign"] == 2, slot["Yardsign"] == 3))

# Find all bands that can be in slot 1
possible_bands = []
for b in bands:
    s = Solver()
    s.add(base_constraints)
    s.add(slot[b] == 1)
    if s.check() == sat:
        possible_bands.append(b)

print("Possible bands for slot 1:", possible_bands)

# Answer choices
choices = {
    "A": {"Yardsign"},
    "B": {"Vegemite", "Wellspring"},
    "C": {"Vegemite", "Yardsign"},
    "D": {"Vegemite", "Wellspring", "Yardsign"},
    "E": {"Vegemite", "Wellspring", "Yardsign", "Zircon"}
}

found = None
for letter, choice_set in choices.items():
    if set(possible_bands) == choice_set:
        found = letter
        break

if found:
    print("STATUS: sat")
    print(f"answer:{found}")
else:
    print("STATUS: unsat")
    print("Refine: No matching answer choice")