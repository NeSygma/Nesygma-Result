from z3 import *

# Variables: positions for each singer
pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z = Ints('pos_K pos_L pos_T pos_W pos_Y pos_Z')
singer_positions = [pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z]
singer_names = ['K', 'L', 'T', 'W', 'Y', 'Z']

def base_constraints(solver):
    """Add domain and distinctness constraints."""
    for p in singer_positions:
        solver.add(p >= 1, p <= 6)
    solver.add(Distinct(singer_positions))

def add_other_constraints(solver):
    """Add constraints that are common to both original and replacement scenarios."""
    # Constraint 2: The fourth audition cannot be recorded (recorded = K or L)
    # So pos != 4 for K and L? No: the fourth position cannot be occupied by K or L.
    solver.add(pos_K != 4)
    solver.add(pos_L != 4)
    
    # Constraint 3: The fifth audition must be recorded (K or L)
    solver.add(Or(pos_K == 5, pos_L == 5))
    
    # Constraint 5: Kammer before Trillo
    solver.add(pos_K < pos_T)
    
    # Constraint 6: Zinn before Yoshida
    solver.add(pos_Z < pos_Y)

def add_original_cond4(solver):
    """Original condition 4: Waite's audition earlier than the two recorded auditions (K and L)."""
    solver.add(pos_W < pos_K)
    solver.add(pos_W < pos_L)

# Replacement conditions for each option
def opt_a(solver):
    """(A) Zinn's audition is the only one that can take place earlier than Waite's.
    Meaning: All auditions except Zinn must be after Waite? Actually "the only one that can take place earlier than Waite's" 
    means if an audition is before Waite, it must be Zinn. So: there is at most one audition before Waite, and that audition is Zinn.
    Or equivalently: for any singer X != Z, pos_X > pos_W.
    And Zinn is before Waite? "Zinn's audition is the only one that can take place earlier than Waite's."
    This means Zinn CAN be before Waite, and no other can be before Waite. So pos_Z < pos_W? Or pos_Z can be before or after?
    "Zinn's audition is the only one that can take place earlier than Waite's" means that if someone is before Waite, that someone must be Zinn.
    It doesn't necessarily require Zinn to be before Waite; just that no other singer can be before Waite.
    So: For all X != Z, pos_X > pos_W. (And pos_Z can be anything relative to W)
    """
    solver.add(And([p > pos_W for name, p in zip(singer_names, singer_positions) if name != 'W' and name != 'Z']))

def opt_b(solver):
    """(B) Waite's audition must take place either immediately before or immediately after Zinn's.
    I.e., |pos_W - pos_Z| == 1
    """
    solver.add(Or(pos_W + 1 == pos_Z, pos_W - 1 == pos_Z))

def opt_c(solver):
    """(C) Waite's audition must take place earlier than Lugo's."""
    solver.add(pos_W < pos_L)

def opt_d(solver):
    """(D) Waite's audition must be either first or second."""
    solver.add(Or(pos_W == 1, pos_W == 2))

def opt_e(solver):
    """(E) The first audition cannot be recorded.
    So first position is not K and not L."""
    solver.add(pos_K != 1)
    solver.add(pos_L != 1)


def check_equivalence(option_constraint_func, option_label):
    """Check if original condition 4 and replacement condition are equivalent.
    Returns True if equivalent, False otherwise."""
    
    # Check O => R: original ∧ ¬replacement should be unsat
    s1 = Solver()
    base_constraints(s1)
    add_other_constraints(s1)
    add_original_cond4(s1)
    # Add negation of replacement
    # We need to add the replacement constraint, but negated.
    # We'll create a fresh solver for checking the negation of replacement under original.
    # Actually easier: check if (original AND NOT replacement) is unsat.
    # To get NOT replacement, we can use the solver with constraints and check if adding NOT replacement leads to unsat.
    # We'll push/pop.
    opt_s1 = Solver()
    base_constraints(opt_s1)
    add_other_constraints(opt_s1)
    add_original_cond4(opt_s1)
    opt_s1.push()
    # Add the negation of the option's constraint
    # We can't easily negate the option function, so we'll create a separate context.
    opt_s1.pop()
    
    # Better approach: Use a different method.
    # Let's create two solvers and check the implications.
    
    return None  # Placeholder


# Let's try a different approach: enumerate all solutions for original and each option.

def enumerate_solutions(solver_setup_func):
    """Enumerate all solutions for a given constraint setup. Returns a set of tuples (pos_K, pos_L, pos_T, pos_W, pos_Y, pos_Z)."""
    solver = Solver()
    base_constraints(solver)
    add_other_constraints(solver)
    solver_setup_func(solver)
    
    solutions = set()
    while solver.check() == sat:
        m = solver.model()
        sol = (m.eval(pos_K).as_long(), m.eval(pos_L).as_long(), m.eval(pos_T).as_long(),
               m.eval(pos_W).as_long(), m.eval(pos_Y).as_long(), m.eval(pos_Z).as_long())
        solutions.add(sol)
        # Block this solution
        solver.add(Or([p != m.eval(p).as_long() for p in singer_positions]))
    return solutions

print("Enumerating solutions for original constraints...")
original_solutions = enumerate_solutions(add_original_cond4)
print(f"Original: {len(original_solutions)} solutions")

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e)
]

equivalent_options = []
for label, opt_func in options:
    print(f"Enumerating solutions for option {label}...")
    sols = enumerate_solutions(opt_func)
    print(f"Option {label}: {len(sols)} solutions")
    if sols == original_solutions:
        equivalent_options.append(label)

print(f"Equivalent options: {equivalent_options}")

if len(equivalent_options) == 1:
    print("STATUS: sat")
    print(f"answer:{equivalent_options[0]}")
elif len(equivalent_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {equivalent_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")