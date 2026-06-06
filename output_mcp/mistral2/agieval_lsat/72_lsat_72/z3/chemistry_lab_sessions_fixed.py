from z3 import *

solver = Solver()

# Days: Wednesday=0, Thursday=1, Friday=2
# Times: Morning=0, Afternoon=1

# Assign each lab assistant to a session (day, time)
# We represent each assignment as a pair (day, time)

Julio_day = Int('Julio_day')
Julio_time = Int('Julio_time')

Kevin_day = Int('Kevin_day')
Kevin_time = Int('Kevin_time')

Lan_day = Int('Lan_day')
Lan_time = Int('Lan_time')

Nessa_day = Int('Nessa_day')
Nessa_time = Int('Nessa_time')

Olivia_day = Int('Olivia_day')
Olivia_time = Int('Olivia_time')

Rebecca_day = Int('Rebecca_day')
Rebecca_time = Int('Rebecca_time')

# Each assistant is assigned to a unique session
solver.add(Distinct(
    Julio_day, Julio_time,
    Kevin_day, Kevin_time,
    Lan_day, Lan_time,
    Nessa_day, Nessa_time,
    Olivia_day, Olivia_time,
    Rebecca_day, Rebecca_time
))

# Days and times are within bounds
solver.add(Julio_day >= 0, Julio_day <= 2)
solver.add(Julio_time >= 0, Julio_time <= 1)

solver.add(Kevin_day >= 0, Kevin_day <= 2)
solver.add(Kevin_time >= 0, Kevin_time <= 1)

solver.add(Lan_day >= 0, Lan_day <= 2)
solver.add(Lan_time >= 0, Lan_time <= 1)

solver.add(Nessa_day >= 0, Nessa_day <= 2)
solver.add(Nessa_time >= 0, Nessa_time <= 1)

solver.add(Olivia_day >= 0, Olivia_day <= 2)
solver.add(Olivia_time >= 0, Olivia_time <= 1)

solver.add(Rebecca_day >= 0, Rebecca_day <= 2)
solver.add(Rebecca_time >= 0, Rebecca_time <= 1)

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