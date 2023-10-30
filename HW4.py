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
matrix = [[8, 4, 0, 0, 5, 0, 0, 0, 0],
          [3, 0, 0, 6, 0, 8, 0, 4, 0],
          [0, 0, 0, 4, 0, 9, 0, 0, 0],
          [0, 2, 3, 0, 0, 0, 9, 8, 0],
          [1, 0, 0, 0, 0, 0, 0, 0, 4],
          [0, 9, 8, 0, 0, 0, 1, 6, 0],
          [0, 0, 0, 5, 0, 3, 0, 0, 0],
          [0, 3, 0, 1, 0, 6, 0, 0, 7],
          [0, 0, 0, 0, 2, 0, 0, 1, 3]]
even = [(0, 6), (2, 2), (2, 8), (3, 4), (4, 3), (4, 5), (5, 4), (6, 0), (6, 6), (8, 2)]
print(is_valid_state(matrix, even))
