from z3 import *

# Five students: Grecia (G), Hakeem (H), Joe (J), Katya (K), Louise (L)
# Days: Monday (0), Tuesday (1), Wednesday (2), Thursday (3), Friday (4)
# Shifts: first (0), second (1)

students = ["G", "H", "J", "K", "L"]
days = list(range(5))  # 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
shifts = [0, 1]  # 0=first, 1=second

# Decision variables: assign[student][day][shift] = Bool (True if student works that shift)
assign = {s: {d: {sh: Bool(f"{s}_{d}_{sh}") for sh in shifts} for d in days} for s in students}

solver = Solver()

# Each shift is worked by exactly one student
for d in days:
    for sh in shifts:
        solver.add(Sum([If(assign[s][d][sh], 1, 0) for s in students]) == 1)

# Each student works exactly two shifts total
for s in students:
    solver.add(Sum([If(assign[s][d][sh], 1, 0) for d in days for sh in shifts]) == 2)

# No student works both shifts of any day
for s in students:
    for d in days:
        solver.add(Not(And(assign[s][d][0], assign[s][d][1])))

# On two consecutive days, Louise works the second shift.
# There exists a pair of consecutive days (d, d+1) such that Louise works second shift on both.
consec_louise_second = []
for d in range(4):
    consec_louise_second.append(And(assign["L"][d][1], assign["L"][d+1][1]))
solver.add(Or(consec_louise_second))

# On two nonconsecutive days, Grecia works the first shift.
# There exist two days d1, d2 with |d1-d2| > 1 such that Grecia works first shift on both.
nonconsec_grecia_first = []
for d1 in range(5):
    for d2 in range(5):
        if abs(d1 - d2) > 1:
            nonconsec_grecia_first.append(And(assign["G"][d1][0], assign["G"][d2][0]))
solver.add(Or(nonconsec_grecia_first))

# Katya works on Tuesday (day 1) and Friday (day 4).
# Katya works exactly one shift on Tuesday and exactly one shift on Friday.
solver.add(Or(assign["K"][1][0], assign["K"][1][1]))  # works Tuesday
solver.add(Or(assign["K"][4][0], assign["K"][4][1]))  # works Friday
# Katya works exactly two shifts total (already covered), so she works Tue and Fri.

# Hakeem and Joe work on the same day as each other at least once.
same_day_hj = []
for d in days:
    # Hakeem works some shift on day d AND Joe works some shift on day d
    same_day_hj.append(And(Or(assign["H"][d][0], assign["H"][d][1]),
                           Or(assign["J"][d][0], assign["J"][d][1])))
solver.add(Or(same_day_hj))

# Grecia and Louise never work on the same day as each other.
for d in days:
    solver.add(Not(And(Or(assign["G"][d][0], assign["G"][d][1]),
                       Or(assign["L"][d][0], assign["L"][d][1]))))

# Now evaluate each option.
# Each option gives the list of students who work the SECOND shift, Monday through Friday.
# So for day d (0..4), the second shift worker must be the given student.

options = {
    "A": ["H", "L", "L", "H", "K"],
    "B": ["J", "H", "G", "L", "L"],
    "C": ["J", "K", "H", "L", "K"],
    "D": ["L", "K", "J", "L", "K"],
    "E": ["L", "L", "H", "J", "J"]
}

found_options = []
for letter, opt_list in options.items():
    solver.push()
    for d in range(5):
        # The student opt_list[d] works the second shift on day d
        solver.add(assign[opt_list[d]][d][1] == True)
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