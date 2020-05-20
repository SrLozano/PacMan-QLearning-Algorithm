# bustersAgents.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# python busters.py
# n GAMES Numero de juegos
# -l LAYOUT FILE El tablero del juego
# -p TYPE El tipo de agente Pac-Man. BustersKeyboardAgent | BasicAgentAA
# -g TYPE El tipo de agente de fantasma. RandomGhost 
# -k NUMGHOSTS El numero maximo de fantasmas. 
# -t Tiempo de delay entre frames.


import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
# from wekaI import Weka
import inference
import busters
import copy

fixed_action = ""


class NullGraphics:
    "Placeholder for graphics"
    def initialize(self, state, isBlue = False):
        pass
    def update(self, state):
        pass
    def pause(self):
        pass
    def draw(self, state):
        pass
    def updateDistributions(self, dist):
        pass
    def finish(self):
        pass

class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """
    aux1 = ""
    aux2 = ""
    aux3 = ""

    def registerInitialState(self, gameState):
        self.countActions = 0

    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs

    def printLineData(self, gameState):
        fileOpen = open('all_data_pacman.arff', 'a')
        
        state = ""
        # Posicion del Pacman X
        state = state + str(gameState.getPacmanPosition()[0]) + ", "
        # Posicion del Pacman Y 
        state = state + str(gameState.getPacmanPosition()[1]) + ", "
        # Ancho del mapa
        state = state + str(gameState.data.layout.width) + ", "
        # Alto del mapa
        state = state + str(gameState.data.layout.height) + ", "
        # Acciones legales de pacman en la posicion actual
        legalActions = gameState.getLegalPacmanActions()
        for i in ["North", "South", "East", "West", "Stop"]:
            if i in legalActions:
                state = state + "1, " #Cuando puede ir a esa direccion ponemos un 1
            else:
                state = state + "0, " #Cuando no puede ir a esa direccion ponemos un 0   
        # Direccion de pacman
        state = state + str(gameState.data.agentStates[0].getDirection())+ ", "
        # Numero de fantasmas
        state = state + str(gameState.getNumAgents() - 1)+ ", "
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        livingGhost = gameState.getLivingGhosts()
        NumberLivingGhost = 0
        for i in livingGhost:
            if i:
                NumberLivingGhost = NumberLivingGhost + 1
        state = state + str(NumberLivingGhost) + ", "
        # Posicion de los fantasmas
        numberGhosts = gameState.getNumAgents() - 1
        GhostPositionsArray = gameState.getGhostPositions()
        for i in range (0, 4):
            if i < numberGhosts:
                state = state + str(GhostPositionsArray[i][0]) + ", "
                state = state + str(GhostPositionsArray[i][1]) + ", "
            else: 
                state = state + "-1, "
                state = state + "-1, "
        # Direciones de los fantasmas
        GhostDirectionsArray = [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        for i in range (0, 4):
            if i < numberGhosts:
                state = state + str(GhostDirectionsArray[i]) + ", "
            else:
                state = state + "Stop, "
        # Distancia de manhattan a los fantasmas
        GhostDistances = gameState.data.ghostDistances
        for i in range (0, 4):
            if i < numberGhosts:
                if GhostDistances[i] == None:
                    state = state + "-1, "
                else:
                    state = state + str(GhostDistances[i]) + ", "
            else:
                state = state + "-1, "   

        # Puntos de comida restantes
        state = state + str(gameState.getNumFood())+ ", "
        # Distancia de manhattan a la comida mas cercana
        closestFood = gameState.getDistanceNearestFood()
        if closestFood == None:
            state = state + "-1, "  
        else:    
            state = state + str(closestFood)+ ", "
        #Siguiente accion
        state = state + str(BustersAgent.getAction(self, gameState)) + ", "
         # Puntuacion
        state = state + str(gameState.getScore())+ ", "
        if self.countActions == 0:
            self.aux1 = state
            #print str(self.aux1)
        elif self.countActions == 1:
            self.aux2 = state
            self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
        elif self.countActions == 2:
            self.aux3 = state
            self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
            self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
        else:
            if self.countActions%3 == 0:
                self.aux1 = self.aux1 + str(gameState.getScore()) + "\n"
                self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
                self.aux3 = self.aux3 + str(gameState.getScore()) + ", "
                fileOpen.write(self.aux1)
                self.aux1 = ""
                self.aux1 = self.aux1 + state
            elif self.countActions%3 == 1:
                self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
                self.aux2 = self.aux2 + str(gameState.getScore()) + "\n"
                self.aux3 = self.aux3 + str(gameState.getScore()) + ", "
                fileOpen.write(self.aux2)
                self.aux2 = ""
                self.aux2 = self.aux2 + state
            elif self.countActions%3 == 2:
                self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
                self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
                self.aux3 = self.aux3 + str(gameState.getScore()) + "\n"
                fileOpen.write(self.aux3)
                self.aux3 = ""
                self.aux3 = self.aux3 + state

        fileOpen.close()
        self.countActions = self.countActions + 1

class BustersAgent:
    "An agent that tracks and displays its beliefs about ghost positions."
    aux1 = ""
    aux2 = ""
    aux3 = ""    
    

    def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable
        #self.weka = Weka()
        #self.weka.start_jvm()

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True
        self.countActions = 0

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        #for index, inf in enumerate(self.inferenceModules):
        #    if not self.firstMove and self.elapseTimeEnable:
        #        inf.elapseTime(gameState)
        #    self.firstMove = False
        #    if self.observeEnable:
        #        inf.observeState(gameState)
        #    self.ghostBeliefs[index] = inf.getBeliefDistribution()
        #self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def printLineData(self, gameState):
        fileOpen = open('all_data_pacman.arff', 'a')
        state = ""
        # Posicion del Pacman X
        state = state + str(gameState.getPacmanPosition()[0]) + ", "
        # Posicion del Pacman Y 
        state = state + str(gameState.getPacmanPosition()[1]) + ", "
        # Ancho del mapa
        self.state = state + str(gameState.data.layout.width) + ", "
        # Alto del mapa
        state = state + str(gameState.data.layout.height) + ", "
        # Acciones legales de pacman en la posicion actual
        legalActions = gameState.getLegalPacmanActions()
        for i in ["North", "South", "East", "West", "Stop"]:
            if i in legalActions:
                state = state + "1, " #Cuando puede ir a esa direccion ponemos un 1
            else:
                state = state + "0, " #Cuando no puede ir a esa direccion ponemos un 0   
        # Direccion de pacman
        state = state + str(gameState.data.agentStates[0].getDirection())+ ", "
        # Numero de fantasmas
        state = state + str(gameState.getNumAgents() - 1)+ ", "
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        livingGhost = gameState.getLivingGhosts()
        NumberLivingGhost = 0
        for i in livingGhost:
            if i:
                NumberLivingGhost = NumberLivingGhost + 1
        state = state + str(NumberLivingGhost) + ", "
        # Posicion de los fantasmas
        numberGhosts = gameState.getNumAgents() - 1
        GhostPositionsArray = gameState.getGhostPositions()
        for i in range (0, 4):
            if i < numberGhosts:
                state = state + str(GhostPositionsArray[i][0]) + ", "
                state = state + str(GhostPositionsArray[i][1]) + ", "
            else: 
                state = state + "-1, "
                state = state + "-1, "
        # Direciones de los fantasmas
        GhostDirectionsArray = [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        for i in range (0, 4):
            if i < numberGhosts:
                state = state + str(GhostDirectionsArray[i]) + ", "
            else:
                state = state + "Stop, "
        # Distancia de manhattan a los fantasmas
        GhostDistances = gameState.data.ghostDistances
        for i in range (0, 4):
            if i < numberGhosts:
                if GhostDistances[i] == None:
                    state = state + "-1, "
                else:
                    state = state + str(GhostDistances[i]) + ", "
            else:
                state = state + "-1, "   

        # Puntos de comida restantes
        state = state + str(gameState.getNumFood())+ ", "
        # Distancia de manhattan a la comida mas cercana
        closestFood = gameState.getDistanceNearestFood()
        if closestFood == None:
            state = state + "-1, "  
        else:    
            state = state + str(closestFood)+ ", "
        #Siguiente accion
        state = state + str(BustersAgent.getAction(self, gameState)) + ", "
         # Puntuacion
        state = state + str(gameState.getScore())+ ", "
        #fileOpen.write(str(gameState.getAction())+ '\n')
        #print self.countActions
        if self.countActions == 0:
            self.aux1 = state
            #print str(self.aux1)
        elif self.countActions == 1:
            self.aux2 = state
            self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
        elif self.countActions == 2:
            self.aux3 = state
            self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
            self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
        else:
            if self.countActions%3 == 0:
                self.aux1 = self.aux1 + str(gameState.getScore()) + "\n"
                self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
                self.aux3 = self.aux3 + str(gameState.getScore()) + ", "
                fileOpen.write(self.aux1)
                self.aux1 = ""
                self.aux1 = self.aux1 + state
            elif self.countActions%3 == 1:
                self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
                self.aux2 = self.aux2 + str(gameState.getScore()) + "\n"
                self.aux3 = self.aux3 + str(gameState.getScore()) + ", "
                fileOpen.write(self.aux2)
                self.aux2 = ""
                self.aux2 = self.aux2 + state
            elif self.countActions%3 == 2:
                self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
                self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
                self.aux3 = self.aux3 + str(gameState.getScore()) + "\n"
                fileOpen.write(self.aux3)
                self.aux3 = ""
                self.aux3 = self.aux3 + state

        fileOpen.close()
        print(str(self.x))
        self.countActions = self.countActions + 1

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP

class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    aux1 = ""
    aux2 = ""
    aux3 = ""

    def registerInitialState(self, gameState):
        self.countActions = 0

    def __init__(self, index = 0, inference = "KeyboardInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def printLineData(self, gameState):
        fileOpen = open('test_samemaps_keyboard.arff', 'a')
        
        state = ""
        # Posicion del Pacman X
        state = state + str(gameState.getPacmanPosition()[0]) + ", "
        # Posicion del Pacman Y 
        state = state + str(gameState.getPacmanPosition()[1]) + ", "
        # Ancho del mapa
        state = state + str(gameState.data.layout.width) + ", "
        # Alto del mapa
        state = state + str(gameState.data.layout.height) + ", "
        # Acciones legales de pacman en la posicion actual
        legalActions = gameState.getLegalPacmanActions()
        for i in ["North", "South", "East", "West", "Stop"]:
            if i in legalActions:
                state = state + "1, " #Cuando puede ir a esa direccion ponemos un 1
            else:
                state = state + "0, " #Cuando no puede ir a esa direccion ponemos un 0   
        # Direccion de pacman
        state = state + str(gameState.data.agentStates[0].getDirection())+ ", "
        # Numero de fantasmas
        state = state + str(gameState.getNumAgents() - 1)+ ", "
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        livingGhost = gameState.getLivingGhosts()
        NumberLivingGhost = 0
        for i in livingGhost:
            if i:
                NumberLivingGhost = NumberLivingGhost + 1
        state = state + str(NumberLivingGhost) + ", "
        # Posicion de los fantasmas
        numberGhosts = gameState.getNumAgents() - 1
        GhostPositionsArray = gameState.getGhostPositions()
        for i in range (0, 4):
            if i < numberGhosts:
                state = state + str(GhostPositionsArray[i][0]) + ", "
                state = state + str(GhostPositionsArray[i][1]) + ", "
            else: 
                state = state + "-1, "
                state = state + "-1, "
        # Direciones de los fantasmas
        GhostDirectionsArray = [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        for i in range (0, 4):
            if i < numberGhosts:
                state = state + str(GhostDirectionsArray[i]) + ", "
            else:
                state = state + "Stop, "
        # Distancia de manhattan a los fantasmas
        GhostDistances = gameState.data.ghostDistances
        for i in range (0, 4):
            if i < numberGhosts:
                if GhostDistances[i] == None:
                    state = state + "-1, "
                else:
                    state = state + str(GhostDistances[i]) + ", "
            else:
                state = state + "-1, "   

        # Puntos de comida restantes
        state = state + str(gameState.getNumFood())+ ", "
        # Distancia de manhattan a la comida mas cercana
        closestFood = gameState.getDistanceNearestFood()
        if closestFood == None:
            state = state + "-1, "  
        else:    
            state = state + str(closestFood)+ ", "
        #Siguiente accion
        state = state + str(BustersAgent.getAction(self, gameState)) + ", "
         # Puntuacion
        state = state + str(gameState.getScore())+ ", "
        if self.countActions == 0:
            self.aux1 = state
        elif self.countActions == 1:
            self.aux2 = state
            self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
        elif self.countActions == 2:
            self.aux3 = state
            self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
            self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
        else:
            if self.countActions%3 == 0:
                self.aux1 = self.aux1 + str(gameState.getScore()) + "\n"
                self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
                self.aux3 = self.aux3 + str(gameState.getScore()) + ", "
                fileOpen.write(self.aux1)
                self.aux1 = ""
                self.aux1 = self.aux1 + state
            elif self.countActions%3 == 1:
                self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
                self.aux2 = self.aux2 + str(gameState.getScore()) + "\n"
                self.aux3 = self.aux3 + str(gameState.getScore()) + ", "
                fileOpen.write(self.aux2)
                self.aux2 = ""
                self.aux2 = self.aux2 + state
            elif self.countActions%3 == 2:
                self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
                self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
                self.aux3 = self.aux3 + str(gameState.getScore()) + "\n"
                fileOpen.write(self.aux3)
                self.aux3 = ""
                self.aux3 = self.aux3 + state

        fileOpen.close()
        self.countActions = self.countActions + 1


    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)

from distanceCalculator import Distancer
from game import Actions
from game import Directions
import random, sys

'''Random PacMan Agent'''
class RandomPAgent(BustersAgent):

    aux1 = ""
    aux2 = ""
    aux3 = ""

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0

    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food

    ''' Print the layout'''
    def printGrid(self, gameState):
        table = ""
        ##print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def printLineData(self, gameState):
        fileOpen = open('all_data_pacman.arff', 'a')
        
        state = ""
        # Posicion del Pacman X
        state = state + str(gameState.getPacmanPosition()[0]) + ", "
        # Posicion del Pacman Y 
        state = state + str(gameState.getPacmanPosition()[1]) + ", "
        # Ancho del mapa
        state = state + str(gameState.data.layout.width) + ", "
        # Alto del mapa
        state = state + str(gameState.data.layout.height) + ", "
        # Acciones legales de pacman en la posicion actual
        legalActions = gameState.getLegalPacmanActions()
        for i in ["North", "South", "East", "West", "Stop"]:
            if i in legalActions:
                state = state + "1, " #Cuando puede ir a esa direccion ponemos un 1
            else:
                state = state + "0, " #Cuando no puede ir a esa direccion ponemos un 0   
        # Direccion de pacman
        state = state + str(gameState.data.agentStates[0].getDirection())+ ", "
        # Numero de fantasmas
        state = state + str(gameState.getNumAgents() - 1)+ ", "
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        livingGhost = gameState.getLivingGhosts()
        NumberLivingGhost = 0
        for i in livingGhost:
            if i:
                NumberLivingGhost = NumberLivingGhost + 1
        state = state + str(NumberLivingGhost) + ", "
        # Posicion de los fantasmas
        numberGhosts = gameState.getNumAgents() - 1
        GhostPositionsArray = gameState.getGhostPositions()
        for i in range (0, 4):
            if i < numberGhosts:
                state = state + str(GhostPositionsArray[i][0]) + ", "
                state = state + str(GhostPositionsArray[i][1]) + ", "
            else: 
                state = state + "-1, "
                state = state + "-1, "
        # Direciones de los fantasmas
        GhostDirectionsArray = [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        for i in range (0, 4):
            if i < numberGhosts:
                state = state + str(GhostDirectionsArray[i]) + ", "
            else:
                state = state + "Stop, "
        # Distancia de manhattan a los fantasmas
        GhostDistances = gameState.data.ghostDistances
        for i in range (0, 4):
            if i < numberGhosts:
                if GhostDistances[i] == None:
                    state = state + "-1, "
                else:
                    state = state + str(GhostDistances[i]) + ", "
            else:
                state = state + "-1, "   

        # Puntos de comida restantes
        state = state + str(gameState.getNumFood())+ ", "
        # Distancia de manhattan a la comida mas cercana
        closestFood = gameState.getDistanceNearestFood()
        if closestFood == None:
            state = state + "-1, "  
        else:    
            state = state + str(closestFood)+ ", "
        #Siguiente accion
        state = state + str(BustersAgent.getAction(self, gameState)) + ", "
         # Puntuacion
        state = state + str(gameState.getScore())+ ", "
        #fileOpen.write(str(gameState.getAction())+ '\n')
        #print self.countActions
        if self.countActions == 0:
            self.aux1 = state
            #print str(self.aux1)
        elif self.countActions == 1:
            self.aux2 = state
            self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
        elif self.countActions == 2:
            self.aux3 = state
            self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
            self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
        else:
            if self.countActions%3 == 0:
                self.aux1 = self.aux1 + str(gameState.getScore()) + "\n"
                self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
                self.aux3 = self.aux3 + str(gameState.getScore()) + ", "
                fileOpen.write(self.aux1)
                self.aux1 = ""
                self.aux1 = self.aux1 + state
            elif self.countActions%3 == 1:
                self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
                self.aux2 = self.aux2 + str(gameState.getScore()) + "\n"
                self.aux3 = self.aux3 + str(gameState.getScore()) + ", "
                fileOpen.write(self.aux2)
                self.aux2 = ""
                self.aux2 = self.aux2 + state
            elif self.countActions%3 == 2:
                self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
                self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
                self.aux3 = self.aux3 + str(gameState.getScore()) + "\n"
                fileOpen.write(self.aux3)
                self.aux3 = ""
                self.aux3 = self.aux3 + state

        fileOpen.close()
        self.countActions = self.countActions + 1

    def chooseAction(self, gameState):
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        move_random = random.randint(0, 3)
        if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move

class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0

    def printLineData(self, gameState):
        fileOpen = open('all_data_pacman.arff', 'a')
        
        state = ""
        # Posicion del Pacman X
        state = state + str(gameState.getPacmanPosition()[0]) + ", "
        # Posicion del Pacman Y 
        state = state + str(gameState.getPacmanPosition()[1]) + ", "
        # Ancho del mapa
        state = state + str(gameState.data.layout.width) + ", "
        # Alto del mapa
        state = state + str(gameState.data.layout.height) + ", "
        # Acciones legales de pacman en la posicion actual
        legalActions = gameState.getLegalPacmanActions()
        for i in ["North", "South", "East", "West", "Stop"]:
            if i in legalActions:
                state = state + "1, " #Cuando puede ir a esa direccion ponemos un 1
            else:
                state = state + "0, " #Cuando no puede ir a esa direccion ponemos un 0   
        # Direccion de pacman
        state = state + str(gameState.data.agentStates[0].getDirection())+ ", "
        # Numero de fantasmas
        state = state + str(gameState.getNumAgents() - 1)+ ", "
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        livingGhost = gameState.getLivingGhosts()
        NumberLivingGhost = 0
        for i in livingGhost:
            if i:
                NumberLivingGhost = NumberLivingGhost + 1
        state = state + str(NumberLivingGhost) + ", "
        # Posicion de los fantasmas
        numberGhosts = gameState.getNumAgents() - 1
        GhostPositionsArray = gameState.getGhostPositions()
        for i in range (0, 4):
            if i < numberGhosts:
                state = state + str(GhostPositionsArray[i][0]) + ", "
                state = state + str(GhostPositionsArray[i][1]) + ", "
            else: 
                state = state + "-1, "
                state = state + "-1, "
        # Direciones de los fantasmas
        GhostDirectionsArray = [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        for i in range (0, 4):
            if i < numberGhosts:
                state = state + str(GhostDirectionsArray[i]) + ", "
            else:
                state = state + "Stop, "
        # Distancia de manhattan a los fantasmas
        GhostDistances = gameState.data.ghostDistances
        for i in range (0, 4):
            if i < numberGhosts:
                if GhostDistances[i] == None:
                    state = state + "-1, "
                else:
                    state = state + str(GhostDistances[i]) + ", "
            else:
                state = state + "-1, "   

        # Puntos de comida restantes
        state = state + str(gameState.getNumFood())+ ", "
        # Distancia de manhattan a la comida mas cercana
        closestFood = gameState.getDistanceNearestFood()
        if closestFood == None:
            state = state + "-1, "  
        else:    
            state = state + str(closestFood)+ ", "
        #Siguiente accion
        state = state + str(BustersAgent.getAction(self, gameState)) + ", "
         # Puntuacion
        state = state + str(gameState.getScore())+ ", "
        if self.countActions == 0:
            self.aux1 = state
        elif self.countActions == 1:
            self.aux2 = state
            self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
        elif self.countActions == 2:
            self.aux3 = state
            self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
            self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
        else:
            if self.countActions%3 == 0:
                self.aux1 = self.aux1 + str(gameState.getScore()) + "\n"
                self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
                self.aux3 = self.aux3 + str(gameState.getScore()) + ", "
                fileOpen.write(self.aux1)
                self.aux1 = ""
                self.aux1 = self.aux1 + state
            elif self.countActions%3 == 1:
                self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
                self.aux2 = self.aux2 + str(gameState.getScore()) + "\n"
                self.aux3 = self.aux3 + str(gameState.getScore()) + ", "
                fileOpen.write(self.aux2)
                self.aux2 = ""
                self.aux2 = self.aux2 + state
            elif self.countActions%3 == 2:
                self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
                self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
                self.aux3 = self.aux3 + str(gameState.getScore()) + "\n"
                fileOpen.write(self.aux3)
                self.aux3 = ""
                self.aux3 = self.aux3 + state

        fileOpen.close()
        self.countActions = self.countActions + 1

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (according to mazeDistance!).

        To find the mazeDistance between any two positions, use:
          self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
          successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief
        distributions for each of the ghosts that are still alive.  It
        is defined based on (these are implementation details about
        which you need not be concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i+1]]
        return Directions.EAST

class BasicAgentAA(BustersAgent):
    
    aux1 = ""
    aux2 = ""
    aux3 = ""
    random_movements = 0
    legal_movements = False
    fixed_action = ""

    
    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0

    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food

    ''' Print the layout'''
    def printGrid(self, gameState):
        table = ""
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def printInfo(self, gameState):
        print "---------------- TICK ", self.countActions, " --------------------------"
        # Dimensiones del mapa
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print "Width: ", width, " Height: ", height
        # Posicion del Pacman
        print "Pacman position: ", gameState.getPacmanPosition()
        # Acciones legales de pacman en la posicion actual
        print "Legal actions: ", gameState.getLegalPacmanActions()
        # Direccion de pacman
        print "Pacman direction: ", gameState.data.agentStates[0].getDirection()
        # Numero de fantasmas
        print "Number of ghosts: ", gameState.getNumAgents() - 1
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        print "Living ghosts: ", gameState.getLivingGhosts()
        # Posicion de los fantasmas
        print "Ghosts positions: ", gameState.getGhostPositions()
        # Direciones de los fantasmas
        print "Ghosts directions: ", [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        # Distancia de manhattan a los fantasmas
        print "Ghosts distances: ", gameState.data.ghostDistances
        # Puntos de comida restantes
        print "Pac dots: ", gameState.getNumFood()
        # Distancia de manhattan a la comida mas cercada
        print "Distance nearest pac dots: ", gameState.getDistanceNearestFood()
        # Paredes del mapa
        print "Map:  \n", gameState.getWalls()
        # Puntuacion
        print "Score: ", gameState.getScore()

    def printLineData(self, gameState):
       
        fileOpen = open('all_data_pacman.arff', 'a') 
        state = ""
        # Posicion del Pacman X
        state = state + str(gameState.getPacmanPosition()[0]) + ", "
        # Posicion del Pacman Y 
        state = state + str(gameState.getPacmanPosition()[1]) + ", "
        # Ancho del mapa
        state = state + str(gameState.data.layout.width) + ", "
        # Alto del mapa
        state = state + str(gameState.data.layout.height) + ", "
        # Acciones legales de pacman en la posicion actual
        legalActions = gameState.getLegalPacmanActions()
        for i in ["North", "South", "East", "West", "Stop"]:
            if i in legalActions:
                state = state + "1, " #Cuando puede ir a esa direccion ponemos un 1
            else:
                state = state + "0, " #Cuando no puede ir a esa direccion ponemos un 0   
        # Direccion de pacman
        state = state + str(gameState.data.agentStates[0].getDirection())+ ", "
        # Numero de fantasmas
        state = state + str(gameState.getNumAgents() - 1)+ ", "
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        livingGhost = gameState.getLivingGhosts()
        NumberLivingGhost = 0
        for i in livingGhost:
            if i:
                NumberLivingGhost = NumberLivingGhost + 1
        state = state + str(NumberLivingGhost) + ", "
        # Posicion de los fantasmas
        numberGhosts = gameState.getNumAgents() - 1
        GhostPositionsArray = gameState.getGhostPositions()
        for i in range (0, 4):
            if i < numberGhosts:
                state = state + str(GhostPositionsArray[i][0]) + ", "
                state = state + str(GhostPositionsArray[i][1]) + ", "
            else: 
                state = state + "-1, "
                state = state + "-1, "
        # Direciones de los fantasmas
        GhostDirectionsArray = [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        for i in range (0, 4):
            if i < numberGhosts:
                state = state + str(GhostDirectionsArray[i]) + ", "
            else:
                state = state + "Stop, "
        # Distancia de manhattan a los fantasmas
        GhostDistances = gameState.data.ghostDistances
        for i in range (0, 4):
            if i < numberGhosts:
                if GhostDistances[i] == None:
                    state = state + "-1, "
                else:
                    state = state + str(GhostDistances[i]) + ", "
            else:
                state = state + "-1, "   

        # Puntos de comida restantes
        state = state + str(gameState.getNumFood())+ ", "
        # Distancia de manhattan a la comida mas cercana
        closestFood = gameState.getDistanceNearestFood()
        if closestFood == None:
            state = state + "-1, "  
        else:    
            state = state + str(closestFood)+ ", "
        #Siguiente accion
        state = state + str(BustersAgent.getAction(self, gameState)) + ", "
        # Puntuacion
        state = state + str(gameState.getScore())+ ", "

        if self.countActions == 0:
            self.aux1 = state
        elif self.countActions == 1:
            self.aux2 = state
            self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
        elif self.countActions == 2:
            self.aux3 = state
            self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
            self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
        else:
            if self.countActions%3 == 0:
                self.aux1 = self.aux1 + str(gameState.getScore()) + "\n"
                self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
                self.aux3 = self.aux3 + str(gameState.getScore()) + ", "
                fileOpen.write(self.aux1)
                self.aux1 = ""
                self.aux1 = self.aux1 + state
            elif self.countActions%3 == 1:
                self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
                self.aux2 = self.aux2 + str(gameState.getScore()) + "\n"
                self.aux3 = self.aux3 + str(gameState.getScore()) + ", "
                fileOpen.write(self.aux2)
                self.aux2 = ""
                self.aux2 = self.aux2 + state
            elif self.countActions%3 == 2:
                self.aux1 = self.aux1 + str(gameState.getScore()) + ", "
                self.aux2 = self.aux2 + str(gameState.getScore()) + ", "
                self.aux3 = self.aux3 + str(gameState.getScore()) + "\n"
                fileOpen.write(self.aux3)
                self.aux3 = ""
                self.aux3 = self.aux3 + state

        fileOpen.close()
        self.countActions = self.countActions + 1
    
    def chooseAction(self, gameState):        
        
        #-----------------------------AGENTE AUTOMATICO PRACTICA 1-----------------------------#

        # # Recoleccion de atributos para determinar en cada uno de los modelos el siguiente paso #
        # x = []
        # # Posicion del Pacman X
        # x.append(gameState.getPacmanPosition()[0])
        # # Posicion del Pacman Y 
        # x.append(gameState.getPacmanPosition()[1])
        # # Ancho del mapa
        # x.append(gameState.data.layout.width)
        # # Alto del mapa
        # x.append(gameState.data.layout.height)
        # # Acciones legales de pacman en la posicion actual
        # legalActions = gameState.getLegalPacmanActions()
        # for i in ["North", "South", "East", "West", "Stop"]:
        #     if i in legalActions:
        #         x.append('1')
        #     else:
        #         x.append('0')
        # # Direccion de pacman
        # x.append(gameState.data.agentStates[0].getDirection())
        # # Numero de fantasmas
        # x.append(gameState.getNumAgents() - 1)
        # # Posicion de los fantasmas
        # numberGhosts = gameState.getNumAgents() - 1
        # GhostPositionsArray = gameState.getGhostPositions()
        # for i in range (0, 4):
        #     if i < numberGhosts:
        #         x.append(GhostPositionsArray[i][0]) 
        #         x.append(GhostPositionsArray[i][1]) 
        #     else: 
        #         x.append(-1)
        #         x.append(-1)
        # # Direciones de los fantasmas
        # GhostDirectionsArray = [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        # for i in range (0, 4):
        #     if i < numberGhosts:
        #         if(GhostDirectionsArray[i] == None):
        #             x.append(str('None'))
        #         else:
        #             x.append(str(GhostDirectionsArray[i]))
        #     else:
        #         x.append('Stop')
        # Puntos de comida restantes
        # x.append(gameState.getNumFood())
        # print(str(x))
        
        #-----------------------------CODIGO DE CLASIFICACION FASE 2-----------------------------#

        # Para ejecutar el clasificador de la fase 2 el codigo del predictor de la fase 3 debe estar comentado hasta control de errores

        #-----------------------------RESULTADOS DE CLASIFICACION FASE 2-----------------------------#
        #a = self.weka.predict('./models/j48.model', x, './trainning/E1CT_filter_data_2_training_keyboard.arff')
        
        #-----------------------------CODIGO DE PREDICCION FASE 3-----------------------------#
        '''
        # Para ejecutar el predictor de la fase 3 comentar la parte de resultado de clasificacion de la fase 2 
        # Predecimos las score para todas las opciones y se toma la que mejor score de

        v = x[:]
        w = x[:]
        y = x[:]
        z = x[:]

        v.append('North')
        v.append(gameState.getScore())
        w.append('South')
        w.append(gameState.getScore())
        x.append('East')
        x.append(gameState.getScore())
        y.append('West')
        y.append(gameState.getScore())

        result_list = []

        #-----------------------------RESULTADOS DE PREDICCION FASE 3-----------------------------#
        
        # Para obtener el resultado de prediccion con Score 1 descomentar el siguiente bloque

        result_list.append(self.weka.predict('./models/LinearRegression.model', v, './trainning/E1RT_score1_filter_data_2_training_keyboard.arff'))
        result_list.append(self.weka.predict('./models/LinearRegression.model', w, './trainning/E1RT_score1_filter_data_2_training_keyboard.arff'))
        result_list.append(self.weka.predict('./models/LinearRegression.model', x, './trainning/E1RT_score1_filter_data_2_training_keyboard.arff'))
        result_list.append(self.weka.predict('./models/LinearRegression.model', y, './trainning/E1RT_score1_filter_data_2_training_keyboard.arff'))

        # Para obtener el resultado de prediccion con Score 1 descomentar el siguiente bloque

        #result_list.append(self.weka.predict('./models/LinearRegression.model', v, './trainning/E1RT_score3_filter_data_2_training_keyboard.arff'))
        #result_list.append(self.weka.predict('./models/LinearRegression.model', w, './trainning/E1RT_score3_filter_data_2_training_keyboard.arff'))
        #result_list.append(self.weka.predict('./models/LinearRegression.model', x, './trainning/E1RT_score3_filter_data_2_training_keyboard.arff'))
        #result_list.append(self.weka.predict('./models/LinearRegression.model', y, './trainning/E1RT_score3_filter_data_2_training_keyboard.arff'))

        pos_max=result_list.index(max(result_list))

        if pos_max == 0:
            a = 'North'
        elif pos_max == 1:
            a = 'South'
        elif pos_max == 2:
            a = 'East'
        elif pos_max == 3:
            a = 'West'
        elif pos_max == 4:
            a = 'Stop'

        '''
        #-----------------------------CONTROL DE ERRORES DE AMBAS FASES-----------------------------#
        # Si puede realizar la accion devuelve la misma y random en caso contrario
        if a in legalActions:
            return a
        else: 
            move = Directions.STOP
            legal = gameState.getLegalActions(0) ##Legal position from the pacman
            move_random = random.randint(0, 3)
            if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
            if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
            if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
            if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
            return move    
        return 
        #-----------------------------AGENTE AUTOMATICO TUTORIAL 1-----------------------------# 
        '''self.countActions = self.countActions + 1
        self.printInfo(gameState)
        legal = gameState.getLegalActions(0) #Legal position from the pacman
        global fixed_action

        move = Directions.STOP
        min = 1000000
        i_min = -1
        for i in range(0, len(gameState.data.ghostDistances)):
            if gameState.data.ghostDistances[i] != None and gameState.data.ghostDistances[i]< min:
                min = gameState.data.ghostDistances[i]
                i_min = i

        if self.random_movements == 0:
            print(self.random_movements)
            ClosestGhost = gameState.getGhostPositions()[i_min]
            PacMan_pos = gameState.getPacmanPosition()
            difX = PacMan_pos[0] - ClosestGhost[0]
            difY = PacMan_pos[1] - ClosestGhost[1]

            if difX >= 0 and difY >= 0:
                if ((difX < difY and difX!=0) or difY==0) and Directions.WEST in legal:
                    move = Directions.WEST
                elif Directions.SOUTH in legal:
                    move = Directions.SOUTH
                else:
                    move_random = random.randint(0, 1)
                    if   ( move_random == 0 ) and Directions.EAST in legal:    
                        move = Directions.EAST
                        self.fixed_action = Directions.EAST
                    if   ( move_random == 1 ) and Directions.NORTH in legal:   
                        move = Directions.NORTH
                        self.fixed_action = Directions.NORTH
                    self.random_movements = 5

            elif difX >= 0 and difY <= 0:
                if ((difX < difY and difX!=0) or difY==0) and Directions.WEST in legal:
                    move = Directions.WEST
                elif Directions.NORTH in legal:
                    move = Directions.NORTH
                else:
                    move_random = random.randint(0, 1)
                    if   ( move_random == 0 ) and Directions.EAST in legal: 
                        move = Directions.EAST
                        self.fixed_action = Directions.EAST
                    if   ( move_random == 1 ) and Directions.SOUTH in legal:  
                        move = Directions.SOUTH
                        self.fixed_action = Directions.SOUTH
                    self.random_movements = 5

            elif difX <= 0 and difY >= 0:
                if ((difX < difY and difX!=0) or difY==0) and Directions.EAST in legal:
                    move = Directions.EAST
                elif Directions.SOUTH in legal:
                    move = Directions.SOUTH
                else:
                    move_random = random.randint(0, 1)
                    if   ( move_random == 0 ) and Directions.WEST in legal: 
                        move = Directions.WEST
                        self.fixed_action = Directions.WEST
                        
                    if   ( move_random == 1 ) and Directions.NORTH in legal:   
                        move = Directions.NORTH
                        self.fixed_action = Directions.NORTH
                    self.random_movements = 5

            elif difX <= 0 and difY <= 0:
                if ((difX < difY and difX!=0) or difY==0) and Directions.EAST in legal:
                    move = Directions.EAST
                elif Directions.NORTH in legal:
                    move = Directions.NORTH
                else:
                    move_random = random.randint(0, 1)
                    if   ( move_random == 0 ) and Directions.WEST in legal: 
                        move = Directions.WEST
                        self.fixed_action = Directions.WEST
                    if   ( move_random == 1 ) and Directions.SOUTH in legal:   
                        move = Directions.SOUTH
                        self.fixed_action = Directions.SOUTH
                    self.random_movements = 5

        else:
            if self.fixed_action in legal:
                move = self.fixed_action
                self.random_movements = self.random_movements - 1 

            else:
                self.random_movements = self.random_movements - 1 
                while not self.legal_movements:
                    move_random = random.randint(0, 3)
                    if   ( move_random == 0 ) and Directions.WEST in legal:
                        move = Directions.WEST 
                        self.legal_movements = True
                    if   ( move_random == 1 ) and Directions.EAST in legal: 
                        move = Directions.EAST
                        self.legal_movements = True
                    if   ( move_random == 2 ) and Directions.NORTH in legal:   
                        move = Directions.NORTH
                        self.legal_movements = True
                    if   ( move_random == 3 ) and Directions.SOUTH in legal: 
                        move = Directions.SOUTH
                        self.legal_movements = True
                self.legal_movements = False

        #print "move: ", move
        #if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        #if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        #if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        #if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move'''

class QLearningAgent(BustersAgent):

    living = 0
    choosen_action = ""
    best_direction = [0, "Stop"] # Es un array que me guarda la mejor direccion a tomar

    def printLineData(self, gameState):
        return
        
    def __init__(self, **args):
        "Initialize Q-values"
        BustersAgent.__init__(self, **args)
        self.actions = {"North":0, "East":1, "South":2, "West":3, "Exit":4, "Stop": 5}
        self.table_file = open("qtable.txt", "r+")
        self.q_table = self.readQtable()
        self.epsilon = 0.3 #Probabilidad de que se mueva random
        self.alpha = 0.1 #Tasa de aprendizaje representa como de agresivo es el aprendizaje 
        self.discount = 0.9 #Factor de descuento para dar mas importancia a las recompensas mas inmediatas
        self.past_state = None
 
 
    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        # Se calcula el numero de fantasmas con el que se empieza el juego
        for i in gameState.getLivingGhosts():
            if i:
                self.living = self.living + 1

    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        ##print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    """
      Q-Learning Agent

      Functions you should fill in:
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
    """
    
    def readQtable(self):
	"Read qtable from disc"
        # print("Estamos en el readQtable")
        table = self.table_file.readlines()
        q_table = []

        for i, line in enumerate(table):
            row = line.split()
            row = [float(x) for x in row]
            q_table.append(row)

        return q_table

    def writeQtable(self):
	"Write qtable to disc"
        # print("Estamos en el writeQtable")
        self.table_file.seek(0)
        self.table_file.truncate()

        for line in self.q_table:
            for item in line:
                self.table_file.write(str(item)+" ")
            self.table_file.write("\n")

    def __del__(self):
	"Destructor. Invokation at the end of each episode"
        # print(self.q_table)
        self.writeQtable()
        self.table_file.close()

    def computePosition(self, state):
	"""
	Compute the row of the qtable for a given state.
	For instance, the state (3,1) is the row 7
	"""
        aux1 = 0
        if self.best_direction[0] == "North":
            aux1 = 0
        elif self.best_direction[0] == "Northeast":
            aux1 = 1
        elif self.best_direction[0] == "East":
            aux1 = 2  
        elif self.best_direction[0] == "Southeast":
            aux1 = 3
        elif self.best_direction[0] == "South":
            aux1 = 4
        elif self.best_direction[0] == "Southwest":
            aux1 = 5
        elif self.best_direction[0] == "West":
            aux1 = 6          
        elif self.best_direction[0] == "Northwest":
            aux1 = 7 

        aux = 0
        if self.best_direction[1] == "North":
            aux = 0
        elif self.best_direction[1] == "South":
            aux = 1
        elif self.best_direction[1] == "East":
            aux = 2   
        elif self.best_direction[1] == "West":
            aux = 3 
        
        return (aux1*4) + aux

    def getQValue(self, state, action):

        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        position = self.computePosition(state)
        # print("Con el 0")
        #print(str(state.getLegalActions(0)))
        # print("Sin el 0")
        #print(str(state.getLegalActions()))
        action_column = self.actions[action]
        
        # print("La posicion es:" +  str(position))
        # print("La action_column es:" +  str(action_column))

        return self.q_table[position][action_column]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
     	legalActions = state.getLegalActions()
        if len(legalActions)==0:
          return 0
        return max(self.q_table[self.computePosition(state)])

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        legalActions = state.getLegalActions()
        if len(legalActions)==0:
          return None

        if "Stop" in legalActions:
            legalActions.remove("Stop")

        print("Las acciones legales son: " + str(legalActions))  

        # POR QUE LO INICIALIZAN ASI
        # best_actions = [legalActions[0]]
        best_actions = []
        best_value = self.getQValue(state, legalActions[0])
        print("ComputeActionFromQValues empieza con: " + str(best_value))        

        for action in legalActions:
            value = self.getQValue(state, action)
            if value == best_value:
                best_actions.append(action)
            if value > best_value:
                best_actions = [action]
                best_value = value
            print("En el for estamos mirando value: " + str(value) + " y best value: " + str(best_value) + " y action es: " + str(action))        
        print("ComputeActionFromQValues devuelve: " + str(best_actions))   
        retorno = random.choice(best_actions) 
        
        print("El retorno es: " + str(retorno))  
        self.choosen_action = retorno 
        return retorno

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
        """
        
        # Pick Action
        legalActions = state.getLegalActions()

        if len(legalActions) == 0:
             return self.state 
        else:
            if "Stop" in legalActions:
                legalActions.remove("Stop")
            #self.new_state = copy.deepcopy(self.calculateBestDirection(state))
            self.best_direction = self.calculateBestDirection(state)
            print("Actualizamos best_direction a: " + str(self.best_direction))

        reward = 0

        if(self.past_state != None):
            aux = 0

            # Calcular el numero de fantasmas vivos
            for i in state.getLivingGhosts():
                if i==True:
                    aux = aux + 1

            # Diferentes recompensas en funcion del numero de fantasmas vivos        
            if aux < self.living: # Caso del ultimo fantasma
                reward = 50
                self.living = aux
                print("Me he comido, tengo reward " + str(reward) + " y hay " + str(self.living) + " fantasmas vivos")
            else: # Caso en que aun no se ha comido ningun fantasma
                min = 1000000
                closest_ghost = -1
                # Calculamos la distancia minima a los fantasmas
                for i in range(0, len(state.data.ghostDistances)):
                    if state.data.ghostDistances[i] != None and state.data.ghostDistances[i]< min:
                        min = state.data.ghostDistances[i]
                        closest_ghost = i
                
                # distance = max((state.data.layout.width-2), (state.data.layout.height-4))
                mazeDistance = self.distancer.getDistance(state.getPacmanPosition(), state.getGhostPositions()[closest_ghost])
                reward = 1.0/mazeDistance # Se suma 1 al minimo porque si esta a 1 de distancia del fantasma ya tienes recimpensa 1
                print("Con distancia " + str(mazeDistance) + " he obtenido un reward de " + str(reward))
                # reward = 0
            #print("Nuestro past_state ahora mismo es: " + str(self.past_state))
            
            self.update(self.past_state, state, reward)
            
        self.past_state = copy.deepcopy(state)

        flip = util.flipCoin(self.epsilon)

        if flip:
            self.choosen_action = random.choice(legalActions)
            return self.choosen_action
        
        print("Hola")
        return self.getPolicy(state)

    def calculateBestDirection(self, state):

        legal = state.getLegalActions()
        ret = []
        i_min = -1
        min = 1000000

        for i in range(0, len(state.data.ghostDistances)):
            if state.data.ghostDistances[i] != None and state.data.ghostDistances[i]< min:
                min = state.data.ghostDistances[i]
                i_min = i

        
        ClosestGhost = state.getGhostPositions()[i_min]
        PacMan_pos = state.getPacmanPosition()
        difX = PacMan_pos[0] - ClosestGhost[0]
        difY = PacMan_pos[1] - ClosestGhost[1]

        # if(abs(difX)<abs(difY)):
        #     ret.append(abs(difX))
        # else:
        #     ret.append(abs(difY))

        if difY == 0: #este u oeste
            if difX > 0: #oeste
                ret.append("West")
            else: #este
                ret.append("East")

        elif difX == 0: #norte o sur
            if difY > 0: #sur
                ret.append("South")
            else: #norte
                ret.append("North")

        elif difX > 0: #oeste
            if difY > 0: #sur
                #suroeste
                ret.append("Southwest")
            else: 
                #noroeste
                ret.append("Northwest")

        elif difX < 0: #este
            if difY > 0: 
                #sureste
                ret.append("Southeast")
            else: 
               #noreste 
               ret.append("Northeast")

        #NORTE, SUR , ESTE , OESTE, NORESTE, NOROESTE, SURESTE, SUROESTE
        add_legal = False
        if ret[0] == "North":
            if Directions.NORTH in legal:
                ret.append(Directions.NORTH)
                add_legal = True

        elif ret[0] == "Northeast":
            if abs(difY) < abs(difX) and Directions.NORTH in legal:
                ret.append(Directions.NORTH)
                add_legal = True
            elif Directions.EAST in legal: 
                ret.append(Directions.EAST)
                add_legal = True
                
        elif ret[0] == "East":
            if Directions.EAST in legal:
                ret.append(Directions.EAST)
                add_legal = True
        
        elif ret[0] == "Southeast":
            if abs(difY) < abs(difX) and Directions.SOUTH in legal:
                ret.append(Directions.SOUTH)
                add_legal = True
            elif Directions.EAST in legal: 
                ret.append(Directions.EAST)
                add_legal = True

        elif ret[0] == "South":
            if Directions.SOUTH in legal:
                ret.append( Directions.SOUTH)
                add_legal = True
            
        elif ret[0] == "Southwest":
            if abs(difY) < abs(difX) and Directions.SOUTH in legal:
                ret.append(Directions.SOUTH)
                add_legal = True
            elif Directions.WEST in legal: 
                ret.append(Directions.WEST)
                add_legal = True
            
        elif ret[0] == "West":
            if Directions.WEST in legal:
                ret.append(Directions.WEST)
                add_legal = True

        elif ret[0] == "Northwest":    
            if abs(difY) < abs(difX) and Directions.NORTH in legal:
                ret.append(Directions.NORTH)
                add_legal = True
            elif Directions.WEST in legal: 
                ret.append(Directions.WEST)  
                add_legal = True

        while not add_legal:
            move_random = random.randint(0, 3)
            if ( move_random == 0 ) and Directions.WEST in legal:
                ret.append(Directions.WEST)
                add_legal = True
            if ( move_random == 1 ) and Directions.EAST in legal: 
                ret.append(Directions.EAST)
                add_legal = True
            if ( move_random == 2 ) and Directions.NORTH in legal:   
                ret.append(Directions.NORTH)
                add_legal = True
            if ( move_random == 3 ) and Directions.SOUTH in legal: 
                ret.append(Directions.SOUTH)
                add_legal = True




        
        # if difX >= 0 and difY >= 0:
        #     if ((difX < difY and difX!=0) or difY==0) and Directions.WEST in legal:
        #         ret.append( Directions.WEST)
        #     elif Directions.SOUTH in legal:
        #         ret.append(  Directions.SOUTH)
        #     else:
        #         move_random = random.randint(0, 1)
        #         if ( move_random == 0 ):
        #             if  Directions.EAST in legal:    
        #                 ret.append( Directions.EAST)
        #                 self.fixed_action = Directions.EAST
        #             else:
        #                 ret.append( Directions.NORTH)
        #                 self.fixed_action = Directions.NORTH        

        #         if   ( move_random == 1 ):      
        #             if  Directions.NORTH in legal:   
        #                 ret.append(  Directions.NORTH)
        #                 self.fixed_action = Directions.NORTH
        #             else:
        #                 ret.append( Directions.EAST)
        #                 self.fixed_action = Directions.EAST     
        #         self.random_movements = 5

        # elif difX >= 0 and difY <= 0:
        #     if ((difX < difY and difX!=0) or difY==0) and Directions.WEST in legal:
        #         ret.append( Directions.WEST)
        #     elif Directions.NORTH in legal:
        #         ret.append( Directions.NORTH)
        #     else:
        #         move_random = random.randint(0, 1)
        #         if ( move_random == 0 ):
        #             if  Directions.EAST in legal: 
        #                 ret.append( Directions.EAST)
        #                 self.fixed_action = Directions.EAST
        #             else: 
        #                 ret.append( Directions.SOUTH)
        #                 self.fixed_action = Directions.SOUTH

        #         if   ( move_random == 1 ):  
        #             if   Directions.SOUTH in legal:  
        #                 ret.append( Directions.SOUTH)
        #                 self.fixed_action = Directions.SOUTH
        #             else:
        #                 ret.append( Directions.EAST)
        #                 self.fixed_action = Directions.EAST

        #         self.random_movements = 5

        # elif difX <= 0 and difY >= 0:
        #     if ((difX < difY and difX!=0) or difY==0) and Directions.EAST in legal:
        #         ret.append( Directions.EAST)
        #     elif Directions.SOUTH in legal:
        #         ret.append( Directions.SOUTH)
        #     else:
        #         move_random = random.randint(0, 1)
        #         if ( move_random == 0 ):
        #             if Directions.WEST in legal: 
        #                 ret.append(  Directions.WEST)
        #                 self.fixed_action = Directions.WEST
        #             else: 
        #                 ret.append( Directions.NORTH)
        #                 self.fixed_action = Directions.NORTH
                        
        #         if   ( move_random == 1 ):   
        #             if  Directions.NORTH in legal:   
        #                 ret.append( Directions.NORTH)
        #                 self.fixed_action = Directions.NORTH
        #             else:
        #                 ret.append( Directions.WEST)
        #                 self.fixed_action = Directions.WEST    
        #         self.random_movements = 5

        # elif difX <= 0 and difY <= 0:
        #     if ((difX < difY and difX!=0) or difY==0) and Directions.EAST in legal:
        #         ret.append( Directions.EAST)
        #     elif Directions.NORTH in legal:
        #         ret.append(  Directions.NORTH)
        #     else:
        #         move_random = random.randint(0, 1)
        #         if ( move_random == 0 ):
        #             if Directions.WEST in legal: 
        #                 ret.append( Directions.WEST)
        #                 self.fixed_action = Directions.WEST
        #             else:
        #                 ret.append( Directions.SOUTH)
        #                 self.fixed_action = Directions.SOUTH

        #         if   ( move_random == 1 ) :
        #             if Directions.SOUTH in legal:   
        #                 ret.append( Directions.SOUTH)
        #                 self.fixed_action = Directions.SOUTH
        #             else:
        #                 ret.append( Directions.WEST)
        #                 self.fixed_action = Directions.WEST
                        
        #         self.random_movements = 5
                
        
        return ret

    def update(self, state, nextState, reward):
        '''
            The parent class calls this to observe a state = action => nextState and reward transition. You should do your Q-Value update here

	        Good Terminal state -> reward 1
	        Bad Terminal state -> reward -1
	        Otherwise -> reward 0

	        Q-Learning update:

	        if terminal_state:
		        Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + 0)
	        else:
	  	        Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + self.discount * max a' Q(nextState, a'))
        '''
        position = self.computePosition(state) #obtenemos la posicion correspondiente con el estado actual
        naction = self.actions[self.choosen_action] #obtenemos el identificador de la accion a tomar

     	print("Actualizando la posicion: " + str(position) + " y la accion " + str(naction) + " y la reward " + str(reward))

        #Esto habra que ver cunado se pasa que no esta claro jejeje
        if reward==1.0: #el estado sera final si el refuerzo es 1
            self.q_table[position][naction] = (1-self.alpha) * self.q_table[position][naction] + self.alpha * (reward + 0)
        else: #si el refuerzo es 0 entonces el estado sera no final
            self.q_table[position][naction] = (1-self.alpha) * self.q_table[position][naction] + self.alpha * (reward + self.discount * self.getValue(nextState))
        
  

    def getPolicy(self, state):
	"Return the best action in the qtable for a given state"
        return self.computeActionFromQValues(state)

    def getValue(self, state):
	"Return the highest q value for a given state"
        return self.computeValueFromQValues(state)

    def chooseAction(self, gameState):
        pass
        # move = Directions.STOP
        # legal = gameState.getLegalActions(0) ##Legal position from the pacman
        # move_random = random.randint(0, 3)
        # if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        # if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        # if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        # if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        # return move

    #-----------------------------AGENTE AUTOMATICO TUTORIAL 1-----------------------------# 
    '''self.countActions = self.countActions + 1
    self.printInfo(gameState)
    legal = gameState.getLegalActions(0) #Legal position from the pacman
    global fixed_action

    move = Directions.STOP
    min = 1000000
    i_min = -1
    for i in range(0, len(gameState.data.ghostDistances)):
        if gameState.data.ghostDistances[i] != None and gameState.data.ghostDistances[i]< min:
            min = gameState.data.ghostDistances[i]
            i_min = i

    if self.random_movements == 0:
        print(self.random_movements)
        ClosestGhost = gameState.getGhostPositions()[i_min]
        PacMan_pos = gameState.getPacmanPosition()
        difX = PacMan_pos[0] - ClosestGhost[0]
        difY = PacMan_pos[1] - ClosestGhost[1]

        if difX >= 0 and difY >= 0:
            if ((difX < difY and difX!=0) or difY==0) and Directions.WEST in legal:
                move = Directions.WEST
            elif Directions.SOUTH in legal:
                move = Directions.SOUTH
            else:
                move_random = random.randint(0, 1)
                if   ( move_random == 0 ) and Directions.EAST in legal:    
                    move = Directions.EAST
                    self.fixed_action = Directions.EAST
                if   ( move_random == 1 ) and Directions.NORTH in legal:   
                    move = Directions.NORTH
                    self.fixed_action = Directions.NORTH
                self.random_movements = 5

        elif difX >= 0 and difY <= 0:
            if ((difX < difY and difX!=0) or difY==0) and Directions.WEST in legal:
                move = Directions.WEST
            elif Directions.NORTH in legal:
                move = Directions.NORTH
            else:
                move_random = random.randint(0, 1)
                if   ( move_random == 0 ) and Directions.EAST in legal: 
                    move = Directions.EAST
                    self.fixed_action = Directions.EAST
                if   ( move_random == 1 ) and Directions.SOUTH in legal:  
                    move = Directions.SOUTH
                    self.fixed_action = Directions.SOUTH
                self.random_movements = 5

        elif difX <= 0 and difY >= 0:
            if ((difX < difY and difX!=0) or difY==0) and Directions.EAST in legal:
                move = Directions.EAST
            elif Directions.SOUTH in legal:
                move = Directions.SOUTH
            else:
                move_random = random.randint(0, 1)
                if   ( move_random == 0 ) and Directions.WEST in legal: 
                    move = Directions.WEST
                    self.fixed_action = Directions.WEST
                    
                if   ( move_random == 1 ) and Directions.NORTH in legal:   
                    move = Directions.NORTH
                    self.fixed_action = Directions.NORTH
                self.random_movements = 5

        elif difX <= 0 and difY <= 0:
            if ((difX < difY and difX!=0) or difY==0) and Directions.EAST in legal:
                move = Directions.EAST
            elif Directions.NORTH in legal:
                move = Directions.NORTH
            else:
                move_random = random.randint(0, 1)
                if   ( move_random == 0 ) and Directions.WEST in legal: 
                    move = Directions.WEST
                    self.fixed_action = Directions.WEST
                if   ( move_random == 1 ) and Directions.SOUTH in legal:   
                    move = Directions.SOUTH
                    self.fixed_action = Directions.SOUTH
                self.random_movements = 5

    else:
        if self.fixed_action in legal:
            move = self.fixed_action
            self.random_movements = self.random_movements - 1 

        else:
            self.random_movements = self.random_movements - 1 
            while not self.legal_movements:
                move_random = random.randint(0, 3)
                if   ( move_random == 0 ) and Directions.WEST in legal:
                    move = Directions.WEST 
                    self.legal_movements = True
                if   ( move_random == 1 ) and Directions.EAST in legal: 
                    move = Directions.EAST
                    self.legal_movements = True
                if   ( move_random == 2 ) and Directions.NORTH in legal:   
                    move = Directions.NORTH
                    self.legal_movements = True
                if   ( move_random == 3 ) and Directions.SOUTH in legal: 
                    move = Directions.SOUTH
                    self.legal_movements = True
            self.legal_movements = False

    #print "move: ", move
    #if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
    #if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
    #if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
    #if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
    return move'''