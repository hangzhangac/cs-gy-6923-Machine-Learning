# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state) #how to use this function
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        print(self.values[5])
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        discount=self.discount
        value=[util.Counter(),util.Counter()]
        mdp=self.mdp
        inf=999999999
        for k in range(self.iterations):
            value[1]=util.Counter()
            all_states=mdp.getStates()
            for state in all_states:
                if mdp.isTerminal(state):
                    value[1][state]=0
                    continue
                actions=mdp.getPossibleActions(state)
                max_v=-inf;
                for action in actions:
                    expected_sum=0
                    next_state_probs=mdp.getTransitionStatesAndProbs(state, action)
                    for next_state,prob in next_state_probs:
                        reward=mdp.getReward(state,action,next_state)
                        expected_sum+=prob*(reward+discount*value[0][next_state])
                    max_v=max(max_v, expected_sum)
                value[1][state]=max_v
                #if max_v!=-inf: #there is at least one valid action and next_state
                #    value[1][state]=max_v
                #else:
                #    value[1][state]=0
            value[0]=value[1]
        self.values=value[0]

        "*** YOUR CODE HERE ***"


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        mdp=self.mdp
        next_state_probs=mdp.getTransitionStatesAndProbs(state, action)
        expected_sum=0
        for next_state,prob in next_state_probs:
            reward=mdp.getReward(state,action,next_state)
            expected_sum+=prob*(reward+self.discount*self.values[next_state])
        return expected_sum
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        inf=999999999
        mdp=self.mdp
        actions=mdp.getPossibleActions(state)
        max_v=-inf;
        ans_action=None
        for action in actions:
            expected_sum=0
            next_state_probs=mdp.getTransitionStatesAndProbs(state, action)
            for next_state,prob in next_state_probs:
                reward=mdp.getReward(state,action,next_state)
                expected_sum+=prob*(reward+self.discount*self.values[next_state])
            if max_v<=expected_sum:
                ans_action=action
                max_v=expected_sum
        return ans_action
        "*** YOUR CODE HERE ***"
        
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        # Write value iteration code here
        discount=self.discount
        #value=[util.Counter(),util.Counter()]
        mdp=self.mdp
        all_states=mdp.getStates()
        num_states=len(all_states)
        inf=999999999
        cur_state_id=0
        value=util.Counter()

        for k in range(self.iterations):
            state=all_states[cur_state_id]
            cur_state_id=(cur_state_id+1)%num_states
            if mdp.isTerminal(state):
                #value[1][state]=0
                continue
            actions=mdp.getPossibleActions(state)
            max_v=-inf;
            for action in actions:
                expected_sum=0
                next_state_probs=mdp.getTransitionStatesAndProbs(state, action)
                for next_state,prob in next_state_probs:
                    reward=mdp.getReward(state,action,next_state)
                    expected_sum+=prob*(reward+discount*value[next_state])
                max_v=max(max_v, expected_sum)
            if max_v!=-inf: #there is at least one valid action and next_state
                value[state]=max_v
            else:
                value[state]=0
        self.values=value

        "*** YOUR CODE HERE ***"

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

