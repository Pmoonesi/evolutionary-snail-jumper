import copy

from player import Player
import numpy as np

class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"

    def binary_find(self, array, x, start, end):
        if end <= start:
            return start
        mid = int((start + end)/2)
        if mid == 0:
            return 0
        if x >= array[mid-1] and x < array[mid]:
            return mid
        elif array[mid] <= x:
            return self.binary_find(array, x, mid + 1, end)
        else:
            return self.binary_find(array, x, start, mid - 1)

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        # TODO (Implement top-k algorithm here)
        for i in range(num_players):
            max = -float('inf')
            max_index = -1
            for j in range(i, len(players)):
                player = players[j]
                if player.fitness > max:
                    max = player.fitness
                    max_index = j
            temp = players[i]
            players[i] = players[max_index]
            players[max_index] = temp
        return players[: num_players]

        ## create chance array
        # prefix_fitness = [players[0].fitness]
        # for i in range(1, len(players)):
        #     new_fitness_sum = prefix_fitness[-1] + players[i].fitness
        #     prefix_fitness.append(new_fitness_sum)
        # total_fitness = prefix_fitness[-1]
        # prefix_fitness = [f / total_fitness for f in prefix_fitness]

        # TODO (Additional: Implement roulette wheel here)
        ## generate num_players uniform random numbers and select next generation
        # selected_players = []
        # for i in range(num_players):
        #     random_number = np.random.uniform()
        #     index = self.binary_find(prefix_fitness, random_number, 0, len(prefix_fitness))
        #     selected_players.append(players[index])
        # return selected_players

        # TODO (Additional: Implement SUS here)
        # selected_players = []
        # interval = 1 / num_players
        # random_var = np.random.uniform(0, interval)
        # index = 0
        # while random_var < 1:
        #     while random_var > prefix_fitness[index]:
        #         index += 1
        #     selected_players.append(players[index])
        #     random_var += interval
        # return selected_players

        # TODO (Additional: Learning curve)
        return players[: num_players]

    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """
        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:
            # TODO ( Parent selection and child generation )
            new_players = prev_players  # DELETE THIS AFTER YOUR IMPLEMENTATION
            return new_players

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player
