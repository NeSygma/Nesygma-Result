from z3 import *

# Six band members, each performs exactly one solo (positions 1-6)
guitarist, keyboard, percussionist, saxophonist, trumpeter, violinist = Ints('guitarist keyboard percussionist saxophonist trumpeter violinist')
members = [guitarist, keyboard, percussionist, saxophonist, trumpeter, violinist]

solver = Solver()

# Each position is from 1 to 6
for m in members:
    solver.add(m >= 1, m <= 6)

# All positions are distinct
solver.add(Distinct(members))

# The guitarist does not perform the fourth solo.
solver.add(guitarist != 4)

# The percussionist performs a solo at some time before the keyboard player does.
solver.add(percussionist < keyboard)

# The keyboard player performs a solo at some time after the violinist does and at some time before the guitarist does.
solver.add(violinist < keyboard)
solver.add(keyboard < guitarist)

# The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both.
# "after either P or T, but not both" means:
# (sax > percussionist) XOR (sax > trumpeter)
# XOR: exactly one of them is true.
solver.add(If(saxophonist > percussionist, 1, 0) + If(saxophonist > trumpeter, 1, 0) == 1)

# The question asks: which CANNOT perform the third solo?
# We need to find the member for whom position 3 is impossible.
# Let's check each option.

found_options = []

# Option A: guitarist
s = Solver()
for m in members:
    s.add(m >= 1, m <= 6)
s.add(Distinct(members))
s.add(guitarist != 4)
s.add(percussionist < keyboard)
s.add(violinist < keyboard)
s.add(keyboard < guitarist)
s.add(If(saxophonist > percussionist, 1, 0) + If(saxophonist > trumpeter, 1, 0) == 1)
s.add(guitarist == 3)
if s.check() == sat:
    found_options.append("A")

# Option B: keyboard player
s = Solver()
for m in members:
    s.add(m >= 1, m <= 6)
s.add(Distinct(members))
s.add(guitarist != 4)
s.add(percussionist < keyboard)
s.add(violinist < keyboard)
s.add(keyboard < guitarist)
s.add(If(saxophonist > percussionist, 1, 0) + If(saxophonist > trumpeter, 1, 0) == 1)
s.add(keyboard == 3)
if s.check() == sat:
    found_options.append("B")

# Option C: saxophonist
s = Solver()
for m in members:
    s.add(m >= 1, m <= 6)
s.add(Distinct(members))
s.add(guitarist != 4)
s.add(percussionist < keyboard)
s.add(violinist < keyboard)
s.add(keyboard < guitarist)
s.add(If(saxophonist > percussionist, 1, 0) + If(saxophonist > trumpeter, 1, 0) == 1)
s.add(saxophonist == 3)
if s.check() == sat:
    found_options.append("C")

# Option D: trumpeter
s = Solver()
for m in members:
    s.add(m >= 1, m <= 6)
s.add(Distinct(members))
s.add(guitarist != 4)
s.add(percussionist < keyboard)
s.add(violinist < keyboard)
s.add(keyboard < guitarist)
s.add(If(saxophonist > percussionist, 1, 0) + If(saxophonist > trumpeter, 1, 0) == 1)
s.add(trumpeter == 3)
if s.check() == sat:
    found_options.append("D")

# Option E: violinist
s = Solver()
for m in members:
    s.add(m >= 1, m <= 6)
s.add(Distinct(members))
s.add(guitarist != 4)
s.add(percussionist < keyboard)
s.add(violinist < keyboard)
s.add(keyboard < guitarist)
s.add(If(saxophonist > percussionist, 1, 0) + If(saxophonist > trumpeter, 1, 0) == 1)
s.add(violinist == 3)
if s.check() == sat:
    found_options.append("E")

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")