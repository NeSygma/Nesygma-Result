from z3 import *

solver = Solver()

# Days: Wednesday=0, Thursday=1, Friday=2
# Times: Morning=0, Afternoon=1

# Assign each lab assistant to a session (day, time)
# We represent each assignment as a pair (day, time)

Julio = (Int('Julio_day'), Int('Julio_time'))
Kevin = (Int('Kevin_day'), Int('Kevin_time'))
Lan = (Int('Lan_day'), Int('Lan_time'))
Nessa = (Int('Nessa_day'), Int('Nessa_time'))
Olivia = (Int('Olivia_day'), Int('Olivia_time'))
Rebecca = (Int('Rebecca_day'), Int('Rebecca_time'))

# Extract day and time for each assistant
Julio_day, Julio_time = Julio
Kevin_day, Kevin_time = Kevin
Lan_day, Lan_time = Lan
Nessa_day, Nessa_time = Nessa
Olivia_day, Olivia_time = Olivia
Rebecca_day, Rebecca_time = Rebecca

# Each assistant is assigned to a unique session
sessions = [Julio, Kevin, Lan, Nessa, Olivia, Rebecca]
solver.add(Distinct([(d, t) for d, t in sessions]))

# Days and times are within bounds
for d, t in sessions:
    solver.add(d >= 0, d <= 2)
    solver.add(t >= 0, t <= 1)

# Constraints from the problem statement

# 1. Kevin and Rebecca must lead sessions on the same day
solver.add(Kevin_day == Rebecca_day)

# 2. Lan and Olivia cannot lead sessions on the same day
solver.add(Lan_day != Olivia_day)

# 3. Nessa must lead an afternoon session
solver.add(Nessa_time == 1)

# 4. Julio's session must meet on an earlier day than Olivia's
solver.add(Julio_day < Olivia_day)

# Additional constraint: Lan does not lead a Wednesday session
solver.add(Lan_day != 0)

# Base constraints for the multiple choice options
# We will test each option to see if the assistant must lead a Thursday session

found_options = []

# Option A: Rebecca leads a Thursday session
solver.push()
solver.add(Rebecca_day == 1)
if solver.check() == sat:
    found_options.append("A")
    model = solver.model()
    print("Option A model:")
    print(f"Rebecca_day = {model[Rebecca_day]}, Rebecca_time = {model[Rebecca_time]}")
solver.pop()

# Option B: Olivia leads a Thursday session
solver.push()
solver.add(Olivia_day == 1)
if solver.check() == sat:
    found_options.append("B")
    model = solver.model()
    print("Option B model:")
    print(f"Olivia_day = {model[Olivia_day]}, Olivia_time = {model[Olivia_time]}")
solver.pop()

# Option C: Nessa leads a Thursday session
solver.push()
solver.add(Nessa_day == 1)
if solver.check() == sat:
    found_options.append("C")
    model = solver.model()
    print("Option C model:")
    print(f"Nessa_day = {model[Nessa_day]}, Nessa_time = {model[Nessa_time]}")
solver.pop()

# Option D: Kevin leads a Thursday session
solver.push()
solver.add(Kevin_day == 1)
if solver.check() == sat:
    found_options.append("D")
    model = solver.model()
    print("Option D model:")
    print(f"Kevin_day = {model[Kevin_day]}, Kevin_time = {model[Kevin_time]}")
solver.pop()

# Option E: Julio leads a Thursday session
solver.push()
solver.add(Julio_day == 1)
if solver.check() == sat:
    found_options.append("E")
    model = solver.model()
    print("Option E model:")
    print(f"Julio_day = {model[Julio_day]}, Julio_time = {model[Julio_time]}")
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