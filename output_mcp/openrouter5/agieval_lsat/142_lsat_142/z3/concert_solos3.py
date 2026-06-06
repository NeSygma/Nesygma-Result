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

# Let's enumerate all solutions to see the full picture
print("All valid assignments:")
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {v: m.eval(v, model_completion=True) for v in members}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([v != m.eval(v, model_completion=True) for v in members]))

print(f"Total solutions: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"  Solution {i+1}: guitarist={sol[guitarist]}, keyboard={sol[keyboard]}, percussionist={sol[percussionist]}, saxophonist={sol[saxophonist]}, trumpeter={sol[trumpeter]}, violinist={sol[violinist]}")

# Now let's check: for each position 1-6, which members can be at that position?
print("\n--- Position analysis ---")
for pos in range(1, 7):
    possible = []
    for member_name, member_var in [("guitarist", guitarist), ("keyboard", keyboard), ("percussionist", percussionist), ("saxophonist", saxophonist), ("trumpeter", trumpeter), ("violinist", violinist)]:
        s = Solver()
        for m in members:
            s.add(m >= 1, m <= 6)
        s.add(Distinct(members))
        s.add(guitarist != 4)
        s.add(percussionist < keyboard)
        s.add(violinist < keyboard)
        s.add(keyboard < guitarist)
        s.add(If(saxophonist > percussionist, 1, 0) + If(saxophonist > trumpeter, 1, 0) == 1)
        s.add(member_var == pos)
        if s.check() == sat:
            possible.append(member_name)
    print(f"  Position {pos}: {possible}")

# Now evaluate each option: "X CANNOT perform the third solo"
# We test: can X perform the third solo? If sat, it's possible. If unsat, it's impossible (CANNOT).
# We want the one that CANNOT, i.e., the one where adding "X == 3" makes it unsat.

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
res = s.check()
print(f"\nOption A (guitarist==3): {res}")
if res == sat:
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
res = s.check()
print(f"Option B (keyboard==3): {res}")
if res == sat:
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
res = s.check()
print(f"Option C (saxophonist==3): {res}")
if res == sat:
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
res = s.check()
print(f"Option D (trumpeter==3): {res}")
if res == sat:
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
res = s.check()
print(f"Option E (violinist==3): {res}")
if res == sat:
    found_options.append("E")

print(f"\nFound options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")