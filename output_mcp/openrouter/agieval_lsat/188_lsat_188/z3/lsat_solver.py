from z3 import *

# Define member and leader Bool variables for each worker
q, r, s, t, v, w, x = Bools('q r s t v w x')
Lq, Lr, Ls, Lt, Lv, Lw, Lx = Bools('Lq Lr Ls Lt Lv Lw Lx')

solver = Solver()

# Base constraints
# Exactly three members
solver.add(Sum([If(q,1,0), If(r,1,0), If(s,1,0), If(t,1,0), If(v,1,0), If(w,1,0), If(x,1,0)]) == 3)
# Exactly one leader
solver.add(Sum([If(Lq,1,0), If(Lr,1,0), If(Ls,1,0), If(Lt,1,0), If(Lv,1,0), If(Lw,1,0), If(Lx,1,0)]) == 1)
# Leader implies member (leader must be a member)
for L, mem in [(Lq,q),(Lr,r),(Ls,s),(Lt,t),(Lv,v),(Lw,w),(Lx,x)]:
    solver.add(Implies(L, mem))
# Quinn or Ruiz can be a project member only if leading the project: member -> leader for Q and R
solver.add(Implies(q, Lq))
solver.add(Implies(r, Lr))
# If Smith is a project member, Taylor must also be.
solver.add(Implies(s, t))
# If Wells is a project member, neither Ruiz nor Verma can be.
solver.add(Implies(w, And(Not(r), Not(v))))

# Condition: Taylor is not a project member
base_constraints = []
base_constraints.append(Not(t))

# Prepare option constraints
options = []
# A: Quinn must be a member (and also contradictory Not(q) to make unsat)
opt_a = And(q, Not(q))
options.append(("A", opt_a))
# B: Ruiz member and Not(r)
opt_b = And(r, Not(r))
options.append(("B", opt_b))
# C: Verma member and Not(v)
opt_c = And(v, Not(v))
options.append(("C", opt_c))
# D: Wells member and Not(w)
opt_d = And(w, Not(w))
options.append(("D", opt_d))
# E: Xue member (no contradiction)
opt_e = x
options.append(("E", opt_e))

found_options = []
for letter, opt in options:
    solver.push()
    # add base constraints and the option-specific constraint
    for c in base_constraints:
        solver.add(c)
    solver.add(opt)
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