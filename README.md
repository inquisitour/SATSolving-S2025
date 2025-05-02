# Graph Coloring to SAT Encoding

This repository contains an implementation of a graph k-colorability to SAT problem converter as part of the SAT Solving course (SS 2025). The program transforms graph coloring problems into Boolean satisfiability (SAT) instances, which can then be solved using SAT solvers.

## Overview

Graph coloring is a classic NP-complete problem that asks whether a graph can be colored using at most k colors such that no adjacent vertices share the same color. This implementation creates a SAT encoding that is satisfiable if and only if the input graph is k-colorable.

## Repository Structure

```
SATSolving-S2025/
└── graph-coloring/           # Graph coloring implementation folder
    ├── graph_coloring.py          # Main implementation
    ├── test/                      # Input graph files
    │   ├── myciel3.col            # Mycielski graph (chromatic number 4)
    │   └── queen5_5.col           # 5x5 Queens graph (chromatic number 5)
    ├── output/                    # Generated SAT encodings
    │   ├── myciel3_2_coloring.cnf # 2-coloring (unsatisfiable)
    │   ├── myciel3_3_coloring.cnf # 3-coloring (unsatisfiable)
    │   ├── myciel3_4_coloring.cnf # 4-coloring (satisfiable)
    │   ├── queen5_5_3_coloring.cnf # 3-coloring (unsatisfiable)
    │   └── queen5_5_5_coloring.cnf # 5-coloring (satisfiable)
    └── results/                   # MiniSat solver results
        ├── result_myciel3_2.txt    # UNSAT result
        ├── result_myciel3_3.txt    # UNSAT result
        ├── result_myciel3_4.txt    # SAT result
        ├── result_queen5_5_3.txt   # UNSAT result
        └── result_queen5_5_5.txt   # SAT result
```

## Implementation Details

The program implements the traditional encoding of graph k-colorability as a SAT problem, using the following types of constraints:

1. **At least one color**: Every vertex must be assigned at least one color
2. **At most one color**: Every vertex must be assigned at most one color
3. **Different colors for adjacent vertices**: Adjacent vertices must have different colors

For a graph with n vertices and k colors, the encoding uses n*k Boolean variables, where variable x_{v,c} is true if and only if vertex v is colored with color c.

## Usage

To run the program:

```bash
python graph_coloring.py <graph_file> <k>
```

Where:
- `<graph_file>` is the name of a graph file in DIMACS format in the test/ directory
- `<k>` is the number of colors

Example:
```bash
python graph_coloring.py myciel3.col 4
```

This will generate a file `output/myciel3_4_coloring.cnf` in DIMACS CNF format.

## Testing

The implementation has been tested on two benchmark graphs:

1. **myciel3**: A Mycielski graph with 11 vertices, known to require 4 colors
2. **queen5_5**: A Queens graph with 25 vertices, known to require 5 colors

The tests confirm that:
- myciel3 is not 2-colorable (UNSAT)
- myciel3 is not 3-colorable (UNSAT)
- myciel3 is 4-colorable (SAT)
- queen5_5 is not 3-colorable (UNSAT)
- queen5_5 is 5-colorable (SAT)

## SAT Solver

The generated CNF files were tested using MiniSat, a widely-used SAT solver. The results are stored in the results/ directory.

To run MiniSat on a generated CNF file:

```bash
minisat output/myciel3_4_coloring.cnf results/result_myciel3_4.txt
```

## References

- The DIMACS graph format is used for input graphs: [DIMACS Format](https://mat.tepper.cmu.edu/COLOR/instances.html)
- The DIMACS CNF format is used for output SAT problems

## Future Improvements

Potential improvements to the implementation could include:
- Support for alternative encodings that might be more efficient
- Extraction and visualization of the coloring solution from SAT solver output
- Performance optimizations for handling larger graphs
