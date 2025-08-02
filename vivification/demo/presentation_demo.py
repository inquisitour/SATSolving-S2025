#!/usr/bin/env python3

import sys
sys.path.append('.')

from src.vivification_solver import VivificationLSAT_Z3_Program
from src.sat_problem_solver import LSAT_Z3_Program
import time

def presentation_demo():
    """5-10 minute presentation demo"""

    print("="*60)
    print("CLAUSE VIVIFICATION IN SAT SOLVING")
    print("Course Project Demonstration")
    print("="*60)

    # Slide 1: What is Vivification?
    print("\n🎯 WHAT IS CLAUSE VIVIFICATION?")
    print("- Preprocessing technique from SAT course (Algorithm 3)")
    print("- Removes redundant clauses before solving")
    print("- Can shorten clauses by removing redundant literals")
    print("- Improves solver performance")

    input("\nPress Enter to see a live example...")

    # Slide 2: Example Problem
    print("\n🔍 EXAMPLE PROBLEM:")
    logic_program = '''# Declarations
person = EnumSort([Alice, Bob])
color = EnumSort([red, blue])
likes = Function([person] -> [color])

# Constraints
likes(Alice) == red ::: Alice likes red
likes(Alice) != blue ::: Alice doesn't like blue (REDUNDANT!)

# Options
Question ::: What does Alice like?
is_valid(likes(Alice) == red) ::: (A)
is_valid(likes(Alice) == blue) ::: (B)'''

    print(logic_program)

    input("\nPress Enter to see standard solving...")

    # Slide 3: Standard Solving
    print("\n⚙️ STANDARD LOGIC-LLM SOLVING:")
    start_time = time.time()
    standard_program = LSAT_Z3_Program(logic_program, 'DEMO')

    if standard_program.flag:
        print("Generated Z3 constraints:")
        for i, constraint in enumerate(standard_program.constraints):
            print(f"  {i+1}. {constraint}")

        result, _ = standard_program.execute_program()
        standard_time = time.time() - start_time
        print(f"\nResult: {result[-1] if result else 'None'}")
        print(f"Time: {standard_time:.3f}s")
        print(f"Constraints processed: {len(standard_program.constraints)}")

    input("\nPress Enter to see vivification in action...")

    # Slide 4: Vivification in Action
    print("\n🧠 VIVIFICATION IN ACTION:")
    start_time = time.time()
    vivification_program = VivificationLSAT_Z3_Program(logic_program, 'DEMO', use_vivification=True)

    if vivification_program.flag:
        result, _ = vivification_program.execute_program()
        vivification_time = time.time() - start_time
        stats = vivification_program.vivification_stats

        print(f"\nResult: {result[-1] if result else 'None'}")
        print(f"Time: {vivification_time:.3f}s")
        print(f"Constraints processed: {stats['final_constraints']}")
        print(f"Constraints removed: {stats['removed_constraints']}")

    input("\nPress Enter for conclusion...")

    # Slide 5: Key Insights
    print("\n🎓 KEY INSIGHTS:")
    print("✓ Vivification preserves correctness")
    print("✓ Reduces problem complexity")
    print("✓ Integrates with existing SAT solvers")
    print("✓ Demonstrates SAT course algorithms in practice")
    print("\nThis project shows how preprocessing techniques")
    print("from SAT theory improve real-world solver performance!")

if __name__ == "__main__":
    presentation_demo()
