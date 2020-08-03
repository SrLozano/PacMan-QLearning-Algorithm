# Implementation of Q-Learning Algorithm for playing Pac-Man
This project is based on the Berkeley CS188 Intro to AI Pac-Man and consist on a solution that implements the Q-Learning Algorithm.

## Authors 🧑‍💻
This Machine Learning project was co-author by **Saray García de la Rosa Jimenez** and **Mario Lozano Cortés**. Computer Science and Engineering students at *Carlos III University of Madrid*.

## Requirements 📦
- The code needs to be run with Python2 🐍 In case you need to install it you can use:
 ```bash
sudo apt install python2
```
-  Tkinter for Python ⚙️  In case you need to install it you can use:
 ```bash
sudo apt-get install python-tk
```

## Run it 🐍⚙️

The training scripts are run by:
```bash
python2 script.py
```

Meanwhile, for running the Q-Learning agent already trained:
```bash
python2 busters.py -k 1 -l labAA1 -p QLearningAgent
```
where:
- k: Number of ghost
- l: Layout file
- p: The agent type 

## The logic behind 🧠 🤖

The [project website](http://ai.berkeley.edu/project_overview.html) contains part of the initial code that was later modified by the professors at Carlos III University. 

After the iterative and incremental process followed in this practice, we build the state, Q-table and reinforcement function described below.

**State**:
|It gets closer/further by moving North| It gets closer/further by moving East| It gets closer/further by moving South| It gets closer/further by moving West|
|--|--|--|--|

We store in a list of 4 positions a 0 or a 1 depending on whether by choosing the corresponding action we get closer or further away from our target. The objective is to be able to establish a target for the agent and not to have indecision about which one he should go for. That is to say, to generate a state that provides instantaneous information for *Pac-Man* without the need to look at the future, that determines what action to take. We will help to know which direction to take calculating which is the one that contributes more to the score by means of the *distancer* tool. This tool will give us back the distance to the target taking into account that there are obstacles in the way, that is, it tells us the length of the optimal path to reach the ghost.

Initially, we will take into account that there is food on the map, so the target can be either the nearest food point or the nearest ghost. We will establish which objective we have closer and from this, we will calculate for each of the possible actions (north, east, south and west) if when taking it approaches (the position of the state will be to 1) or if it moves away (the position of the state will be to 0). In the case that there is no food on the map it will focus only on the nearest ghost.

**Reinforcement function**
- Eating a ghost. This is the most important goal of the game as it allows Pac-Man to win, so it provides the highest reinforcement, this will be ***100***.

- Eating a food point. It is not the final objective but it helps to increase the score, so it provides a reinforcement of ***50***.

- Getting closer to the target. To make the agent aware that it is moving in the right direction, a reinforcement (less than 1) will be provided as it approaches the target. The closer it gets, the closer it will be to 1. ***1/Distance to target.*** 

- Moving away from the target. If it moves away from the target it will be sanctioned. ***-1/Distance to target.***

**Parámetros**.

- Alpha **α**. Tasa de aprendizaje, representa como de agresivo es el aprendizaje que realiza.

- Epsilon **ε**. Probabilidad de que el movimiento del agente sea aleatorio y no basado en los valores de la tabla q.

- Factor de descuento **γ**. Ayuda a dar más importancia a las acciones más próximas al final de la ejecución.

## The Q-Learning Algorithm 🧭

More information about the algorithm used can be found [here](https://en.wikipedia.org/wiki/Q-learning).