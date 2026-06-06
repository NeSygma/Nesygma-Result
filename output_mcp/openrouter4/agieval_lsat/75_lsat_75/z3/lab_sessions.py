from z3 import *

# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Times: 0=morning, 1=afternoon

# Variables for each assistant
assistants = ['Julio', 'Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']
day = {a: Int(f'day_{a}') for a in assistants}
time = {a: Int(f'time_{a}') for a in assistants}

solver = Solver()

# Domain constraints
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(time[a] >= 0, time[a] <= 1)

# All (day, time) pairs are distinct (each assistant gets a unique session slot)
for i, a1 in enumerate(assistants):
    for a2 in assistants[i+1:]:
        solver.add(Not(And(day[a1] == day[a2], time[a1] == time[a2])))

# Constraint 1: Kevin and Rebecca on same day
solver.add(day['Kevin'] == day['Rebecca'])

# Constraint 2: Lan and Olivia not on same day
solver.add(day['Lan'] != day['Olivia'])

# Constraint 3: Nessa leads afternoon session
solver.add(time['Nessa'] == 1)

# Constraint 4: Julio's day earlier than Olivia's
solver.add(day['Julio'] < day['Olivia'])

# Given: Julio leads Thursday afternoon
solver.add(day['Julio'] == 1)
solver.add(time['Julio'] == 1)

# First, let's check if the constraints are satisfiable
result = solver.check()
print(f"Overall satisfiability: {result}")

if result == sat:
    m = solver.model()
    print("One solution found:")
    for a in assistants:
        print(f"  {a}: day={m[day[a]]}, time={m[time[a]]}")
    
    # Now determine for each of the other 5 assistants if their session is uniquely determined
    other_assistants = ['Kevin', 'Lan', 'Nessa', 'Olivia', 'Rebecca']
    determined = []
    not_determined = []
    
    for a in other_assistants:
        # Get the value in one solution
        s_check = Solver()
        s_check.add(solver.assertions)
        if s_check.check() == sat:
            m = s_check.model()
            d_val = m[day[a]].as_long()
            t_val = m[time[a]].as_long()
            
            # Check if there's an alternative solution with a different (day, time)
            s_check.push()
            s_check.add(Or(day[a] != d_val, time[a] != t_val))
            alt_result = s_check.check()
            s_check.pop()
            
            if alt_result == unsat:
                determined.append((a, d_val, t_val))
            else:
                not_determined.append(a)
    
    print(f"\nDetermined assistants: {determined}")
    print(f"Not determined: {not_determined}")
    determined_count = len(determined)
    print(f"Count: {determined_count}")
    
    # Now use the multiple choice skeleton
    opt_a_constr = (determined_count == 1)
    opt_b_constr = (determined_count == 2)
    opt_c_constr = (determined_count == 3)
    opt_d_constr = (determined_count == 4)
    opt_e_constr = (determined_count == 5)
    
    found_options = []
    for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
        s_opt = Solver()
        s_opt.add(constr)
        if s_opt.check() == sat:
            found_options.append(letter)
    
    if len(found_options) == 1:
        print("STATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")
else:
    print("STATUS: unsat")
    print("Refine: No solution found for base constraints")