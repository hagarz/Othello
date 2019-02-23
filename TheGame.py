__author__ = 'Hagar'

import random, math, csv, multiprocessing, Simulations
from tkinter import *


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
        dict = self.getDiscsDict()
        for disc in dict:
            if dict[disc] == "B": black += 1
            if dict[disc] == "W": white += 1
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
    def __init__(self, board):
        """
        Initializes two players and the Board class

        """
        # create two player objects:
        self.player1 = Player(True,"W")
        self.player2 = Player(False,"B")
        self.board = board
        self.player = self.player1 # this is the current player playing


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
        for neighbor in AdjacencyDict[disc]: # looping over all adjacent discs
            if self.board.getDiscColor(neighbor) == cont:  # check if adjacent disc is in opponent's color
                direction = neighbor - disc
                nextDisc = neighbor
                next2nextDisc = nextDisc + direction
                while not flag:
                    # check if next disc is adjacent (for example, disc 8 is not adjacent to 9. 9 is in a different row)
                    if next2nextDisc in AdjacencyDict[nextDisc]:
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

    def isPossibleMove(self):
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
        w = 0
        b = 0
        for key in range (1,65):
            if self.board.getDiscColor(key) == "B":
                b += 1
            if self.board.getDiscColor(key) == "W":
                w += 1
            if self.board.getDiscColor(key) is None and b>0 and w>0:
                return False
        else: return True

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
        for neighbor in AdjacencyDict[disc]:  # looping over all adjacent discs
            flag = False
            counter = 0
            if self.board.getDiscColor(neighbor) == cont:  # check if adjacent disc is in opponent's color
                direction = neighbor - disc
                nextDisc = neighbor
                next2nextDisc = nextDisc + direction
                while not flag:
                    counter += 1 # accounting for number of discs consecutively
                    # check if next disc is adjacent (for example, disc 8 is not adjacent to 9. 9 is in a different row)
                    if next2nextDisc in AdjacencyDict[nextDisc]:
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


class BoardVisualization:
    """
    creating a GUI of the game using tkinter
    This is the main loop of the game
    """
    def __init__(self):
        """Initializes visualization with the specified parameters"""

        self.board = Board()
        self.play = GameController(self.board)
        self.player = self.play.whoIsNext()

        # Initialize a drawing surface
        self.master = Tk()
        self.text = Text(self.master)
        self.text.config(state=DISABLED)
        self.w = Canvas(self.master, width=500, height=500)
        self.w.pack()
        self.master.update()

        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(8, 8)
        self.w.create_rectangle(x1, y1, x2, y2, fill="green")

        # Draw gridlines
        for i in range(9):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, 8)
            self.w.create_line(x1, y1, x2, y2)
        for i in range(9):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(8, i)
            self.w.create_line(x1, y1, x2, y2)

        # draw first 4 discs in the center
        xb1,yb1 = 5,4
        xb2,yb2 = 4,5
        xw1,yw1 = 4,4
        xw2,yw2 = 5,5
        self.w.create_oval([xw1*55-20, yw1*55-20, xw1*55+20, yw1*55+20], fill="white")
        self.w.create_oval([xb1*55-20, yb1*55-20, xb1*55+20, yb1*55+20], fill="black")
        self.w.create_oval([xw2*55-20, yw2*55-20, xw2*55+20, yw2*55+20], fill="white")
        self.w.create_oval([xb2*55-20, yb2*55-20, xb2*55+20, yb2*55+20], fill="black")

        # Draw some status text
        self.status_text = self.w.create_text(25, 3, font="Verdana 11 bold", anchor=NW, fill="blue",
                                              text=self._status_string())
        self.status_text2 = self.w.create_text(25, 478, font="Verdana 11 bold", anchor=NW, fill="blue",
                                        text=self._status_string2())

        # create message texts for later
        self.text2 = self.w.create_text(200, 200, fill="red", font="bold", text="Invalid move. Try again")
        self.r = self.w.create_rectangle(self.w.bbox(self.text2), fill="white")
        self.w.tag_lower(self.r, self.text2)
        self.text3 = self.w.create_text(250, 250, anchor=CENTER, fill="purple",
                                        font="Times 250 bold", text="GAME OVER")
        self.r3 = self.w.create_rectangle(self.w.bbox(self.text3), fill="black")
        self.text4 = self.w.create_text(250, 250, anchor=CENTER, text="No possible moves ")
        self.r4 = self.w.create_rectangle(self.w.bbox(self.text4), fill="white")
        self.text5 = self.w.create_text(135, 20, font="Verdana 12 bold", fill="red", anchor=NW, text="BLACK")
        self.text6 = self.w.create_text(250, 250, anchor=CENTER, text="No possible moves ")
        self.r6 = self.w.create_rectangle(self.w.bbox(self.text6), fill="white")
        self.w.delete(self.text2)
        self.w.delete(self.r)
        self.w.delete(self.text3)
        self.w.delete(self.r3)
        self.w.delete(self.text4)
        self.w.delete(self.r4)
        self.w.delete(self.text5)
        self.w.delete(self.text6)
        self.w.delete(self.r6)

        self.line1 = self.w.create_line(15, 25, 200, 25, dash=(4, 2), fill="yellow")
        self.w.delete(self.line1)

        # event trigger - mouse-click
        self.w.bind("<Button-1>",self.mouse_click)
        self.master.update()

        # main loop
        self.master.mainloop()


    def _status_string(self):
        """Returns an appropriate status string to print:
        what player is playing now, number of black and white discs and what percent of the board is full"""

        if self.play.whoIsNext().getPlayerColor() == "W": self.playing="WHITE"
        else: self.playing = "BLACK"
        return f"Now playing: {str(self.playing)}"

    def _status_string2(self):
        """Returns an appropriate status string to print:
        what player is playing now, number of black and white discs and what percent of the board is full"""
        self.num_black = self.board.numBlackandWhite()[0]
        self.num_white = self.board.numBlackandWhite()[1]
        self.percent_full = round(100*((self.num_black + self.num_white)/64))
        return f"White: {self.num_white},  Black: {self.num_black};  {self.percent_full}% filled"

    def _map_coords(self,x,y):
        """ Maps grid positions to window positions (in pixels)"""
        return (250+450*(x-4)/8,250+450*(4-y)/8)

    def mouse_click(self,location):
        """triggered by mouse click on board game"""

        # converting from pixel-location to x,y coordinate location
        x, y = location.x , location.y
        xa = 1 + math.floor(8 * x / 450 + 4 - 8 * 250 / 450)
        ya = 1 + math.floor(8 * y / 450 + 4 - 8 * 250 / 450)
        if xa < 1: xa=1
        if xa > 8: xa = 8
        if ya < 1: ya = 1
        if ya > 8: ya = 8

        disc = self.board.getLocToDisc(xa,ya)

        # checking if there is a possible move for player
        if not self.play.isPossibleMove():
            self.player = self.play.whoIsNext()

            # popup message "No possible moves":
            self.text4 = self.w.create_text(250, 230, anchor=CENTER, fill="blue",
                                            font="Times 20 bold", text="No possible moves ")
            self.r4 = self.w.create_rectangle(self.w.bbox(self.text4), fill="white")
            self.w.tag_lower(self.r4, self.text4)

            # update move, so other player is next
            self.player.updateNumMoves()
            # update status text:
            self.w.delete(self.status_text)
            self.w.delete(self.status_text2)
            self.w.delete(self.line1)
            self.w.delete(self.text5)
            self.player = self.play.whoIsNext()
            color = self.player.getPlayerColor()
            if color == "B": color = "BLACK"
            else: color="WHITE"
            self.status_text = self.w.create_text(
                20, 3, font="Verdana 12 bold", fill="blue", anchor=NW, text=self._status_string())
            self.status_text2 = self.w.create_text(25, 478, font="Verdana 11 bold", anchor=NW, fill="blue",
                                                   text=self._status_string2())
            self.text5 = self.w.create_text(
                138, 4, font="Verdana 12 bold", fill="red", anchor=NW, text=color)
            self.line1 = self.w.create_line(135, 20, 200, 20, dash=(4, 2), fill="black")

        # checking if chosen move is valid, if yes updating accordingly
        if self.play.isValidMove(disc):
            self.w.delete(self.text2)
            self.w.delete(self.r)
            self.w.delete(self.text4)
            self.w.delete(self.r4)
            updateList = self.play.updateColorDiscs(disc) # updating main dictionary
            # updating visualization:
            color = self.board.getDiscColor(disc)
            if color == "W": color = "white"
            else: color = "black"
            x1, y1 = xa * 55, ya * 55
            self.w.create_oval([x1 - 20, y1 - 20, x1 + 20, y1 + 20], fill=color)
            # draw discs:
            for k in updateList:
                xa,ya = self.board.getDiscToLoc(k)
                x1, y1 = xa * 55, ya * 55
                self.w.create_oval([x1 - 20, y1 - 20, x1 + 20, y1 + 20], fill=color)


            # Update status text
            self.w.delete(self.status_text)
            self.w.delete(self.status_text2)
            self.status_text = self.w.create_text(
                20, 3, font="Verdana 12 bold",fill="blue",anchor=NW,text=self._status_string())
            self.status_text2 = self.w.create_text(25, 478, font="Verdana 11 bold", anchor=NW, fill="blue",
                                                   text=self._status_string2())

            # checking if game over
            if self.play.isGameOver():
                black, white = self.board.numBlackandWhite()
                if black > white: winner = "black"
                elif black == white: winner = "no one"
                else: winner = "white"
                self.text3 = self.w.create_text(250, 270, anchor=CENTER, fill="Yellow",
                                                font="Times 30 bold",text="GAME OVER\n"+"    "+str(winner)+" wins!")
                self.r3 = self.w.create_rectangle(self.w.bbox(self.text3), fill="black")
                self.w.tag_lower(self.r3, self.text3)

        else:
            self.w.delete(self.text4)
            self.w.delete(self.r4)
            self.w.delete(self.text2)
            self.w.delete(self.r)
            # "invalid move" popup message
            self.text2 = self.w.create_text(250, 250, anchor=CENTER,fill="red",
                                            font="Times 18 bold",text="Invalid move. Try again")
            self.r = self.w.create_rectangle(self.w.bbox(self.text2), fill="white")
            self.w.tag_lower(self.r, self.text2)

        self.master.update()

        # # checking if game over:
        if self.play.isGameOver():
            black, white = self.board.numBlackandWhite()
            if black > white:
                winner = "black"
            elif black == white:
                winner = "no one"
            else:
                winner = "white"
            self.text3 = self.w.create_text(250, 270, anchor=CENTER, fill="Yellow",
                                            font="Times 30 bold", text="GAME OVER\n" + "    " + str(winner) + " wins!")
            self.r3 = self.w.create_rectangle(self.w.bbox(self.text3), fill="black")
            self.w.tag_lower(self.r3, self.text3)

        # activating computer as a player
        if not self.play.whoIsNext().doesPlayFirst():
            self.text6 = self.w.create_text(250, 250, anchor=NW,font="Times 18 bold", text="Computer is thinking...")
            self.r6 = self.w.create_rectangle(self.w.bbox(self.text6), fill="white")
            self.w.tag_lower(self.r6, self.text6)
            self.master.update()
            self.computerPlaying()

            # checking if game over before continuing with the game
            if self.play.isGameOver():
                black, white = self.board.numBlackandWhite()
                if black > white:
                    winner = "black"
                elif black == white:
                    winner = "no one"
                else:
                    winner = "white"
                self.text3 = self.w.create_text(250, 270, anchor=CENTER, fill="lime",
                                                font="Times 30 bold",
                                                text="GAME OVER\n" + "    " + str(winner) + " wins!")
                self.r3 = self.w.create_rectangle(self.w.bbox(self.text3), fill="black")
                self.w.tag_lower(self.r3, self.text3)

            else:
                # checking if there is a possible move for human player
                if not self.play.isPossibleMove():
                    self.player = self.play.whoIsNext()
                    # popup message "No possible moves":
                    self.text4 = self.w.create_text(250, 230, anchor=CENTER, fill="blue",
                                                    font="Times 20 bold", text="No possible moves ")
                    self.r4 = self.w.create_rectangle(self.w.bbox(self.text4), fill="white")
                    self.w.tag_lower(self.r4, self.text4)
                    # update move, so other player is next
                    self.player.updateNumMoves()
                    # update status text:
                    self.w.delete(self.status_text)
                    self.w.delete(self.status_text2)
                    self.w.delete(self.line1)
                    self.w.delete(self.text5)
                    self.player = self.play.whoIsNext()
                    color = self.player.getPlayerColor()
                    if color == "B":
                        color = "BLACK"
                    else:
                        color = "WHITE"
                    self.status_text = self.w.create_text(
                        20, 3, font="Verdana 12 bold", fill="blue", anchor=NW, text=self._status_string())
                    self.status_text2 = self.w.create_text(25, 478, font="Verdana 11 bold", anchor=NW, fill="blue",
                                                           text=self._status_string2())
                    self.text5 = self.w.create_text(
                        138, 4, font="Verdana 12 bold", fill="red", anchor=NW, text=color)
                    self.line1 = self.w.create_line(135, 20, 200, 20, dash=(4, 2), fill="black")

                    if not self.play.whoIsNext().doesPlayFirst():
                        self.text6 = self.w.create_text(250, 250, anchor=NW, font="Times 18 bold",
                                                        text="Computer is thinking...")
                        self.r6 = self.w.create_rectangle(self.w.bbox(self.text6), fill="white")
                        self.w.tag_lower(self.r6, self.text6)
                        self.master.update()
                        self.computerPlaying()

                        if self.play.isGameOver():
                            black, white = self.board.numBlackandWhite()
                            if black > white:
                                winner = "black"
                            elif black == white:
                                winner = "no one"
                            else:
                                winner = "white"
                            self.text3 = self.w.create_text(250, 270, anchor=CENTER, fill="lime",
                                                            font="Times 30 bold",
                                                            text="GAME OVER\n" + "    " + str(winner) + " wins!")
                            self.r3 = self.w.create_rectangle(self.w.bbox(self.text3), fill="black")
                            self.w.tag_lower(self.r3, self.text3)
                    else:
                        self.w.delete(self.text4)
                        self.w.delete(self.r4)
                        self.text4 = self.w.create_text(250, 230, anchor=CENTER, fill="blue",
                                                        font="Times 20 bold", text="Play")
                        self.r4 = self.w.create_rectangle(self.w.bbox(self.text4), fill="white")


    def computerPlaying(self):
        """activates the computer as a player by using simulation (file: Simulations)
        returns: disc number"""
        # arguments for the simulations:

        discDictCopy = self.board.getDiscsDict().copy()
        player1Color = self.play.whoIsNext().getPlayerColor()
        player1Moves = self.play.whoIsNext().GetNumMoves()
        player2Moves = self.play.whoIsNext().GetNumMoves()+1

        manager = Simulations.SimulationManager() # initializing the simulation manager
        args = (discDictCopy,player1Color,player1Moves,player2Moves,AdjacencyDict)
        args_list = []
        for i in range(1000):  # this range determines the number of simulations; the multiprocessing method will go over all args tuple in the args_list
            args_list.append(args)

        result = manager.run(args_list)

        self.w.delete(self.line1)
        self.w.delete(self.text5)

        resultsDict = {}
        for Rdict in result: # for the result of each simulation
            RdictValue = Rdict.__iter__().__next__()  #  dictionary key
            if Rdict[RdictValue] == 1: # if simulation was successful,
                resultsDict[RdictValue] = resultsDict.get(RdictValue, 0) + 1  # increment result
        maxMove = 0
        winner = 0
        for move in resultsDict:
            if resultsDict[move] > maxMove:
                maxMove = resultsDict[move]
                winner = move
        if winner == 0: # if all simulations lost the game
            disc = result[0].__iter__().__next__() # choose the first move of the first game
        else: disc = winner

        updateList = self.play.updateColorDiscs(disc)
        color = self.board.getDiscColor(disc)
        if color == "W":
            color = "white"
        else:
            color = "black"
        xa,ya = self.board.getDiscToLoc(disc)
        x1, y1 = xa * 55, ya * 55
        self.w.create_oval([x1 - 20, y1 - 20, x1 + 20, y1 + 20], fill=color)

        # draw discs:
        for k in updateList:
            xa, ya = self.board.getDiscToLoc(k)
            x1, y1 = xa * 55, ya * 55
            self.w.create_oval([x1 - 20, y1 - 20, x1 + 20, y1 + 20], fill=color)

        # Update status text
        self.w.delete(self.text4)
        self.w.delete(self.r4)
        self.w.delete(self.text5)
        self.w.delete(self.line1)
        self.w.delete(self.status_text)
        self.w.delete(self.status_text2)
        self.status_text = self.w.create_text(
            20, 3, font="Verdana 12 bold", fill="blue", anchor=NW, text=self._status_string())
        self.status_text2 = self.w.create_text(25, 478, font="Verdana 11 bold", anchor=NW, fill="blue",
                                               text=self._status_string2())
        self.w.delete(self.text6)
        self.w.delete(self.r6)



class NoPossibleMovesException(Exception):
    """ NoPossibleMovesException is raised by the possible moves() method in the simulations
    class to indicate that there are no possible moves for player in current situation"""


"""STARTING THE GAME"""

if __name__ == '__main__':
    AdjacencyDict = load_Adj()
    game = BoardVisualization()

