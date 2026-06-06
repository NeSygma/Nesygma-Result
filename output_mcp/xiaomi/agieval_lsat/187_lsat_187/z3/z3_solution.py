from z3 import *

solver = Solver()

# Workers: Quinn, Ruiz, Smith, Taylor, Verma, Wells, Xue
# Boolean variables: is_selected (project member), is_leader (project leader)
Q_sel = Bool('Q_sel')
R_sel = Bool('R_sel')
S_sel = Bool('S_sel')
T_sel = Bool('T_sel')
V_sel = Bool('V_sel')
W_sel = Bool('W_sel')
X_sel = Bool('X_sel')

Q_lead = Bool('Q_lead')
R_lead = Bool('R_lead')
S_lead = Bool('S_lead')
T_lead = Bool('T_lead')
V_lead = Bool('V_lead')
W_lead = Bool('W_lead')
X_lead = Bool('X_lead')

selected = [Q_sel, R_sel, S_sel, T_sel, V_sel, W_sel, X_sel]
leaders = [Q_lead, R_lead, S_lead, T_lead, V_lead, W_lead, X_lead]

# Exactly 3 workers selected
solver.add(Sum([If(s, 1, 0) for s in selected]) == 3)

# Exactly 1 leader
solver.add(Sum([If(l, 1, 0) for l in leaders]) == 1)

# Leader must be selected
for s, l in zip(selected, leaders):
    solver.add(Implies(l, s))

# Constraint 1: Quinn or Ruiz can be a project member only if leading the project
solver.add(Implies(Q_sel, Q_lead))
solver.add(Implies(R_sel, R_lead))

# Constraint 2: If Smith is a project member, Taylor must also be
solver.add(Implies(S_sel, T_sel))

# Constraint 3: If Wells is a project member, neither Ruiz nor Verma can be
solver.add(Implies(W_sel, And(Not(R_sel), Not(V_sel))))

# The question: Verma could be the project leader if which one of the following is true?
# We need to find which additional constraint makes it possible for V_lead to be true.

# Define option constraints
opt_a = And(Not(Q_sel), Not(S_sel))  # Neither Quinn nor Smith is selected
opt_b = And(Not(R_sel), Not(T_sel))  # Neither Ruiz nor Taylor is selected
opt_c = And(Not(S_sel), Not(T_sel))  # Neither Smith nor Taylor is selected
opt_d = And(Not(S_sel), Not(X_sel))  # Neither Smith nor Xue is selected
opt_e = And(Not(T_sel), Not(W_sel))  # Neither Taylor nor Wells is selected

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    solver.add(V_lead == True)  # Verma is the project leader
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