#1.
# variabile: fiecare casuta din sudoku
# domeniu: numerele de la 1 la 9
# restricții: fiecare linie, coloană sau regiune 3x3 conține toate valorile de la 1 la 9.
# Anumite căsuțe trebuie să conțină un număr par.

def initialize_problem_state(initial_state, even_positions):
    if is_valid_state(initial_state, even_positions):
        return initial_state
    else:
        print("Starea inițială nu este validă.")
        return 0

def is_valid_state(state, even_positions):
    #dimensiunea matricei trebuie să fie 9x9
    if len(state) != 9 or any(len(row) != 9 for row in state):
        return False

    #trebuie sa ne asiguram ca matricea nu are doar 0-uri
    #si ca nu este deja completata
    numbers = set()
    flag = False
    for row in state:
        for num in row:
            if num in range(10):
                flag = True
    if flag == False:
        return False
    if(is_goal_state(state, even_positions)):
        return False
    #verificam daca numerele de pe pozitiile din even_positions sunt pare sau 0
    for i, j in even_positions:
        if state[i][j] % 2 != 0 and state[i][j] != 0:
            return False
    return True

def is_goal_state(matrix, even_numbers):
    numbers = [element for row in matrix for element in row if element != 0]
    return numbers == list(range(1, len(numbers) + 1)) and all(matrix[i][j] % 2 == 0 for i, j in even_numbers)


# exemplu de stare initiala
# matrix = [[8, 4, 0, 0, 5, 0, 0, 0, 0],
#           [3, 0, 0, 6, 0, 8, 0, 4, 0],
#           [0, 0, 0, 4, 0, 9, 0, 0, 0],
#           [0, 2, 3, 0, 0, 0, 9, 8, 0],
#           [1, 0, 0, 0, 0, 0, 0, 0, 4],
#           [0, 9, 8, 0, 0, 0, 1, 6, 0],
#           [0, 0, 0, 5, 0, 3, 0, 0, 0],
#           [0, 3, 0, 1, 0, 6, 0, 0, 7],
#           [0, 0, 0, 0, 2, 0, 0, 1, 3]]
# even = [(0, 6), (2, 2), (2, 8), (3, 4), (4, 3), (4, 5), (5, 4), (6, 0), (6, 6), (8, 2)]
# print(is_valid_state(matrix, even))

#2
def forward_checking(state, even_positions):
    for i, j in even_positions:
        if state[i][j] != 0:
            # If the variable is assigned, eliminate it from the domains of variables in the same row, column, and 3x3 box.
            value = state[i][j]
            for x in range(9):
                if x != j and value in state[i]:
                    state[i][x] = 0
                if x != i and value in [state[y][j] for y in range(9)]:
                    state[x][j] = 0
            row_start, col_start = 3 * (i // 3), 3 * (j // 3)
            for x in range(row_start, row_start + 3):
                for y in range(col_start, col_start + 3):
                    if x != i and y != j and value in [state[x][y] for x in range(row_start, row_start + 3) for y in range(col_start, col_start + 3)]:
                        state[i][j] = 0
    return state

#3
def find_min_remaining_value(state, even_positions):
    min_remaining_values = float('inf')
    selected_cell = None

    for i, j in even_positions:
        if state[i][j] == 0:
            remaining_values = 0
            for value in range(1, 10):
                if value not in state[i] and value not in [state[y][j] for y in range(9)]:
                    row_start, col_start = 3 * (i // 3), 3 * (j // 3)
                    valid = True
                    for x in range(row_start, row_start + 3):
                        for y in range(col_start, col_start + 3):
                            if state[x][y] == 0 and value in [state[a][b] for a in range(row_start, row_start + 3) for b in range(col_start, col_start + 3)]:
                                valid = False
                                break
                        if not valid:
                            break
                    if valid:
                        remaining_values += 1

            if remaining_values < min_remaining_values:
                min_remaining_values = remaining_values
                selected_cell = (i, j)

    return selected_cell

matrix = [[0, 6, 0, 0, 3, 0, 5, 0, 0],
          [9, 0, 0, 0, 6, 0, 0, 0, 0],
          [1, 7, 0, 0, 0, 9, 0, 0, 0],
          [0, 1, 8, 7, 0, 0, 4, 3, 6],
          [0, 0, 0, 0, 5, 0, 0, 0, 7],
          [2, 3, 8, 0, 0, 0, 0, 9, 0],
          [0, 2, 0, 9, 0, 8, 0, 0, 0],
          [0, 0, 0, 0, 4, 0, 0, 0, 2],
          [0, 4, 5, 0, 2, 0, 0, 1, 0]]
even = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 4), (1, 6), (1, 7), (2, 2), (2, 4), (2, 6), (2, 7), (3, 2), (3, 5),
        (3, 6), (3, 8), (4, 0), (4, 2), (4, 3), (4, 7), (5, 0), (5, 3), (5, 5), (5, 6), (6, 0), (6, 1), (6, 5), (6, 8),
        (7, 1), (7, 4), (7, 7), (7, 8), (8, 1), (8, 4), (8, 5), (8, 8)]
