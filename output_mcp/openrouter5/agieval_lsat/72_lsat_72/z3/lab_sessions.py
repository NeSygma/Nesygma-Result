from z3 import *

# Six lab sessions: 3 days (Wed, Thu, Fri) x 2 slots (morning, afternoon)
# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Slots: 0=morning, 1=afternoon
# We'll assign each assistant to a (day, slot) pair.

# Assistants: Julio, Kevin, Lan, Nessa, Olivia, Rebecca
# We'll use integer variables for day and slot for each assistant.
Julio_day, Julio_slot = Ints('Julio_day Julio_slot')
Kevin_day, Kevin_slot = Ints('Kevin_day Kevin_slot')
Lan_day, Lan_slot = Ints('Lan_day Lan_slot')
Nessa_day, Nessa_slot = Ints('Nessa_day Nessa_slot')
Olivia_day, Olivia_slot = Ints('Olivia_day Olivia_slot')
Rebecca_day, Rebecca_slot = Ints('Rebecca_day Rebecca_slot')

assistants = [Julio_day, Julio_slot, Kevin_day, Kevin_slot, Lan_day, Lan_slot,
              Nessa_day, Nessa_slot, Olivia_day, Olivia_slot, Rebecca_day, Rebecca_slot]

solver = Solver()

# Domain constraints: day in {0,1,2}, slot in {0,1}
for d, s in [(Julio_day, Julio_slot), (Kevin_day, Kevin_slot), (Lan_day, Lan_slot),
             (Nessa_day, Nessa_slot), (Olivia_day, Olivia_slot), (Rebecca_day, Rebecca_slot)]:
    solver.add(And(d >= 0, d <= 2))
    solver.add(And(s >= 0, s <= 1))

# Each session is led by a different assistant -> all (day, slot) pairs must be distinct.
# We can enforce that no two assistants share the same (day, slot).
pairs = [(Julio_day, Julio_slot), (Kevin_day, Kevin_slot), (Lan_day, Lan_slot),
         (Nessa_day, Nessa_slot), (Olivia_day, Olivia_slot), (Rebecca_day, Rebecca_slot)]

for i in range(6):
    for j in range(i+1, 6):
        solver.add(Not(And(pairs[i][0] == pairs[j][0], pairs[i][1] == pairs[j][1])))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day.
solver.add(Kevin_day == Rebecca_day)

# Constraint 2: Lan and Olivia cannot lead sessions on the same day.
solver.add(Lan_day != Olivia_day)

# Constraint 3: Nessa must lead an afternoon session.
solver.add(Nessa_slot == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's.
solver.add(Julio_day < Olivia_day)

# Additional condition: Lan does not lead a Wednesday session.
solver.add(Lan_day != 0)

# Now evaluate each option: which assistant MUST lead a Thursday session?
# We test each option by asserting that the assistant does NOT lead a Thursday session.
# If that leads to unsat, then the assistant MUST lead a Thursday session.

found_options = []

# Option A: Rebecca must lead a Thursday session.
solver.push()
solver.add(Rebecca_day != 1)
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: Olivia must lead a Thursday session.
solver.push()
solver.add(Olivia_day != 1)
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: Nessa must lead a Thursday session.
solver.push()
solver.add(Nessa_day != 1)
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: Kevin must lead a Thursday session.
solver.push()
solver.add(Kevin_day != 1)
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: Julio must lead a Thursday session.
solver.push()
solver.add(Julio_day != 1)
if solver.check() == unsat:
    found_options.append("E")
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