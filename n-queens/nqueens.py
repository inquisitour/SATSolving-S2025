#!/usr/bin/env python3
"""
N-Queens Solution Counter using Incremental SAT Solving

This program counts all solutions to the N-Queens problem by encoding it as a SAT problem
and using incremental SAT solving to enumerate all satisfying assignments.

Author: Pratik Deshmukh
Course: SAT Solving SS 2025
"""

import sys
from pysat.solvers import Glucose3

def encode_nqueens(n):
    """
    Encode the N-Queens problem as SAT clauses.
    
    Variables: x_{i,j} = True if there's a queen at position (i,j)
    Variable numbering: x_{i,j} gets variable number i*n + j + 1 (1-indexed)
    
    Args:
        n (int): Board size (n x n)
        
    Returns:
        tuple: (clauses, num_vars) where clauses is list of clauses and num_vars is total variables
    """
    clauses = []
    num_vars = n * n
    
    def var(i, j):
        """Convert (i,j) position to variable number (1-indexed for SAT solver)"""
        return i * n + j + 1
    
    # Constraint 1: Exactly one queen per row
    for i in range(n):
        # At least one queen per row
        row_clause = []
        for j in range(n):
            row_clause.append(var(i, j))
        clauses.append(row_clause)
        
        # At most one queen per row
        for j1 in range(n):
            for j2 in range(j1 + 1, n):
                clauses.append([-var(i, j1), -var(i, j2)])
    
    # Constraint 2: At most one queen per column
    for j in range(n):
        for i1 in range(n):
            for i2 in range(i1 + 1, n):
                clauses.append([-var(i1, j), -var(i2, j)])
    
    # Constraint 3: At most one queen per diagonal (top-left to bottom-right)
    for d in range(-(n-1), n):  # diagonal offset
        diagonal_vars = []
        for i in range(n):
            j = i + d
            if 0 <= j < n:
                diagonal_vars.append(var(i, j))
        
        # At most one queen per diagonal
        for v1_idx in range(len(diagonal_vars)):
            for v2_idx in range(v1_idx + 1, len(diagonal_vars)):
                clauses.append([-diagonal_vars[v1_idx], -diagonal_vars[v2_idx]])
    
    # Constraint 4: At most one queen per anti-diagonal (top-right to bottom-left)
    for d in range(2 * n - 1):  # anti-diagonal sum
        antidiagonal_vars = []
        for i in range(n):
            j = d - i
            if 0 <= j < n:
                antidiagonal_vars.append(var(i, j))
        
        # At most one queen per anti-diagonal
        for v1_idx in range(len(antidiagonal_vars)):
            for v2_idx in range(v1_idx + 1, len(antidiagonal_vars)):
                clauses.append([-antidiagonal_vars[v1_idx], -antidiagonal_vars[v2_idx]])
    
    return clauses, num_vars

def decode_solution(model, n):
    """
    Decode a SAT model into queen positions.
    
    Args:
        model (list): SAT model (assignment of variables)
        n (int): Board size
        
    Returns:
        list: List of (row, col) tuples representing queen positions
    """
    def var(i, j):
        return i * n + j + 1
    
    queens = []
    for i in range(n):
        for j in range(n):
            var_num = var(i, j)
            if var_num <= len(model) and model[var_num - 1] > 0:
                queens.append((i, j))
    
    return queens

def print_board(queens, n):
    """Print the board with queens for debugging."""
    board = [['.' for _ in range(n)] for _ in range(n)]
    for i, j in queens:
        board[i][j] = 'Q'
    
    for row in board:
        print(' '.join(row))
    print()

def count_solutions(n, verbose=False):
    """
    Count all solutions to the N-Queens problem using incremental SAT.
    
    Args:
        n (int): Board size
        verbose (bool): If True, print debug information
        
    Returns:
        int: Number of solutions
    """
    print(f"Encoding {n}-Queens problem...")
    
    # Get the SAT encoding
    clauses, num_vars = encode_nqueens(n)
    
    print(f"Generated {len(clauses)} clauses with {num_vars} variables")
    
    # Initialize the SAT solver
    solver = Glucose3()
    
    # Add all N-Queens constraints
    for clause in clauses:
        solver.add_clause(clause)
    
    solution_count = 0
    
    print("Counting solutions...")
    
    # Incremental SAT solving loop
    while True:
        # Try to find a solution
        if solver.solve():
            # Get the model (satisfying assignment)
            model = solver.get_model()
            solution_count += 1
            
            if verbose:
                print(f"Solution {solution_count}:")
                queens = decode_solution(model, n)
                print_board(queens, n)
            else:
                # Print progress for larger problems
                if solution_count % 10 == 0:
                    print(f"Found {solution_count} solutions so far...")
            
            # Create blocking clause to exclude this solution
            blocking_clause = []
            for i in range(len(model)):
                if model[i] > 0:
                    blocking_clause.append(-(i + 1))
                else:
                    blocking_clause.append(i + 1)
            
            # Add the blocking clause to prevent finding the same solution again
            solver.add_clause(blocking_clause)
        else:
            # No more solutions
            break
    
    # Clean up
    solver.delete()
    
    return solution_count

def main():
    """Main function to handle command line arguments and execute the solution counting."""
    if len(sys.argv) != 2:
        print("Usage: python nqueens.py <N>")
        print("Example: python nqueens.py 8")
        sys.exit(1)
    
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Error: N must be an integer")
        sys.exit(1)
    
    if n <= 3:
        print("Error: N must be > 3")
        sys.exit(1)
    
    print(f"Solving {n}-Queens problem...")
    print("=" * 40)
    
    # Count solutions
    solutions = count_solutions(n, verbose=(n <= 6))
    
    print("=" * 40)
    print(f"Number of solutions for {n}-Queens: {solutions}")
    
    # Verification against known results
    known_results = {
        4: 2, 5: 10, 6: 4, 7: 40, 8: 92, 9: 352, 10: 724,
        11: 2680, 12: 14200, 13: 73712, 14: 365596
    }
    
    if n in known_results:
        expected = known_results[n]
        if solutions == expected:
            print(f"✓ Verification: Result matches OEIS A000170")
        else:
            print(f"✗ Verification: Expected {expected}, got {solutions}")
if __name__ == "__main__":
    main()