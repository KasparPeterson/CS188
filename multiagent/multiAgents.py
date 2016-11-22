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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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

        GhostState:
            self.start = startConfiguration
            self.configuration = startConfiguration
                Configuration:
                    self.pos = pos
                    self.direction = direction
            self.isPacman = isPacman
            self.scaredTimer = 0
            self.numCarrying = 0
            self.numReturned = 0

        Food (Grid):


        Evaluation:
            1) If ghost is coming to our planned position then -1000
                - If ghost is near us with Manhattan distance 2 then -500
            2) If we eat food in next position +100
            3) If next most close food is better than current then +10

        """
        GHOST = -1000000
        GHOST_CLOSE = -10000
        KILL_GHOST = 1000
        KILL_GHOST_POSSIBLE = 100
        FOOD_CLOSER = 100
        FOOD = 1000

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        currentPos = currentGameState.getPacmanPosition()
        currentFood = currentGameState.getFood()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        result = 0

        # Is ghost in our position?
        for ghostState in newGhostStates:
            if ghostState.scaredTimer < 3:
                if manhattanDistance(ghostState.configuration.pos, newPos) < 1:
                    result += GHOST
                elif manhattanDistance(ghostState.configuration.pos, newPos) < 3:
                    result += GHOST_CLOSE
            else:
                if manhattanDistance(ghostState.configuration.pos, newPos) < 1:
                    result += KILL_GHOST
                elif manhattanDistance(ghostState.configuration.pos, newPos) < 3:
                    result += KILL_GHOST_POSSIBLE

        # Is there food in our next position
        if len(newFood.asList()) < len(currentFood.asList()):
            result += FOOD

        # Are we getting closer to food?
        oldClosestFood = findClosestFoodManhattanDistance(currentPos, currentFood.asList())
        newClosestFood = findClosestFoodManhattanDistance(newPos, newFood.asList())

        if newClosestFood < oldClosestFood:
            result += FOOD_CLOSER

        return result

def scoreEvaluationFunction(currentGameState):
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
        python autograder.py -t test_cases/q2/0-small-tree.test
    """
    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        scores = []
        legalMoves = gameState.getLegalActions()
        for action in legalMoves:
            scores.append(self.minValue(self.depth, gameState.generateSuccessor(0, action), 1))
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def maxValue(self, depth, gameState):
        if depth == 0:
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(0)
        if not legalActions:
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

        best_value = -99999999999

        for action in legalActions:
            value = self.minValue(depth, gameState.generateSuccessor(0, action), 1)
            if value > best_value:
                best_value = value
        return best_value

    def minValue(self, depth, gameState, agentIndex):
        if depth == 0:
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

        best_value = 99999999999
        for action in legalActions:
            if agentIndex + 1 < gameState.getNumAgents():
                value = self.minValue(depth, gameState.generateSuccessor(agentIndex, action), agentIndex + 1)
            else:
                value = self.maxValue(depth - 1, gameState.generateSuccessor(agentIndex, action))

            if value < best_value:
                best_value = value
        return best_value

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        scores = []
        legalMoves = gameState.getLegalActions()
        alfa = -999999999
        beta = 999999999
        for action in legalMoves:
            v = self.minValue(self.depth, gameState.generateSuccessor(0, action), 1, alfa, beta)
            scores.append(v)
            alfa = max(alfa, v)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def maxValue(self, depth, gameState, alfa, beta):
        if depth == 0:
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(0)
        if not legalActions:
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

        v = -99999999999
        for action in legalActions:
            value = self.minValue(depth, gameState.generateSuccessor(0, action), 1, alfa, beta)
            v = max(v, value)

            if v > beta:
                return v

            alfa = max(alfa, v)
        return v

    def minValue(self, depth, gameState, agentIndex, alfa, beta):
        if depth == 0:
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

        v = 99999999999
        for action in legalActions:
            if agentIndex + 1 < gameState.getNumAgents():
                value = self.minValue(depth, gameState.generateSuccessor(agentIndex, action), agentIndex + 1, alfa, beta)
            else:
                value = self.maxValue(depth - 1, gameState.generateSuccessor(agentIndex, action), alfa, beta)

            v = min(v, value)

            if v < alfa:
                return v

            beta = min(beta, v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        scores = []
        legalMoves = gameState.getLegalActions()
        for action in legalMoves:
            v = self.expectiMax(self.depth, gameState.generateSuccessor(0, action), 1)
            scores.append(v)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def expectiMax(self, depth, gameState, agentIndex):
        if depth == 0:
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(agentIndex)
        if not legalActions:
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

        sum = 0
        actionCount = 0
        for action in legalActions:
            if agentIndex + 1 < gameState.getNumAgents():
                value = self.expectiMax(depth, gameState.generateSuccessor(agentIndex, action), agentIndex + 1)
            else:
                value = self.maxValue(depth - 1, gameState.generateSuccessor(agentIndex, action))
            sum += value
            actionCount += 1
        return sum / actionCount

    def maxValue(self, depth, gameState):
        if depth == 0:
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(0)
        if not legalActions:
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

        v = -99999999999
        for action in legalActions:
            value = self.expectiMax(depth, gameState.generateSuccessor(0, action), 1)
            v = max(v, value)
        return v

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def findClosestFoodManhattanDistance(pos, foodList):
    closest_food = 99999999
    for food in foodList:
        food_distance = manhattanDistance(food, pos)
        if food_distance < closest_food:
            closest_food = food_distance
    return closest_food

# Abbreviation
better = betterEvaluationFunction

