from z3 import *

# Define students mapping
students = ['George','Helen','Irving','Kyle','Lenore','Nina','Olivia','Robert']
idx = {name:i for i,name in enumerate(students)}
# slot variables
MonM, MonA, TueM, TueA, WedM, WedA = Ints('MonM MonA TueM TueA WedM WedA')
slots = [MonM, MonA, TueM, TueA, WedM, WedA]
solver = Solver()
# each slot must be one of the 8 students
for s in slots:
    solver.add(And(s >= 0, s < 8))
# distinct
solver.add(Distinct(slots))
# Tuesday only day for George
for s in [MonM, MonA, WedM, WedA]:
    solver.add(s != idx['George'])
# Olivia and Robert cannot be afternoon
for s in [MonA, TueA, WedA]:
    solver.add(s != idx['Olivia'])
    solver.add(s != idx['Robert'])
# Nina rule
# Helper: next day slots sets
# If Nina on Monday -> Tuesday slots must be Helen and Irving
nina = idx['Nina']
helen = idx['Helen']
irving = idx['Irving']
# Monday condition
nina_mon = Or(MonM == nina, MonA == nina)
# Tuesday condition for Nina on Tuesday
nina_tue = Or(TueM == nina, TueA == nina)
# Implications
# If Nina Monday then Tue slots are Helen and Irving (order any)
solver.add(Implies(nina_mon,
    And(Or(TueM == helen, TueM == irving),
        Or(TueA == helen, TueA == irving),
        TueM != TueA)))
# If Nina Tuesday then Wed slots are Helen and Irving
solver.add(Implies(nina_tue,
    And(Or(WedM == helen, WedM == irving),
        Or(WedA == helen, WedA == irving),
        WedM != WedA)))
# No extra condition for Nina Wednesday (allowed)

# Define option constraints as list of tuples (letter, list of (slot, student))
options = []
# A
options.append(('A', [
    (MonM, 'Helen'), (MonA, 'Robert'),
    (TueM, 'Olivia'), (TueA, 'Irving'),
    (WedM, 'Lenore'), (WedA, 'Kyle')
]))
# B
options.append(('B', [
    (MonM, 'Irving'), (MonA, 'Olivia'),
    (TueM, 'Helen'), (TueA, 'Kyle'),
    (WedM, 'Nina'), (WedA, 'Lenore')
]))
# C
options.append(('C', [
    (MonM, 'Lenore'), (MonA, 'Helen'),
    (TueM, 'George'), (TueA, 'Kyle'),
    (WedM, 'Robert'), (WedA, 'Irving')
]))
# D
options.append(('D', [
    (MonM, 'Nina'), (MonA, 'Helen'),
    (TueM, 'Robert'), (TueA, 'Irving'),
    (WedM, 'Olivia'), (WedA, 'Lenore')
]))
# E
options.append(('E', [
    (MonM, 'Olivia'), (MonA, 'Nina'),
    (TueM, 'Irving'), (TueA, 'Helen'),
    (WedM, 'Kyle'), (WedA, 'George')
]))

found = []
for letter, assigns in options:
    solver.push()
    # add equality constraints for this option
    for slot, name in assigns:
        solver.add(slot == idx[name])
    # check
    if solver.check() == sat:
        found.append(letter)
    solver.pop()

print('STATUS: sat' if len(found)==1 else 'STATUS: unsat')
print('found_options:', found)