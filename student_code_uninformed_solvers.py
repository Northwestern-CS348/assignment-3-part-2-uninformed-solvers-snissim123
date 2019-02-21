from solver import *
from collections import deque

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        # Check to see if condition is met
        if self.gm.isWon():
            return True


        # mark as visited
        self.visited[self.currentState] = True
        # generate available moves
        possMoves = self.gm.getMovables()

        # go through each possible move
        for move in possMoves:
            self.gm.makeMove(move)

            gameState = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
            gameState.parent = self.currentState


            if gameState not in self.visited:
                self.currentState.children.append(gameState)
                self.visited[gameState] = False

            elif self.visited[gameState] == False:
                self.currentState.children.append(gameState)

            self.gm.reverseMove(move)

        # Which child we should be looking at 
        childNum = self.currentState.nextChildToVisit

        while self.currentState.depth != 0 and childNum == len(self.currentState.children):
            childNum = self.currentState.nextChildToVisit

            self.currentState = self.currentState.parent

            self.gm.reverseMove(self.currentState.requiredMovable)


        childNum = self.currentState.nextChildToVisit

        if self.visited[self.currentState.children[childNum]] == False:
            self.currentState.nextChildToVisit += 1

            self.gm.makeMove(self.currentState.children[childNum].requiredMovable)

            self.currentState = self.currentState.children[childNum]

        return False
   

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.myList = dict()
        self.myQueue = deque()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        # Check to see if condition is met
        if self.gm.isWon():
            return True

        # mark as visited
        self.visited[self.currentState] = True
        # generate available moves
        possMoves = self.gm.getMovables()

        if not self.currentState.depth:
            self.myList[self.currentState] = []

        # go through each possible move
        for move in possMoves:
            self.gm.makeMove(move)
            gameState = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
            gameState.parent = self.currentState

            if gameState not in self.visited:
                self.currentState.children.append(gameState)
                self.visited[gameState] = False
                self.myQueue.append(gameState)
                
                self.myList[gameState] = []
                for elem in self.myList[self.currentState]:
                    self.myList[gameState].append(elem)
                self.myList[gameState].append(gameState)
                
            self.gm.reverseMove(move)

        # Find list of moves before
        before = self.myList[self.currentState]
        before.reverse()
        self.currentState = self.myQueue.popleft()
        # undo those moves
        for move in before: 
            self.gm.reverseMove(move.requiredMovable)
        after = self.myList[self.currentState]
        for move in after: 
            self.gm.makeMove(move.requiredMovable)

        return False
        