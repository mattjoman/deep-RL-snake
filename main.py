def main():

    rows = 20
    columns = 20
    square_size = 12

    print()
    print("Blank: Single Player")
    print("1: Train an AI")
    print()
    mode = input("Enter a number to choose the game mode: ")

    if mode == '':
        import single_player as sp
        while True:
            sp.run(rows, columns, square_size)

    elif mode == '1':
        import train_ai as ta
        ta.run(rows, columns, square_size)


if __name__ == "__main__":
    main()
