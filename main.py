import time as time
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

def is_goal_state(matrix):
    numbers = [element for row in matrix for element in row if element != 0]
    return numbers == list(range(1, len(numbers) + 1))

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


#4.
def IDDFS(src, max_depth):
    for depth in range(max_depth + 1):
        visited_states = set()
        if DLS(src, depth, visited_states):
            print("Number of states visited: ", len(visited_states))
            return True
    print("Number of states visited: ", len(visited_states))
    return False

def DLS(src, depth, visited):
    if depth == 0 and is_goal_state(src):
        print(src)
        return True
    if depth > 0:
        visited.add(tuple(map(tuple, src)))  # Add the state (as a tuple) to the visited set
        for direction in ["up", "down", "left", "right"]:
            new_state = move(list(map(list, src)), direction)  # Create a copy of the state
            if tuple(map(tuple, new_state)) not in visited:
                if DLS(new_state, depth - 1, visited):
                    return True
    return False

def run(state, max_depth):
    initialized_state = initialize_problem_state(state)
    if initialized_state is not None:
        result = IDDFS(initialized_state, max_depth)
        if result:
            print("Solution found")
        else:
            print("Solution not found")

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

"""
run(initial_state, 15)
run(initial_state1, 15)
run(initial_state2, 15)
"""
#5
def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            num = state[i][j]
            if num != 0:
                target_i, target_j = num // 3, num % 3
                distance += abs(i - target_i) + abs(j - target_j)
    return distance

def hamming_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            num = state[i][j]
            if num != 0 and num != i * 3 + j + 1:
                distance += 1
    return distance

#heuristic that calculates the number of swaps required to move the elements from their current positions to their correct positions
def max_swap(state):
    max_swaps = 0

    for i in range(3):
        for j in range(3):
            num = state[i][j]
            if num != 0:
                target_i, target_j = num // 3, num % 3
                distance = abs(i - target_i) + abs(j - target_j)
                max_swaps = max(max_swaps, distance)

    return max_swaps

def greedy_best_search(state, heuristic):
    states_count = 0
    visited_states = set()
    queue = [(state, 0)]  # Coada ce contine stari si costul euristic al fiecarei stari

    while queue:
        queue.sort(key=lambda x: heuristic(x[0]))  # Sortare in functie de valoarea euristica
        current_state, depth = queue.pop(0)

        if is_goal_state(current_state):
            print(current_state)
            print("Solution found")
            print("Number of states visited: ", len(queue))
            return True
        if depth < 50: #evitarea buclelor infinite
            visited_states.add(tuple(map(tuple, current_state)))
            for direction in ["up", "down", "left", "right"]:
                new_state = move(list(map(list, current_state)), direction)
                if tuple(map(tuple, new_state)) not in visited_states:
                    queue.append((new_state, depth + 1))
                    states_count += 1


    print("Solution not found")
    print("Number of states visited: ", len(queue))
    return False

# print("Using Manhattan Distance Heuristic:")
# greedy_best_search(initial_state, manhattan_distance)
#
# print("\nUsing Hamming Distance Heuristic:")
# greedy_best_search(initial_state, hamming_distance)
#
# print("\nUsing Max Swap Heuristic:")
# greedy_best_search(initial_state, max_swap)

#6
def run_all_strategies(initial_state, max_depth):
    start_time = time.time()
    print("Using IDDFS:")
    run(initial_state, max_depth)
    print("Time elapsed: ", time.time() - start_time)

    start_time = time.time()
    print("\nUsing Manhattan Distance Heuristic:")
    greedy_best_search(initial_state, manhattan_distance)
    print("Time elapsed: ", time.time() - start_time)

    start_time = time.time()
    print("\nUsing Hamming Distance Heuristic:")
    greedy_best_search(initial_state, hamming_distance)
    print("Time elapsed: ", time.time() - start_time)

    start_time = time.time()
    print("\nUsing Max Swap Heuristic:")
    greedy_best_search(initial_state, max_swap)
    print("Time elapsed: ", time.time() - start_time)

run_all_strategies(initial_state, 50)