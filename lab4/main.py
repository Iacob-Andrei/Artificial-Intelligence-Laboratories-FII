from cmath import inf
from collections import defaultdict

Q_domains = defaultdict(lambda: [])
Q_positions = dict()


def initialize(n, blocked_positions):
    for i in range(1, n + 1):
        Q_domains[i] = [x for x in range(1, n + 1)]
    for block in blocked_positions:
        Q_domains[block[0]].remove(block[1])

    for domain in Q_domains.keys():
        Q_positions[domain] = None
        print(f"{domain}: {Q_domains[domain]}")


def heuristic():
    res = -1
    min_available = inf

    for column in Q_domains:
        current_len = len(Q_domains[column])

        if current_len < min_available and current_len is not 0:
            res = column
            min_available = current_len
            
    return res


def check_available_position(position):  # don't know if we need it
    if position[1] in Q_domains[position[0]]:
        return True

    return False


def is_final():
    return None not in Q_positions.values()


def update_domains(position):
    # Block columns
    for column in Q_domains:
        remove_from_list(column, position[1])

    # Block whole line
    Q_domains[position[0]] = []

    # block principal diagonal, current-down
    key, value = position
    while key <= len(Q_domains) & value <= len(Q_domains):
        remove_from_list(key, value)
        key += 1
        value += 1

    # block principal diagonal, current-up
    key, value = position
    while key >= 1 & value >= 1:
        remove_from_list(key, value)
        key -= 1
        value -= 1

    # block secondary diagonal, current-down
    key, value = position
    while key <= len(Q_domains) & value >= 1:
        remove_from_list(key, value)
        key += 1
        value -= 1

    # block secondary diagonal, current-up
    key, value = position
    while key >= 1 & value <= len(Q_domains):
        remove_from_list(key, value)
        key -= 1
        value += 1


def remove_from_list(key, value):
    if value in Q_domains[key]:
        Q_domains[key].remove(value)


def solve(column):
    if is_final():
        return True

    copy_domains = Q_domains
    copy_positions = Q_positions

    for value in copy_domains[column]:

        Q_positions[column] = value  # put queen no. column in position value
        update_domains((column, value))  # update the domain array

        next_queen = heuristic()
        if solve(next_queen):
            return True

        Q_positions.update(copy_positions)  # no solution found for queen no. column in poz value
        Q_domains.update(copy_domains)      # go back to previews states

    return False


if __name__ == "__main__":
    initialize(4, [(1, 1), (2, 2), (4, 3)])

    if solve(heuristic()):
        print("we have solution")
        print(Q_positions)
    else:
        print("no solution found for given instance.")