from z3 import *

solver = Solver()

# Declare position variables for each person
p_Peters = Int('p_Peters')
p_Quinn = Int('p_Quinn')
p_Rovero = Int('p_Rovero')
p_Stanton = Int('p_Stanton')
p_Tao = Int('p_Tao')
p_Villas = Int('p_Villas')
p_White = Int('p_White')

# Base constraints
# All positions between 1 and 7
solver.add(1 <= p_Peters, p_Peters <= 7)
solver.add(1 <= p_Quinn, p_Quinn <= 7)
solver.add(1 <= p_Rovero, p_Rovero <= 7)
solver.add(1 <= p_Stanton, p_Stanton <= 7)
solver.add(1 <= p_Tao, p_Tao <= 7)
solver.add(1 <= p_Villas, p_Villas <= 7)
solver.add(1 <= p_White, p_White <= 7)

# All distinct
solver.add(Distinct([p_Peters, p_Quinn, p_Rovero, p_Stanton, p_Tao, p_Villas, p_White]))

# Peters was recruited fourth
solver.add(p_Peters == 4)

# Quinn earlier than Rovero
solver.add(p_Quinn < p_Rovero)

# Villas immediately before White
solver.add(p_Villas + 1 == p_White)

# Stanton not adjacent to Tao
solver.add(Not(p_Stanton + 1 == p_Tao))
solver.add(Not(p_Tao + 1 == p_Stanton))

# Now test each option
found_options = []

# Option A: Quinn, Stanton, Peters, Tao, Villas
opt_a = And(p_Quinn == 2, p_Stanton == 3, p_Peters == 4, p_Tao == 5, p_Villas == 6)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: Quinn, Stanton, Peters, Tao, White
opt_b = And(p_Quinn == 2, p_Stanton == 3, p_Peters == 4, p_Tao == 5, p_White == 6)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: Villas, White, Peters, Quinn, Stanton
opt_c = And(p_Villas == 2, p_White == 3, p_Peters == 4, p_Quinn == 5, p_Stanton == 6)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: Villas, White, Peters, Rovero, Stanton
opt_d = And(p_Villas == 2, p_White == 3, p_Peters == 4, p_Rovero == 5, p_Stanton == 6)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Villas, White, Quinn, Rovero, Stanton
opt_e = And(p_Villas == 2, p_White == 3, p_Quinn == 4, p_Rovero == 5, p_Stanton == 6)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")