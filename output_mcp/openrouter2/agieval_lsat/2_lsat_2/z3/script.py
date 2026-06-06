from z3 import *

# Define enum sort for students
Student, (G,H,I,N,O,R) = EnumSort('Student', ['G','H','I','N','O','R'])

# Define variables for each slot
MonMorning = Const('MonMorning', Student)
MonAfternoon = Const('MonAfternoon', Student)
TueMorning = Const('TueMorning', Student)
TueAfternoon = Const('TueAfternoon', Student)
WedMorning = Const('WedMorning', Student)
WedAfternoon = Const('WedAfternoon', Student)

solver = Solver()

# Distinctness
solver.add(Distinct([MonMorning, MonAfternoon, TueMorning, TueAfternoon, WedMorning, WedAfternoon]))

# G only Tuesday
solver.add(MonMorning != G, MonAfternoon != G, WedMorning != G, WedAfternoon != G)
solver.add(Or(TueMorning == G, TueAfternoon == G))

# O and R only morning
solver.add(MonAfternoon != O, MonAfternoon != R,
          TueAfternoon != O, TueAfternoon != R,
          WedAfternoon != O, WedAfternoon != R)

# Nina condition
n_on_mon = Or(MonMorning == N, MonAfternoon == N)
n_on_tue = Or(TueMorning == N, TueAfternoon == N)
solver.add(Implies(n_on_mon, And(Or(TueMorning == H, TueAfternoon == H),
                                 Or(TueMorning == I, TueAfternoon == I))))
solver.add(Implies(n_on_tue, And(Or(WedMorning == H, WedAfternoon == H),
                                 Or(WedMorning == I, WedAfternoon == I))))

# Options
opt_a_constr = And(MonMorning == H, TueMorning == G, WedMorning == N)
opt_b_constr = And(MonMorning == I, TueMorning == R, WedMorning == H)
opt_c_constr = And(MonMorning == N, TueMorning == H, WedMorning == O)
opt_d_constr = And(MonMorning == O, TueMorning == R, WedMorning == I)
opt_e_constr = And(MonMorning == R, TueMorning == G, WedMorning == H)

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