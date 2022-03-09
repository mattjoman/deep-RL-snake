def main():
    print("ok")

    rows = 100
    columns = 100
    square_size = 8
    print()
    print("Blank: Single Player")
    print()
    mode = input("Enter a number to choose the game mode: ")

    if mode == '':
        print("YES")
        import single_player as sp
        sp.run(rows, columns, square_size)


if __name__ == "__main__":
    main()
