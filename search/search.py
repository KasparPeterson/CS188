# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


class Node:

    def __init__(self, state, action=None, path_cost=0, parent=None):
        self.state = state
        self.action = action
        self.path_cost = path_cost
        self.parent = parent

    def expand(self, problem):
        """
        Returns the possible Nodes reachable from this Node
        """
        successor_nodes = list()
        for successor_triple in problem.getSuccessors(self.state):
            successor, action, step_cost = successor_triple
            successor_nodes.append(Node(successor, action, step_cost, self))
        return successor_nodes

    def solution(self):
        actions = self.get_actions(self)
        actions.reverse()
        return actions

    def path(self):
        print "TODO: path!!, state is: ", self.state

    def get_actions(self, node, actions=None):
        if actions is None:
            actions = list()
        if node.action is not None:
            actions.append(node.action)
        if node.parent is not None:
            return self.get_actions(node.parent, actions)
        return actions

    def __eq__(self, other):
        return self.state == other.state

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    frontier = util.Stack()
    explored = set()
    frontier.push(Node(problem.getStartState()))
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return node.solution()
        explored.add(node.state)
        successor_nodes = node.expand(problem)
        for node in successor_nodes:
            if node.state not in explored:
                frontier.push(node)
    return None


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    frontier = util.Queue()
    explored = set()
    frontier.push(Node(problem.getStartState()))
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return node.solution()
        explored.add(node.state)
        successor_nodes = node.expand(problem)
        for node in successor_nodes:
            if node.state not in explored and not isInFrontier(node, frontier):
                frontier.push(node)
    return None


def graph_search(problem, frontier):
    explored = set()
    frontier.push(Node(problem.getStartState()))
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return node.solution()
        explored.add(node.state)
        successor_nodes = node.expand(problem)
        for node in successor_nodes:
            if node.state not in explored and not isInFrontier(node, frontier):
                frontier.push(node)
    return None


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    explored = set()
    frontier = util.PriorityQueue()
    frontier.push(Node(problem.getStartState()), 0)
    while not frontier.isEmpty():
        node = frontier.pop()
        print "Exploring state: "
        print node.state
        if problem.isGoalState(node.state):
            return node.solution()
        explored.add(node.state)
        successor_nodes = node.expand(problem)
        for node in successor_nodes:
            if node.state not in explored:
                frontier.update(node, problem.getCostOfActions(node.solution()))
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    explored = set()
    frontier = util.PriorityQueue()
    frontier.push(Node(problem.getStartState()), 0)
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return node.solution()
        explored.add(node.state)
        successor_nodes = node.expand(problem)
        for node in successor_nodes:
            if node.state not in explored:
                path_cost = problem.getCostOfActions(node.solution())
                heuristic_cost = heuristic(node.state, problem)
                frontier.update(node, path_cost + heuristic_cost)
    return None

def isInFrontier(element, frontier):
    # Frontier can be either Stack or Queue
    for e in frontier.list:
        if e.state == element.state:
            return True
    return False


def isInPriorityQueue(element, priorityQueue):
    for e in priorityQueue.heap:
        if e[2].state == element.state:
            return True
    return False

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
