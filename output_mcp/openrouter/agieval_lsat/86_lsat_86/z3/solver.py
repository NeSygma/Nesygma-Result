from z3 import *

# Declare zone variables for each representative
zone_Kim = Int('zone_Kim')
zone_Mahr = Int('zone_Mahr')
zone_Parra = Int('zone_Parra')
zone_Quinn = Int('zone_Quinn')
zone_Stuckey = Int('zone_Stuckey')
zone_Tiao = Int('zone_Tiao')
zone_Udall = Int('zone_Udall')

vars = [zone_Kim, zone_Mahr, zone_Parra, zone_Quinn, zone_Stuckey, zone_Tiao, zone_Udall]

solver = Solver()

# Each zone is 1, 2, or 3
for v in vars:
    solver.add(Or(v == 1, v == 2, v == 3))

# Either Parra or Tiao (but not both) works in Zone 1
solver.add(Xor(zone_Parra == 1, zone_Tiao == 1))
# Either Tiao or Udall (but not both) works in Zone 2
solver.add(Xor(zone_Tiao == 2, zone_Udall == 2))
# Parra and Quinn same zone
solver.add(zone_Parra == zone_Quinn)
# Stuckey and Udall same zone
solver.add(zone_Stuckey == zone_Udall)
# More reps in Zone 3 than in Zone 2
count_zone3 = Sum([If(v == 3, 1, 0) for v in vars])
count_zone2 = Sum([If(v == 2, 1, 0) for v in vars])
solver.add(count_zone3 > count_zone2)

# Define constraints for each option: Quinn same zone as X
opt_a_constr = zone_Quinn == zone_Kim
opt_b_constr = zone_Quinn == zone_Mahr
opt_c_constr = zone_Quinn == zone_Stuckey
opt_d_constr = zone_Quinn == zone_Tiao
opt_e_constr = zone_Quinn == zone_Udall

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

all_opts = ["A","B","C","D","E"]
impossible = [o for o in all_opts if o not in found_options]
if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
else:
    # If something unexpected, report unsat for refinement
    print("STATUS: unsat")
    print(f"Refine: unexpected number of impossible options {impossible}")