from z3 import *

k, l, m_bool, n, o, p = Bools('k l m n o p')
vars_list = [k, l, m_bool, n, o, p]
var_names = ['K', 'L', 'M', 'N', 'O', 'P']

def get_base_solver():
    solver = Solver()
    solver.add(m_bool != p)
    solver.add(k == n)
    solver.add(Implies(k, o))
    solver.add(Implies(m_bool, Not(n)))
    return solver

def is_fully_determined(option_constraint):
    """
    Check if option_constraint together with base constraints
    forces all 6 variables to a unique assignment.
    We do this by checking, for each variable, whether both True and False
    are possible. If any variable can be both, schedule is not fully determined.
    """
    for i, var in enumerate(vars_list):
        # Can var be True?
        s_true = get_base_solver()
        s_true.add(option_constraint)
        s_true.add(var)
        can_be_true = s_true.check() == sat
        
        # Can var be False?
        s_false = get_base_solver()
        s_false.add(option_constraint)
        s_false.add(Not(var))
        can_be_false = s_false.check() == sat
        
        if can_be_true and can_be_false:
            return False, f"{var_names[i]} can be both True and False"
    
    # Also need to ensure the option is actually satisfiable
    s = get_base_solver()
    s.add(option_constraint)
    if s.check() != sat:
        return False, "Option is unsatisfiable"
    
    return True, "Schedule fully determined"

# Options
# Note: True = fall, False = spring
options = [
    ("A", And(k, Not(l))),                          # K fall, L spring
    ("B", And(o, Not(p))),                          # O fall, P spring
    ("C", And(p, Not(l))),                          # P fall, L spring
    ("D", And(Not(k), Not(l))),                     # K and L spring
    ("E", And(m_bool, l))                           # M and L fall
]

found_options = []
for letter, constr in options:
    determined, reason = is_fully_determined(constr)
    print(f"Option {letter}: {reason}")
    if determined:
        found_options.append(letter)
        # Print the unique model
        s = get_base_solver()
        s.add(constr)
        s.check()
        sol_model = s.model()
        for i, var in enumerate(vars_list):
            print(f"  {var_names[i]} = {sol_model.eval(var)}")

print(f"\nFound options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")