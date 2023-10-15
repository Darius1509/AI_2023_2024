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
# WIP
#Functia de initializare a starii
# def initialize_problem_state(initial_state):
#     if is_valid_state(initial_state):
#         return initial_state
#     else:
#         print("Starea inițială nu este validă.")
#         return None