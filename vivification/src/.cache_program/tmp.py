from z3 import *

person_sort, (Alice, Bob) = EnumSort('person', ['Alice', 'Bob'])
color_sort, (red, blue) = EnumSort('color', ['red', 'blue'])
person = [Alice, Bob]
color = [red, blue]
likes = Function('likes', person_sort, color_sort)

pre_conditions = []
pre_conditions.append(likes(Alice) == red)
pre_conditions.append(likes(Alice) == red)

def is_valid(option_constraints):
    solver = Solver()
    solver.add(pre_conditions)
    solver.add(Not(option_constraints))
    return solver.check() == unsat

def is_unsat(option_constraints):
    solver = Solver()
    solver.add(pre_conditions)
    solver.add(option_constraints)
    return solver.check() == unsat

def is_sat(option_constraints):
    solver = Solver()
    solver.add(pre_conditions)
    solver.add(option_constraints)
    return solver.check() == sat

def is_accurate_list(option_constraints):
    return is_valid(Or(option_constraints)) and all([is_sat(c) for c in option_constraints])

def is_exception(x):
    return not x


if is_valid(likes(Alice) == red): print('(A)')
if is_valid(likes(Alice) == blue): print('(B)')