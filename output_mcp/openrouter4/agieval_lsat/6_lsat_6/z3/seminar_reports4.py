from z3 import *

solver = Solver()

# Students: 0=George, 1=Helen, 2=Irving, 3=Kyle, 4=Lenore, 5=Nina, 6=Olivia, 7=Robert
n = 8
gives = [Bool(f'gives_{i}') for i in range(n)]
day = [Int(f'day_{i}') for i in range(n)]
time = [Int(f'time_{i}') for i in range(n)]

# Exactly 6 give reports
solver.add(Sum([If(gives[i], 1, 0) for i in range(n)]) == 6)

# Domain constraints for those who give
for i in range(n):
    solver.add(Implies(gives[i], And(day[i] >= 0, day[i] <= 2)))
    solver.add(Implies(gives[i], And(time[i] >= 0, time[i] <= 1)))

# Exactly 2 reports per day (one morning, one afternoon)
for d in range(3):
    solver.add(Sum([If(And(gives[i], day[i] == d), 1, 0) for i in range(n)]) == 2)
    solver.add(Sum([If(And(gives[i], day[i] == d, time[i] == 0), 1, 0) for i in range(n)]) == 1)
    solver.add(Sum([If(And(gives[i], day[i] == d, time[i] == 1), 1, 0) for i in range(n)]) == 1)

# Constraint 1: George can only give on Tuesday (day=1)
solver.add(Implies(gives[0], day[0] == 1))

# Constraint 2: Neither Olivia nor Robert can give an afternoon report
solver.add(Implies(gives[6], time[6] == 0))
solver.add(Implies(gives[7], time[7] == 0))

# Constraint 3: If Nina gives, then on the next day Helen and Irving must both give,
# unless Nina's report is given on Wednesday (day=2)
# i.e., if Nina gives on Monday (0) or Tuesday (1), then Helen and Irving give on the next day
for d in [0, 1]:
    solver.add(Implies(And(gives[5], day[5] == d),
                       And(gives[1], day[1] == d+1, gives[2], day[2] == d+1)))

# Given condition: Helen, Kyle, Lenore give the three morning reports
solver.add(gives[1])  # Helen gives
solver.add(gives[3])  # Kyle gives
solver.add(gives[4])  # Lenore gives

solver.add(time[1] == 0)  # Helen morning
solver.add(time[3] == 0)  # Kyle morning
solver.add(time[4] == 0)  # Lenore morning

# They are on different days
solver.add(Distinct([day[1], day[3], day[4]]))

# For "must be true" analysis: test each option by checking if its negation is satisfiable.
# If the negation leads to unsat, then the option is forced (must be true).

base_solver = solver  # The solver with base constraints

must_true_options = []

# Test each option's negation
for letter, neg_constr in [
    ("A", day[1] != 0),  # NOT (Helen gives on Monday)
    ("B", Not(And(gives[2], day[2] == 0))),  # NOT (Irving gives on Monday)
    ("C", Not(And(gives[2], day[2] == 2))),  # NOT (Irving gives on Wednesday)
    ("D", day[3] != 1),  # NOT (Kyle gives on Tuesday)
    ("E", day[3] != 2),  # NOT (Kyle gives on Wednesday)
]:
    test_solver = Solver()
    test_solver.add(base_solver.assertions())
    test_solver.add(neg_constr)
    result = test_solver.check()
    if result == unsat:
        # The negation is unsatisfiable, so the option must be true
        must_true_options.append(letter)
    elif result == sat:
        m = test_solver.model()
        print(f"Option {letter}: NEGATION is SAT - shows a model where option {letter} is FALSE")
        for i, name in enumerate(["George","Helen","Irving","Kyle","Lenore","Nina","Olivia","Robert"]):
            g = m.eval(gives[i])
            if g:
                d = m.eval(day[i])
                t = m.eval(time[i])
                day_str = "Mon" if d==0 else "Tue" if d==1 else "Wed"
                time_str = "morning" if t==0 else "afternoon"
                print(f"  {name}: {day_str} {time_str}")
    else:
        print(f"Option {letter}: unknown result")

print(f"\nOptions that must be true: {must_true_options}")

if len(must_true_options) == 1:
    print("STATUS: sat")
    print(f"answer:{must_true_options[0]}")
elif len(must_true_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_true_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")