#!/usr/bin/env python3
"""
Comprehensive test suite for vivification 
"""

import sys
sys.path.append('.')

from src.vivification_solver import VivificationLSAT_Z3_Program
from src.sat_problem_solver import LSAT_Z3_Program
from educational_examples import get_all_examples
import time

def run_comprehensive_tests():
    """Run all vivification tests"""
    print("="*60)
    print("COMPREHENSIVE VIVIFICATION TEST SUITE")
    print("="*60)
    
    examples = get_all_examples()
    results = []
    
    for example_name, logic_program in examples:
        print(f"\n{'='*20} {example_name} {'='*20}")
        
        # Test standard solving
        print("\n--- Standard Solving ---")
        start_time = time.time()
        standard_program = LSAT_Z3_Program(logic_program, 'TEST')
        if standard_program.flag:
            standard_result, _ = standard_program.execute_program()
            standard_time = time.time() - start_time
            standard_constraints = len(standard_program.constraints)
        else:
            print("❌ Standard program failed")
            continue
        
        # Test vivification solving
        print("\n--- Vivification Solving ---")
        start_time = time.time()
        vivification_program = VivificationLSAT_Z3_Program(logic_program, 'TEST', use_vivification=True)
        if vivification_program.flag:
            vivification_result, _ = vivification_program.execute_program()
            vivification_time = time.time() - start_time
            vivification_stats = vivification_program.vivification_stats
        else:
            print("❌ Vivification program failed")
            continue
        
        # Analyze results
        result = {
            'name': example_name,
            'standard_time': standard_time,
            'vivification_time': vivification_time,
            'standard_constraints': standard_constraints,
            'final_constraints': vivification_stats['final_constraints'],
            'removed_constraints': vivification_stats['removed_constraints'],
            'correctness_preserved': standard_result == vivification_result,
            'reduction_percentage': (vivification_stats['removed_constraints'] / standard_constraints) * 100 if standard_constraints > 0 else 0
        }
        
        results.append(result)
        
        print(f"\n--- Results for {example_name} ---")
        print(f"Correctness preserved: {'✓' if result['correctness_preserved'] else '❌'}")
        print(f"Constraints reduced: {result['removed_constraints']}/{result['standard_constraints']} ({result['reduction_percentage']:.1f}%)")
        print(f"Time comparison: {standard_time:.3f}s → {vivification_time:.3f}s")
    
    # Summary
    print(f"\n{'='*60}")
    print("OVERALL SUMMARY")
    print(f"{'='*60}")
    
    total_tests = len(results)
    successful_tests = sum(1 for r in results if r['correctness_preserved'])
    total_original_constraints = sum(r['standard_constraints'] for r in results)
    total_removed_constraints = sum(r['removed_constraints'] for r in results)
    
    print(f"Tests run: {total_tests}")
    print(f"Successful: {successful_tests}/{total_tests}")
    print(f"Total constraints removed: {total_removed_constraints}/{total_original_constraints}")
    print(f"Overall reduction: {(total_removed_constraints/total_original_constraints)*100:.1f}%")

if __name__ == "__main__":
    run_comprehensive_tests()
