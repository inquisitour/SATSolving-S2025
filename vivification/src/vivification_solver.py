#!/usr/bin/env python3
"""
Vivification implementation with conservative redundancy detection
"""

from .sat_problem_solver import LSAT_Z3_Program
import time

class VivificationLSAT_Z3_Program(LSAT_Z3_Program):
    def __init__(self, logic_program: str, dataset_name: str, use_vivification=True):
        self.use_vivification = use_vivification
        self.vivification_stats = {
            'original_constraints': 0,
            'final_constraints': 0,
            'removed_constraints': 0,
            'vivification_time': 0.0
        }
        
        # Initialize parent class
        super().__init__(logic_program, dataset_name)
        
        # Apply conservative vivification
        if self.use_vivification and self.flag:
            self._apply_conservative_vivification()
    
    def _apply_conservative_vivification(self):
        """Apply conservative vivification focusing on obvious redundancies"""
        print("=== Applying Conservative Vivification ===")
        
        start_time = time.time()
        
        original_constraint_count = len(self.constraints)
        self.vivification_stats['original_constraints'] = original_constraint_count
        
        print(f"Original constraints: {original_constraint_count}")
        for i, constraint in enumerate(self.constraints):
            print(f"  C{i+1}: {constraint}")
        
        # Apply conservative vivification
        vivified_constraints = self._conservative_vivify(self.constraints)
        
        # Only update if we actually found redundancies
        if len(vivified_constraints) < len(self.constraints):
            self.constraints = vivified_constraints
            # Regenerate Z3 code with vivified constraints
            self.standard_code = self.to_standard_code()
        
        self.vivification_stats['final_constraints'] = len(self.constraints)
        self.vivification_stats['removed_constraints'] = original_constraint_count - len(self.constraints)
        self.vivification_stats['vivification_time'] = time.time() - start_time
        
        print(f"\nVivified constraints: {len(self.constraints)}")
        for i, constraint in enumerate(self.constraints):
            print(f"  C{i+1}: {constraint}")
        
        print(f"\nVivification completed in {self.vivification_stats['vivification_time']:.3f}s")
        self._print_vivification_stats()
    
    def _conservative_vivify(self, constraints):
        """
        Conservative vivification - only remove obviously redundant constraints
        """
        vivified_constraints = []
        
        print("\nApplying conservative vivification...")
        
        for constraint_idx, target_constraint in enumerate(constraints):
            print(f"\nChecking constraint {constraint_idx + 1}/{len(constraints)}")
            print(f"  Target: {target_constraint}")
            
            # Check for obvious patterns of redundancy
            is_redundant = self._is_obviously_redundant(target_constraint, constraints, constraint_idx)
            
            if is_redundant:
                print(f"  → REMOVED (obviously redundant)")
            else:
                print(f"  → KEPT")
                vivified_constraints.append(target_constraint)
        
        return vivified_constraints
    
    def _is_obviously_redundant(self, target_constraint, all_constraints, target_idx):
        """
        Conservative check for obvious redundancy patterns
        """
        # Pattern 1: If we have "x == a" and "x != b" where a != b, then "x != b" is redundant
        other_constraints = [c for i, c in enumerate(all_constraints) if i != target_idx]
        
        # Look for negation redundancy
        if " != " in target_constraint:
            var_part = target_constraint.split(" != ")[0].strip()
            neg_value = target_constraint.split(" != ")[1].strip()
            
            # Check if there's a positive constraint that makes this negative one redundant
            for other_constraint in other_constraints:
                if " == " in other_constraint:
                    other_var = other_constraint.split(" == ")[0].strip()
                    pos_value = other_constraint.split(" == ")[1].strip()
                    
                    # If same variable is assigned to a different value, the != is redundant
                    if var_part == other_var and pos_value != neg_value:
                        return True
        
        # Pattern 2: Exact duplicates
        for other_constraint in other_constraints:
            if target_constraint == other_constraint:
                return True
        
        # Pattern 3: Simple logical implications we can detect with string matching
        # This is conservative - only catches obvious cases
        
        return False  # Default: keep the constraint
    
    def _print_vivification_stats(self):
        """Print vivification statistics"""
        stats = self.vivification_stats
        print("\n=== Conservative Vivification Statistics ===")
        print(f"Original constraints: {stats['original_constraints']}")
        print(f"Final constraints: {stats['final_constraints']}")
        print(f"Removed constraints: {stats['removed_constraints']}")
        print(f"Processing time: {stats['vivification_time']:.3f}s")
        
        if stats['original_constraints'] > 0:
            reduction_percent = (stats['removed_constraints'] / stats['original_constraints']) * 100
            print(f"Constraint reduction: {reduction_percent:.1f}%")
    
    def execute_program(self):
        """Execute the vivified program"""
        result, error = super().execute_program()
        
        if self.use_vivification:
            print("\n=== Conservative Vivification Applied ===")
            self._print_vivification_stats()
        
        return result, error