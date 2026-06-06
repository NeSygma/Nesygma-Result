from z3 import *

# Mapping names to integers
GRE = 0
HAK = 1
JOE = 2
KAT = 3
LOU = 4

# Days indices 0..4 for Mon..Fri
first = [Int(f'first_{d}') for d in range(5)]

solver = Solver()

# Domain constraints for first shifts
for d in range(5):
    solver.add(And(first[d] >= 0, first[d] <= 4))

# Base constraints (common to all options)
# 1. No student works both shifts of any day (first != second) will be added per option because second varies.
# 2. Each student works exactly two shifts total.
for s in range(5):
    total = Sum([If(first[d] == s, 1, 0) for d in range(5)])
    # second occurrences will be added per option
    # We'll store these partial sums and later add second contributions per option.
    # Use a placeholder list to accumulate later.
    pass

# We'll construct option-specific constraints as a single Bool expression.

def option_constraints(second_list):
    cons = []
    # second_list is list of ints length 5
    # 1. No student works both shifts of any day
    for d in range(5):
        cons.append(first[d] != second_list[d])
    # 2. Each student works exactly two shifts total (first + second)
    for s in range(5):
        cnt = Sum([If(first[d] == s, 1, 0) for d in range(5)]) + Sum([If(second_list[d] == s, 1, 0) for d in range(5)])
        cons.append(cnt == 2)
    # 3. Grecia works first shift on two nonconsecutive days, never second
    # Ensure second list has no Grecia
    for d in range(5):
        cons.append(second_list[d] != GRE)
    # Exactly two first shifts for Grecia
    gre_first_days = [If(first[d] == GRE, 1, 0) for d in range(5)]
    cons.append(Sum(gre_first_days) == 2)
    # Nonconsecutive: no adjacent days both Grecia first
    for d in range(4):
        cons.append(Not(And(first[d] == GRE, first[d+1] == GRE)) )
    # 4. Louise works second shift on two consecutive days, exactly two shifts total, never first
    # Ensure first never Louise
    for d in range(5):
        cons.append(first[d] != LOU)
    # Count Louise in second list
    lou_second = [If(second_list[d] == LOU, 1, 0) for d in range(5)]
    cons.append(Sum(lou_second) == 2)
    # Consecutive days condition: there exists d such that second[d]==Lou and second[d+1]==Lou
    consecutive = Or([And(second_list[d] == LOU, second_list[d+1] == LOU) for d in range(4)])
    cons.append(consecutive)
    # Also ensure not more than two consecutive? Since total is 2, consecutive automatically means they are the two.
    # 5. Katya works on Tuesday (day1) and Friday (day4) exactly those two days.
    # Ensure Katya appears on those days (either shift)
    for d in [1,4]:
        cons.append(Or(first[d] == KAT, second_list[d] == KAT))
    # Ensure Katya does not appear on other days
    for d in [0,2,3]:
        cons.append(And(first[d] != KAT, second_list[d] != KAT))
    # Also total shifts for Katya will be enforced by overall count (2).
    # 6. Hakeem and Joe share a day (at least once)
    share = []
    for d in range(5):
        share.append(Or(And(first[d] == HAK, second_list[d] == JOE), And(first[d] == JOE, second_list[d] == HAK)))
    cons.append(Or(share))
    # 7. Grecia and Louise never work on same day
    for d in range(5):
        # Since Louise only appears in second, just ensure if second is Louise then first not Grecia
        cons.append(Implies(second_list[d] == LOU, first[d] != GRE))
    return And(cons)

# Define options
options = {
    "A": [HAK, LOU, LOU, HAK, KAT],
    "B": [JOE, HAK, GRE, LOU, LOU],
    "C": [JOE, KAT, HAK, LOU, KAT],
    "D": [LOU, KAT, JOE, LOU, KAT],
    "E": [LOU, LOU, HAK, JOE, JOE]
}

found_options = []
for letter, sec in options.items():
    solver.push()
    solver.add(option_constraints(sec))
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