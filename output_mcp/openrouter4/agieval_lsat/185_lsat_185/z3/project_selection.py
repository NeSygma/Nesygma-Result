from z3 import *

# Variables: membership and leadership for each of the 7 workers
member = {name: Bool(f"member_{name}") for name in ["Q", "R", "S", "T", "V", "W", "X"]}
leader = {name: Bool(f"leader_{name}") for name in ["Q", "R", "S", "T", "V", "W", "X"]}

solver = Solver()

# Exactly 3 members
solver.add(Sum([If(member[name], 1, 0) for name in member]) == 3)

# Exactly 1 leader
solver.add(Sum([If(leader[name], 1, 0) for name in leader]) == 1)

# If someone is leader, they must be a member
for name in member:
    solver.add(Implies(leader[name], member[name]))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project
# member_Q => leader_Q
solver.add(Implies(member["Q"], leader["Q"]))
# member_R => leader_R
solver.add(Implies(member["R"], leader["R"]))

# Constraint 2: If Smith is a project member, Taylor must also be
# member_S => member_T
solver.add(Implies(member["S"], member["T"]))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be
# member_W => (Not member_R AND Not member_V)
solver.add(Implies(member["W"], And(Not(member["R"]), Not(member["V"]))))

# Now check each option
# Option A: Ruiz (leader), Taylor, Wells
opt_a_members = And(member["R"], member["T"], member["W"], 
                    Not(member["Q"]), Not(member["S"]), Not(member["V"]), Not(member["X"]))
opt_a_leader = And(leader["R"], Not(leader["Q"]), Not(leader["S"]), Not(leader["T"]), 
                   Not(leader["V"]), Not(leader["W"]), Not(leader["X"]))

# Option B: Verma (leader), Quinn, Taylor
opt_b_members = And(member["V"], member["Q"], member["T"],
                    Not(member["R"]), Not(member["S"]), Not(member["W"]), Not(member["X"]))
opt_b_leader = And(leader["V"], Not(leader["Q"]), Not(leader["R"]), Not(leader["S"]), 
                   Not(leader["T"]), Not(leader["W"]), Not(leader["X"]))

# Option C: Verma (leader), Smith, Taylor
opt_c_members = And(member["V"], member["S"], member["T"],
                    Not(member["Q"]), Not(member["R"]), Not(member["W"]), Not(member["X"]))
opt_c_leader = And(leader["V"], Not(leader["Q"]), Not(leader["R"]), Not(leader["S"]), 
                   Not(leader["T"]), Not(leader["W"]), Not(leader["X"]))

# Option D: Verma (leader), Smith, Xue
opt_d_members = And(member["V"], member["S"], member["X"],
                    Not(member["Q"]), Not(member["R"]), Not(member["T"]), Not(member["W"]))
opt_d_leader = And(leader["V"], Not(leader["Q"]), Not(leader["R"]), Not(leader["S"]), 
                   Not(leader["T"]), Not(leader["W"]), Not(leader["X"]))

# Option E: Xue (leader), Verma, Wells
opt_e_members = And(member["X"], member["V"], member["W"],
                    Not(member["Q"]), Not(member["R"]), Not(member["S"]), Not(member["T"]))
opt_e_leader = And(leader["X"], Not(leader["Q"]), Not(leader["R"]), Not(leader["S"]), 
                   Not(leader["T"]), Not(leader["V"]), Not(leader["W"]))

# Combine member and leader constraints for each option
opt_a_constr = And(opt_a_members, opt_a_leader)
opt_b_constr = And(opt_b_members, opt_b_leader)
opt_c_constr = And(opt_c_members, opt_c_leader)
opt_d_constr = And(opt_d_members, opt_d_leader)
opt_e_constr = And(opt_e_members, opt_e_leader)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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