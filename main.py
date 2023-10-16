#1.
#For the first task, we've set upon using a 3x3 matrix to represent our data structure.
#In regards to the fact that we cannot go back to the previous state, we will memorize the value
#of the last number that was moved(since the values in the matrix are unique) and we'll add this check
#in the state validation function
#EX:
# initial_state = [
#     [1, 3, 2],
#     [4, 8, 5],
#     [7, 6, 0]
# ]

#2.

def is_valid_state(state):    
    #dimensiunea matricei trebuie să fie 3x3
    if len(state) != 3 or any(len(row) != 3 for row in state):
        return False

    #toate numerele de la 0 la 8 trebuie să apară exact o dată
    numbers = set()
    for row in state:
        for num in row:
            if num not in range(9):
                return False
            numbers.add(num)
    
    return len(numbers) == 9

#functia de initializare a starii
def initialize_problem_state(initial_state):
    if is_valid_state(initial_state):
        return initial_state
    else:
        print("Starea inițială nu este validă.")
        return None

def is_goal_state(state):
    elements = [element for row in state for element in row if element != 0]

    return elements == list(range(1, len(elements) + 1))

"""
# Test 1: Goal state with numbers in ascending order (excluding 0)
state1 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]
print(is_goal_state(state1))  # Should return True
"""