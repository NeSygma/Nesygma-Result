from z3 import *

solver = Solver()

# Six auditions: positions 0 through 5 (1-indexed in problem, 0-indexed in code)
# We'll use 0-indexed internally but map to 1-indexed for clarity.
# Let's assign each singer a position (0 to 5).
Kammer, Lugo, Trillo, Waite, Yoshida, Zinn = Ints('Kammer Lugo Trillo Waite Yoshida Zinn')
singers = [Kammer, Lugo, Trillo, Waite, Yoshida, Zinn]

# Each singer gets a distinct position from 0 to 5
solver.add(Distinct(singers))
for s in singers:
    solver.add(s >= 0, s <= 5)

# Recorded auditions: Kammer and Lugo
# The fourth audition (position 3 in 0-indexed) cannot be recorded.
# So Kammer and Lugo cannot be at position 3.
solver.add(Kammer != 3)
solver.add(Lugo != 3)

# The fifth audition (position 4 in 0-indexed) must be recorded.
# So either Kammer or Lugo must be at position 4.
solver.add(Or(Kammer == 4, Lugo == 4))

# Waite's audition must take place earlier than the two recorded auditions.
# So Waite's position < Kammer's position AND Waite's position < Lugo's position.
solver.add(Waite < Kammer)
solver.add(Waite < Lugo)

# Kammer's audition must take place earlier than Trillo's audition.
solver.add(Kammer < Trillo)

# Zinn's audition must take place earlier than Yoshida's audition.
solver.add(Zinn < Yoshida)

# Now evaluate each option for the sixth audition (position 5 in 0-indexed)
found_options = []

# Option A: Kammer's audition is 6th (position 5)
opt_a = (Kammer == 5)

# Option B: Lugo's audition is 6th (position 5)
opt_b = (Lugo == 5)

# Option C: Trillo's audition is 6th (position 5)
opt_c = (Trillo == 5)

# Option D: Waite's audition is 6th (position 5)
opt_d = (Waite == 5)

# Option E: Zinn's audition is 6th (position 5)
opt_e = (Zinn == 5)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
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