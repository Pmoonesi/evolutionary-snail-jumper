# evolutionary-snail-jumper
This is the third project for the course Computational Intelligence - Spring 2022, Dr. Ebadzadeh

**Neuroevolution game assignment.**  
**Spring 2022 - Computer Intelligence.**  

This game has been developed as an assignment for students at Amirkabir University of Technology to apply neuroevolution using a simple game.  

![Snail Jumber](SnailJumper.png)

## introduction
In this game, we use simple fully connected neural networks to decide the actions for a player. But, instead of backpropagation, we use evolutionary algorithms to find the weights for better players' neural networks.

## structure
There are six python files in total, three of which we need to complete. their names are nn.py, player.py and evolution.py. other three python files are for the game itself and we need not to worry about them.

    .
    ├── ...
    ├── evolution.py                  
    ├── game.py
    ├── nn.py
    ├── player.py
    ├── plot.py
    └── variables.py

### nn.py
In this file we first initialize a variable sized neural network and the activation function for it. then we define the feedforward function for the neural network.

### player.py
First we have to decide the neural network architecture for our player. after that, we have to define the `think` functionality for our player. think of it this way: our player is a normal human being and he sees the screen, the position of its agent and the obstacles. then he has to decide. so in the think function, we have to extract as much features as we mean for our network to pay attention to and then feed them to the neural network. finally, based on the outcome of the feedforward, we decide to jump/hit the space bar as if we were a human player.

### evolution.py
We have to implement two main functionalities in this file.

First, we have to implement how we chose the survivors based on their fitness. there are many ways to do this but, we were asked to implement the following: top k, roulette wheel, sus and q-tournament. this is done in `next_population_selection` function. keep in mind that we are using the $(\mu + \lambda)$ strategy.

Second, we have to implement how we create the next generation players. for parent selection, we tried a few methods, the one we chose to go with is to select all players for the first parent and use q-tournament for the second parent. for the crossover, we went with the whole arithmetic crossover. for the mutation, we went with the gaussian mutation. this is done in `generate_new_population` function.
