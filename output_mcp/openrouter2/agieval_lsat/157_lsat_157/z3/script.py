from z3 import *

solver = Solver()

# Define variables
photographers = ["Frost","Gonzalez","Heideck","Knutson","Lai","Mays"]
vars = {}
for p in photographers:
    vars[p+"_Silva"] = Bool(p+"_Silva")
    vars[p+"_Thorne"] = Bool(p+"_Thorne")

# No double assignment
for p in photographers:
    solver.add(Not(And(vars[p+"_Silva"], vars[p+"_Thorne"])) )

# At least two per ceremony
solver.add(Sum([If(vars[p+"_Silva"],1,0) for p in photographers]) >= 2)
solver.add(Sum([If(vars[p+"_Thorne"],1,0) for p in photographers]) >= 2)

# Frost and Heideck together
solver.add(vars["Frost_Silva"] == vars["Heideck_Silva"])
solver.add(vars["Frost_Thorne"] == vars["Heideck_Thorne"])

# Lai and Mays not same ceremony
solver.add(Not(And(vars["Lai_Silva"], vars["Mays_Silva"])) )
solver.add(Not(And(vars["Lai_Thorne"], vars["Mays_Thorne"])) )

# Gonzalez to Silva implies Lai to Thorne
solver.add(Implies(vars["Gonzalez_Silva"], vars["Lai_Thorne"]))

# If Knutson not to Thorne, then Heideck and Mays to Thorne
solver.add(Implies(Not(vars["Knutson_Thorne"]), And(vars["Heideck_Thorne"], vars["Mays_Thorne"])) )

# Option constraints
opt_a_constr = []
for p in photographers:
    if p in ["Frost","Gonzalez","Heideck","Knutson"]:
        opt_a_constr.append(vars[p+"_Silva"] == True)
    else:
        opt_a_constr.append(vars[p+"_Silva"] == False)

opt_b_constr = []
for p in photographers:
    if p in ["Frost","Gonzalez","Heideck"]:
        opt_b_constr.append(vars[p+"_Silva"] == True)
    else:
        opt_b_constr.append(vars[p+"_Silva"] == False)

opt_c_constr = []
for p in photographers:
    if p in ["Gonzalez","Knutson"]:
        opt_c_constr.append(vars[p+"_Silva"] == True)
    else:
        opt_c_constr.append(vars[p+"_Silva"] == False)

opt_d_constr = []
for p in photographers:
    if p in ["Heideck","Lai"]:
        opt_d_constr.append(vars[p+"_Silva"] == True)
    else:
        opt_d_constr.append(vars[p+"_Silva"] == False)

opt_e_constr = []
for p in photographers:
    if p in ["Knutson","Mays"]:
        opt_e_constr.append(vars[p+"_Silva"] == True)
    else:
        opt_e_constr.append(vars[p+"_Silva"] == False)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(*constr)
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