from z3 import *

solver = Solver()

# Students: Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio
# Years: 1921, 1922, 1923, 1924
# We need to assign exactly 4 students to the 4 years.
# Let's model: for each student, a variable indicating which year they are assigned (0-3 for 1921-1924),
# or a special value meaning "not assigned".

# We'll use Int variables for each student, domain 0..4 where 0=1921,1=1922,2=1923,3=1924, and 4=not assigned.
Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio = Ints('Louis Mollie Onyx Ryan Tiffany Yoshio')

# Domain: each student gets a value 0..4
students = [Louis, Mollie, Onyx, Ryan, Tiffany, Yoshio]
for s in students:
    solver.add(s >= 0, s <= 4)

# Exactly four students are assigned (value 0..3), and two are not assigned (value 4).
# Count how many are assigned (value < 4)
solver.add(Sum([If(s < 4, 1, 0) for s in students]) == 4)

# Each year (0..3) has exactly one student assigned to it.
# So for each year y, exactly one student has value == y.
for y in range(4):
    solver.add(Sum([If(s == y, 1, 0) for s in students]) == 1)

# Condition 1: Only Louis or Tiffany can be assigned to 1923 (year 2).
# So if someone else is assigned to 1923, that's invalid.
# Actually: "Only Louis or Tiffany can be assigned to 1923" means:
# If a student is assigned to 1923, that student must be Louis or Tiffany.
# Equivalently: For any student s, if s == 2 then s must be Louis or Tiffany.
# We can encode: For each student other than Louis and Tiffany, they cannot be 2.
solver.add(And([s != 2 for s in [Mollie, Onyx, Ryan, Yoshio]]))
# Also: Louis and Tiffany could be 2, but at least one of them must be? No, "only" means
# no one else can be 1923. It doesn't require that 1923 is assigned. But we already have
# exactly one student per year, so 1923 must be assigned to someone. So it must be Louis or Tiffany.
# Already covered by the above.

# Condition 2: If Mollie is assigned to the project, then she must be assigned to either 1921 or 1922.
# Mollie assigned means Mollie < 4. Then Mollie must be 0 or 1.
solver.add(Implies(Mollie < 4, Or(Mollie == 0, Mollie == 1)))

# Condition 3: If Tiffany is assigned to the project, then Ryan must be assigned to the project.
solver.add(Implies(Tiffany < 4, Ryan < 4))

# Condition 4: If Ryan is assigned to the project, then Onyx must be assigned to the year immediately prior to Ryan's.
# Ryan assigned means Ryan < 4. Then Onyx must be assigned and Onyx == Ryan - 1.
solver.add(Implies(Ryan < 4, And(Onyx < 4, Onyx == Ryan - 1)))

# Additional constraint from condition 4: if Ryan is assigned, Onyx must be assigned to the year prior.
# Since years are 0..3, Ryan must be at least 1 (1922 or later) for there to be a prior year.
# But the condition says "immediately prior" - if Ryan is 0 (1921), there's no prior year, so Ryan cannot be 0.
solver.add(Implies(Ryan < 4, Ryan >= 1))

# Given: Yoshio is not assigned to the project.
solver.add(Yoshio == 4)

# Now evaluate each option
# Option A: Louis is not assigned to the project.
opt_a = (Louis == 4)

# Option B: Ryan is not assigned to the project.
opt_b = (Ryan == 4)

# Option C: Tiffany is not assigned to the project.
opt_c = (Tiffany == 4)

# Option D: Onyx is assigned to 1922 (year 1).
opt_d = (Onyx == 1)

# Option E: Louis is assigned to 1924 (year 3).
opt_e = (Louis == 3)

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