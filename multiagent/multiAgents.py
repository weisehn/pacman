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
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newCapsules = successorGameState.getCapsules()
        cNum=len(newCapsules)
        fDistance = 9999.0
        cDistance = 9999.0
        pacmanPower = [0.0,0.0]
        ghostPower = [30.0,30.0]
        for food in newFood.asList():
            if fDistance >manhattanDistance(food,newPos):
                fDistance = manhattanDistance(food,newPos)
        if (fDistance==9999.0):
            fDistance=0.0
        for cap in newCapsules:
            if cDistance >manhattanDistance(cap,newPos):
                cDistance = manhattanDistance(cap,newPos)
        if (cDistance==9999.0):
            cDistance=0.0
        gDistance = [10.0,10.0]
        fNum = len(newFood.asList())
        score = successorGameState.getScore() - 0.1*fDistance -2.0*cDistance - 3.0*fNum - 600.0*cNum
        for i in range(len(newGhostStates)):
            gDistance [i] = manhattanDistance(newGhostStates[i].getPosition(),newPos)
            if newScaredTimes[i] == 0:
                pacmanPower[i]=1.0
            if newScaredTimes[i] != 0:
                pacmanPower[i] = 42.0
            if (gDistance[i] > 1 and pacmanPower[i]<ghostPower[i]):
                gDistance[i] = 10
            score += (ghostPower[i]-pacmanPower[i])*gDistance[i]
        return  score
        #return successorGameState.getScore()
        
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
        #util.raiseNotDefined()
        def minMax(gameState,depth,bow):
            num=gameState.getNumAgents()
            if(True):
                score=0
                bestScore=-99999
                if ((bow-depth)%num>0):
                    bestScore=99999
                legalMoves = gameState.getLegalActions((bow-depth)%num)
                actions=""
                if(len(legalMoves)==0):
                    return self.evaluationFunction(gameState)
                for action in legalMoves:
                    successorState=gameState.generateSuccessor((bow-depth)%num, action)
                    if(depth>1):
                        score = minMax (successorState,depth-1,bow)
                    if(depth==1):
                        score = self.evaluationFunction(successorState)
                    if ((bow-depth)%num==0):
                        if(bestScore<score):
                            bestScore=score
                            actions=action
                    if ((bow-depth)%num>0):
                        if(bestScore>score):
                            bestScore=score
                            actions=action
                #print actions
                if(depth==bow):
                    return actions
                return bestScore
        num= gameState.getNumAgents()
        legalMoves = gameState.getLegalActions()
        bestaction=minMax(gameState,self.depth*(num),self.depth*(num))
        return bestaction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        
        def alBt(gameState,depth,bow,al,bt):
            num=gameState.getNumAgents()
            if(True):
                score=0
                bestScore=88888
                legalMoves = gameState.getLegalActions((bow-depth)%num)
                actions=""
                if(len(legalMoves)==0):
                    return self.evaluationFunction(gameState)
                for action in legalMoves:
                    successorState=gameState.generateSuccessor((bow-depth)%num, action)
                    if(depth>1):
                        score = alBt (successorState,depth-1,bow,al,bt)
                    if(depth==1):
                        score = self.evaluationFunction(successorState)
                    if ((bow-depth)%num==0):
                        if(score>bt):
                            return score
                        if(score>al):
                            actions=action
                            al=score
                            bestScore=score
                    if ((bow-depth)%num>0):
                        if(score<al):
                            return score
                        if(score<bt):
                            actions=action
                            bt=score
                            bestScore=score
                    if(bestScore==88888):
                        bestScore = score
                if(depth==bow):
                    return actions
                return bestScore
        num=gameState.getNumAgents()
        bestaction=alBt(gameState,self.depth*num,self.depth*num,-99999,99999)
        return bestaction
        
        """
        def albt(gameState,depth,bow,al,bt):
            if(True):
                score=0
                bestScore=88888
                legalMoves = gameState.getLegalActions()
                actions=""
                if(len(legalMoves)==0):
                    return -self.evaluationFunction(gameState)
                for action in legalMoves:
                    successorState=gameState.generateSuccessor(0, action)
                    dlegalMoves = successorState.getLegalActions()
                    if(depth>1):
                        score = -albt (successorState,depth-1,bow,-bt,-al)
                    if(depth==1):
                        score = -self.evaluationFunction(successorState)
                    if(score>bt):
                        if(depth==bow):
                            return action
                        return bt
                    if (score>al):
                        actions=action
                        al=score
                        bestScore=score
                    if(bestScore==88888):
                        bestScore = score
                if(depth==bow):
                    return actions
                return bestScore
        num=gameState.getNumAgents()
        bestaction=albt(gameState,self.depth*num,self.depth*num,-99999,99999)
        return bestaction
        """
        """
        def MAX(gameState,al,bt):
            v =-99999
            legalMoves = gameState.getLegalActions()
            for action in legalMoves:
                successorState=gameState.generateSuccessor(0, action)
                v=MAX(v,MIN(successorState,al,bt))
                if v>bt:
                    return v
                al=max(al,v)
            return v
        
        def MIN(gameState,al,bt):
            v =99999
            legalMoves = gameState.getLegalActions()
            for action in legalMoves:
                successorState=gameState.generateSuccessor(0, action)
                v=MIN(v,MAX(successorState,al,bt))
                if v<al:
                    return v
                bt=min(bt,v)
            return v
        
        """
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
        #util.raiseNotDefined()
        def expMax(gameState,depth,bow):
            num=gameState.getNumAgents()
            if(True):
                i=0.0
                score=0.0
                bestScore=-99999.0
                if ((bow-depth)%num>0):
                    bestScore=0.0
                legalMoves = gameState.getLegalActions((bow-depth)%num)
                actions=""
                if(len(legalMoves)==0):
                    return self.evaluationFunction(gameState)
                for action in legalMoves:
                    successorState=gameState.generateSuccessor((bow-depth)%num, action)
                    if(depth>1):
                        score = expMax (successorState,depth-1,bow)
                    if(depth==1):
                        score = self.evaluationFunction(successorState)
                    if ((bow-depth)%num==0):
                        if(bestScore<score):
                            bestScore=score
                            actions=action
                    if ((bow-depth)%num>0):
                        bestScore=(bestScore*i+score)/(i+1.0)
                        i+=1.0
                        actions=action
                if(depth==bow):
                    return actions
                return bestScore
        num=gameState.getNumAgents()
        bestaction=expMax(gameState,self.depth*(num),self.depth*(num))
        return bestaction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newCapsules = currentGameState.getCapsules()
    cNum=len(newCapsules)
    fDistance = 9999.0
    cDistance = 9999.0
    pacmanPower = [0.0,0.0]
    ghostPower = [30.0,30.0]
    for food in newFood.asList():
        if fDistance >manhattanDistance(food,newPos):
            fDistance = manhattanDistance(food,newPos)
    if (fDistance==9999.0):
        fDistance=0.0
    for cap in newCapsules:
        if cDistance >manhattanDistance(cap,newPos):
            cDistance = manhattanDistance(cap,newPos)
    if (cDistance==9999.0):
        cDistance=0.0
    gDistance = [10.0,10.0]
    fNum = len(newFood.asList())
    score = currentGameState.getScore() - 0.1*fDistance -2.0*cDistance - 3.0 * fNum - 600 * cNum
    for i in range(len(newGhostStates)):
        gDistance [i] = manhattanDistance(newGhostStates[i].getPosition(),newPos)
        if newScaredTimes[i] == 0:
            pacmanPower[i]=1.0
        if newScaredTimes[i] != 0:
            pacmanPower[i] = 42.0
        if (gDistance[i] > 0 and pacmanPower[i]<ghostPower[i]):
            gDistance[i] = 10
        score += (ghostPower[i]-pacmanPower[i])*gDistance[i]
    return  score

    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newCapsules = currentGameState.getCapsules()
    cNum=len(newCapsules)
    fDistance = 9999.0
    for food in newFood.asList():
        if fDistance > util.rtDistance(food,newPos):
            fDistance = util.rtDistance(food,newPos)
    if (fDistance==9999.0):
        fDistance=0.0
    gDistance = [10.0,10.0]
    ghDistance=[10.0,10.0]
    score = currentGameState.getScore() - 0.1 * fDistance - cNum*1000
    for i in range(len(newGhostStates)):
        if newScaredTimes[i] == 0:
            gDistance [i] = util.rtDistance(newGhostStates[i].getPosition(),newPos)
        if newScaredTimes[i] != 0:
            ghDistance [i] = util.rtDistance(newGhostStates[i].getPosition(),newPos)
        if (gDistance[i] > 0):
            gDistance[i] = 10
        score += 200000.0 * (2.0**(gDistance[i])) -  ghDistance[i]
    return  score
    """
# Abbreviation
better = betterEvaluationFunction

