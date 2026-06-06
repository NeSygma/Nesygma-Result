from z3 import *

# Base variables for each color: forest, olive, peach, turquoise, white, yellow
colors = ['forest', 'olive', 'peach', 'turquoise', 'white', 'yellow']
vars = {c: Int(c) for c in colors}
solver = Solver()

# Domain: -1 (unused) or 0,1,2 (rug indices)
for v in vars.values():
    solver.add(Or(v == -1, And(v >= 0, v <= 2)))

# Exactly one color unused
unused = [If(v == -1, 1, 0) for v in vars.values()]
solver.add(Sum(unused) == 1)

# Each rug must have at least one color assigned
# Count colors per rug
for r in range(3):
    cnt = Sum([If(v == r, 1, 0) for v in vars.values()])
    solver.add(cnt >= 1)

# White rule: if white used in rug r, that rug must have exactly 3 colors
w = vars['white']
# For each rug, if white assigned to that rug, then count == 3
for r in range(3):
    cnt = Sum([If(v == r, 1, 0) for v in vars.values()])
    solver.add(Implies(w == r, cnt == 3))

# Olive implies peach in same rug
solver.add(Implies(vars['olive'] != -1, vars['olive'] == vars['peach']))

# Forbidden pairs not in same rug (if both used)
for (c1, c2) in [('forest','turquoise'), ('peach','turquoise'), ('peach','yellow')]:
    solver.add(Or(vars[c1] == -1, vars[c2] == -1, vars[c1] != vars[c2]))

# Helper to create option constraints

def option_A():
    # forest only, turquoise only, olive+peach+white together, yellow unused
    f = vars['forest']; t = vars['turquoise']; o = vars['olive']; p = vars['peach']; w = vars['white']; y = vars['yellow']
    # unused yellow
    opt = []
    opt.append(y == -1)
    # forest alone
    opt.append(f != -1)
    opt.append(And([Or(c == -1, c != f) for c in [t,o,p,w]]) )
    # turquoise alone
    opt.append(t != -1)
    opt.append(And([Or(c == -1, c != t) for c in [f,o,p,w]]) )
    # olive, peach, white together
    opt.append(o != -1)
    opt.append(p == o)
    opt.append(w == o)
    # ensure no other color shares that rug (yellow already -1)
    opt.append(And([Or(c == -1, c != o) for c in [f,t]]) )
    return And(opt)

def option_B():
    # forest only; turquoise only; olive, peach, yellow together; white unused
    f = vars['forest']; t = vars['turquoise']; o = vars['olive']; p = vars['peach']; w = vars['white']; y = vars['yellow']
    opt = []
    opt.append(w == -1)
    opt.append(y != -1)
    # forest alone
    opt.append(f != -1)
    opt.append(And([Or(c == -1, c != f) for c in [t,o,p,y]]) )
    # turquoise alone
    opt.append(t != -1)
    opt.append(And([Or(c == -1, c != t) for c in [f,o,p,y]]) )
    # olive, peach, yellow together
    opt.append(o != -1)
    opt.append(p == o)
    opt.append(y == o)
    # ensure no other color shares that rug (white unused)
    opt.append(And([Or(c == -1, c != o) for c in [f,t]]) )
    return And(opt)

def option_C():
    # peach only; turquoise only; forest, olive, white together; yellow unused
    f = vars['forest']; o = vars['olive']; p = vars['peach']; t = vars['turquoise']; w = vars['white']; y = vars['yellow']
    opt = []
    opt.append(y == -1)
    # peach alone
    opt.append(p != -1)
    opt.append(And([Or(c == -1, c != p) for c in [f,o,t,w]]) )
    # turquoise alone
    opt.append(t != -1)
    opt.append(And([Or(c == -1, c != t) for c in [f,o,p,w]]) )
    # forest, olive, white together
    opt.append(f != -1)
    opt.append(o == f)
    opt.append(w == f)
    # olive implies peach (already enforced globally) -> will cause conflict because peach not same rug
    # ensure no other color shares that rug (peach, turquoise are separate)
    opt.append(And([Or(c == -1, c != f) for c in [p,t]]) )
    return And(opt)

def option_D():
    # yellow only; forest and turquoise together; olive and peach together; white unused
    f = vars['forest']; t = vars['turquoise']; o = vars['olive']; p = vars['peach']; w = vars['white']; y = vars['yellow']
    opt = []
    opt.append(w == -1)
    # yellow alone
    opt.append(y != -1)
    opt.append(And([Or(c == -1, c != y) for c in [f,t,o,p]]) )
    # forest and turquoise together
    opt.append(f != -1)
    opt.append(t == f)
    # ensure no other color shares that rug
    opt.append(And([Or(c == -1, c != f) for c in [o,p,y]]) )
    # olive and peach together
    opt.append(o != -1)
    opt.append(p == o)
    # ensure no other color shares that rug
    opt.append(And([Or(c == -1, c != o) for c in [f,y]]) )
    return And(opt)

def option_E():
    # yellow only; olive and peach together; turquoise and white together; forest unused
    f = vars['forest']; o = vars['olive']; p = vars['peach']; t = vars['turquoise']; w = vars['white']; y = vars['yellow']
    opt = []
    opt.append(f == -1)
    # yellow alone
    opt.append(y != -1)
    opt.append(And([Or(c == -1, c != y) for c in [o,p,t,w]]) )
    # olive and peach together
    opt.append(o != -1)
    opt.append(p == o)
    # ensure no other color shares that rug
    opt.append(And([Or(c == -1, c != o) for c in [t,w,y]]) )
    # turquoise and white together
    opt.append(t != -1)
    opt.append(w == t)
    # white rule requires exactly 3 colors in that rug, but only two present -> will cause unsat
    # ensure no other color shares that rug
    opt.append(And([Or(c == -1, c != t) for c in [o,y]]) )
    return And(opt)

# Map options to constructors
option_constr = {
    "A": option_A(),
    "B": option_B(),
    "C": option_C(),
    "D": option_D(),
    "E": option_E()
}

found_options = []
for letter, constr in [("A", option_constr["A"]), ("B", option_constr["B"]), ("C", option_constr["C"]), ("D", option_constr["D"]), ("E", option_constr["E"])]:
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