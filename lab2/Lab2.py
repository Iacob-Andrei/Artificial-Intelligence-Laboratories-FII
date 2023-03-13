# 3, 4, 5 de prezentat la Laboratorul 3
import queue
from collections import deque
import math

# This function is used to initialize the 
# dictionary elements with a default value.
from collections import defaultdict

from numpy import equal

m = n = k = 0  # The number of liters we want at the end


def initialize():
    return 0, 0


def is_final(state):
    if state[0] == k or state[1] == k:
        return True

    return False


def is_valid_state(state):
    if 0 <= state[0] <= m and 0 <= state[1] <= n:
        return True

    return False


def fill(state, poz):
    if poz == 0:
        return m, state[1]
    else:
        return state[0], n


def empty(state, poz):
    if poz == 0:
        return 0, state[1]
    else:
        return state[0], 0


def transfer(state, poz):  # transfer a -> b
    if poz == 0:
        a = state[0]
        b = state[1]
        limit_b = n
    else:
        a = state[1]
        b = state[0]
        limit_b = m

    max_to_add = limit_b - b
    if a >= max_to_add:
        a -= max_to_add
        b += max_to_add
    else:
        b += a
        a = 0

    if limit_b == n:  # needed to return the tuple in correct form
        return a, b
    else:
        return b, a


def heuristic(state):
    return abs(k - state[0]) * abs(k - state[1])


def print_path(path, state):
    for pair in path:
        if pair[0] == state:
            print_path(path, pair[1])
            print(pair[0])
            break


def bfs(initial_state):
    visited = set()
    path = [(initial_state, -1)]  # contains tuple (state, parent_state)

    to_visit = deque()
    to_visit.append(initial_state)

    while len(to_visit) > 0:
        state = to_visit.popleft()

        if (state[0], state[1]) in visited:  # check if was already visited
            continue

        if not is_valid_state(state):  # check if valid state
            continue

        if is_final(state):
            print_path(path, state)
            return state

        # start transitioning
        # fill one jar at a time
        new_state = fill(state, 0)
        to_visit.append(new_state)
        path.append((new_state, state))

        new_state = fill(state, 1)
        to_visit.append(new_state)
        path.append((new_state, state))

        # empty one jar at a time
        new_state = empty(state, 0)
        to_visit.append(new_state)
        path.append((new_state, state))

        new_state = empty(state, 1)
        to_visit.append(new_state)
        path.append((new_state, state))

        # try and transfer as much water from one jar to another
        new_state = transfer(state, 0)
        to_visit.append(new_state)
        path.append((new_state, state))

        new_state = transfer(state, 1)
        to_visit.append(new_state)
        path.append((new_state, state))

        visited.add((state[0], state[1]))

    print("no solution found!")


def backtracking(state):
    # Checks for our goal and 
    # returns true if achieved.
    if is_final(state):
        print(state)
        return True

    # Checks if we have already visited the
    # combination or not. If not, then it proceeds further.
    if visited[state] == False:
        print(state)

        # Changes the boolean value of
        # the combination as it is visited. 
        visited[state] = True

        # Check for all the 6 possibilities and 
        # see if a solution is found in any one of them.
        return (backtracking(fill(state, 0)) or
                backtracking(fill(state, 1)) or
                backtracking(empty(state, 0)) or
                backtracking(empty(state, 1)) or
                backtracking(transfer(state, 0)) or
                backtracking(transfer(state, 1)))
    else:
        return False


def print_for_a_star(came_from, current):
    while current != (0, 0):
        print(current)
        current = came_from[current]


def a_star(state):
    frontier = queue.PriorityQueue()
    frontier.put((0, state))
    came_from = dict()
    came_from[state] = None
    cost_so_far = dict()        # also saves the visited nodes
    cost_so_far[state] = 0

    while not frontier.empty():
        current = frontier.get()

        if is_final(state):
            print_for_a_star(came_from, current)
            return True

        for new_state in generate_all_states(state):
            new_cost = cost_so_far[current] + 1
            if new_state not in cost_so_far or new_cost < cost_so_far[new_state]:
                cost_so_far[new_state] = new_cost
                priority = new_cost + heuristic(new_state)
                frontier.put((priority, new_state))
                came_from[new_state] = current


def generate_all_states(state):
    return [fill(state, 0),
            fill(state, 1),
            empty(state, 0),
            empty(state, 1),
            transfer(state, 0),
            transfer(state, 1)]

# Algorithm for Simple Hill climbing :  

# Evaluate the initial state. If it is a goal state then stop and return success. Otherwise, make the initial state as the current state. 
# Loop until the solution state is found or there are no new operators present which can be applied to the current state. 
# Select a state that has not been yet applied to the current state and apply it to produce a new state. 
# Perform these to evaluate the new state.
# If the current state is a goal state, then stop and return success. 
# If it is better than the current state, then make it the current state and proceed further. 
# If it is not better than the current state, then continue in the loop until a solution is found. 
# Exit from the function.



# Initialize dictionary with
# default value as false.
visited = defaultdict(lambda: [])
path = []


def hillclimbing(state):
    if state not in path: # We check this because heuristic compare greater or equal, not just equal
        path.append(state)

    if is_final(state):
        print(path)
        return True

    current_state = state

    for state in generate_all_states(current_state):
        if state not in visited[current_state]:
                
            visited[current_state].append(state)
            
            if heuristic(state) <= heuristic(current_state):
                if (hillclimbing(state) == True): # No more iterations, we already have the answer
                    return True

    return False


def check_if_solution_exists():
    if k > m or k > n:
        return False

    if k % math.gcd(m, n) != 0:
        return False

    return True


def menu():
    initial_state = initialize()

    print("\n=== MENU ===\n")
    print("1. BFS")
    print("2. Backtracking")
    print("3. A*")
    print("4. Hill Climbing")
    print("============")

    option = int(input("Enter your choice: "))

    if option == 1:
        bfs(initial_state)
    elif option == 2:
        backtracking(initial_state)
    elif option == 3:
        a_star(initial_state)
    elif option == 4:
        hillclimbing(initial_state)


def main():
    global m, n, k

    m = int(input("Enter value for m: "))
    n = int(input("Enter value for n: "))
    k = int(input("Enter value for k: "))

    if not check_if_solution_exists():
        print("No solution for problem instance.")
        return

    menu()


if __name__ == "__main__":
    main()
