from z3 import *

# Define bands
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]
slot = {b: Int(f"slot_{b}") for b in bands}

solver = Solver()

# All slots distinct and between 1 and 6
for b in bands:
    solver.add(slot[b] >= 1, slot[b] <= 6)
solver.add(Distinct([slot[b] for b in bands]))

# Constraints
# Vegemite before Zircon
solver.add(slot["Vegemite"] < slot["Zircon"])
# Wellspring before Xpert
solver.add(slot["Wellspring"] < slot["Xpert"])
# Zircon before Xpert
solver.add(slot["Zircon"] < slot["Xpert"])
# Uneasy in last three slots (4,5,6)
solver.add(Or(slot["Uneasy"] == 4, slot["Uneasy"] == 5, slot["Uneasy"] == 6))
# Yardsign in first three slots (1,2,3)
solver.add(Or(slot["Yardsign"] == 1, slot["Yardsign"] == 2, slot["Yardsign"] == 3))

# Find all bands that can be in slot 1
possible_bands = []
for b in bands:
    s = Solver()
    s.add([slot[bb] >= 1, slot[bb] <= 6 for bb in bands])
    s.add(Distinct([slot[bb] for bb in bands]))
    s.add(slot["Vegemite"] < slot["Zircon"])
    s.add(slot["Wellspring"] < slot["Xpert"])
    s.add(slot["Zircon"] < slot["Xpert"])
    s.add(Or(slot["Uneasy"] == 4, slot["Uneasy"] == 5, slot["Uneasy"] == 6))
    s.add(Or(slot["Yardsign"] == 1, slot["Yardsign"] == 2, slot["Yardsign"] == 3))
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