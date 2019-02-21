from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.
        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.
        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        allDisks = [parse_input("fact: (on ?x peg1)"), parse_input("fact: (on ?x peg2)"), parse_input("fact: (on ?x peg3)")]

        allBindings = [self.kb.kb_ask(i) for i in allDisks]
        numList = []

        for i in allBindings:
            if i:
                miniList = []
                for j in i:
                    
                    for k in j.bindings:
                        miniList.append(int(str(k)[-1]))
                        miniList.sort()
                numList.append(tuple(miniList))
            else:
                numList.append(tuple())

        numList = tuple(numList)
        return numList

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        ### Student code goes here
        stateTerms = movable_statement.terms
        dstPeg = stateTerms[2]
        srcPeg = stateTerms[1]
        disk = stateTerms[0]

        self.kb.kb_retract(Fact(["top", disk, srcPeg]))
        self.kb.kb_retract(Fact(["on", disk, srcPeg]))
        newTop = str(self.kb.kb_ask(Fact(["topOf", disk, "?disk"]))[0].bindings[0].constant)
        self.kb.kb_assert(Fact(["top", newTop, srcPeg]))
        self.kb.kb_assert(Fact(["on", disk, dstPeg]))
        self.kb.kb_retract(Fact(["topOf", disk, newTop]))
        oldTop = str(self.kb.kb_ask(Fact(["top", "?disk", dstPeg]))[0].bindings[0].constant)
        self.kb.kb_assert(Fact(["topOf", disk, oldTop]))
        self.kb.kb_retract(Fact(["top", oldTop, dstPeg]))
        self.kb.kb_assert(Fact(["top", disk, dstPeg]))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))


class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        myList = [[0, 0, 0], [0, 0,0], [0, 0,0]]
        allTiles = self.kb.kb_ask(parse_input("fact: (pos ?tile ?posx ?posy)"))
        
        for t in allTiles:
            myTile = str(t.bindings_dict["?tile"][4])
            
            if myTile == "y":
                myTile = -1
            else:
                myTile = int(myTile)

            row = int(t.bindings_dict["?posx"][-1]) - 1
            col = int(t.bindings_dict["?posy"][-1]) - 1

            myList[col][row] = myTile

        for i in range(len(myList)):
            myList[i] = tuple(myList[i])

        return tuple(myList)
        


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        stateTerms = movable_statement.terms
        dstY = stateTerms[4]
        dstX = stateTerms[3]
        srcY = stateTerms[2]
        srcX = stateTerms[1]
        tile = stateTerms[0]
        if self.kb.kb_ask(Fact(["pos", "?empty", dstX, dstY])):
            self.kb.kb_retract(Fact(["pos", tile, srcX, srcY]))
            # move empty block to previous
            self.kb.kb_retract(Fact(["pos", "?empty", dstX, dstY]))
            self.kb.kb_assert(Fact(["pos", tile, dstX, dstY]))
            self.kb.kb_assert(Fact(["pos", "empty", srcX, srcY]))
            
            

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
