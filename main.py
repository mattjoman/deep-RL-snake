def main():

    rows = 60
    columns = 60
    square_size = 12

    print()
    print("Blank: Single Player")
    print()
    mode = input("Enter a number to choose the game mode: ")

    if mode == '':
        import single_player as sp
        sp.run(rows, columns, square_size)


if __name__ == "__main__":
    main()
