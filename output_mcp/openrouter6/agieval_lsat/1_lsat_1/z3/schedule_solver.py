from z3 import *

# Student indices
George = 0
Helen = 1
Irving = 2
Kyle = 3
Lenore = 4
Nina = 5
Olivia = 6
Robert = 7

# Slot indices: 0=Mon morning, 1=Mon afternoon, 2=Tue morning, 3=Tue afternoon,
# 4=Wed morning, 5=Wed afternoon
slot = [Int(f'slot_{i}') for i in range(6)]

solver = Solver()

# Base constraints
# 1. All slots distinct
solver.add(Distinct(slot))

# 2. George only on Tuesday (slots 2 or 3)
for i in [0, 1, 4, 5]:
    solver.add(slot[i] != George)

# 3. Olivia and Robert cannot give afternoon reports (slots 1,3,5)
for i in [1, 3, 5]:
    solver.add(slot[i] != Olivia)
    solver.add(slot[i] != Robert)

# 4. Nina condition
nina_mon = Or(slot[0] == Nina, slot[1] == Nina)
nina_tue = Or(slot[2] == Nina, slot[3] == Nina)
# nina_wed = Or(slot[4] == Nina, slot[5] == Nina)  # not needed

# If Nina on Monday, then Tuesday must have Helen and Irving
solver.add(Implies(nina_mon, Or(And(slot[2] == Helen, slot[3] == Irving),
                                 And(slot[2] == Irving, slot[3] == Helen))))
# If Nina on Tuesday, then Wednesday must have Helen and Irving
solver.add(Implies(nina_tue, Or(And(slot[4] == Helen, slot[5] == Irving),
                                 And(slot[4] == Irving, slot[5] == Helen))))

# Define schedule constraints for each option
def schedule_constraints(option):
    if option == "A":
        return [slot[0] == Helen, slot[1] == Robert,
                slot[2] == Olivia, slot[3] == Irving,
                slot[4] == Lenore, slot[5] == Kyle]
    elif option == "B":
        return [slot[0] == Irving, slot[1] == Olivia,
                slot[2] == Helen, slot[3] == Kyle,
                slot[4] == Nina, slot[5] == Lenore]
    elif option == "C":
        return [slot[0] == Lenore, slot[1] == Helen,
                slot[2] == George, slot[3] == Kyle,
                slot[4] == Robert, slot[5] == Irving]
    elif option == "D":
        return [slot[0] == Nina, slot[1] == Helen,
                slot[2] == Robert, slot[3] == Irving,
                slot[4] == Olivia, slot[5] == Lenore]
    elif option == "E":
        return [slot[0] == Olivia, slot[1] == Nina,
                slot[2] == Irving, slot[3] == Helen,
                slot[4] == Kyle, slot[5] == George]
    else:
        return []

# Evaluate each option
found_options = []
for letter in ["A", "B", "C", "D", "E"]:
    solver.push()
    solver.add(schedule_constraints(letter))
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