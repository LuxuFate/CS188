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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    path = []
    visited = []
    visited.append(problem.getStartState())
    stack = util.Stack()
    for successor in problem.getSuccessors(problem.getStartState()):
        stack.push((successor, [successor[1]]))
        # (((4, 5), 'West', 1), ['West'])
    currState = problem.getStartState()
    while not stack.isEmpty():
        currState = stack.pop()
        if problem.isGoalState(currState[0][0]):
            path = currState[1]
            break
        if currState[0][0] not in visited:
            visited.append(currState[0][0])
            for s in problem.getSuccessors(currState[0][0]):
                if s[0] not in visited:
                    stack.push((s, currState[1]+[s[1]]))
    return path

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    path = []
    visited = []
    queue = util.Queue()
    queue.push((problem.getStartState(), path))
    while not queue.isEmpty():
        currState = queue.pop()
        #print(currState)
        position = currState[0]
        path = [i for i in currState[1]]
        if position not in visited:
            visited.append(position)
            if problem.isGoalState(position):
                return path
            for s in problem.getSuccessors(position):
                if s[0] not in visited:
                    queue.push((s[0], path + [s[1]]))
    return path

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    path = []
    visited = []
    visited.append(problem.getStartState())
    pqueue = util.PriorityQueue()
    for successor in problem.getSuccessors(problem.getStartState()):
        pqueue.push((successor, [successor[1]]), problem.getCostOfActions([successor[1]]))
        # (((4, 5), 'West', 1), ['West'])
    currState = problem.getStartState()
    while not pqueue.isEmpty():
        currState = pqueue.pop()
        if problem.isGoalState(currState[0][0]):
            path = currState[1]
            break
        if currState[0][0] not in visited:
            visited.append(currState[0][0])
            for s in problem.getSuccessors(currState[0][0]):
                if s[0] not in visited:
                    action = currState[1]+[s[1]]
                    pqueue.update((s, action), problem.getCostOfActions(action))
    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    path = []
    visited = []
    visited.append(problem.getStartState())
    pqueue = util.PriorityQueue()
    for successor in problem.getSuccessors(problem.getStartState()):
        cost = problem.getCostOfActions([successor[1]]) + heuristic(successor[0], problem)
        pqueue.update((successor, [successor[1]]), cost)
        # (((4, 5), 'West', 1), ['West'])
    currState = problem.getStartState()
    while not pqueue.isEmpty():
        currState = pqueue.pop()
        if problem.isGoalState(currState[0][0]):
            path = currState[1]
            break
        if currState[0][0] not in visited:
            visited.append(currState[0][0])
            for s in problem.getSuccessors(currState[0][0]):
                if s[0] not in visited:
                    action = currState[1]+[s[1]]
                    cost = problem.getCostOfActions(action) + heuristic(s[0], problem)
                    pqueue.update((s, action), cost)
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
