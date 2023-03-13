earns = list()
players = list()
moves = list()
no_lines = 0
no_columns = 0


def initialize():
    global no_lines, no_columns
    f = open("input.txt", "r")
    input_file = f.read().split('\n')

    for line in input_file[:2]:
        players.append(line.split(' ')[0])
        moves.append(line.split(' ')[1:])

    for line in input_file[2:]:
        arr_line = []
        for pair in line.split(' '):
            x1, x2 = pair.split('/')
            arr_line.append((int(x1), int(x2)))
        earns.append(arr_line)
    f.close()
    no_lines = len(moves[0])
    no_columns = len(moves)


def print_matrix():
    print(players)
    print(moves[0])

    for line in range(no_lines):
        print(moves[1][line], end=' ')
        for column in range(no_columns):
            print(earns[line][column], end=' ')
        print()


def nash_equilibrium():
    best_column = dict()
    best_line = dict()

    for i in range(no_columns):  # columns have 1st poz
        maximum = -1
        poz = []
        for j in range(no_lines):
            if earns[j][i][0] > maximum:
                maximum = earns[j][i][0]
                poz = [j]
            elif earns[j][i][0] == maximum:
                poz.append(j)
        for position in poz:
            best_column[(position, i)] = maximum

    for j in range(no_lines):  # lines have 2nd poz
        maximum = -1
        poz = []
        for i in range(no_columns):
            if earns[i][j][1] > maximum:
                maximum = earns[i][j][1]
                poz = [i]
            elif earns[i][j][1] == maximum:
                poz.append(i)
        for position in poz:
            best_line[(j, position)] = maximum

    print(f"columns: {best_column}")
    print(f"lines: {best_line}")

    print('\nEquilibrium in next line/columns:')
    for pair in best_column:
        if pair in best_line:
            print(f"{pair}: {best_column[pair]}/{best_line[pair]}")


def print_dominant_strategy():
    for fixed_line in range(no_lines):

        for other_line in range(no_lines):
            if fixed_line == other_line:  # We don't compare ourselves
                continue

            is_dominant = True

            for column in range(no_columns):
                if earns[fixed_line][column][0] <= earns[other_line][column][0]:
                    is_dominant = False
                    break

            if is_dominant:
                print(f"The line #{fixed_line + 1} is dominated by line #{other_line + 1} =>")
                print(f"{earns[fixed_line]}\n{earns[other_line]}")

    for fixed_column in range(no_columns):

        for other_column in range(no_columns):
            if fixed_column == other_column:  # We don't compare ourselves
                continue

            is_dominant = True

            for line in range(no_lines):
                if earns[fixed_column][line][1] <= earns[other_column][line][1]:
                    is_dominant = False
                    break

            if is_dominant:
                print(f"The column #{fixed_column + 1} is dominated by column #{other_column + 1} =>")
                print(f"{earns[fixed_column]}\n{earns[other_column]}")


if __name__ == '__main__':
    initialize()
    # print_matrix()
    # print_dominant_strategy()
    nash_equilibrium()
