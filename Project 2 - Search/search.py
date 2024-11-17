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
    from util import Stack
    frontiera = Stack() #initializam stiva 
    frontiera.push((problem.getStartState(), [], []))
    vizitate = set()
    while not frontiera.isEmpty():
        stare, actiuni, cale = frontiera.pop()
        if stare in vizitate:
            continue
        vizitate.add(stare) #marcam starea ca fiind vizitata
        if problem.isGoalState(stare): #vizitam daca am ajuns la obiectiv (*)
            return actiuni #(*)si returnam secventa care ne a adus acolo
        for succesor, actiune, costPas in problem.getSuccessors(stare):
            if succesor not in vizitate:
                frontiera.push((succesor, actiuni + [actiune], cale + [stare]))
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    frontiera = Queue()
    frontiera.push((problem.getStartState(), []))
    vizitate = set()
    while not frontiera.isEmpty():
        stare, actiuni = frontiera.pop()
        if problem.isGoalState(stare):
            return actiuni
        if stare not in vizitate: #daca starea nu a fost vizitata anterior, o marchez ca vizitata
            vizitate.add(stare)
            for succesor, actiune, costPas in problem.getSuccessors(stare):
                if succesor not in vizitate:
                    frontiera.push((succesor, actiuni + [actiune])) #adaugam succesorul in coada
    return []  #daca nu gasim nici o cale se returneaza o lista goala

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    frontiera = PriorityQueue() #initializam coada
    frontiera.push((problem.getStartState(), []), 0)
    costuri_vizitate = {problem.getStartState(): 0}
    while not frontiera.isEmpty():
        stare, actiuni = frontiera.pop()
        if problem.isGoalState(stare): #daca s a ajuns la goal, se returneaza secventa de actiuni
            return actiuni
        for succesor, actiune, costPas in problem.getSuccessors(stare):
            cost_nou = costuri_vizitate[stare] + costPas
            if succesor not in costuri_vizitate or cost_nou < costuri_vizitate[succesor]: #daca succesorul nu a fost vizitat sau s a gasit un cost mai mic
                costuri_vizitate[succesor] = cost_nou
                frontiera.push((succesor, actiuni + [actiune]), cost_nou)
    return []  #daca nu gasim nici o cale se returneaza o lista goala

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    frontiera = PriorityQueue() #initializam coada de prioritati cu start_state si costul total ca fiind 0
    start_state = problem.getStartState()
    frontiera.push((start_state, [], 0), 0) 
    costuri_vizitate = {start_state: 0}
    while not frontiera.isEmpty():
        stare, actiuni, cost_total = frontiera.pop()
        if problem.isGoalState(stare): #daca s a ajuns la goal, se returneaza secventa de actiuni
            return actiuni
        for succesor, actiune, costPas in problem.getSuccessors(stare):
            cost_nou = cost_total + costPas
            if succesor not in costuri_vizitate or cost_nou < costuri_vizitate[succesor]:
                costuri_vizitate[succesor] = cost_nou
                prioritate = cost_nou + heuristic(succesor, problem)
                frontiera.push((succesor, actiuni + [actiune], cost_nou), prioritate)
    return []  #daca nu gasim nici o cale se returneaza o lista goala

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
