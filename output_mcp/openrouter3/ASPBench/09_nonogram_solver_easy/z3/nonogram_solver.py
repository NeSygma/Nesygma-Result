from z3 import *

def solve_nonogram():
    solver = Solver()
    
    # Create 5x5 grid of binary variables (0=white, 1=black)
    grid = [[Int(f"cell_{i}_{j}") for j in range(5)] for i in range(5)]
    
    # Constraint 1: Each cell must be 0 or 1
    for i in range(5):
        for j in range(5):
            solver.add(Or(grid[i][j] == 0, grid[i][j] == 1))
    
    # Helper function to check if a row/column matches a clue
    def check_clue(sequence, clue):
        """Check if a sequence matches the given clue pattern."""
        n = len(sequence)
        clue_len = len(clue)
        
        # If clue is empty, all cells must be white
        if clue_len == 0:
            return And([cell == 0 for cell in sequence])
        
        # Create variables for group positions
        # For each group, we need to know where it starts and ensure it's the right length
        # We'll use a different approach: check that the sequence produces exactly the groups in clue
        
        # Count groups in the sequence and their lengths
        # We'll use Z3 to enforce that the sequence has exactly the groups specified
        
        # Create a list to track group lengths
        group_lengths = []
        current_length = 0
        in_group = False
        
        # We need to encode this logically
        # For each position, we can track whether we're in a group and the current group length
        
        # Alternative approach: Use a state machine
        # States: 0 = between groups, 1 = in a group
        # We'll track the current group index and position within group
        
        # For simplicity, let's use a direct constraint approach
        # We'll ensure that the sequence has exactly the groups specified
        
        # Create variables for group boundaries
        # For each possible start position of each group
        # This gets complex, so let's use a simpler method
        
        # Method: Check that the sequence can be partitioned into the clue groups
        # with at least one white cell between groups
        
        # For each possible assignment of group positions
        # We'll create constraints that ensure the groups appear in order
        
        # Let's use a different approach: encode the sequence as a string of 0s and 1s
        # and check that it matches the pattern
        
        # For each possible pattern that matches the clue, add an OR constraint
        # This is exponential but works for small puzzles
        
        # Generate all valid patterns for this clue
        patterns = generate_patterns(clue, n)
        
        if not patterns:
            return False
        
        # Create OR of all valid patterns
        pattern_constraints = []
        for pattern in patterns:
            pattern_match = And([sequence[i] == pattern[i] for i in range(n)])
            pattern_constraints.append(pattern_match)
        
        return Or(pattern_constraints)
    
    def generate_patterns(clue, length):
        """Generate all valid binary patterns for a given clue and length."""
        if not clue:
            return [[0] * length]
        
        patterns = []
        
        def backtrack(pos, group_idx, current_pattern):
            if group_idx == len(clue):
                # Fill remaining with zeros
                while pos < length:
                    current_pattern.append(0)
                    pos += 1
                patterns.append(current_pattern[:])
                return
            
            group_len = clue[group_idx]
            
            # Try placing the group starting at each possible position
            for start in range(pos, length - sum(clue[group_idx:]) - (len(clue) - group_idx - 1) + 1):
                # Check if we have enough space
                remaining_groups = sum(clue[group_idx + 1:])
                min_space_after = remaining_groups + (len(clue) - group_idx - 1)  # groups + separators
                if start + group_len + min_space_after > length:
                    continue
                
                # Fill zeros before the group
                while len(current_pattern) < start:
                    current_pattern.append(0)
                
                # Add the group
                for _ in range(group_len):
                    current_pattern.append(1)
                
                # Add at least one zero after the group (unless it's the last group)
                if group_idx < len(clue) - 1:
                    current_pattern.append(0)
                
                # Recurse for next group
                backtrack(len(current_pattern), group_idx + 1, current_pattern)
                
                # Backtrack: remove what we added
                while len(current_pattern) > start:
                    current_pattern.pop()
        
        backtrack(0, 0, [])
        return patterns
    
    # Row constraints
    row_clues = [
        [2],      # Row 1
        [1],      # Row 2
        [3],      # Row 3
        [1, 1],   # Row 4
        [2]       # Row 5
    ]
    
    for i in range(5):
        row = grid[i]
        clue = row_clues[i]
        solver.add(check_clue(row, clue))
    
    # Column constraints
    col_clues = [
        [1, 1],   # Column 1
        [1, 3],   # Column 2
        [2],      # Column 3
        [1],      # Column 4
        [1]       # Column 5
    ]
    
    for j in range(5):
        col = [grid[i][j] for i in range(5)]
        clue = col_clues[j]
        solver.add(check_clue(col, clue))
    
    # Check for solution
    result = solver.check()
    
    if result == sat:
        model = solver.model()
        print("STATUS: sat")
        print("Solution found:")
        for i in range(5):
            row_str = ""
            for j in range(5):
                cell_val = model[grid[i][j]]
                row_str += str(cell_val) + " "
            print(f"Row {i+1}: {row_str}")
        
        # Also print as a grid for clarity
        print("\nGrid:")
        for i in range(5):
            row_str = ""
            for j in range(5):
                cell_val = model[grid[i][j]]
                row_str += "█" if cell_val == 1 else " "
            print(f"Row {i+1}: {row_str}")
            
    elif result == unsat:
        print("STATUS: unsat")
        print("No solution exists")
    else:
        print("STATUS: unknown")
        print("Solver returned unknown")

if __name__ == "__main__":
    solve_nonogram()