#1.
# variabile: fiecare casuta din sudoku
# domeniu: numerele de la 1 la 9
# restricții: fiecare linie, coloană sau regiune 3x3 conține toate valorile de la 1 la 9.
# Anumite căsuțe trebuie să conțină un număr par.

#marimea matricii
M = 9

#functie de afisare a matricii
def puzzle(a):
    for i in range(M):
        for j in range(M):
            print(a[i][j], end=" ")
        print()

#functia de validare a starii
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

#functie de verificare a validitatii unei asignari
def is_valid_assignment(grid, row, col, num, even_positions):
    for x in range(M):
        if grid[row][x] == num:
            return False

    for x in range(M):
        if grid[x][col] == num:
            return False

    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False

    if (row, col) in even_positions and num % 2 != 0:
        return False

    return True

#2. forward checking - eliminarea valorilor din domeniu
def forward_check(grid, row, col, domain):
    for x in range(M):
        if grid[row][x] == 0:
            domain[row][x].discard(grid[row][col])
        if grid[x][col] == 0:
            domain[x][col].discard(grid[row][col])

    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            r, c = i + startRow, j + startCol
            if grid[r][c] == 0:
                domain[r][c].discard(grid[row][col])

#functie pt resetarea domeniului
def reset_domain(domain):
    for i in range(M):
        for j in range(M):
            domain[i][j] = set(range(1, 10))

#3. MRV - Minimum Remaining Values
def get_empty_cell_with_mrv(grid, domain, even_positions):
    min_domain_size = float('inf')
    selected_cell = None

    for i in range(M):
        for j in range(M):
            if grid[i][j] == 0:
                if (i, j) in even_positions:
                    remaining_values = [num for num in domain[i][j] if num % 2 == 0]
                else:
                    remaining_values = list(domain[i][j])

                if len(remaining_values) < min_domain_size:
                    min_domain_size = len(remaining_values)
                    selected_cell = (i, j)

    return selected_cell

#functie de rezolvare a unei instante de sudoku
def Sudoku(grid, even_positions, domain):
    empty_cell = get_empty_cell_with_mrv(grid, domain, even_positions)
    if empty_cell is None:
        return True

    row, col = empty_cell
    remaining_values = list(domain[row][col])

    for num in remaining_values:
        if is_valid_assignment(grid, row, col, num, even_positions):
            grid[row][col] = num
            forward_check(grid, row, col, domain)

            if Sudoku(grid, even_positions, domain):
                return True

            grid[row][col] = 0
            reset_domain(domain)

    return False

#exemplu de rulare
even = [(0, 6), (2, 2), (2, 8), (3, 4), (4, 3), (4, 5), (5, 4), (6, 0), (6, 6), (8, 2)]

grid = [[8, 4, 0, 0, 5, 0, 0, 0, 0],
        [3, 0, 0, 6, 0, 8, 0, 4, 0],
        [0, 0, 0, 4, 0, 9, 0, 0, 0],
        [0, 2, 3, 0, 0, 0, 9, 8, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 9, 8, 0, 0, 0, 1, 6, 0],
        [0, 0, 0, 5, 0, 3, 0, 0, 0],
        [0, 3, 0, 1, 0, 6, 0, 0, 7],
        [0, 0, 0, 0, 2, 0, 0, 1, 3]]

#initializarea domeniului
domain = [[set(range(1, 10)) for _ in range(M)] for _ in range(M)]

#rulare
if is_valid_state(grid, even):
    if Sudoku(grid, even, domain):
        puzzle(grid)
    else:
        print("Solution does not exist :(")

