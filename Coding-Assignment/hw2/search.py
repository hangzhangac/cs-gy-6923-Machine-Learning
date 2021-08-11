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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    dic=dict() #key:(pointx,pointy) value:( (last pointx,last pointy), direction from last point)
    stack=util.Stack()
    stack.push(problem.getStartState()) #push the start state to stack
    dic[problem.getStartState()]=() # the start state do not come from any points, so its value is set to empty tuple
    visit=set() # "visit" is used to record the point which has been visited
    goal_state=None #record the goal state
    while not stack.isEmpty():
        cur_state=stack.pop() #current state
        if problem.isGoalState(cur_state):
            goal_state=cur_state #we find the goal 
            break
        else:
            if cur_state not in visit:
                visit.add(cur_state)
                for next_state_info in problem.getSuccessors(cur_state):
                    next_state,direction,cost=next_state_info
                    if next_state in visit: #the state has been visited
                        continue
                    dic[next_state]=(cur_state,direction) # record the path(from current state to next state)  
                    stack.push(next_state) 
    cur_state=goal_state
    ans_direction_list=[] #the answer
    while len(dic[cur_state])!=0:
        ans_direction_list.append(dic[cur_state][1]) #append the direction in reverse order
        cur_state=dic[cur_state][0]
    

    #print(type(problem.getStartState()))
    #print(type(problem).__name__)
    #print("Start:", problem.getStartState())
    #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #print("Start's successors:", problem.getSuccessors(problem.getStartState()))
   # Start: (5, 5)
   # Is the start a goal? False
   # Start's successors: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
    return list(reversed(ans_direction_list)) #reverse the list to get the direction sequence in correct order

    "*** YOUR CODE HERE ***"
    
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    #There are so many same parts with DFS, so I do not have to write annotations is this funtion.
    dic=dict() #key:(pointx,pointy) value:( (last pointx,last pointy), direction from last point)
    queue=util.Queue()
    queue.push(problem.getStartState())
    dic[problem.getStartState()]=()
    goal_state=None
    while not queue.isEmpty():
        cur_state=queue.pop()
        if problem.isGoalState(cur_state):
            goal_state=cur_state
            break
        else:
            for next_state_info in problem.getSuccessors(cur_state):
                next_state,direction,cost=next_state_info
                if next_state in dic:
                    continue
                dic[next_state]=(cur_state,direction)   
                queue.push(next_state)

    cur_state=goal_state
    ans_direction_list=[]

    while len(dic[cur_state])!=0:
        ans_direction_list.append(dic[cur_state][1])
        cur_state=dic[cur_state][0]
    
    return list(reversed(ans_direction_list))  

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    dic=dict() #key:current state value:( last state, actions from start to current state,path_cost from start point)
    PQ=util.PriorityQueue()
    PQ.push(problem.getStartState(),0) # push the start state to priority_queue
    dic[problem.getStartState()]=(None,[],0) # the start state do not come from any points, so its value is set to empty tuple
    visit=set() # "visit" is used to record the point which has been visited
    goal_state=None #record the goal state
    while not PQ.isEmpty():
        cur_state=PQ.pop() #current state 
        visit.add(cur_state) # set current state to a visited status
        cur_actions=dic[cur_state][1]
        if problem.isGoalState(cur_state):
            goal_state=cur_state #we find the goal, so we can break the loop
            break
        else:
            for next_state_info in problem.getSuccessors(cur_state):
                next_state,direction,cost=next_state_info
                if next_state in visit: #the state has been visited
                    continue
                cost=problem.getCostOfActions(cur_actions+[direction])
                if next_state not in dic: # the first time we arrive at next_state
                    dic[next_state]=(cur_state,cur_actions+[direction],cost) # record the path and actions sequence(from current state to next state)  
                    PQ.push(next_state,cost)
                elif dic[next_state][2]>cost: # not the first time we arrive at next_state, so we compare the cost
                    dic[next_state]=(cur_state,cur_actions+[direction],cost) #if the new cost is less than old cost, we should update
                    PQ.update(next_state,cost)

    cur_state=goal_state
    return dic[cur_state][1]
    '''
    ans_direction_list=[] #the answer
    while dic[cur_state][0] is not None:
        ans_direction_list.append(dic[cur_state][1]) #append the direction in reverse order
        cur_state=dic[cur_state][0]
    
    return list(reversed(ans_direction_list)) #reverse the list to get the direction sequence in correct order
    '''
 

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
