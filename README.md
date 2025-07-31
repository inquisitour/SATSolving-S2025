# SAT Solving Course - SS 2025

This repository contains implementations and solutions for the SAT Solving course exercises. The course covers fundamental and advanced techniques in Boolean satisfiability solving, including DPLL, CDCL, preprocessing techniques, and applications to combinatorial problems.

## Repository Structure

```
SATSolving-S2025/
├── graph-coloring/          # Exercise 1: Graph Coloring
│   ├── graph_coloring.py         # Main implementation
│   ├── test/                     # Input graph files
│   │   ├── myciel3.col           # Mycielski graph (chromatic number 4)
│   │   └── queen5_5.col          # 5x5 Queens graph (chromatic number 5)
│   ├── output/                   # Generated SAT encodings
│   │   ├── myciel3_2_coloring.cnf # 2-coloring (unsatisfiable)
│   │   ├── myciel3_3_coloring.cnf # 3-coloring (unsatisfiable)
│   │   ├── myciel3_4_coloring.cnf # 4-coloring (satisfiable)
│   │   ├── queen5_5_3_coloring.cnf # 3-coloring (unsatisfiable)
│   │   └── queen5_5_5_coloring.cnf # 5-coloring (satisfiable)
│   └── results/                  # MiniSat solver results
│       ├── result_myciel3_2.txt  # UNSAT result
│       ├── result_myciel3_3.txt  # UNSAT result
│       ├── result_myciel3_4.txt  # SAT result
│       ├── result_queen5_5_3.txt # UNSAT result
│       └── result_queen5_5_5.txt # SAT result
└── n-queens/                # Exercise 2: N-Queens Problem
    ├── nqueens.py                # Main implementation
    ├── nqueens-env/              # Virtual environment
    ├── run_nqueens.sh            # Execution script
    ├── test_results.txt          # Comprehensive test results
    └── requirements.txt          # Python dependencies
```

## Exercise 1: Graph Coloring to SAT

### Overview
Graph coloring is a classic NP-complete problem that asks whether a graph can be colored using at most k colors such that no adjacent vertices share the same color. This implementation creates a SAT encoding that is satisfiable if and only if the input graph is k-colorable.

### Implementation Details
The program implements the traditional encoding of graph k-colorability as a SAT problem, using three types of constraints:

1. **At least one color**: Every vertex must be assigned at least one color
2. **At most one color**: Every vertex must be assigned at most one color  
3. **Different colors for adjacent vertices**: Adjacent vertices must have different colors

For a graph with n vertices and k colors, the encoding uses n×k Boolean variables, where variable x_{v,c} is true if and only if vertex v is colored with color c.

### Usage
```bash
cd graph-coloring
python graph_coloring.py <graph_file> <k>
```

### Testing Results
- **myciel3**: Mycielski graph (11 vertices, chromatic number 4)
- **queen5_5**: Queens graph (25 vertices, chromatic number 5)
- All results verified using MiniSat SAT solver

## Exercise 2: N-Queens Solution Counter

### Overview
Implementation of an incremental SAT-based solution counter for the N-Queens problem. The program enumerates all possible ways to place N chess queens on an N×N chessboard such that no two queens attack each other.

### Technical Approach
- **SAT Encoding**: Traditional encoding with comprehensive constraint modeling
- **Solver**: PySAT toolkit with Glucose3 backend
- **Method**: Incremental SAT solving with solution blocking for complete enumeration
- **Constraints**: Row exclusivity, column exclusivity, diagonal exclusivity (both directions)

### Key Features
- ✅ **Complete enumeration** of all distinct solutions
- ✅ **Automatic verification** against OEIS sequence A000170
- ✅ **Scalable performance** (tested up to N=10)
- ✅ **Progress reporting** for larger instances
- ✅ **Professional output formatting**

### Installation and Setup
```bash
cd n-queens
python3 -m venv nqueens-env
./nqueens-env/bin/pip install python-sat
```

### Usage
```bash
# Using the virtual environment directly
./nqueens-env/bin/python nqueens.py <N>

# Or using the provided script
./run_nqueens.sh <N>
```

### Performance Results
| N | Solutions | Clauses | Variables | Runtime |
|---|-----------|---------|-----------|---------|
| 4 | 2 | 80 | 16 | < 1s |
| 5 | 10 | 165 | 25 | < 1s |
| 6 | 4 | 296 | 36 | < 1s |
| 8 | 92 | 736 | 64 | ~3s |
| 9 | 352 | 1065 | 81 | ~15s |
| 10 | 724 | 1480 | 100 | ~45s |

All results verified against the authoritative OEIS sequence A000170.

### Example Output
```bash
$ ./run_nqueens.sh 8
Solving 8-Queens problem...
========================================
Encoding 8-Queens problem...
Generated 736 clauses with 64 variables
Counting solutions...
Found 10 solutions so far...
Found 20 solutions so far...
...
Found 90 solutions so far...
========================================
Number of solutions for 8-Queens: 92
✓ Verification: Result matches OEIS A000170
```

## Dependencies and Requirements

### Exercise 1
- **Python 3.x**
- **MiniSat** (or compatible SAT solver)
- Standard Python libraries

### Exercise 2
- **Python 3.x** 
- **PySAT toolkit** (`python-sat` library)
- **Virtual environment** (for dependency management)

## References

- **DIMACS graph format**: [COLOR instances](https://mat.tepper.cmu.edu/COLOR/instances.html)
- **DIMACS CNF format**: Standard format for SAT problems
- **OEIS A000170**: [N-Queens sequence](https://oeis.org/A000170)
- **PySAT toolkit**: Python library for SAT solving

This repository contains practical implementations of modern SAT solving techniques.