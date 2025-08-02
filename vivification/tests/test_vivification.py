#!/usr/bin/env python3
"""
Test the vivification implementation
"""

import sys
sys.path.append('.')

from src.vivification_solver import VivificationLSAT_Z3_Program
from src.sat_problem_solver import LSAT_Z3_Program

def create_reliable_test_problem():
    """Create a problem with clear redundancy"""
    return '''# Declarations
person = EnumSort([Alice])
color = EnumSort([red, blue, green])
likes = Function([person] -> [color])

# Constraints
likes(Alice) == red ::: Alice likes red
likes(Alice) != blue ::: Alice doesn't like blue (REDUNDANT!)
likes(Alice) != green ::: Alice doesn't like green (REDUNDANT!)

# Options
Question ::: What does Alice like?
is_valid(likes(Alice) == red) ::: (A)
is_valid(likes(Alice) == blue) ::: (B)
is_valid(likes(Alice) == green) ::: (C)'''

def test_fixed_vivification():
    """Test the fixed implementation"""
    print("="*60)
    print("TESTING FIXED VIVIFICATION")
    print("="*60)
    
    logic_program = create_reliable_test_problem()
    
    # Test standard
    print("\n--- Standard Logic-LLM ---")
    standard_program = LSAT_Z3_Program(logic_program, 'TEST')
    if standard_program.flag:
        standard_result, _ = standard_program.execute_program()
        print(f"Standard result: {standard_result}")
        print(f"Standard constraints: {len(standard_program.constraints)}")
    
    # Test vivification
    print("\n--- Fixed Vivification ---")
    vivification_program = VivificationLSAT_Z3_Program(logic_program, 'TEST', use_vivification=True)
    if vivification_program.flag:
        vivification_result, _ = vivification_program.execute_program()
        print(f"Vivification result: {vivification_result}")
        
        # Check correctness
        if standard_result == vivification_result:
            print("✅ CORRECTNESS PRESERVED")
        else:
            print("❌ CORRECTNESS BROKEN")
        
        stats = vivification_program.vivification_stats
        if stats['removed_constraints'] > 0:
            print(f"✅ SUCCESSFULLY REMOVED {stats['removed_constraints']} REDUNDANT CONSTRAINTS")
        else:
            print("ℹ️ NO REDUNDANT CONSTRAINTS DETECTED")

if __name__ == "__main__":
    test_fixed_vivification()