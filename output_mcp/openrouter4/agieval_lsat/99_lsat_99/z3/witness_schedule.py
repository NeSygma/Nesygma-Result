from z3 import *

solver = Solver()

# Days: Monday=0, Tuesday=1, Wednesday=2
Mon, Tue, Wed = 0, 1, 2

# Witnesses
Franco = Int('Franco')
Garcia = Int('Garcia')
Hong = Int('Hong')
Iturbe = Int('Iturbe')
Jackson = Int('Jackson')
witness_vars = [Franco, Garcia, Hong, Iturbe, Jackson]

# Domain: each witness testifies on exactly one day (0,1,2)
for w in witness_vars:
    solver.add(w >= 0, w <= 2)

# Constraints
# 1. Franco does not testify on the same day as Garcia
solver.add(Franco != Garcia)

# 2. Iturbe testifies on Wednesday
solver.add(Iturbe == Wed)

# 3. Exactly two witnesses testify on Tuesday
solver.add(Sum([If(w == Tue, 1, 0) for w in witness_vars]) == 2)

# 4. Hong does not testify on Monday
solver.add(Hong != Mon)

# 5. At least one witness testifies on Monday
solver.add(Sum([If(w == Mon, 1, 0) for w in witness_vars]) >= 1)

# Now evaluate each option

# Option A: Franco is the only witness scheduled to testify on Monday.
opt_a = And(Franco == Mon,
            Garcia != Mon,
            Hong != Mon,
            Iturbe != Mon,
            Jackson != Mon)

# Option B: Franco is scheduled to testify on the same day as Iturbe.
opt_b = (Franco == Iturbe)

# Option C: Garcia and Hong are both scheduled to testify on Tuesday.
opt_c = And(Garcia == Tue, Hong == Tue)

# Option D: Garcia is the only witness scheduled to testify on Monday AND Hong is one of two witnesses scheduled to testify on Wednesday.
opt_d1 = And(Garcia == Mon,
             Franco != Mon,
             Hong != Mon,
             Iturbe != Mon,
             Jackson != Mon)
opt_d2 = And(Hong == Wed,
             Sum([If(w == Wed, 1, 0) for w in witness_vars]) == 2)
opt_d = And(opt_d1, opt_d2)

# Option E: Jackson is scheduled to testify on Tuesday AND two witnesses are scheduled to testify on Monday.
opt_e = And(Jackson == Tue,
            Sum([If(w == Mon, 1, 0) for w in witness_vars]) == 2)

# Now test each option
found_options = []
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