from z3 import *

def solve():
    # Articles
    articles = ['G', 'H', 'J', 'Q', 'R', 'S', 'Y']
    # Topics: F (Finance), N (Nutrition), W (Wildlife)
    # G, H, J -> F
    # Q, R, S -> N
    # Y -> W
    
    # pos[article] = position (1-7)
    pos = {a: Int(f'pos_{a}') for a in articles}
    
    solver = Solver()
    
    # Domain constraints
    for a in articles:
        solver.add(pos[a] >= 1, pos[a] <= 7)
    solver.add(Distinct([pos[a] for a in articles]))
    
    # Topic mapping
    # topic_at_pos[p] = topic (0: F, 1: N, 2: W)
    topic_at_pos = [Int(f'topic_at_pos_{p}') for p in range(1, 8)]
    
    for p in range(1, 8):
        # F: 0, N: 1, W: 2
        is_F = Or(pos['G'] == p, pos['H'] == p, pos['J'] == p)
        is_N = Or(pos['Q'] == p, pos['R'] == p, pos['S'] == p)
        is_W = (pos['Y'] == p)
        
        solver.add(If(is_F, topic_at_pos[p-1] == 0, 
                   If(is_N, topic_at_pos[p-1] == 1, 
                   topic_at_pos[p-1] == 2)))
    
    # Condition 1: Consecutive articles cannot cover the same topic
    for p in range(6):
        solver.add(topic_at_pos[p] != topic_at_pos[p+1])
        
    # Condition 2: S < Q only if Q is 3rd
    solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))
    
    # Condition 3: S < Y
    solver.add(pos['S'] < pos['Y'])
    
    # Condition 4: J < G < R
    solver.add(pos['J'] < pos['G'], pos['G'] < pos['R'])
    
    # Options
    options = [
        ("A", pos['H'] == 4),
        ("B", pos['H'] == 6),
        ("C", pos['R'] == 4),
        ("D", pos['R'] == 7),
        ("E", pos['Y'] == 5)
    ]
    
    def count_solutions(base_solver, constraint):
        base_solver.push()
        base_solver.add(constraint)
        
        solutions = []
        while base_solver.check() == sat:
            m = base_solver.model()
            sol = {a: m[pos[a]].as_long() for a in articles}
            solutions.append(sol)
            # Block this solution
            base_solver.add(Or([pos[a] != m[pos[a]] for a in articles]))
            if len(solutions) > 1:
                break
        base_solver.pop()
        return len(solutions)

    found_options = []
    for letter, constr in options:
        if count_solutions(solver, constr) == 1:
            found_options.append(letter)
            
    if len(found_options) == 1:
        print("STATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")

solve()