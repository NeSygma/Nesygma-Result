from z3 import *

def solve_send_more_money():
    # Create solver
    solver = Solver()
    
    # Declare variables for each letter
    S, E, N, D, M, O, R, Y = Ints('S E N D M O R Y')
    
    # Constraint 1: Each letter gets a digit from 0-9
    letters = [S, E, N, D, M, O, R, Y]
    for letter in letters:
        solver.add(letter >= 0, letter <= 9)
    
    # Constraint 2: All letters must have different digits
    solver.add(Distinct(letters))
    
    # Constraint 3: Leading zeros - S and M cannot be 0
    solver.add(S != 0)
    solver.add(M != 0)
    
    # Constraint 4: Arithmetic correctness
    # SEND = 1000*S + 100*E + 10*N + D
    # MORE = 1000*M + 100*O + 10*R + E
    # MONEY = 10000*M + 1000*O + 100*N + 10*E + Y
    send = 1000*S + 100*E + 10*N + D
    more = 1000*M + 100*O + 10*R + E
    money = 10000*M + 1000*O + 100*N + 10*E + Y
    
    solver.add(send + more == money)
    
    # Check for solution
    result = solver.check()
    
    if result == sat:
        model = solver.model()
        print("STATUS: sat")
        
        # Extract assignment using the correct method
        assignment = {}
        for letter in letters:
            # Use model.eval() or model[letter] and convert to Python int
            val = model[letter]
            if val is not None:
                assignment[str(letter)] = int(str(val))
        
        # Print assignment
        print("Assignment:")
        for letter, digit in sorted(assignment.items()):
            print(f"  {letter} = {digit}")
        
        # Create equation string
        s_val = assignment['S']
        e_val = assignment['E']
        n_val = assignment['N']
        d_val = assignment['D']
        m_val = assignment['M']
        o_val = assignment['O']
        r_val = assignment['R']
        y_val = assignment['Y']
        
        send_num = 1000*s_val + 100*e_val + 10*n_val + d_val
        more_num = 1000*m_val + 100*o_val + 10*r_val + e_val
        money_num = 10000*m_val + 1000*o_val + 100*n_val + 10*e_val + y_val
        
        equation = f"{send_num} + {more_num} = {money_num}"
        print(f"Equation: {equation}")
        
        # Verify the solution
        valid = (send_num + more_num == money_num)
        print(f"Valid: {valid}")
        
        return assignment, equation, valid
        
    elif result == unsat:
        print("STATUS: unsat")
        print("No solution exists for the given constraints.")
        return None, None, False
    else:
        print("STATUS: unknown")
        return None, None, False

# Run the solver
assignment, equation, valid = solve_send_more_money()