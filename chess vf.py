# This file is an attempt to code the game chess in python
# Authors: Sverre Nystad, Eskild Øveren, Kristoffer Olaisen

# functions that
def make_board():  # Make the starting board that is an 2d array
    # ["♜", "♝", "♞", "♛", "♚", "♟"]
    # ["R", "B", "H", "Q", "K", "P"]
    # ["R", "B", "H", "Q", "K", "P"]
    board = [
        ["r", "h", "b", "k", "q", "b", "h", "r"],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'H', 'B', 'K', 'Q', 'B', 'H', 'R']
    ]
    return board


board = make_board()


def squar_to_index(squar):
    letter_pos = ["a", "b", "c", "d", "e", "f", "g", "h"]
    nums_pos = [1, 2, 3, 4, 5, 6, 7, 8]
    return [nums_pos.index(int(squar[1])), letter_pos.index(squar[0])]


def index_to_square(arr):
    letter_pos = ["a", "b", "c", "d", "e", "f", "g", "h"]
    nums_pos = [1, 2, 3, 4, 5, 6, 7, 8]
    return f"{letter_pos[arr[1]]}{nums_pos[arr[0]]}"


def what_pice(pos):  # fungerer
    # print(pos)
    pice = board[pos[0]][pos[1]]

    if pice == pice.lower():
        player = 0
    if pice == pice.upper():
        player = 1
    return pice, player


def user_input():  # skal gi brukeren mulighet for å si hvilken rute de tenker på
    letter = ["a", "b", "c", "d", "e", "f", "g", "h"]
    nums = [1, 2, 3, 4, 5, 6, 7, 8]
    try:
        move = input(f"""From which square to (a2,a4) """)
        move = (move.replace(" ", "")).split(",")
        if len(move) == 2 and len(move[0]) == len(move[1]) and len(move[0]) == 2:
            if move[0][0] in letter and int(move[0][1]) in nums and move[1][0] in letter and int(move[1][1]) in nums:
                return move
        print("Bad input try again.")
        return user_input()
    except ValueError:
        print("Bad input try again.")
        return user_input()


# start_pos, end_pos er begge lister. move_pice() skal ikke brukes før is_legal er True


def move_pice(start_pos, end_pos):
    board[end_pos[0]][end_pos[1]] = what_pice(start_pos)[0]
    board[start_pos[0]][start_pos[1]] = " "


def show_board():  # show_board Tegner opp brettet for spillerne så de kan se brettet
    # print(board)
    # Problem temp_board og board peker til samme sted i minne som gjøre
    # temp_board = list(board)
    # temp_board = board.copy()
    temp_board = board[:]

    # print(f"temp_board: id={id(temp_board)}, board: id={id(board)}")
    # pices = [["♜", "♝", "♞", "♛", "♚", "♟"], ["♖", "♗", "♘", "♕", "♔", "♙"]]
    # # Denne forløkken endrer alle brikkene i temp_board om til den symbolbrikker
    # for i in range(len(temp_board)):
    #     for j in range(len(temp_board[i])):
    #         pice, x = what_pice([i, j])
    #         temp_pice = pice
    #         temp_pice = temp_pice.lower()
    #         if temp_pice == "r":
    #             temp_board[i][j] = pices[x][0]
    #         if temp_pice == "b":
    #             temp_board[i][j] = pices[x][1]
    #         if temp_pice == "h":
    #             temp_board[i][j] = pices[x][2]
    #         if temp_pice == "q":
    #             temp_board[i][j] = pices[x][3]
    #         if temp_pice == "k":
    #             temp_board[i][j] = pices[x][4]
    #         if temp_pice == "p":
    #             temp_board[i][j] = pices[x][5]
    # print(board)

    # Tegner brettet og legger til kordinater på sidene
    string = f"  +=+=+=+=+=+=+=+=+\n"
    for i in range(len(temp_board)):
        string += f"{i+1} "
        for j in range(len(temp_board[i])):
            string += f"|{temp_board[i][j]}"
        string += "|\n"
    string += f"  +=+=+=+=+=+=+=+=+\n"
    string += f"   a b c d e f g h \n"
    print(string)


def is_friendly_fire(players_turn, start_pos, end_pos):
    pice_1, player_1 = what_pice(start_pos)
    pice_2, player_2 = what_pice(end_pos)
    # print(players_turn, pice_1, pice_2, player_1, player_2,
    #       players_turn == player_1 and player_1 == player_2 and pice_2 != " ")
    # Passer på at man kun prøver å flytte sin egen brykke og at det er en findelig brikke på endeposisjonen eller tom:
    return players_turn == player_1 and player_1 == player_2 and pice_1 != " " and pice_2 != " "


def limits(pos):
    # LIMITS
    # must find how far it can go towards the end of the board. So i can stop an out of IndexError. Very useful for bishops
    vertical = len(board)
    horizontal = len(board[0])
    to_left = pos[1]
    to_right = horizontal - pos[1]
    to_top = pos[0]
    to_bot = vertical - pos[0]
    ltrb = [to_left, to_top, to_right, to_bot]
    # Find all the diagonals:
    diagonals = []
    # top left:
    if to_top >= to_left:
        diagonals.append(to_left)
    else:
        diagonals.append(to_top)
    # top right:
    if to_top >= to_right:
        diagonals.append(to_right)
    else:
        diagonals.append(to_top)
    # Bot right:
    if to_bot >= to_right:
        diagonals.append(to_right)
    else:
        diagonals.append(to_bot)
    # Bot left:
    if to_bot >= to_left:
        diagonals.append(to_left)
    else:
        diagonals.append(to_bot)
    return ltrb, diagonals


def is_legal(players_turn, start_pos, end_pos):
    pice_1 = what_pice(start_pos)[0]
    pice_2 = what_pice(end_pos)[0]
    # Passer på at man kun prøver å flytte sin egen brykke og at det er en findelig brikke på endeposisjonen eller tom:
    if is_friendly_fire(players_turn, start_pos, end_pos):
        # print("Friendly fire")
        return [], False
    else:
        pice_1 = pice_1.lower()
        # Skal bruke forløkker til å finne alle lovelige moves en brikke kan gjøre og sette de inn i legal_moves om man finner en pos lik end_pos i listen kan skal den returnere true. Dette kan bli nyttig for å sjekke om kongen er i sjakk senere.
        legal_moves = []
        left_top_right_bot, diagonal_left_top_right_bot = limits(start_pos)
        # print(left_top_right_bot, diagonal_left_top_right_bot)
        # ALL FUNCTIONS FOR PICES:

        def rook_legal_moves():
            all_rook_legal_moves = []
            # Left
            for i in range(start_pos[1]-1, -1, -1):
                if what_pice([start_pos[0], i])[0] == ' ':
                    all_rook_legal_moves.append([start_pos[0], i])
                else:
                    if not is_friendly_fire(players_turn, start_pos, [start_pos[0], i]):
                        all_rook_legal_moves.append([start_pos[0], i])
                    break
            # Top
            for i in range(start_pos[0]-1, -1, -1):
                if what_pice([i, start_pos[1]])[0] == ' ':
                    all_rook_legal_moves.append([i, start_pos[1]])
                else:
                    if not is_friendly_fire(players_turn, start_pos, [i, start_pos[1]]):
                        all_rook_legal_moves.append([i, start_pos[1]])
                    break
            # Right
            for i in range(start_pos[1]+1, len(board[start_pos[0]])):
                if what_pice([start_pos[0], i])[0] == ' ':
                    all_rook_legal_moves.append([start_pos[0], i])
                else:
                    if not is_friendly_fire(players_turn, start_pos, [start_pos[0], i]):
                        all_rook_legal_moves.append([start_pos[0], i])
                    break
            # Bot
            for i in range(start_pos[0]+1, len(board[start_pos[0]])):
                if what_pice([i, start_pos[1]])[0] == ' ':
                    all_rook_legal_moves.append([i, start_pos[1]])
                else:
                    if not is_friendly_fire(players_turn, start_pos, [i, start_pos[1]]):
                        all_rook_legal_moves.append([i, start_pos[1]])
                    break
            return all_rook_legal_moves

        def bishop_legal_moves():
            all_bishop_legal_moves = []
            # TRENGER
            # Finne alle posisjoner som b kan gå
            # For løkker osm sjekker hver posisjon, med grenser funnet i diagonal left-right
            # Er en av feltene den ser på okkupert?
            #   - Hvis ja, er den vennlig eller fiendtlig
            #       - Break for løkker
            # Up- left
            for i in range(1, diagonal_left_top_right_bot[0]+1):
                if what_pice([start_pos[0]-i, start_pos[1]-i])[0] == ' ':
                    all_bishop_legal_moves.append(
                        [start_pos[0]-i, start_pos[1]-i])
                else:
                    if not is_friendly_fire(players_turn, start_pos, [start_pos[0]+i, start_pos[0]-i]):
                        all_bishop_legal_moves.append(
                            [start_pos[0]+i, start_pos[1]-i])
                    break
            # Up-right
            for i in range(1, diagonal_left_top_right_bot[1]+1):
                if what_pice([start_pos[0]-i, start_pos[1]+i])[0] == ' ':
                    all_bishop_legal_moves.append(
                        [start_pos[0]-i, start_pos[1]+i])
                else:
                    if not is_friendly_fire(players_turn, start_pos, [start_pos[0]-i, start_pos[1]+i]):
                        all_bishop_legal_moves.append(
                            [start_pos[0]-i, start_pos[1]+i])
                    break
            # Down-right
            for i in range(1, diagonal_left_top_right_bot[2]+1):
                if what_pice([start_pos[0]+i, start_pos[0]+i])[0] == ' ':
                    all_bishop_legal_moves.append(
                        [start_pos[0]+i, start_pos[1]+i])
                else:
                    if not is_friendly_fire(players_turn, start_pos, [start_pos[0]+i, start_pos[0]+i]):
                        all_bishop_legal_moves.append(
                            [start_pos[0]+i, start_pos[1]+i])
                    break
            # Down-left
            for i in range(1, diagonal_left_top_right_bot[3]+1):
                if what_pice([start_pos[0]+i, start_pos[0]-i])[0] == ' ':
                    all_bishop_legal_moves.append(
                        [start_pos[0]+i, start_pos[1]-i])
                else:
                    if not is_friendly_fire(players_turn, start_pos, [start_pos[0]+i, start_pos[0]+i]):
                        all_bishop_legal_moves.append(
                            [start_pos[0]+i, start_pos[1]-i])
                    break
            return all_bishop_legal_moves
        # Rook. Moves only in horisontal or vertical lines. # this is bad but it all works
        if pice_1 == "r":
            legal_moves.extend(rook_legal_moves())

        if pice_1 == "p":
            # The pond only moves forward one square. But the first move can walk two squars, and it can take at diagonals
            # NB: Man kan gjøre mye her til en funksjon som man påkaller.
            if what_pice([start_pos[0], start_pos[1]])[1] == 0:  # Hvit
                if what_pice([start_pos[0]+1, start_pos[1]])[0] == ' ':
                    legal_moves.append([start_pos[0]+1, start_pos[1]])
                    if what_pice([start_pos[0]+2, start_pos[1]])[0] == ' ' and start_pos[0] == 1:
                        legal_moves.append([start_pos[0]+2, start_pos[1]])
                # else:
                if start_pos[1]-1 >= 0:
                    if not is_friendly_fire(players_turn, start_pos, [start_pos[0]+1, start_pos[1]-1]) and what_pice([start_pos[0]+1, start_pos[1]-1])[0] != " ":
                        legal_moves.append(
                            [start_pos[0]+1, start_pos[1]-1])  # left
                if start_pos[1]+1 < len(board):
                    if not is_friendly_fire(players_turn, start_pos, [start_pos[0]+1, start_pos[1]+1]) and what_pice([start_pos[0]+1, start_pos[1]+1])[0] != " ":
                        legal_moves.append(
                            [start_pos[0]+1, start_pos[1]+1])  # right

            if what_pice([start_pos[0], start_pos[1]])[1] == 1:  # Sort
                if what_pice([start_pos[0]-1, start_pos[1]])[0] == ' ':
                    legal_moves.append([start_pos[0]-1, start_pos[1]])
                    if what_pice([start_pos[0]-2, start_pos[1]])[0] == ' ' and start_pos[0] == 6:
                        legal_moves.append([start_pos[0]-2, start_pos[1]])
                else:
                    # Må bruke to if statments siden begge mulighetene må testes
                    if start_pos[1]-1 >= 0:
                        if not is_friendly_fire(players_turn, start_pos, [start_pos[0]-1, start_pos[1]-1]) and what_pice([start_pos[0]-1, start_pos[1]-1])[0] != " ":
                            legal_moves.append(
                                [start_pos[0]-1, start_pos[1]-1])  # left
                    if start_pos[1]+1 < len(board):
                        if not is_friendly_fire(players_turn, start_pos, [start_pos[0]-1, start_pos[1]+1]) and what_pice([start_pos[0]-1, start_pos[1]+1])[0] != " ":
                            legal_moves.append(
                                [start_pos[0]-1, start_pos[1]+1])  # right

        if pice_1 == "h":
            # Sjekker alle de forskjellige posisjonene hesten kan dra. Det er kun åtte og man trenger ikke å sjekke veien bort til end_pos
            def add_arrays(arr1, arr2):
                return [arr1[0] + arr2[0], arr1[1] + arr2[1]]

            posible_horse_pos = [add_arrays(start_pos, [2, -1]), add_arrays(start_pos, [2, +1]), add_arrays(start_pos, [-2, 1]), add_arrays(
                start_pos, [-2, -1]), add_arrays(start_pos, [1, -2]), add_arrays(start_pos, [-1, -2]), add_arrays(start_pos, [1, 2]), add_arrays(start_pos, [-1, -2])]

            for i in posible_horse_pos:
                # Sjekker om den er utenfor brettet
                if i[0] < 0 or i[0] > len(board) - 1 or i[1] < 0 or i[1] > len(board) - 1:
                    continue
                # Sjekker om det er en vennelig brikke på hver av de mulige stedene, Dette kan bli viktig for check gfunksjonen
                if is_friendly_fire(players_turn, start_pos, i):
                    continue
                legal_moves.append(i)

        if pice_1 == "b":
            legal_moves.extend(bishop_legal_moves())

        if pice_1 == "q":
            # Just check all the values from rook and bishop and add them to the list
            # print(pice_1)
            all_queen_legal_moves = []
            all_queen_legal_moves.extend(bishop_legal_moves())
            all_queen_legal_moves.extend(rook_legal_moves())
            legal_moves.extend(all_queen_legal_moves)

        if pice_1 == "k":
            # sjekke alle 8 posisjonene:
            posible_king_pos = [
                [start_pos[0]-1, start_pos[1]-1], [start_pos[0]-1,
                                                   start_pos[1]], [start_pos[0]-1, start_pos[1]+1],
                [start_pos[0], start_pos[1]-1], [start_pos[0], start_pos[1]+1],
                [start_pos[0]+1, start_pos[1]-1], [start_pos[0]+1,
                                                   start_pos[1]], [start_pos[0]+1, start_pos[1]+1]
            ]
            # Burde sjekke om trekket er is_check == True
            for i in range(len(posible_king_pos)):
                # if what_pice([posible_king_pos[i][0], posible_king_pos[i][1]])[0] == " ":
                if what_pice(posible_king_pos[i])[0] == " ":
                    legal_moves.append(posible_king_pos[i])
                else:
                    if not is_friendly_fire(players_turn, start_pos, posible_king_pos[i]):
                        legal_moves.append(
                            posible_king_pos[i])
    # print(legal_moves)
    # Gjør det mer leselig
    legal_moves_squares = []
    for i in range(len(legal_moves)):
        legal_moves_squares.append(index_to_square(legal_moves[i]))
    # print(legal_moves_squares)
    in_list = end_pos in legal_moves
    # print(in_list)
    return legal_moves, in_list  # , legal_moves_squares


def is_check(players_turn, king_pos):
    # Skal bruke is_legal til å finne om noen brikker på motstanderlaget kan komme seg til kongens posisjon. Må dermed treversjere alle rutene
    # Skal returne boolsk variabel
    for i in range(len(board)):
        for j in range(len(board[i])):
            # print(players_turn, index_to_square([i, j]), king_pos), is_legal(
            #     players_turn, [i, j], king_pos)[1]
            if what_pice([i, j])[0] == " ":
                continue
            if is_legal(players_turn, [i, j], king_pos)[1]:
                return True
    return False


def whos_turn(nr):
    if nr % 2 == 0:
        return 0
    else:
        return 1


def find_king():
    kings_pos = ["", ""]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if what_pice([i, j])[0] == "k":
                kings_pos[0] = [i, j]
            if what_pice([i, j])[0] == "K":
                kings_pos[1] = [i, j]
    loss_index = ""
    for i in range(len(kings_pos)):
        if kings_pos[i] == "":
            loss_index = i
    # print(kings_pos, loss_index)
    return kings_pos, loss_index


def change_pawn_input():
    pice = input("What pice shall the pawn become: (r,h,b,q) or (R,H,B,Q)")
    temp = pice.lower()
    pices = ["r", "h", "b", "q"]
    if temp in pices:
        return pice
    print("Bad input... please write again")
    return change_pawn_input()


def change_pawn():
    pawnes_pos = []
    pawnes_colors = []
    for i in [0, 7]:
        for j in range(len(board)):
            if what_pice([i, j])[0] == "p":
                pawnes_pos.append([i, j])
                pawnes_colors.append(0)
            if what_pice([i, j])[0] == "P":
                pawnes_pos.append([i, j])
                pawnes_colors.append(1)
    # print(pawnes_pos)
    # print(pawnes_colors)

    for i in range(len(pawnes_pos)):
        pice = change_pawn_input()
        if pawnes_colors[i] == 0:
            board[pawnes_pos[i][0]][pawnes_pos[i][1]] = pice.lower()
        else:
            board[pawnes_pos[i][0]][pawnes_pos[i][1]] = pice.upper()
    # trenger å endre brikken til hva den skal bli


def main():
    turn_message = [f"Whites turn!", f"Blacks turn"]
    turn = 0
    game_condtion = True
    while game_condtion:
        show_board()

        # TURN
        players_turn = whos_turn(turn)
        print(turn_message[players_turn])
        print(f"It is turn: {turn}")

        # CHOISE
        player_choise = user_input()
        while what_pice(squar_to_index(player_choise[0]))[1] != players_turn:
            # print(what_pice(squar_to_index(player_choise[0])))
            print(
                f"It is not your turn...  it is {turn_message[players_turn]}")
            player_choise = user_input()

        # print(is_legal(players_turn, squar_to_index(player_choise[0]), squar_to_index(player_choise[1])))
        if is_legal(players_turn, squar_to_index(player_choise[0]), squar_to_index(player_choise[1]))[1]:
            move_pice(squar_to_index(
                player_choise[0]), squar_to_index(player_choise[1]))
            turn += 1
        # Finner ut om det er noen bønder som er på rad 1 eller 8 og endrer dem til hva spilleren ønsker
        change_pawn()
        # Finner ut om man har tapt eller er i sjakk
        kings_pos, loss = find_king()
        print("King pos = ", kings_pos)
        if loss != "":
            break
        # for i in range(len(kings_pos)):
            # print(i, kings_pos, players_turn, whos_turn(players_turn+1))
            # if is_check(whos_turn(turn+1), kings_pos[i]):
            #     print("King in check")

    if loss == 0:
        victor = "White"
    else:
        victor = "Black"
    print(f"{victor} WON!")


main()

# "%%%%%%%%%%%%%%" TESTS:
# show_board:
# show_board()
# print(board[0][1])

# is_check:
# print(is_check(1, squar_to_index("d4")))
# print(is_check(1, squar_to_index("d8")))

# print(squar_to_index("d8"))

# is_legal:
# print(is_legal(0, squar_to_index("h2"), squar_to_index("h4")))
# limits: fungerer
# print(limits(squar_to_index("c2")))

# is_friendly_fire:
# print(is_friendly_fire(0, squar_to_index("a1"), squar_to_index("a2"))) # brude gi: True
# print(is_friendly_fire(0, squar_to_index("a1"), squar_to_index("a3"))) # brude gi: False
# print(is_friendly_fire(0, squar_to_index("a1"), squar_to_index("a8"))) # brude gi: False

# print(is_friendly_fire(1, squar_to_index("a1"), squar_to_index("a2"))) # brude gi: False
# print(is_friendly_fire(1, squar_to_index("a1"), squar_to_index("a3"))) # brude gi: False
# print(is_friendly_fire(1, squar_to_index("a1"), squar_to_index("a8"))) # brude gi: False
# print(is_friendly_fire(1, squar_to_index("b4"), squar_to_index("a4")))  # brude gi: False

# what_pice:
# print(what_pice(squar_to_index("a1")))
# print(what_pice(squar_to_index("a8")))

# move_pice:
# move_pice([0, 0], [2, 0])
# move_pice([0, 0], [0, 1])

# print(squar_to_index("a2"))
# print(user_input())

# Current know bugs:

# The pawns can walk of the map?
