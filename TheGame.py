__author__ = 'Hagar'

import random, math, csv, multiprocessing, Simulations,time, sys
from Visualization import *
from tkinter import *

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")


"""
    Adjacency list loaded from given csv file
""" 
def load_Adj():
    """ a dictionary representing adjacencies for each disc """
    AdjacencyDict = {}
    index = 0
    with open("AdjList.csv", 'r') as file:
        for row in file:
            row = [x.strip() for x in row.split(',')]
            row = list(filter(None,row))
            tempList = []
            index += 1
            for j in row[1:]:
                tempList.append(int(j))
            AdjacencyDict[index] = tempList
    file.close()
    return AdjacencyDict


class Board(object):
    """
    Board represents the color of discs on the board

    A board has 8* 8 tiles with 64 discs.
    The board is represented by a dictionary,
    each of the discs is either black ("B"), white ("W") or empty (None).
    """

    def __init__(self):

        # initializing discs color dictionary
        self.discsDict = {}
        for i in range (1,65):
            self.discsDict[i] = None
        # game starts with 2 black and 2 white discs at the centre of the board
        self.discsDict[28], self.discsDict[29], self.discsDict[36], self.discsDict[37] = "W", "B", "B", "W"

        # location coordination to discs dictionary
        self.locToDiscDict = {}
        m = 0
        for j in range(1, 9):
            for k in range(1, 9):
                m += 1
                self.locToDiscDict[j, k] = m

    def getDiscColor (self,disc):
        """
        Returns the color of a disc
        """
        return self.discsDict[disc]

    def updateDisc(self,disc,color):
        """
        Updates disc color in dictionary
        """
        self.discsDict[disc] = color

    def getDiscsDict(self):
        """ returns discs color dictionary"""
        return self.discsDict

    def numBlackandWhite(self):
        """returns the current number of black and white discs"""
        black = 0
        white = 0
        discs_dict = self.getDiscsDict()
        for disc in discs_dict:
            if discs_dict[disc] == "B": black += 1
            if discs_dict[disc] == "W": white += 1
        return black, white

    def getLocToDisc(self,x,y):
        """
        returns the disc number for location on board
        location is an x,y coordination
        Example: for the location 8,8 will return 64
        """
        return self.locToDiscDict[x,y]

    def getDiscToLoc(self,disc):
        """
        returns location on board as an x,y coordinate for disc number
        disc is an int
        Example: for the disc 64, will return the location 8,8
        """
        self.discToLocDict = {} # discs to location coordination dictionary
        for i in self.locToDiscDict:
            self.discToLocDict[self.locToDiscDict[i]] = i

        return self.discToLocDict[disc]


class Player (object):
    """
    Represents a player. A player has a color and number of moves
    """
    def __init__(self,playsFirst,color):
        """
        color: a string, the color of player's disc (either "B" for black or "W" for white).
        playsFirst: a boolean, indicates if the player is the one who plays first
        """
        self.playsFirst = playsFirst
        self.numMoves = 0 # number of moves by player
        self.color = color

    def GetNumMoves(self):
        """
        Returns number of moves for player so far.
        this will help to decide who should play next
        """
        return self.numMoves

    def updateNumMoves(self):
        """    Adds a move to player's number of moves   """
        self.numMoves += 1

    def getPlayerColor(self):
        return self.color

    def doesPlayFirst(self):
        """ check if current player was the firs player. Return boolean"""
        return self.playsFirst


class GameController (object):
    """
    GameController represents the enforcement of the game rules and logic.
    """
    def __init__(self,visualization):
        """
        Initializes two players and the Board class
        """
        # create two player objects:
        self.player1 = Player(True,"W")
        self.player2 = Player(False,"B")
        self.board = visualization.board
        self.player = self.player1 # this is the current player playing
        self.AdjacencyDict = load_Adj()
        self.visualization = visualization

    def whoIsNext(self):
        """
        Checks who's turn it is to play
        return: player object
        """
        if self.player1.GetNumMoves() == self.player2.GetNumMoves():
            return self.player1
        else:
            return self.player2

    def isValidMove(self,disc):
        """
        Checks if move is valid. disc is the move to be checked if valid
        disc is an int representing disc number
        return: True if valid, False if not
        """
        self.player = self.whoIsNext()

        # a move is valid only if current location on board is empty
        if self.board.getDiscColor(disc) is not None:
            return False

        discColor = self.player.getPlayerColor()
        if discColor == "W":
            cont = "B"
        else: cont = "W"

        flag = False
        # a move is valid if:
        #  chosen location on board is next to (at least one) opposite color disc
        # and is bounded by the disc just placed and another disc of the current player's color
        for neighbor in self.AdjacencyDict[disc]: # looping over all adjacent discs
            if self.board.getDiscColor(neighbor) == cont:  # check if adjacent disc is in opponent's color
                direction = neighbor - disc
                nextDisc = neighbor
                next2nextDisc = nextDisc + direction
                while not flag:
                    # check if next disc is adjacent (for example, disc 8 is not adjacent to 9. 9 is in a different row)
                    if next2nextDisc in self.AdjacencyDict[nextDisc]:
                        # if the next disc is in current player's color, we are done:
                        if self.board.getDiscColor(next2nextDisc) == discColor:
                            return True
                        # if the next disc is in opponent's color, we continue to the following disc:
                        elif self.board.getDiscColor(next2nextDisc) == cont:
                            nextDisc = next2nextDisc
                            next2nextDisc = nextDisc + direction
                        else: break # if the next disc is neither black nor white, it is empty
                    else: break # if neighboring disc is not in opponent's color, the move is not valid

        return flag

    def anyPossibleMoves(self):
        """checks if the current player has a possible next move in current situation"""
        self.player = self.whoIsNext()
        discDict = self.board.getDiscsDict()
        for i in discDict:
            if discDict[i] == None:
                if self.isValidMove(i):
                    return True
        return False


    def isGameOver(self):
        """
        Checks if game over
        return: True or False
        """

        black, white = self.board.numBlackandWhite()
        for key in range(1,65):
            if self.board.getDiscColor(key) is None and black > 0 and white > 0:
                return False
        else: return True

    def getWinner(self):
        """returns a string of the winner when game is over"""
        black, white = self.board.numBlackandWhite()
        if black > white:
            return "black"
        elif black == white:
            return "no one"
        else:
            return "white"

    def updateColorDiscs(self,disc):
        """
        colors adjacent discs in accordance with chosen location for disc on board and game rules
         disc is player's chosen move
         disc is an int representing disc number
         """

        # check the color of current player:
        self.player = self.whoIsNext()
        discColor = self.player.getPlayerColor()
        if discColor == "W":
            cont = "B"
        else:
            cont = "W"

        nbrList = [] # this is the list of neighbors
        # check which discs need to be colored
        for neighbor in self.AdjacencyDict[disc]:  # looping over all adjacent discs
            flag = False
            counter = 0
            if self.board.getDiscColor(neighbor) == cont:  # check if adjacent disc is in opponent's color
                direction = neighbor - disc
                nextDisc = neighbor
                next2nextDisc = nextDisc + direction
                while not flag:
                    counter += 1 # accounting for number of discs consecutively
                    # check if next disc is adjacent (for example, disc 8 is not adjacent to 9. 9 is in a different row)
                    if next2nextDisc in self.AdjacencyDict[nextDisc]:
                        # if the next disc is in current player's color, we are done:
                        if self.board.getDiscColor(next2nextDisc) == discColor:
                            flag = True
                            # the adjacent disc and number of consecutively discs are added to the list:
                            nbrList.append([neighbor, counter])
                        # if the next disc is in opponent's color, we continue to the following disc:
                        elif self.board.getDiscColor(next2nextDisc) == cont:
                            nextDisc = next2nextDisc
                            next2nextDisc = nextDisc + direction
                        else: break  # if the next disc is neither black nor white, it is empty and hence invalid
                    else: break

                if flag:
                    # now we have a list of all neighboring list to be colored
                    # and the number of following discs to be colored as well
                    nbrList.append([neighbor, counter])
        # create a list of the discs which need to be colored
        self.updateList=[]
        self.updateList.append(disc)
        for nbr in nbrList:
            angle = nbr[0] - disc
            for distance in range(nbr[1]):
                x = nbr[0] + angle * distance
                self.updateList.append(x)

        # update discs in main dictionary
        for disc in self.updateList:
            self.board.updateDisc(disc,discColor)
        # add move to number of moves for player
        self.player.updateNumMoves()

        return self.updateList

    def computerPlaying(self):
        """activates the computer as a player by using simulation (file: Simulations)
        returns: disc number"""
        print('computer playing')
        # arguments for the simulations:
        discDictCopy = self.board.getDiscsDict().copy()
        player1Color = self.whoIsNext().getPlayerColor()
        player1Moves = self.whoIsNext().GetNumMoves()
        player2Moves = self.whoIsNext().GetNumMoves() + 1
        AdjacencyDict = self.AdjacencyDict

        manager = Simulations.SimulationManager()  # initializing the simulation manager
        args = (discDictCopy,player1Color,player1Moves,player2Moves,AdjacencyDict)
        args_list = []
        for i in range(10):  # this range determines the number of simulations; the multiprocessing method will go over all args tuple in the args_list
            args_list.append(args)

        result = manager.run(args_list)

        # self.visualization.w.delete(self.line1)
        # self.visualization.w.delete(self.text5)

        resultsDict = {}
        for Rdict in result:  # for the result of each simulation
            RdictValue = Rdict.__iter__().__next__()  # dictionary key
            if Rdict[RdictValue] == 1:  # if simulation was successful,
                resultsDict[RdictValue] = resultsDict.get(RdictValue, 0) + 1  # increment result
        maxMove = 0
        winner = 0
        for move in resultsDict:
            if resultsDict[move] > maxMove:
                maxMove = resultsDict[move]
                winner = move
        if winner == 0:  # if all simulations lost the game
            disc = result[0].__iter__().__next__()  # choose the first move of the first game
        else: disc = winner

        updateList = self.updateColorDiscs(disc)

        self.visualization.computerPlayingVisual(disc, updateList)



class NoPossibleMovesException(Exception):
    """ NoPossibleMovesException is raised by the possible moves() method in the simulations
    class to indicate that there are no possible moves for player in current situation"""


"""STARTING THE GAME"""

if __name__ == '__main__':
    #AdjacencyDict = load_Adj()
    game = BoardVisualization()

