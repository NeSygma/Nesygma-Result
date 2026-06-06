from z3 import *

solver = Solver()

# Slots: 6 slots for 3 days, 2 per day
# s0 = Mon morning, s1 = Mon afternoon
# s2 = Tue morning, s3 = Tue afternoon
# s4 = Wed morning, s5 = Wed afternoon
s0, s1, s2, s3, s4, s5 = Ints('s0 s1 s2 s3 s4 s5')

# Student numbers:
# 0: George, 1: Helen, 2: Irving, 3: Kyle, 4: Lenore, 5: Nina, 6: Olivia, 7: Robert

# Domain: each slot is one of the 8 students
for s in [s0, s1, s2, s3, s4, s5]:
    solver.add(s >= 0, s <= 7)

# All slots have distinct students (exactly 6 different students, 2 not assigned)
solver.add(Distinct([s0, s1, s2, s3, s4, s5]))

# Condition 1: Tuesday is the only day George can give a report
# George cannot be on Monday or Wednesday
solver.add(And(s0 != 0, s1 != 0, s4 != 0, s5 != 0))

# Condition 2: Neither Olivia nor Robert can give an afternoon report
# Olivia (6) and Robert (7) cannot be in afternoon slots (s1, s3, s5)
solver.add(And(s1 != 6, s3 != 6, s5 != 6))
solver.add(And(s1 != 7, s3 != 7, s5 != 7))

# Condition 3: If Nina gives a report, then on the next day Helen and Irving must both give reports,
# unless Nina's report is given on Wednesday.
nina_monday = Or(s0 == 5, s1 == 5)
nina_tuesday = Or(s2 == 5, s3 == 5)

helen_tuesday = Or(s2 == 1, s3 == 1)
irving_tuesday = Or(s2 == 2, s3 == 2)
helen_wednesday = Or(s4 == 1, s5 == 1)
irving_wednesday = Or(s4 == 2, s5 == 2)

solver.add(Implies(nina_monday, And(helen_tuesday, irving_tuesday)))
solver.add(Implies(nina_tuesday, And(helen_wednesday, irving_wednesday)))

# Now test each option
options = {
    "A": And(s0 == 1, s1 == 7, s2 == 6, s3 == 2, s4 == 4, s5 == 3),  # Helen, Robert, Olivia, Irving, Lenore, Kyle
    "B": And(s0 == 2, s1 == 6, s2 == 1, s3 == 3, s4 == 5, s5 == 4),  # Irving, Olivia, Helen, Kyle, Nina, Lenore
    "C": And(s0 == 4, s1 == 1, s2 == 0, s3 == 3, s4 == 7, s5 == 2),  # Lenore, Helen, George, Kyle, Robert, Irving
    "D": And(s0 == 5, s1 == 1, s2 == 7, s3 == 2, s4 == 6, s5 == 4),  # Nina, Helen, Robert, Irving, Olivia, Lenore
    "E": And(s0 == 6, s1 == 5, s2 == 2, s3 == 1, s4 == 3, s5 == 0),  # Olivia, Nina, Irving, Helen, Kyle, George
}

found_options = []
for letter, constr in options.items():
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