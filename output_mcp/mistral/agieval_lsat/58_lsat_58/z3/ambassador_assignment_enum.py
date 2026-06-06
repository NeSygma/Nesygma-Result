from z3 import *

# Define the countries and candidates as EnumSort
Country = EnumSort('Country', ['Venezuela', 'Yemen', 'Zambia'])
Candidate = EnumSort('Candidate', ['Jaramillo', 'Kayne', 'Landon', 'Novetzke', 'Ong'])

# Create a solver
solver = Solver()

# Assignments: country -> candidate (using EnumSort)
assignment = {c: Const(f"assignment_{c}", Candidate) for c in Country}

# Candidate assignment: candidate -> Bool (True if assigned)
assigned = {p: Bool(f"assigned_{p}") for p in Candidate}

# Constraint 1: Each country is assigned exactly one candidate
for c in Country:
    # Each country is assigned some candidate
    solver.add(Or([assignment[c] == p for p in Candidate]))

# Constraint 2: Each candidate is assigned to at most one country
for p in Candidate:
    solver.add(AtMost(*[assignment[c] == p for c in Country], 1))

# Constraint 3: Exactly one of Kayne or Novetzke is assigned
solver.add(assigned[Candidate.Kayne] != assigned[Candidate.Novetzke])
solver.add(Or(assigned[Candidate.Kayne], assigned[Candidate.Novetzke]))

# Constraint 4: If Jaramillo is assigned, then Kayne is assigned
solver.add(Implies(assigned[Candidate.Jaramillo], assigned[Candidate.Kayne]))

# Constraint 5: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen
solver.add(Implies(assignment[Country.Venezuela] == Candidate.Ong, assignment[Country.Yemen] != Candidate.Kayne))

# Constraint 6: If Landon is assigned, it is to Zambia
solver.add(Implies(assigned[Candidate.Landon], assignment[Country.Zambia] == Candidate.Landon))

# Link assignment to assigned
for p in Candidate:
    solver.add(assigned[p] == Or([assignment[c] == p for c in Country]))

# Base constraints are set. Now evaluate the multiple-choice options.

# Define the options as constraints
# Option A: Jaramillo is assigned as ambassador to Zambia
opt_a_constr = (assignment[Country.Zambia] == Candidate.Jaramillo)

# Option B: Kayne is assigned as ambassador to Zambia
opt_b_constr = (assignment[Country.Zambia] == Candidate.Kayne)

# Option C: Novetzke is assigned as ambassador to Zambia
opt_c_constr = (assignment[Country.Zambia] == Candidate.Novetzke)

# Option D: Landon is not assigned to an ambassadorship
opt_d_constr = Not(assigned[Candidate.Landon])

# Option E: Ong is not assigned to an ambassadorship
opt_e_constr = Not(assigned[Candidate.Ong])

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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