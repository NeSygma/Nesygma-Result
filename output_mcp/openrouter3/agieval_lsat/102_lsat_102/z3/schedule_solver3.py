from z3 import *

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
Franco = Int('Franco')
Garcia = Int('Garcia')
Hong = Int('Hong')
Iturbe = Int('Iturbe')
Jackson = Int('Jackson')

# Base constraints
base_constraints = [
    Franco >= 0, Franco <= 2,
    Garcia >= 0, Garcia <= 2,
    Hong >= 0, Hong <= 2,
    Iturbe >= 0, Iturbe <= 2,
    Jackson >= 0, Jackson <= 2,
    Franco != Garcia,
    Iturbe == 2,
    Sum([If(Franco == 1, 1, 0),
         If(Garcia == 1, 1, 0),
         If(Hong == 1, 1, 0),
         If(Iturbe == 1, 1, 0),
         If(Jackson == 1, 1, 0)]) == 2,
    Hong != 0,
    Sum([If(Franco == 0, 1, 0),
         If(Garcia == 0, 1, 0),
         If(Hong == 0, 1, 0),
         If(Iturbe == 0, 1, 0),
         If(Jackson == 0, 1, 0)]) >= 1,
    Franco == Hong  # Given condition
]

# Answer choices as constraints
opt_a = (Franco == 2)  # A: Franco on Wednesday
opt_b = (Garcia == 0)  # B: Garcia on Monday
opt_c = (Garcia == 2)  # C: Garcia on Wednesday
opt_d = (Hong == 1)    # D: Hong on Tuesday
opt_e = And(Iturbe == 2,
            Franco != 2,
            Garcia != 2,
            Hong != 2,
            Jackson != 2)  # E: Iturbe only on Wednesday

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# For each option, check if the constraints + NOT(option) is unsatisfiable
must_be_true = []
for letter, opt in options:
    s = Solver()
    s.add(base_constraints)
    s.add(Not(opt))
    if s.check() == unsat:
        must_be_true.append(letter)

if len(must_be_true) == 1:
    print("STATUS: proved")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unknown")
    print(f"Refine: Multiple options must be true: {must_be_true}")
else:
    print("STATUS: unknown")
    print("Refine: No option must be true")