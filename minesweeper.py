# Constants to define the size of the game board
import random
ROWS = 8
COLS = 8
MINES = 10

# A 2D array to represent the game board
board = []

# An array to keep track of the positions of mines on the board
mines = []

# A 2D array to represent the fog of war
fog = [['#' for _ in range(COLS)] for _ in range(ROWS)]

# Initialize the board, state, and place mines randomly
for row in range(ROWS):
    board.append([0] * COLS)

i = 0
while i < MINES:
    row = random.randint(0, ROWS - 1)
    col = random.randint(0, COLS - 1)
    if board[row][col] != "*":
        board[row][col] = "*"
        mines.append([row, col])
        i += 1

# Function to count the number of mines around a cell


def countMines(row, col):
    count = 0
    for r in range(max(0, row - 1), min(row + 2, ROWS)):
        for c in range(max(0, col - 1), min(col + 2, COLS)):
            if board[r][c] == "*":
                count += 1
    return count


# Populate the board with the number of mines around each cell
for mine in mines:
    row = mine[0]
    col = mine[1]
    for r in range(max(0, row - 1), min(row + 2, ROWS)):
        for c in range(max(0, col - 1), min(col + 2, COLS)):
            if board[r][c] != "*":
                board[r][c] = str(countMines(r, c))

# Function to display the game board in the console


def displayBoard():
    print(" " + " ".join(str(i) for i in range(COLS)))
    for row in range(ROWS):
        print(str(row) + " " + " ".join(str(i) for i in fog[row]))

# Function to reveal a cell


def revealCell(row, col):
    # If the selected cell is out of the board boundaries, ignore it
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return True

    # If the selected cell is a mine, game over
    if board[row][col] == "*":
        fog[row][col] = "*"
        return False

    # If the selected cell was already revealed, ignore it
    if fog[row][col] != "#":
        return True

    # Get the count of mines around the cell
    count = countMines(row, col)

    # If the cell has no surrounding mines, reveal all its surrounding cells
    if count == 0:
        fog[row][col] = ' '
        for r in range(max(0, row - 1), min(row + 2, ROWS)):
            for c in range(max(0, col - 1), min(col + 2, COLS)):
                revealCell(r, c)
    else:
        # Otherwise, just reveal the cell
        fog[row][col] = str(count)

    return True

# Function to reveal a cell from user input


def reveal():
    while True:
        try:
            x = int(input("Enter the row number (0-based index): "))
            y = int(input("Enter the column number (0-based index): "))

            if x < 0 or x >= ROWS or y < 0 or y >= COLS:
                print(
                    f"Invalid input. Please enter numbers between 0 and {ROWS-1} for row and between 0 and {COLS-1} for column.")
                continue

            if board[x][y] == "*":
                print("You lost!")
                return
            revealCell(x, y)

            # Check if there are no more spaces to reveal (besides bombs)
            if all(val != '#' for row in fog for val in row):
                print("You win!")
                return

            displayBoard()

        except ValueError:
            print("Invalid input. Please enter a valid number.")


# Call the displayBoard function to display the initial state of the board
displayBoard()

# Call the reveal function to start the game
reveal()
