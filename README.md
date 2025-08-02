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
├── n-queens/                # Exercise 2: N-Queens Problem
│   ├── nqueens.py                # Main implementation
│   ├── run_nqueens.sh            # Execution script
│   ├── test_results.txt          # Comprehensive test results
│   └── requirements.txt          # Python dependencies
└── vivification/            # Course Project: Clause Vivification
    ├── src/                      # Source code
    │   ├── vivification_solver.py     # Vivification implementation
    │   ├── sat_problem_solver.py      # Logic-LLM base solver
    │   └── code_translator.py         # DSL to Z3 translator
    ├── tests/                    # Test suite
    │   ├── test_vivification.py       # Main functionality tests
    │   ├── educational_examples.py    # Course-specific examples
    │   └── comprehensive_tests.py     # Complete test coverage
    ├── demo/                     # Interactive demonstration
    │   └── presentation_demo.py       # Live presentation script
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
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Usage
```bash
# Run the shell script
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

## Course Project: Clause Vivification Implementation

### Overview
Implementation of clause vivification (Algorithm 3 from the course), a preprocessing technique for SAT solvers that removes redundant constraints before solving. This project demonstrates how vivification can be utilised for SAT solving optimizations.

### Technical Approach
- **Algorithm**: Conservative implementation of Algorithm 3 (Vivification) from course materials
- **Integration**: Built on Logic-LLM framework for symbolic reasoning
- **Solver**: Z3 theorem prover with custom preprocessing pipeline
- **Method**: Pattern-based redundancy detection with correctness preservation

### Key Features
- ✅ **Real constraint removal** from Z3 solver input (30% average reduction)
- ✅ **100% correctness preservation** across all test cases
- ✅ **Logic-LLM integration** maintaining full symbolic reasoning capabilities
- ✅ **Conservative approach** prioritizing reliability over aggressive optimization
- ✅ **Educational examples** demonstrating different vivification scenarios

### Implementation Details
The vivification implementation analyzes constraint patterns to identify obvious redundancies:

1. **Positive-Negative Redundancy**: If `x == a` exists, then `x != b` (where a ≠ b) is redundant
2. **Duplicate Detection**: Exact constraint duplicates are removed
3. **Conservative Strategy**: Only removes constraints with clear logical implications

### Installation and Setup
```bash
cd vivification
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Usage
```bash
# Individual functionality tests
python tests/test_vivification.py

# Run comprehensive test suite
python tests/comprehensive_tests.py
```

### Performance Results
| Example | Original Constraints | Final Constraints | Reduction | Correctness |
|---------|---------------------|-------------------|-----------|-------------|
| Basic Redundancy | 2 | 1 | 50.0% | ✓ Preserved |
| Complex Redundancy | 5 | 3 | 40.0% | ✓ Preserved |
| No Redundancy | 3 | 3 | 0.0% | ✓ Preserved |
| **Overall** | **10** | **7** | **30.0%** | **100%** |

### Example Output
```bash
$ python demo/presentation_demo.py
=== Applying Conservative Vivification ===
Original constraints: 3
  C1: likes(Alice) == red
  C2: likes(Alice) != blue
  C3: likes(Alice) != green

Checking constraint 2/3
  Target: likes(Alice) != blue
  → REMOVED (obviously redundant)

Vivified constraints: 1
  C1: likes(Alice) == red

Constraint reduction: 66.7%
✓ Correctness preserved: (A)
```

### Course Connection
This project implements **Algorithm 3 (Vivification)** from the SAT Solving course at TU Wien Austria, demonstrating:
- Practical application of course theoretical concepts
- Integration of SAT preprocessing with modern symbolic reasoning frameworks
- Real performance improvements through constraint optimization
- Educational value in understanding SAT solver internals

## Dependencies and Requirements

### Exercise 1
- **Python 3.x**
- **MiniSat** (or compatible SAT solver)
- Standard Python libraries

### Exercise 2
- **Python 3.x** 
- **PySAT toolkit** (`python-sat` library)
- **Virtual environment** (for dependency management)

### Course Project
- **Python 3.x**
- **Z3 theorem prover** (`z3-solver` library)
- **PLY parser** (`ply` library)
- **Virtual environment** (for dependency isolation)

## References

- **DIMACS graph format**: [COLOR instances](https://mat.tepper.cmu.edu/COLOR/instances.html)
- **DIMACS CNF format**: Standard format for SAT problems
- **OEIS A000170**: [N-Queens sequence](https://oeis.org/A000170)
- **PySAT toolkit**: Python library for SAT solving
- **Logic-LLM framework**: [GitHub repository](https://github.com/teacherpeterpan/Logic-LLM)
- **Z3 theorem prover**: Microsoft Research SMT solver

This repository contains practical implementations of modern SAT solving techniques and demonstrates the application of course concepts to real-world symbolic reasoning frameworks.
