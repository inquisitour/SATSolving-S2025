#!/usr/bin/env python3
"""
Educational examples for vivification 
"""

def example_1_basic_redundancy():
    """Simple redundant constraints"""
    return '''# Declarations
x = EnumSort([a, b])

# Constraints
x != a ::: x is not a
x == b ::: x is b (REDUNDANT - implied by x != a)

# Options
Question ::: What is x?
is_valid(x == a) ::: (A)
is_valid(x == b) ::: (B)'''

def example_2_complex_redundancy():
    """More complex logical redundancy"""
    return '''# Declarations
people = EnumSort([Alice, Bob, Charlie])
colors = EnumSort([red, blue, green])
likes = Function([people] -> [colors])

# Constraints
likes(Alice) == red ::: Alice likes red
likes(Bob) != red ::: Bob doesn't like red
likes(Charlie) != red ::: Charlie doesn't like red
likes(Alice) != blue ::: Alice doesn't like blue (REDUNDANT)
likes(Alice) != green ::: Alice doesn't like green (REDUNDANT)

# Options
Question ::: What does Alice like?
is_valid(likes(Alice) == red) ::: (A)
is_valid(likes(Alice) == blue) ::: (B)
is_valid(likes(Alice) == green) ::: (C)'''

def example_3_no_redundancy():
    """Example with no redundant constraints"""
    return '''# Declarations
x = EnumSort([a, b, c])
y = EnumSort([d, e, f])
rel = Function([x] -> [y])

# Constraints
rel(a) != rel(b) ::: a and b map to different values
rel(b) != rel(c) ::: b and c map to different values  
rel(a) != rel(c) ::: a and c map to different values

# Options
Question ::: Are all mappings different?
is_valid(rel(a) != rel(b)) ::: (A)'''

def get_all_examples():
    return [
        ("Basic Redundancy", example_1_basic_redundancy()),
        ("Complex Redundancy", example_2_complex_redundancy()),
        ("No Redundancy", example_3_no_redundancy())
    ]
