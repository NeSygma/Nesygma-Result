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
                while len(current_pattern) < length:
                    current_pattern.append(0)
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
        
        # Print grid values
        for i in range(5):
            row_vals = []
            for j in range(5):
                cell_val = model[grid[i][j]]
                row_vals.append(int(str(cell_val)))
            print(f"Row {i+1}: {row_vals}")
        
        # Verify the solution manually
        print("\nVerification:")
        print("Row clues: [2], [1], [3], [1,1], [2]")
        print("Column clues: [1,1], [1,3], [2], [1], [1]")
        
        # Check each row
        for i in range(5):
            row_vals = [int(str(model[grid[i][j]])) for j in range(5)]
            groups = []
            current = 0
            for val in row_vals:
                if val == 1:
                    current += 1
                else:
                    if current > 0:
                        groups.append(current)
                        current = 0
            if current > 0:
                groups.append(current)
            print(f"Row {i+1}: {row_vals} -> groups: {groups} (expected: {row_clues[i]})")
        
        # Check each column
        for j in range(5):
            col_vals = [int(str(model[grid[i][j]])) for i in range(5)]
            groups = []
            current = 0
            for val in col_vals:
                if val == 1:
                    current += 1
                else:
                    if current > 0:
                        groups.append(current)
                        current = 0
            if current > 0:
                groups.append(current)
            print(f"Col {j+1}: {col_vals} -> groups: {groups} (expected: {col_clues[j]})")
            
    elif result == unsat:
        print("STATUS: unsat")
        print("No solution exists")
    else:
        print("STATUS: unknown")
        print("Solver returned unknown")

if __name__ == "__main__":
    solve_nonogram()