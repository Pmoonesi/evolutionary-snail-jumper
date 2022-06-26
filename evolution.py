import copy

from player import Player
import numpy as np

class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"
        self.sigma = 1

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

    def get_top_k(self, players, k):
        for i in range(k):
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
        return players[: k]

    def get_fitness_prefix_sum(self, players):
        prefix_fitness = [players[0].fitness]
        for i in range(1, len(players)):
            new_fitness_sum = prefix_fitness[-1] + players[i].fitness
            prefix_fitness.append(new_fitness_sum)
        total_fitness = prefix_fitness[-1]
        return [f / total_fitness for f in prefix_fitness]

    def get_roulette_wheel(self, players, num_players, prefix_fitness):
        selected_players = []
        for i in range(num_players):
            random_number = np.random.uniform()
            index = self.binary_find(prefix_fitness, random_number, 0, len(prefix_fitness))
            selected_players.append(players[index])
        return selected_players

    def get_sus(self, players, num_players, prefix_fitness):
        selected_players = []
        interval = 1 / num_players
        random_var = np.random.uniform(0, interval)
        index = 0
        while random_var < 1:
            while random_var > prefix_fitness[index]:
                index += 1
            selected_players.append(players[index])
            random_var += interval
        return selected_players

    def get_q_tournament(self, players, num_players, Q):
        selected_players = []
        for _ in range(num_players):
            max_index = -1
            max_fitness = -float('inf')
            for __ in range(Q):
                index = int(np.random.uniform() * num_players)
                if players[index].fitness > max_fitness:
                    max_fitness = players[index].fitness
                    max_index = index
            selected_players.append(players[max_index])
        return selected_players

    def get_selection_pressure(self, players):
        max_fitness = -float('inf')
        total_fitness = 0
        for player in players:
            if player.fitness > max_fitness:
                max_fitness = player.fitness
            total_fitness += player.fitness
        return max_fitness / total_fitness

    def get_statistics(self, players):
        min_fitness = float('inf')
        max_fitness = -float('inf')
        sum_fitness = 0
        for player in players:
            f = player.fitness
            sum_fitness += f
            if f < min_fitness:
                min_fitness = f
            if f > max_fitness: 
                max_fitness = f
        avg_fitness = sum_fitness / len(players)
        return (min_fitness, avg_fitness, max_fitness) 

    def save_to_file(self, min, avg, max):
        with open('statistics.txt', 'a+') as f:
            output = "{}-{:.2f}-{}\n".format(min, avg, max)
            f.write(output)

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        # TODO (Implement top-k algorithm here)
        # next_gen_players = self.get_top_k(players, num_players)

        # TODO (Additional: Implement roulette wheel here)
        # # create chance array
        # prefix_fitness = self.get_fitness_prefix_sum(players)
        # # generate num_players uniform random numbers and select next generation
        # next_gen_players = self.get_roulette_wheel(players, num_players, prefix_fitness)

        # TODO (Additional: Implement SUS here)
        ## create chance array
        prefix_fitness = self.get_fitness_prefix_sum(players)
        next_gen_players = self.get_sus(players, num_players, prefix_fitness)

        # TODO (Additional: Implement Q-tournament here)
        # ## select pressure calculations
        # SP = self.get_selection_pressure(players)
        # Q = int(SP * num_players - 1) + 1

        # ## select next gen
        # next_gen_players = self.get_q_tournament(players, num_players, Q)

        # TODO (Additional: Learning curve)
        min, avg, max = self.get_statistics(next_gen_players)
        self.save_to_file(min, avg, max)
        return next_gen_players

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
            ## select parents

            # TODO select all of the generation as parents
            # parents1 = prev_players
            # parents2 = prev_players[-1::-1]

            # TODO select parents with roulette wheel
            # prefix_fitness = self.get_fitness_prefix_sum(prev_players)
            # parents1 = prev_players
            # parents2 = self.get_roulette_wheel(prev_players, num_players, prefix_fitness)

            # TODO select paretns with SUS
            # prefix_fitness = self.get_fitness_prefix_sum(prev_players)
            # parents1 = prev_players
            # parents2 = self.get_sus(prev_players, num_players, prefix_fitness)

            # TODO select parents with Q-tournament
            SP = self.get_selection_pressure(prev_players)
            Q = int(SP * num_players - 1) + 1
            parents1 = prev_players
            parents2 = self.get_q_tournament(prev_players, num_players, Q)

            ## crossover
            Pc = 0.4
            children = []
            alpha = 0.3
            assert len(parents1) == len(parents2)
            for i in range(len(parents1)):
                random_var = np.random.random()
                parent1, parent2 = parents1[i], parents2[i]
                child1 = self.clone_player(parent1)
                child2 = self.clone_player(parent2)
                if random_var <= Pc:
                    for l in range(len(parent1.nn.weights)):
                        weight1 = (1 - alpha) * parent1.nn.weights[l] + alpha * parent2.nn.weights[l]
                        weight2 = alpha * parent1.nn.weights[l] + (1 - alpha) * parent2.nn.weights[l]
                        bias1 = (1 - alpha) * parent1.nn.biases[l] + alpha * parent2.nn.biases[l]
                        bias2 = alpha * parent1.nn.biases[l] + (1 - alpha) * parent2.nn.biases[l]
                        child1.nn.weights[l], child1.nn.biases[l] = weight1, bias1
                        child2.nn.weights[l], child2.nn.biases[l] = weight2, bias2
                children.append(child1)
                children.append(child2)

            ## mutation
            ## update sigma
            taw = 0.1
            self.sigma = self.sigma * np.exp(taw * np.random.normal(0, 1))

            ## mutate
            for i in range(len(children)):
                child = children[i]
                for l in range(len(child.nn.weights)):
                    new_weight = child.nn.weights[l] + self.sigma * np.random.normal(0, 1, child.nn.weights[l].shape)
                    child.nn.weights[l] = new_weight
                    new_bias = child.nn.biases[l] + self.sigma * np.random.normal(0, 1, child.nn.biases[l].shape)
                    child.nn.biases[l] = new_bias

            # new_players = prev_players  # DELETE THIS AFTER YOUR IMPLEMENTATION
            new_players = prev_players + children
            return new_players

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player
