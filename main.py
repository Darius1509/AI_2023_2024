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

#3.
previous_value = None
def get_zero_position(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return (i, j)

def valid_transition(state, direction):
    global previous_value
    i, j = get_zero_position(state)
    if direction == "up":
        if i == 0 or state[i - 1][j] == previous_value:
            return False
    elif direction == "down":
        if i == 2 or state[i + 1][j] == previous_value:
            return False
    elif direction == "left":
        if j == 0 or state[i][j - 1] == previous_value:
            return False
    elif direction == "right":
        if j == 2 or state[i][j + 1] == previous_value:
            return False
    return True


def move(state, direction):
    global previous_value
    i, j = get_zero_position(state)
    if valid_transition(state, direction):
        if direction == "up":
                state[i][j], state[i - 1][j] = state[i - 1][j], state[i][j]
                previous_value = state[i][j]
        elif direction == "down":
                state[i][j], state[i + 1][j] = state[i + 1][j], state[i][j]
                previous_value = state[i][j]
        elif direction == "left":
                state[i][j], state[i][j - 1] = state[i][j - 1], state[i][j]
                previous_value = state[i][j]
        elif direction == "right":
                state[i][j], state[i][j + 1] = state[i][j + 1], state[i][j]
                previous_value = state[i][j]
    return state  # Return the modified state

def IDDFS(src, target, max_depth):
    for depth in range(max_depth + 1):
        visited_states = set()
        if DLS(src, target, depth, visited_states):
            return True
    return False

def DLS(src, target, depth, visited):
    if depth == 0 and src == target:
        return True
    if depth > 0:
        visited.add(tuple(map(tuple, src)))  # Add the state (as a tuple) to the visited set
        for direction in ["up", "down", "left", "right"]:
            new_state = move(list(map(list, src)), direction)  # Create a copy of the state
            if tuple(map(tuple, new_state)) not in visited:
                if DLS(new_state, target, depth - 1, visited):
                    return True
    return False

visited_states = set()

initial_state = [
    [8, 6, 7],
    [2, 5, 4], 
    [0, 3, 1]
]

initial_state1 = [
    [2, 5, 3], 
    [1, 0, 6], 
    [4, 7, 8]
]

initial_state2 = [
    [2, 7, 5],
    [0, 8, 4], 
    [3, 1, 6]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

def run(state, goal, max_depth):
    if initialize_problem_state(state) != None:
        result = IDDFS(state, goal, max_depth)
        if result:
            print("Solution found")
        else:
            print("Solution not found")

run(initial_state, goal_state, 15)
run(initial_state1, goal_state, 15)
run(initial_state2, goal_state, 15)