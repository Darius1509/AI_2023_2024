import math

#1:
#reprezentarea starii: o matrice de 3x3
def initialize_state():
    return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

def is_final_state(board):
    for i in range(3):
        if (board[i][0] + board[i][1] + board[i][2] == 15 or
            board[0][i] + board[1][i] + board[2][i] == 15):
            return True
    if (board[0][0] + board[1][1] + board[2][2] == 15 or
        board[0][2] + board[1][1] + board[2][0] == 15):
        return True
    return False

def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))

def check_winner(board, player):
    for i in range(3):
        if (board[i][0] + board[i][1] + board[i][2] == 15 or
            board[0][i] + board[1][i] + board[2][i] == 15):
            return player
    if (board[0][0] + board[1][1] + board[2][2] == 15 or
        board[0][2] + board[1][1] + board[2][0] == 15):
        return player
    return None

def is_board_full(board):
    return all(all(cell != 0 for cell in row) for row in board)

#2
def is_valid_move(board, num):
    return any(num in row for row in board)

#3
#euristica maximizarii: maximizeaza scorul jucatorului 2
#euristica minimizarii: minimizeaza scorul jucatorului 1
#verifica daca starea duce la victoria jucatorului 1(returzeaza 1) sau a jucatorului 2[AI](returzeaza -1) sau 0 pt remiza
def evaluate_state(board, player):
    for i in range(3):
        if (board[i][0] + board[i][1] + board[i][2] == 15 or
            board[0][i] + board[1][i] + board[2][i] == 15):
            return 1 if player == 1 else -1
    if (board[0][0] + board[1][1] + board[2][2] == 15 or
        board[0][2] + board[1][1] + board[2][0] == 15):
        return 1 if player == 1 else -1
    return 0

#4
def minmax(board, depth, maximizing_player, player):
    if depth == 0 or is_final_state(board):
        return evaluate_state(board, player)

    if maximizing_player:
        max_eval = -math.inf
        for move in range(1, 10):
            if not is_valid_move(board, move):
                row = (move - 1) // 3
                col = (move - 1) % 3
                board[row][col] = move
                eval = minmax(board, depth - 1, False, player)
                board[row][col] = 0
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for move in range(1, 10):
            if not is_valid_move(board, move):
                row = (move - 1) // 3
                col = (move - 1) % 3
                board[row][col] = move
                eval = minmax(board, depth - 1, True, player)
                board[row][col] = 0
                min_eval = min(min_eval, eval)
        return min_eval

def best_move(board, player):
    best_eval = -math.inf if player == 1 else math.inf
    best_move = None

    for move in range(1, 10):
        if not is_valid_move(board, move):
            row = (move - 1) // 3
            col = (move - 1) % 3
            board[row][col] = move
            eval = minmax(board, 2, False, player)
            board[row][col] = 0

            if (player == 1 and eval > best_eval) or (player == 2 and eval < best_eval):
                best_eval = eval
                best_move = move

    return best_move

#rulare
def main():
    board = initialize_state()
    player = 1

    print("Jocul Number Scrabble")
    print_board(board)

    while True:
        try:
            if player == 1:
                num = int(input(f"Jucător {player}, alege un număr de la 1 la 9: "))
                if num < 1 or num > 9:
                    print("Numărul trebuie să fie între 1 și 9.")
                    continue
            else:
                num = best_move(board, 2)

            row = (num - 1) // 3
            col = (num - 1) % 3

            if board[row][col] != 0:
                print("Numărul a fost deja ales. Alege alt număr.")
                continue

            board[row][col] = num
            print_board(board)

            winner = check_winner(board, player)
            if winner:
                print(f"Jucătorul {winner} a câștigat!")
                break

            if is_board_full(board):
                print("Remiză! Nu mai pot fi alese numere.")
                break

            player = 3 - player  # Schimbă jucătorul între 1 și 2
        except ValueError:
            print("Introdu un număr valid.")

if __name__ == "__main__":
    main()
