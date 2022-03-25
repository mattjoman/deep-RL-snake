from single_player import single_player
from train_ai import train_ai

def main():

    rows = 20
    columns = 20
    square_size = 16

    print()
    print("Blank: Single Player")
    print("1: Train an AI")
    print()
    mode = input("Enter a number to choose the game mode: ")

    if mode == '':
        while True:
            single_player(rows, columns, square_size)

    elif mode == '1':
        train_ai(rows=10, columns=10, square_size=square_size)


if __name__ == "__main__":
    main()
