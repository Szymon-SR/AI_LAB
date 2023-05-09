import matplotlib.pyplot as plt

heuristic_values_in_order = []


def plot_game_history():
    # plot the history of heuristic values, allows
    # us to see when the game started to go in favor
    # of one of the players
    plt.style.use("ggplot")
    xs = [i for i in range(len(heuristic_values_in_order))]
    plt.scatter(xs, heuristic_values_in_order)
    plt.title("Values of heuristic over time")
    plt.show()
