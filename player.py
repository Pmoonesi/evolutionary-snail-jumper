import random

import pygame
from variables import global_variables
from nn import NeuralNetwork
import numpy as np

class Player(pygame.sprite.Sprite):
    def __init__(self, game_mode):
        super().__init__()

        # loading images
        player_walk1 = pygame.image.load('Graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('Graphics/Player/player_walk_2.png').convert_alpha()

        # rotating -90 degree and scaling by factor of 0.5
        player_walk1 = pygame.transform.rotozoom(player_walk1, -90, 0.5)
        player_walk2 = pygame.transform.rotozoom(player_walk2, -90, 0.5)

        # flipping vertically
        player_walk1 = pygame.transform.flip(player_walk1, flip_x=False, flip_y=True)
        player_walk2 = pygame.transform.flip(player_walk2, flip_x=False, flip_y=True)

        self.player_walk = [player_walk1, player_walk2]

        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midleft=(177, 656))

        self.player_gravity = 'left'
        self.gravity = 10
        self.game_mode = game_mode
        self.first_time = True

        if self.game_mode == "Neuroevolution":
            self.fitness = 0  # Initial fitness

            layer_sizes = [4, 10, 1]  # TODO (Design your architecture here by changing the values)
            self.nn = NeuralNetwork(layer_sizes)

    def filter_past_obstacles(self, obstacles, player_y):
        filtered = filter(lambda x: x['y'] < player_y, obstacles)
        return list(filtered)

    def get_obstacles_divided(self, obstacles):
        ## left
        left_list = list(filter(lambda i: i['x'] <= 201, obstacles))
        ## middle
        middle_list = list(filter(lambda i: i['x'] > 201 and i['x'] <= 402, obstacles))
        ## right
        right_list = list(filter(lambda i: i['x'] > 402, obstacles))
        
        return [left_list, middle_list, right_list]

    def closest_obstacle(self, obstacles):
        closest = (obstacles[0]['y'] - (-100)) / (640 - (-100)) if len(obstacles) > 0 else 0
        return closest

    def obstacle_count(self, obstacles, total_obstacles):
        count = len(obstacles) / len(total_obstacles)
        return count

    def player_nx(self, player_x):
        return (player_x - 177) / 233

    def obstacle_variance(self, obstacles):
        ## maximum variance where half of obstacles are at -100 and the other half at 640 -> mean = 270
        max_var = (370) ** 2
        ## real variance
        sum = 0
        for o in obstacles:
            sum += o['y']
        mean = sum / len(obstacles)
        sum = 0
        for o in obstacles:
            sum += (o['y'] - mean) ** 2
        var = sum / len(obstacles)
        return var / max_var

    def think(self, screen_width, screen_height, obstacles, player_x, player_y):
        """
        Creates input vector of the neural network and determines the gravity according to neural network's output.

        :param screen_width: Game's screen width which is 604.
        :param screen_height: Game's screen height which is 800.
        :param obstacles: List of obstacles that are above the player. Each entry is a dictionary having 'x' and 'y' of
        the obstacle as the key. The list is sorted based on the obstacle's 'y' point on the screen. Hence, obstacles[0]
        is the first obstacle on the scene. It is also worthwhile noting that 'y' range is in [-100, 656], such that
        -100 means it is off screen (Topmost point) and 656 means in parallel to our player's 'y' point.
        :param player_x: 'x' position of the player
        :param player_y: 'y' position of the player
        """
        # TODO (change player's gravity here by calling self.change_gravity)
        [left_obs, middle_obs, right_obs] = self.get_obstacles_divided(obstacles)
        
        ## closes obstacles
        c_l = self.closest_obstacle(left_obs)
        c_m = self.closest_obstacle(middle_obs)
        c_r = self.closest_obstacle(right_obs)

        ## player x
        p_x = self.player_nx(player_x)

        input = np.array([c_l, c_m, c_r, p_x]).reshape(4, 1)
        output = self.nn.forward(input)

        if output[0] > 0.5:
            self.change_gravity('right')
        else:
            self.change_gravity('left')

    def change_gravity(self, new_gravity):
        """
        Changes the self.player_gravity based on the input parameter.
        :param new_gravity: Either "left" or "right"
        """
        new_gravity = new_gravity.lower()

        if new_gravity != self.player_gravity:
            self.player_gravity = new_gravity
            self.flip_player_horizontally()

    def player_input(self):
        """
        In manual mode: After pressing space from the keyboard toggles player's gravity.
        """
        if global_variables['events']:
            for pygame_event in global_variables['events']:
                if pygame_event.type == pygame.KEYDOWN:
                    if pygame_event.key == pygame.K_SPACE:
                        self.player_gravity = "left" if self.player_gravity == 'right' else 'right'
                        self.flip_player_horizontally()

    def apply_gravity(self):
        if self.player_gravity == 'left':
            self.rect.x -= self.gravity
            if self.rect.left <= 177:
                self.rect.left = 177
        else:
            self.rect.x += self.gravity
            if self.rect.right >= 430:
                self.rect.right = 430

    def animation_state(self):
        """
        Animates the player.
        After each execution, it increases player_index by 0.1. Therefore, after ten execution, it changes the
        player_index and player's frame correspondingly.
        """
        self.player_index += 0.1
        if self.player_index >= len(self.player_walk):
            self.player_index = 0

        self.image = self.player_walk[int(self.player_index)]

    def update(self):
        """
        Updates the player according to the game_mode. If it is "Manual", it listens to the keyboard. Otherwise the
        player changes its location based on `think` method.
        """
        if self.game_mode == "Manual":
            self.player_input()
        if self.game_mode == "Neuroevolution":
            obstacles = []
            for obstacle in global_variables['obstacle_groups']:
                if obstacle.rect.y <= 656:
                    obstacles.append({'x': obstacle.rect.x, 'y': obstacle.rect.y})

            self.think(global_variables['screen_width'],
                       global_variables['screen_height'],
                       obstacles, self.rect.x, self.rect.y)

        self.apply_gravity()
        self.animation_state()

    def flip_player_horizontally(self):
        """
        Flips horizontally to have a better graphic after each jump.
        """
        for i, player_surface in enumerate(self.player_walk):
            self.player_walk[i] = pygame.transform.flip(player_surface, flip_x=True, flip_y=False)
