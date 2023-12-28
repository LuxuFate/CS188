# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        # print(legalMoves[chosenIndex])
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        # newGhostPositions = successorGameState.getGhostPositions()
        foodList = newFood.asList()
        disToFood = float("inf")
        disToGhost = float("inf")
        
        for food in foodList:
            tempDis = manhattanDistance(newPos, food)
            if tempDis < disToFood:
                disToFood = tempDis
        for ghost in newGhostStates:
            tempDis = manhattanDistance(newPos, ghost.getPosition())
            if tempDis < disToGhost:
                disToGhost = tempDis
            if disToGhost == 0 and ghost.scaredTimer > 0:
                return float("inf")

        value = 10*(1.1/disToFood) + disToGhost*0.75
        return successorGameState.getScore() + value

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def miniMax(currIter, gameState, agent, maxIter):
            if currIter == maxIter or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            if agent > gameState.getNumAgents()-1:
                agent = 0
            
            actions = gameState.getLegalActions(agent)
            actionValues = []
            for action in actions:
                actionValues.append(miniMax(currIter+1, gameState.generateSuccessor(agent, action), agent+1, maxIter))
            if agent == 0:
                return max(actionValues)
            else:
                return min(actionValues)

        legalMoves = gameState.getLegalActions(agentIndex=0)
        currIter = 1
        maxIter = self.depth * gameState.getNumAgents()
        allActionValues = []
        for action in legalMoves:
            allActionValues.append(miniMax(currIter, gameState.generateSuccessor(0, action), 1, maxIter))
            
        bestScore = max(allActionValues)
        bestIndices = [index for index in range(len(allActionValues)) if allActionValues[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]

        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def abPrune(currIter, gameState, agent, maxIter, a, b):
            if currIter == maxIter or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            if agent > gameState.getNumAgents()-1:
                agent = 0
            
            actions = gameState.getLegalActions(agent)
            if agent == 0:
                value = -float("inf")
                for action in actions:
                    value = max(value, abPrune(currIter+1, gameState.generateSuccessor(agent, action), agent+1, maxIter, a, b))
                    if value > b:
                        return value
                    a = max(a, value)
                return value
            else:
                value = float("inf")
                for action in actions:
                    value = min(value, abPrune(currIter+1, gameState.generateSuccessor(agent, action), agent+1, maxIter, a, b))
                    if value < a:
                        return value
                    b = min(b, value)
                return value
            
        legalMoves = gameState.getLegalActions(agentIndex=0)
        currIter = 1
        maxIter = self.depth * gameState.getNumAgents()
        allActionValues = []
        alpha = -float("inf")
        for action in legalMoves:
            v = abPrune(currIter, gameState.generateSuccessor(0, action), 1, maxIter, alpha, float("inf"))
            alpha = max(v, alpha)
            allActionValues.append(v)
        bestScore = max(allActionValues)
        bestIndices = [index for index in range(len(allActionValues)) if allActionValues[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectiMax(currIter, gameState, agent, maxIter):
            if currIter == maxIter or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            if agent > gameState.getNumAgents()-1:
                agent = 0
            
            actions = gameState.getLegalActions(agent)
            actionValues = []
            for action in actions:
                actionValues.append(expectiMax(currIter+1, gameState.generateSuccessor(agent, action), agent+1, maxIter))
            if agent == 0:
                return max(actionValues)
            else:
                return sum(actionValues)/len(actionValues)

        legalMoves = gameState.getLegalActions(agentIndex=0)
        currIter = 1
        maxIter = self.depth * gameState.getNumAgents()
        allActionValues = []
        for action in legalMoves:
            allActionValues.append(expectiMax(currIter, gameState.generateSuccessor(0, action), 1, maxIter))
            
        bestScore = max(allActionValues)
        bestIndices = [index for index in range(len(allActionValues)) if allActionValues[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    powerPellets = currentGameState.getCapsules()

    foodList = foods.asList()
    disToFood = float("inf")
    disToGhost = float("inf")
    disToPellet = float("inf")

    for food in foodList:
        tempDis = manhattanDistance(pos, food)
        if tempDis < disToFood:
            disToFood = tempDis
    for pellet in powerPellets:
        tempDis = manhattanDistance(pos, pellet)
        if tempDis < disToPellet:
            disToPellet = tempDis
    for ghost in GhostStates:
        tempDis = manhattanDistance(pos, ghost.getPosition())
        if tempDis < disToGhost:
            disToGhost = tempDis
        if disToGhost == 0 and ghost.scaredTimer > 0:
            return float("inf")
        if disToGhost < 1 and ghost.scaredTimer > 1:
            return 10000

    value = 4*(1.1/disToFood) + disToGhost*0.75 + 5*(1/disToPellet)
    return currentGameState.getScore() + value*1.3

# Abbreviation
better = betterEvaluationFunction
