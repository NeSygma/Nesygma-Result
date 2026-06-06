from z3 import *

# Candidates: Jaramillo, Kayne, Landon, Novetzke, Ong
# Countries: Venezuela, Yemen, Zambia
# We'll assign each country an ambassador (one of the candidates)
# Use Int variables: 0=Jaramillo, 1=Kayne, 2=Landon, 3=Novetzke, 4=Ong

J, K, L, N, O = 0, 1, 2, 3, 4

venezuela = Int('venezuela')
yemen = Int('yemen')
zambia = Int('zambia')

solver = Solver()

# Domain: each country gets one of the 5 candidates
solver.add(And(venezuela >= 0, venezuela <= 4))
solver.add(And(yemen >= 0, yemen <= 4))
solver.add(And(zambia >= 0, zambia <= 4))

# No ambassador assigned to more than one country (all distinct)
solver.add(Distinct(venezuela, yemen, zambia))

# Constraint 1: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships.
# Exactly one of {Kayne, Novetzke} is assigned to some country.
# Count how many of {K, N} appear among the three assignments.
solver.add(Sum([If(venezuela == K, 1, 0), If(yemen == K, 1, 0), If(zambia == K, 1, 0),
                If(venezuela == N, 1, 0), If(yemen == N, 1, 0), If(zambia == N, 1, 0)]) == 1)

# Constraint 2: If Jaramillo is assigned to one of the ambassadorships, then so is Kayne.
# If J is assigned anywhere, then K is assigned somewhere.
solver.add(Implies(
    Or(venezuela == J, yemen == J, zambia == J),
    Or(venezuela == K, yemen == K, zambia == K)
))

# Constraint 3: If Ong is assigned as ambassador to Venezuela, Kayne is not assigned as ambassador to Yemen.
solver.add(Implies(venezuela == O, yemen != K))

# Constraint 4: If Landon is assigned to an ambassadorship, it is to Zambia.
solver.add(Implies(
    Or(venezuela == L, yemen == L, zambia == L),
    zambia == L
))

# Now evaluate each option
# Option A: Venezuela: Jaramillo, Yemen: Ong, Zambia: Novetzke
opt_a = And(venezuela == J, yemen == O, zambia == N)

# Option B: Venezuela: Kayne, Yemen: Jaramillo, Zambia: Landon
opt_b = And(venezuela == K, yemen == J, zambia == L)

# Option C: Venezuela: Landon, Yemen: Novetzke, Zambia: Ong
opt_c = And(venezuela == L, yemen == N, zambia == O)

# Option D: Venezuela: Novetzke, Yemen: Jaramillo, Zambia: Kayne
opt_d = And(venezuela == N, yemen == J, zambia == K)

# Option E: Venezuela: Ong, Yemen: Kayne, Zambia: Landon
opt_e = And(venezuela == O, yemen == K, zambia == L)

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