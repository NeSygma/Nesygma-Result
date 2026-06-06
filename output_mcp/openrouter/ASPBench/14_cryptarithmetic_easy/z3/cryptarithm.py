from z3 import *

# Declare variables for each letter
letters = ['S','E','N','D','M','O','R','Y']
vars = {l: Int(l) for l in letters}

solver = Solver()

# Domain constraints: each digit 0-9
for v in vars.values():
    solver.add(v >= 0, v <= 9)

# All different
solver.add(Distinct(list(vars.values())))

# Leading letters not zero
solver.add(vars['S'] != 0)
solver.add(vars['M'] != 0)

# Equation: SEND + MORE = MONEY
SEND = 1000*vars['S'] + 100*vars['E'] + 10*vars['N'] + vars['D']
MORE = 1000*vars['M'] + 100*vars['O'] + 10*vars['R'] + vars['E']
MONEY = 10000*vars['M'] + 1000*vars['O'] + 100*vars['N'] + 10*vars['E'] + vars['Y']
solver.add(SEND + MORE == MONEY)

result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print assignment
    for l in letters:
        print(f"{l} = {m[vars[l]]}")
    # Build numeric strings
    send_val = sum([m[vars[ch]].as_long()*10**i for ch,i in zip(['D','N','E','S'], [0,1,2,3])])
    more_val = sum([m[vars[ch]].as_long()*10**i for ch,i in zip(['E','R','O','M'], [0,1,2,3])])
    money_val = sum([m[vars[ch]].as_long()*10**i for ch,i in zip(['Y','E','N','O','M'], [0,1,2,3,4])])
    print(f"equation = {send_val} + {more_val} = {money_val}")
else:
    print("STATUS: unsat")