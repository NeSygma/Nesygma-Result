from z3 import *

# Define member Bool variables for each worker
Q = Bool('Q')  # Quinn
R = Bool('R')  # Ruiz
S = Bool('S')  # Smith
T = Bool('T')  # Taylor
V = Bool('V')  # Verma
W = Bool('W')  # Wells
X = Bool('X')  # Xue

# Define leader Bool variables
QL = Bool('QL')
RL = Bool('RL')
SL = Bool('SL')
TL = Bool('TL')
VL = Bool('VL')
WL = Bool('WL')
XL = Bool('XL')

solver = Solver()

# Exactly three members
members = [Q, R, S, T, V, W, X]
solver.add(Sum([If(m, 1, 0) for m in members]) == 3)

# Exactly one leader
leaders = [QL, RL, SL, TL, VL, WL, XL]
solver.add(Sum([If(l, 1, 0) for l in leaders]) == 1)

# Leader implies member
for mem, lead in [(Q, QL), (R, RL), (S, SL), (T, TL), (V, VL), (W, WL), (X, XL)]:
    solver.add(Implies(lead, mem))

# Quinn or Ruiz can be a member only if leading the project: member => leader for Q and R
solver.add(Implies(Q, QL))
solver.add(Implies(R, RL))

# If Smith is a member, Taylor must also be
solver.add(Implies(S, T))

# If Wells is a member, neither Ruiz nor Verma can be
solver.add(Implies(W, Not(R)))
solver.add(Implies(W, Not(V)))

# Goal: Verma could be the project leader
goal_leader = VL == True

# Define option constraints
opt_a = And(Not(Q), Not(S))  # Neither Quinn nor Smith is selected.
opt_b = And(Not(R), Not(T))  # Neither Ruiz nor Taylor is selected.
opt_c = And(Not(S), Not(T))  # Neither Smith nor Taylor is selected.
opt_d = And(Not(S), Not(X))  # Neither Smith nor Xue is selected.
opt_e = And(Not(T), Not(W))  # Neither Taylor nor Wells is selected.

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, opt_constr in options:
    solver.push()
    # Add the option condition and the goal that Verma is leader
    solver.add(opt_constr)
    solver.add(goal_leader)
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