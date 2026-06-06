from z3 import *

solver = Solver()

# Students: Juana, Kelly, Lateefah, Mei, Olga
# Teams: 0 = green, 1 = red
# Facilitator: 1 = facilitator, 0 = not facilitator

# Variables for team assignment (0=green, 1=red)
juana = Int('juana')
kelly = Int('kelly')
lateefah = Int('lateefah')
mei = Int('mei')
olga = Int('olga')

# Variables for facilitator status (1=yes, 0=no)
juana_fac = Int('juana_fac')
kelly_fac = Int('kelly_fac')
lateefah_fac = Int('lateefah_fac')
mei_fac = Int('mei_fac')
olga_fac = Int('olga_fac')

students = [juana, kelly, lateefah, mei, olga]
facilitators = [juana_fac, kelly_fac, lateefah_fac, mei_fac, olga_fac]

# Domain constraints: team is 0 or 1, facilitator is 0 or 1
for s in students:
    solver.add(Or(s == 0, s == 1))
for f in facilitators:
    solver.add(Or(f == 0, f == 1))

# Exactly one team has 2 members, the other has 3 members
green_count = Sum([If(s == 0, 1, 0) for s in students])
solver.add(Or(green_count == 2, green_count == 3))

# One member of each team is designated as facilitator
green_fac_count = Sum([If(And(students[i] == 0, facilitators[i] == 1), 1, 0) for i in range(5)])
red_fac_count = Sum([If(And(students[i] == 1, facilitators[i] == 1), 1, 0) for i in range(5)])
solver.add(green_fac_count == 1)
solver.add(red_fac_count == 1)

# Juana is assigned to a different team than Olga
solver.add(juana != olga)

# Lateefah is assigned to the green team
solver.add(lateefah == 0)

# Kelly is not a facilitator
solver.add(kelly_fac == 0)

# Olga is a facilitator
solver.add(olga_fac == 1)

# The question asks: "Which one of the following must be false?"
# This means we need to find the option that CANNOT be true under the constraints.
# So we check each option: if it's UNSAT (impossible), that's the answer.

# Option A: Lateefah is a facilitator, and she is assigned to the same team as Kelly is.
opt_a_constr = And(lateefah_fac == 1, lateefah == kelly)

# Option B: Mei is a facilitator, and she is assigned to the same team as Kelly is.
opt_b_constr = And(mei_fac == 1, mei == kelly)

# Option C: Olga is a facilitator, and she is assigned to the same team as Mei is.
opt_c_constr = And(olga_fac == 1, olga == mei)

# Option D: Lateefah is a facilitator, and she is assigned to a different team than Juana is.
opt_d_constr = And(lateefah_fac == 1, lateefah != juana)

# Option E: Mei is a facilitator, and she is assigned to a different team than Olga is.
opt_e_constr = And(mei_fac == 1, mei != olga)

# For "must be false" - we want the option that is UNSAT (impossible)
# Let's check each one
results = {}
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    s = Solver()
    # Add all base constraints
    for c in solver.assertions():
        s.add(c)
    s.add(constr)
    res = s.check()
    results[letter] = res
    print(f"Option {letter}: {res}")
    if res == sat:
        m = s.model()
        for i, name in enumerate(['juana', 'kelly', 'lateefah', 'mei', 'olga']):
            print(f"  {name}: team={m[students[i]]}, fac={m[facilitators[i]]}")

# The option that must be false is the one that is UNSAT
unsat_options = [letter for letter, res in results.items() if res == unsat]
print(f"UNSAT options (must be false): {unsat_options}")

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")