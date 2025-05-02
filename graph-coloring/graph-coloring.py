import sys
import os

def read_graph(filename):
    """
    Read a graph in DIMACS format from a file.
    
    The DIMACS format for graph coloring has the following structure:
    - Lines starting with 'c' are comments
    - The line 'p edge n m' specifies the problem with n vertices and m edges
    - Each line 'e u v' represents an edge between vertices u and v
    
    Args:
        filename (str): Path to the DIMACS format graph file
        
    Returns:
        tuple: (n, edges) where n is the number of vertices and 
               edges is a list of tuples (u, v) representing edges
    """
    n = 0
    edges = []
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('c'):
                continue
            
            parts = line.split()
            if parts[0] == 'p':
                # Parse the problem line: p edge n m
                n = int(parts[2])
            elif parts[0] == 'e':
                # Parse an edge line: e u v
                u, v = int(parts[1]), int(parts[2])
                edges.append((u, v))
    
    return n, edges

def encode_graph_coloring(n, edges, k):
    """
    Encode the k-colorability problem as a SAT instance using the traditional encoding.
    
    The traditional encoding uses three types of constraints:
    1. Every vertex must have at least one color
    2. Every vertex must have at most one color
    3. Adjacent vertices must have different colors
    
    Args:
        n (int): Number of vertices in the graph
        edges (list): List of edges as tuples (u, v)
        k (int): Number of colors
        
    Returns:
        list: List of clauses, where each clause is a list of integers representing literals
    """
    clauses = []
    
    # Variable indexing function: maps vertex v and color c to a unique variable index
    # Variables are numbered from 1 to n*k
    def var_index(v, c):
        """
        Convert vertex and color to variable index.
        For vertex v and color c, the variable index is (v-1)*k + c
        
        Args:
            v (int): Vertex number (1-indexed)
            c (int): Color number (1-indexed)
            
        Returns:
            int: Variable index for SAT formula
        """
        return (v - 1) * k + c
    
    # 1. Every vertex must have at least one color
    for v in range(1, n + 1):
        # Create a clause (x_{v,1} ∨ x_{v,2} ∨ ... ∨ x_{v,k})
        clause = [var_index(v, c) for c in range(1, k + 1)]
        clauses.append(clause)
    
    # 2. Every vertex must have at most one color
    for v in range(1, n + 1):
        for c1 in range(1, k + 1):
            for c2 in range(c1 + 1, k + 1):
                # Create a clause (¬x_{v,c1} ∨ ¬x_{v,c2})
                # This ensures vertex v cannot have both colors c1 and c2
                clauses.append([-var_index(v, c1), -var_index(v, c2)])
    
    # 3. Adjacent vertices must have different colors
    for u, v in edges:
        for c in range(1, k + 1):
            # Create a clause (¬x_{u,c} ∨ ¬x_{v,c})
            # This ensures vertices u and v cannot both have color c
            clauses.append([-var_index(u, c), -var_index(v, c)])
    
    return clauses

def write_dimacs_cnf(clauses, num_vars, output_file=None):
    """
    Write the CNF formula in DIMACS format.
    
    The DIMACS CNF format has the following structure:
    - The line 'p cnf num_vars num_clauses' specifies the problem
    - Each subsequent line represents a clause, where integers represent
      literals (positive for variables, negative for negated variables),
      and each clause ends with a 0
    
    Args:
        clauses (list): List of clauses, where each clause is a list of integers
        num_vars (int): Number of variables in the formula
        output_file (str, optional): Path to output file. If None, print to stdout
    """
    num_clauses = len(clauses)
    # Create the header line
    lines = [f"p cnf {num_vars} {num_clauses}"]
    
    # Create a line for each clause
    for clause in clauses:
        # Each clause is space-separated and ends with 0
        lines.append(" ".join(map(str, clause)) + " 0")
    
    output = "\n".join(lines)
    
    if output_file:
        with open(output_file, 'w') as file:
            file.write(output)
    else:
        print(output)

def main():
    """
    Main function to parse command line arguments and execute the conversion.
    
    Command line arguments:
    1. Path to the graph file in DIMACS format
    2. Number of colors (k)
    
    Example usage:
    python graph_coloring.py myciel3.col 3
    """
    # Parse command line arguments
    if len(sys.argv) != 3:
        print("Usage: python graph_coloring.py <graph_file> <k>")
        sys.exit(1)
    
    # Get the graph file path
    graph_file = sys.argv[1]
    
    # Check if path is relative and adjust if needed
    if not os.path.isabs(graph_file):
        # Assuming the graph files are in the 'test' directory
        graph_file = os.path.join('test', graph_file)
    
    # Get the number of colors
    k = int(sys.argv[2])
    
    # Read the graph and encode it as a SAT problem
    n, edges = read_graph(graph_file)
    clauses = encode_graph_coloring(n, edges, k)
    
    # Calculate the total number of variables (n vertices × k colors)
    num_vars = n * k
    
    # Set up the output file path
    base_name = os.path.basename(graph_file)
    output_dir = 'output'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create output filename with format: [original_name]_[k]_coloring.cnf
    output_file = os.path.join(output_dir, f"{os.path.splitext(base_name)[0]}_{k}_coloring.cnf")
    
    # Write the CNF formula to the output file
    write_dimacs_cnf(clauses, num_vars, output_file)
    print(f"SAT encoding written to {output_file}")

# Execute main function when the script is run directly
if __name__ == "__main__":
    main()
