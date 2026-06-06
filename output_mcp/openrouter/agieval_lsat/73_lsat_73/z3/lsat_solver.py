from z3 import *

# Define assistants
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
# Slot indices: 0 WedM,1 WedA,2 ThuM,3 ThuA,4 FriM,5 FriA
slot = {name: Int(f"slot_{name}") for name in assistants}

solver = Solver()
# Domain constraints
for v in slot.values():
    solver.add(v >= 0, v <= 5)
# All distinct slots
solver.add(Distinct([slot[name] for name in assistants]))
# Nessa must be afternoon
solver.add(Or([slot["Nessa"] == i for i in (1,3,5)]))
# Kevin and Rebecca same day
solver.add(slot["Kevin"] / 2 == slot["Rebecca"] / 2)
# Lan and Olivia different day
solver.add(slot["Lan"] / 2 != slot["Olivia"] / 2)
# Julio earlier day than Olivia
solver.add(slot["Julio"] / 2 < slot["Olivia"] / 2)
# Additional condition: Kevin's day is the day before Nessa's
solver.add(slot["Kevin"] / 2 == slot["Nessa"] / 2 - 1)

# Options definitions (list of assistants that could be Thursday afternoon)
options = {
    "A": ["Julio", "Nessa"],
    "B": ["Kevin", "Rebecca"],
    "C": ["Kevin", "Nessa", "Rebecca"],
    "D": ["Julio", "Kevin", "Nessa", "Rebecca"],
    "E": ["Julio", "Kevin", "Lan", "Nessa", "Rebecca"]
}

found_options = []
for letter, listed in options.items():
    ok = True
    # Check each listed assistant can be Thursday afternoon (slot 3)
    for a in listed:
        solver.push()
        solver.add(slot[a] == 3)
        if solver.check() != sat:
            ok = False
        solver.pop()
        if not ok:
            break
    if not ok:
        continue
    # Check assistants not listed cannot be Thursday afternoon
    for a in [x for x in assistants if x not in listed]:
        solver.push()
        solver.add(slot[a] == 3)
        if solver.check() == sat:
            ok = False
        solver.pop()
        if not ok:
            break
    if ok:
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