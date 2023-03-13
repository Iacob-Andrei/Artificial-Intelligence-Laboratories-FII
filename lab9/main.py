import numpy as np

Q = np.zeros((48, 4))

agent_start = (3, 0)
final_position = (3, 11)

general_reward = -1
bad_reward = -100
bad_positions = [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10)]
actions = ["left", "right", "up", "down"]
epsilon = 0.2


def next_state(agent_state: tuple, a: str) -> tuple:
    if agent_state[1] == 0 and a == "left":
        # print("impossible to go left")
        return agent_state

    if agent_state[1] == 11 and a == "right":
        # print("impossible to go right")
        return agent_state

    if agent_state[0] == 0 and a == "up":
        # print("impossible to go up")
        return agent_state

    if agent_state[0] == 3 and a == "down":
        # print("impossible to go down")
        return agent_state

    if a == "left":
        agent_state = (agent_state[0], agent_state[1] - 1)
    elif a == "right":
        agent_state = (agent_state[0], agent_state[1] + 1)
    elif a == "up":
        agent_state = (agent_state[0] - 1, agent_state[1])
    else:
        agent_state = (agent_state[0] + 1, agent_state[1])

    return agent_state


def epsilon_greedy(q, state):
    if np.random.random() < epsilon:
        # choose a random action
        return np.random.choice(actions)
    else:
        # choose the action with the highest Q-value
        return actions[np.argmax(q[state[0] * 12 + state[1]])]


def show_policy(q):
    policy = np.array([np.argmax(q[key]) for key in range(48)]).reshape((4, 12))
    for index, action in enumerate(actions):
        print(action, ':', index, end='   ')
    print('\n', policy)


def q_learning(q, episodes, gamma, learning_rate):
    global epsilon
    for index in range(episodes):
        state = agent_start

        while state != final_position:
            action = epsilon_greedy(q, state)
            epsilon = epsilon - 0.001
            next_position = next_state(state, action)

            if next_position in bad_positions:
                reward = bad_reward
                next_position = agent_start
            else:
                reward = general_reward

            q[state[0] * 12 + state[1]][actions.index(action)] = \
                q[state[0] * 12 + state[1]][actions.index(action)] + \
                learning_rate * (reward + gamma * max(q[next_position[0] * 12 + next_position[1]]) -
                                 q[state[0] * 12 + state[1]][actions.index(action)])
            state = next_position

    # print(q)
    show_policy(q)


q_learning(Q, 1000, 0.99, 0.1)
