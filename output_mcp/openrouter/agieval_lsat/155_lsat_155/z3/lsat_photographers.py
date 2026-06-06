from z3 import *

solver = Solver()

# Photographers list
photogs = ['Frost', 'Gonzalez', 'Heideck', 'Knutson', 'Lai', 'Mays']
# Create Bool vars for each photographer assignment to Silva (S) and Thorne (T)
assign = {}
for p in photogs:
    assign[p] = (Bool(f"{p}_S"), Bool(f"{p}_T"))
    pS, pT = assign[p]
    # cannot be assigned to both
    solver.add(Not(And(pS, pT)))
    # optional: no other constraints on being unassigned

# At least two photographers per ceremony
solver.add(Sum([If(assign[p][0], 1, 0) for p in photogs]) >= 2)
solver.add(Sum([If(assign[p][1], 1, 0) for p in photogs]) >= 2)

# Constraint 1: Frost and Heideck together at one ceremony, both assigned
F_S, F_T = assign['Frost']
H_S, H_T = assign['Heideck']
# Both must be assigned (at least one true each) and same ceremony
solver.add(Or(F_S, F_T))
solver.add(Or(H_S, H_T))
# same ceremony: (F_S and H_S) or (F_T and H_T)
solver.add(Or(And(F_S, H_S), And(F_T, H_T)))

# Constraint 2: If Lai and Mays both assigned, they must be to different ceremonies
L_S, L_T = assign['Lai']
M_S, M_T = assign['Mays']
# If both assigned somewhere (i.e., Or(L_S, L_T) and Or(M_S, M_T)) then not same ceremony
both_assigned = And(Or(L_S, L_T), Or(M_S, M_T))
# same ceremony condition
same_ceremony = Or(And(L_S, M_S), And(L_T, M_T))
solver.add(Implies(both_assigned, Not(same_ceremony)))

# Constraint 3: If Gonzalez assigned to Silva then Lai assigned to Thorne
G_S, G_T = assign['Gonzalez']
solver.add(Implies(G_S, L_T))

# Constraint 4: If Knutson not assigned to Thorne then both Heideck and Mays assigned to Thorne
K_S, K_T = assign['Knutson']
solver.add(Implies(Not(K_T), And(H_T, M_T)))

# Now define option constraints

def option_constraint(option):
    # option is dict with keys 'Silva' and 'Thorne' listing photographer names
    cons = []
    # Set assignments per option
    for p in photogs:
        pS, pT = assign[p]
        if p in option.get('Silva', []):
            cons.append(pS == True)
            cons.append(pT == False)
        elif p in option.get('Thorne', []):
            cons.append(pT == True)
            cons.append(pS == False)
        else:
            # unassigned
            cons.append(pS == False)
            cons.append(pT == False)
    return And(cons)

# Define each option
opt_A = option_constraint({'Silva': ['Gonzalez', 'Lai'], 'Thorne': ['Frost', 'Heideck', 'Mays']})
opt_B = option_constraint({'Silva': ['Gonzalez', 'Mays'], 'Thorne': ['Knutson', 'Lai']})
opt_C = option_constraint({'Silva': ['Frost', 'Gonzalez', 'Heideck'], 'Thorne': ['Knutson', 'Lai', 'Mays']})
opt_D = option_constraint({'Silva': ['Frost', 'Heideck', 'Mays'], 'Thorne': ['Gonzalez', 'Lai']})
opt_E = option_constraint({'Silva': ['Frost', 'Heideck', 'Mays'], 'Thorne': ['Gonzalez', 'Knutson', 'Lai']})

found_options = []
for letter, constr in [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]:
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