from z3 import *

def get_all_models(constraints, variables):
    """Return a list of models (as tuples of variable values) satisfying constraints."""
    s = Solver()
    s.add(constraints)
    models = []
    while s.check() == sat:
        m = s.model()
        # Evaluate each variable to get its value
        values = tuple(m.eval(v, model_completion=True) for v in variables)
        models.append(values)
        # Blocking clause: at least one variable must differ from this model
        block = Or([v != m.eval(v, model_completion=True) for v in variables])
        s.add(block)
    return models

def main():
    # Define variables for each clue (chapter number 1..7)
    R, S, T, U, W, X, Z = Ints('R S T U W X Z')
    variables = [R, S, T, U, W, X, Z]
    
    # Base constraints (excluding T != 1 and options)
    base_constraints = [
        # All chapters distinct
        Distinct(R, S, T, U, W, X, Z),
        # Each chapter between 1 and 7
        And([And(v >= 1, v <= 7) for v in variables]),
        # T before W with exactly two chapters between
        W == T + 3,
        T < W,
        # S and Z not adjacent
        Abs(S - Z) != 1,
        # W and X not adjacent
        Abs(W - X) != 1,
        # U and X adjacent
        Abs(U - X) == 1,
    ]
    
    # Original constraint: T != 1
    original_constraint = T != 1
    
    # Get all models for original problem
    original_models = get_all_models(base_constraints + [original_constraint], variables)
    print(f"Original problem has {len(original_models)} solutions.")
    
    # Define options as (letter, constraint)
    options = [
        ("A", U != 2),
        ("B", W != 4),
        ("C", X != 6),
        ("D", U < T),
        ("E", X < W),
    ]
    
    # For each option, get models with that constraint instead of T != 1
    matching_options = []
    for letter, opt_constr in options:
        models = get_all_models(base_constraints + [opt_constr], variables)
        print(f"Option {letter}: {len(models)} solutions.")
        if set(models) == set(original_models):
            matching_options.append(letter)
    
    # Output result
    if len(matching_options) == 1:
        print("STATUS: sat")
        print(f"answer:{matching_options[0]}")
    elif len(matching_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {matching_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")

if __name__ == "__main__":
    main()