from z3 import *

# Students: Grecia (G), Hakeem (H), Joe (J), Katya (K), Louise (L)
students = ['G', 'H', 'J', 'K', 'L']
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
shifts = [0, 1]  # 0 = first shift, 1 = second shift

# We'll model using a 3D boolean: assign[s][d][sh] = True if student s works day d shift sh
# But easier: use Int variables for each shift slot: shift[day][shift_num] = student index (0-4)
# shift[day][0] = first shift, shift[day][1] = second shift

shift = [[Int(f"shift_{d}_{sh}") for sh in shifts] for d in range(5)]

solver = Solver()

# Domain: each shift is assigned to exactly one student (0-4)
for d in range(5):
    for sh in shifts:
        solver.add(shift[d][sh] >= 0, shift[d][sh] <= 4)

# Each student works exactly two shifts total
student_shift_count = [Sum([If(shift[d][sh] == s, 1, 0) for d in range(5) for sh in shifts]) for s in range(5)]
for s in range(5):
    solver.add(student_shift_count[s] == 2)

# No student works both shifts of any day
for d in range(5):
    solver.add(shift[d][0] != shift[d][1])

# On two consecutive days, Louise works the second shift.
# Louise = index 4. Second shift = sh=1.
# Two consecutive days: (Mon,Tue), (Tue,Wed), (Wed,Thu), (Thu,Fri)
# Exactly one pair of consecutive days where Louise works second shift on both.
consec_pairs = [(0,1), (1,2), (2,3), (3,4)]
louise_second_consec = [And(shift[d1][1] == 4, shift[d2][1] == 4) for (d1,d2) in consec_pairs]
solver.add(Sum([If(lc, 1, 0) for lc in louise_second_consec]) == 1)

# On two nonconsecutive days, Grecia works the first shift.
# Grecia = index 0. First shift = sh=0.
# Nonconsecutive pairs: (Mon,Wed), (Mon,Thu), (Mon,Fri), (Tue,Thu), (Tue,Fri), (Wed,Fri)
nonconsec_pairs = [(0,2), (0,3), (0,4), (1,3), (1,4), (2,4)]
gracia_first_nonconsec = [And(shift[d1][0] == 0, shift[d2][0] == 0) for (d1,d2) in nonconsec_pairs]
solver.add(Sum([If(gf, 1, 0) for gf in gracia_first_nonconsec]) == 1)

# Katya works on Tuesday and Friday.
# Katya = index 3. She works at least one shift on Tuesday (day 1) and at least one on Friday (day 4).
solver.add(Or(shift[1][0] == 3, shift[1][1] == 3))  # Tuesday
solver.add(Or(shift[4][0] == 3, shift[4][1] == 3))  # Friday

# Hakeem and Joe work on the same day as each other at least once.
# Hakeem = index 1, Joe = index 2.
# At least one day where both work (any shifts, possibly different)
solver.add(Or([Or(And(shift[d][0] == 1, shift[d][1] == 2),
                  And(shift[d][0] == 2, shift[d][1] == 1),
                  And(shift[d][0] == 1, shift[d][0] == 2),
                  And(shift[d][1] == 1, shift[d][1] == 2)) for d in range(5)]))

# Actually simpler: Hakeem and Joe work on the same day means there exists a day d
# such that (shift[d][0] == 1 or shift[d][1] == 1) AND (shift[d][0] == 2 or shift[d][1] == 2)
solver.add(Or([And(Or(shift[d][0] == 1, shift[d][1] == 1),
                   Or(shift[d][0] == 2, shift[d][1] == 2)) for d in range(5)]))

# Grecia and Louise never work on the same day as each other.
# Grecia = 0, Louise = 4.
for d in range(5):
    solver.add(Not(And(Or(shift[d][0] == 0, shift[d][1] == 0),
                       Or(shift[d][0] == 4, shift[d][1] == 4))))

# Additional constraint: Hakeem works on Wednesday (day 2).
# This is the "if" condition in the question.
solver.add(Or(shift[2][0] == 1, shift[2][1] == 1))

# Now evaluate each option: which pair of days must Joe work on?
# Joe = index 2.
# Option A: Monday and Wednesday (days 0 and 2)
# Option B: Monday and Thursday (days 0 and 3)
# Option C: Tuesday and Wednesday (days 1 and 2)
# Option D: Tuesday and Thursday (days 1 and 3)
# Option E: Wednesday and Thursday (days 2 and 3)

# For each option, we check: does Joe work on BOTH days of that pair?
# We need to find which option MUST be true (i.e., is forced by the constraints).
# So we test each option: add the constraint that Joe does NOT work on that pair,
# and see if it becomes unsatisfiable. If so, that pair is forced.

# Actually, the question says: "If Hakeem works on Wednesday, then Joe must work on which pair?"
# So we need to find which pair is NECESSARILY true.
# We can check: for each option, add the negation (Joe doesn't work on both those days)
# and see if the whole thing becomes unsat. If unsat, that option is forced.

found_options = []
option_days = {
    "A": (0, 2),  # Mon, Wed
    "B": (0, 3),  # Mon, Thu
    "C": (1, 2),  # Tue, Wed
    "D": (1, 3),  # Tue, Thu
    "E": (2, 3)   # Wed, Thu
}

for letter, (d1, d2) in option_days.items():
    solver.push()
    # Negation: Joe does NOT work on both d1 and d2
    # Joe works on a day if he has either shift on that day
    joe_works_d1 = Or(shift[d1][0] == 2, shift[d1][1] == 2)
    joe_works_d2 = Or(shift[d2][0] == 2, shift[d2][1] == 2)
    # Negation: not (joe works d1 AND joe works d2)
    solver.add(Not(And(joe_works_d1, joe_works_d2)))
    if solver.check() == unsat:
        # If negating this option makes it unsat, then this option is forced
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