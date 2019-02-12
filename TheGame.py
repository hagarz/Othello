__author__ = 'Hagar'

import random, numpy as np, pylab, math, csv, multiprocessing
from tkinter import *


"""
    Adjacency list loaded from given csv file
"""
def load_Adj():
    AdjacencyDict = {}
    index = 0

    with open("AdjList.csv", 'r') as file:
        # a = [{k: int(v) for k, v in row.items()}
        #      for row in csv.DictReader(f, skipinitialspace=True)]
        for row in file:
            row = [x.strip() for x in row.split(',')]
            row = list(filter(None,row))
            tempList = []
            index += 1
            for j in row[1:]:
                tempList.append(int(j))
            AdjacencyDict[index] = tempList
            #AdjacencyDict[index] = row[1:]
    file.close()
    return AdjacencyDict



class Board(object):
    """
    Board represents the color of discs on the board

    A board has 8* 8 tiles with 64 discs.
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
        example: for the location 8,8 will return 64
        """
        return self.locToDiscDict[x,y]

    def getDiscToLoc(self,disc):
        """
                returns location on board as an x,y coordinate for disc number
                disc is an int
                example: for the disc 64, will return the location 8,8
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
        return self.playsFirst


class GameMoves (object):
    """
    NEED TO FILL
    """
    def __init__(self, board):
        """
        Initializes two players and the Board class


        """
        self.player1 = Player(True,"W")
        self.player2 = Player(False,"B")
        self.board = board
        self.player = self.player1


    def whoIsNext(self):
        """
        Checks who's turn it is to play
        return: player
        """
        if self.player1.GetNumMoves() == self.player2.GetNumMoves():
            return self.player1
        else:
            return self.player2

    def isValidMove(self,disc):
        """
        Checks if move is valid
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
        # a move is valid if chosen location on board is next to (at least one) opposite color disc and
        # is bounded by the disc just placed and another disc of the current player's color
        for neighbor in AdjacencyDict[disc]:
            if self.board.getDiscColor(neighbor) == cont:
                d = neighbor - disc
                tempA = neighbor
                tempB = tempA + d
                while not flag:
                    if tempB in AdjacencyDict[tempA]:
                        if self.board.getDiscColor(tempB) == discColor  :
                            return True
                        elif self.board.getDiscColor(tempB) == cont:
                            tempA = tempB
                            tempB = tempA + d
                        else: break
                    else: break

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
        for key in range (1,65):
            if self.board.getDiscColor(key) is None:
                return False
        else: return True

    def updateColorDiscs(self,disc):
        """ colors adjacent discs in accordance with chosen location for disc on board and game rules
         disc is an int representing disc number
         """
        self.player = self.whoIsNext()
        discColor = self.player.getPlayerColor()
        if discColor == "W":
            cont = "B"
        else:
            cont = "W"

        nbrList = [] # this is the list of neighbors
        # check which discs need to be colored
        for neighbor in AdjacencyDict[disc]:
            flag = False
            counter = 0
            if self.board.getDiscColor(neighbor) == cont:
                d = neighbor - disc
                tempA = neighbor
                tempB = tempA + d
                while not flag:
                    counter += 1
                    if tempB in AdjacencyDict[tempA]:
                        if self.board.getDiscColor(tempB) == discColor:
                            flag = True
                            nbrList.append([neighbor, counter])
                        elif self.board.getDiscColor(tempB) == cont:
                            tempA = tempB
                            tempB = tempA + d
                        else: break
                    else:
                        break

                if flag:
                    nbrList.append([neighbor, counter])
        # create a list of the discs which need to be colored
        self.updateList=[]
        self.updateList.append(disc)
        for nbr in nbrList:
            d = nbr[0] - disc
            for count in range(nbr[1]):
                x= nbr[0] + d*count
                self.updateList.append(x)

        # update discs in main dictionary
        for disc in self.updateList:
            self.board.updateDisc(disc,discColor)
        # add move to number of moves for player
        self.player.updateNumMoves()

        return self.updateList


class BoardVisualization:
    """creating a GUI of the game using tkinter"""
    def __init__(self):
        """Initializes a visualization with the specified parameters"""

        self.board = Board()
        self.play = GameMoves(self.board)
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
        self.text1 = self.w.create_text(20, 3, font="Verdana 12 bold",anchor=NW, fill="blue",
                                       text=self._status_string())

        # create message texts for later
        self.text2 = self.w.create_text(200, 200, fill="red", font="bold", text="Invalid move. Try again")
        self.r = self.w.create_rectangle(self.w.bbox(self.text2), fill="white")
        self.w.tag_lower(self.r, self.text2)
        self.text3 = self.w.create_text(250, 250, anchor=CENTER, fill="Crimson",
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
        self.num_black = self.board.numBlackandWhite()[0]
        self.num_white = self.board.numBlackandWhite()[1]
        self.percent_full = round(100*((self.num_black + self.num_white)/64))
        if self.play.whoIsNext().getPlayerColor() == "W": self.playing="WHITE"
        else: self.playing = "BLACK"
        return "Now playing: "+str(self.playing)+";  white: %d; black: %d;  %d%% filled" % \
               (self.num_white, self.num_black, self.percent_full)


    def mouse_click(self,location):
        """triggered by mouse click on board game"""
        #self.location = location

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

            # popup message
            self.text4 = self.w.create_text(250, 230, anchor=CENTER, fill="Indigo",
                                            font="Times 20 bold", text="No possible moves ")
            self.r4 = self.w.create_rectangle(self.w.bbox(self.text4), fill="white")
            self.w.tag_lower(self.r4, self.text4)

            # update move, so other player is next
            self.player.updateNumMoves()
            self.player = self.play.whoIsNext()
            color = self.player.getPlayerColor()
            if color == "B": color = "BLACK"
            else: color="WHITE"

            # update status text
            self.w.delete(self.text1)
            self.w.delete(self.line1)
            self.w.delete(self.text5)
            self.text1 = self.w.create_text(
                20, 3, font="Verdana 12 bold", fill="blue", anchor=NW, text=self._status_string())
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
            # updating visualization
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

            print("Hello! in: mouse_click\is valid move")

            # Update status text
            self.w.delete(self.text1)
            self.text1 = self.w.create_text(
                20, 3, font="Verdana 12 bold",fill="blue",anchor=NW,text=self._status_string())

            # checking if game over
            if self.play.isGameOver():
                black, white = self.board.numBlackandWhite()
                if black > white: winner = "black"
                elif black == white: winner = "no one"
                else: winner = "white"
                self.text3 = self.w.create_text(250, 270, anchor=CENTER, fill="lime",
                                                font="Times 30 bold",text="GAME OVER\n"+"    "+str(winner)+" wins!")
                self.r3 = self.w.create_rectangle(self.w.bbox(self.text3), fill="black")
                self.w.tag_lower(self.r3, self.text3)

        else:
            print("else:invalid move")

            self.w.delete(self.text4)
            self.w.delete(self.r4)
            self.w.delete(self.text2)
            self.w.delete(self.r)
            # "invalid move" popup message
            self.text2 = self.w.create_text(250, 250, anchor=CENTER,fill="Crimson",
                                            font="Times 18 bold",text="Invalid move. Try again")
            self.r = self.w.create_rectangle(self.w.bbox(self.text2), fill="white")
            self.w.tag_lower(self.r, self.text2)

        self.master.update()

        # checking if game over
        if self.play.isGameOver():
            black, white = self.board.numBlackandWhite()
            if black > white:
                winner = "black"
            elif black == white:
                winner = "no one"
            else:
                winner = "white"
            self.text3 = self.w.create_text(250, 270, anchor=CENTER, fill="lime",
                                            font="Times 30 bold", text="GAME OVER\n" + "    " + str(winner) + " wins!")
            self.r3 = self.w.create_rectangle(self.w.bbox(self.text3), fill="black")
            self.w.tag_lower(self.r3, self.text3)

        # activating computer as a player
        #if self.play.whoIsNext().getPlayerColor() == "B":
        if not self.play.whoIsNext().doesPlayFirst():
            print('Hello! in: if next is "B"')
            self.text6 = self.w.create_text(250, 250, anchor=NW,font="Times 18 bold", text="Computer is thinking...")
            self.r6 = self.w.create_rectangle(self.w.bbox(self.text6), fill="white")
            self.w.tag_lower(self.r6, self.text6)
            self.master.update()
            self.computerPlaying()

    def computerPlaying(self):
        print ("Hello! in: computerPlaying")
        discDict = self.board.getDiscsDict()
        player1Color = self.play.whoIsNext().getPlayerColor()
        player1Moves = self.play.whoIsNext().GetNumMoves()
        player2Moves = self.play.whoIsNext().GetNumMoves()+1
        disc = Simple_Simulations(discDict,player1Color,player1Moves,player2Moves).simulation(player1Moves,player2Moves,discDict)
        print(f"COMPUTER PLAYING,DISC {disc}")
        # self.w.delete(self.text2)
        # self.w.delete(self.r)
        # self.w.delete(self.text4)
        # self.w.delete(self.r4)
        updateList = self.play.updateColorDiscs(disc)
        print("COMPUTER PLAYING,after updateList:",self.board.getDiscsDict())
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

        # Update text
        self.w.delete(self.text1)
        self.text1 = self.w.create_text(
            20, 3, font="Verdana 12 bold", fill="blue", anchor=NW, text=self._status_string())


        self.w.delete(self.text6)
        self.w.delete(self.r6)


    def _map_coords(self,x,y):
        return (250+450*(x-4)/8,250+450*(4-y)/8)

class Coputer(object):
    """TO Be updated"""
    def __init__(self,player,board,gameMoves):
        self.player = player
        self.color = self.player.getPlayerColor()
        self.board = board
        self.play = gameMoves


class LevelEasy(Coputer):
    """chooses the next step randomly from available valid moves.
    returns a number of disc"""
    def __init__(self):
        pass

    def game(self):
        optionalList = []
        discDict = self.board.getDiscsDict()
        for i in discDict:
            if discDict[i] == None:
                if self.play.isValidMove(i):
                    optionalList.append(i)
        # choose a random move from available possible moves
        self.move = random.choice(optionalList)


# class Simple_Simulations(object):
#     def __init__(self,discDict,player1Color,player1Moves,player2Moves):
#         self.discDictCopy = discDict.copy()
#         print(f"Adj {AdjacencyDict}")
#         self.winnersDict={}
#         self.player1c = player1Color
#         if self.player1c == "B": self.player2c = "W"
#         else: self.player2c = "B"
#         self.currentPlayer = player1Color
#         self.player1Moves = player1Moves
#         self.player2Moves = player2Moves
#         self.AdjacencyDict = load_Adj()
#         self.count = 0
#         self.possibleMovesList = self.possible_moves()
#         #self.simulation(numSimulations,self.player1Moves,self.player2Moves,self.discDictCopy)
#     def simulation(self, player1Moves, player2Moves, discDict):
#         numSimulations = 1000
#         print(f"IN SIMULATION\np1moves: {player1Moves} \np2moves: {player2Moves}\ncolor: {self.currentPlayer}")
#
#         for simulation in range(numSimulations):
#             discDictC = discDict.copy()
#             self.reset_vars(player1Moves, player2Moves, discDictC)       #reseting so each simulations starts from the same place
#             firstMove = random.choice(self.possibleMovesList)
#             self.update_dict(firstMove,self.player1c)
#             self.updateDiscsColor(firstMove)
#             self.update_num_moves(self.player1c)
#             self.game_on(firstMove)
#
#         print("winnerDict:",self.winnersDict)
#         maxMove = 0
#         winner = 0
#         for move in self.winnersDict:
#             if self.winnersDict[move] > maxMove:
#                 maxMove = self.winnersDict[move]
#                 winner = move
#         print ("winner:",winner,maxMove)
#         return winner
#
#
#     def reset_vars(self,player1Moves,player2Moves,discDict):
#         self.player1Moves = player1Moves
#         self.player2Moves = player2Moves
#         self.discDictCopy = discDict
#         self.count = 0
#
#     def possible_moves(self):
#         psbleMovesList=[]
#         for i in self.discDictCopy:
#             if self.discDictCopy[i] is None:
#                 if self.valid_moves(i):
#                     psbleMovesList.append(i)
#         if len(psbleMovesList) > 0:
#             self.count = 0
#             return psbleMovesList
#         else:
#             if self.count < 2:
#                 self.count += 1
#                 raise NoPossibleMovesException
#             else:
#                 counter = 0
#                 print("no moves?",self.discDictCopy)
#                 for k in self.discDictCopy:
#                     if self.discDictCopy[k] is None:
#                         counter += 1
#                         self.discDictCopy[k] = "N"
#                 print ("counter=",counter)
#                 raise NoPossibleMovesException
#
#     def valid_moves(self,disc):
#         discColor = self.now_playing()
#         if discColor == "W":
#             cont = "B"
#         else:
#             cont = "W"
#
#         flag = False
#
#         for neighbor in self.AdjacencyDict[disc]:
#             if self.get_disc_color(neighbor) == cont:
#                 d = neighbor - disc
#                 tempA = neighbor
#                 tempB = tempA + d
#                 while not flag:
#                     if tempB in self.AdjacencyDict[tempA]:
#                         if self.get_disc_color(tempB) == discColor:
#                             return True
#                         elif self.get_disc_color(tempB) == cont:
#                             tempA = tempB
#                             tempB = tempA + d
#                         else:
#                             break
#                     else:
#                         break
#         return flag
#
#     def now_playing(self):
#         if self.get_num_moves(self.player2c) > self.get_num_moves(self.player1c):
#             return self.player1c
#         elif self.get_num_moves(self.player1c) == self.get_num_moves(self.player2c):
#             return self.player2c
#
#     def get_num_moves(self,player):
#         if player == self.player1c:
#             return self.player1Moves
#         elif player == self.player2c:
#             return self.player2Moves
#
#     def update_num_moves(self, player):
#         if player == self.player1c:
#             self.player1Moves +=1
#         elif player == self.player2c:
#             self.player2Moves += 1
#
#     def get_disc_color(self,disc):
#         return self.discDictCopy[disc]
#
#     def update_dict(self,disc,color):
#         self.discDictCopy[disc] = color
#
#     def fin_check(self):
#         for i in self.discDictCopy:
#             if self.discDictCopy[i] is None:
#                 return False
#         return True
#
#
#     def updateDiscsColor(self,disc):
#         """ colors adjacent discs in accordance with chosen disc and game rules
#          disc is an int representing disc number
#          """
#         discColor = self.now_playing()
#         if discColor == "W":
#             cont = "B"
#         else:
#             cont = "W"
#
#         nbrList = []
#         # check which discs need to be colored
#         for neighbor in AdjacencyDict[disc]:
#             flag = False
#             counter = 0
#             if self.get_disc_color(neighbor) == cont:
#                 d = neighbor - disc # this is the direction
#                 tempA = neighbor
#                 tempB = tempA + d
#                 while not flag:
#                     counter += 1
#                     if tempB in self.AdjacencyDict[tempA]:
#                         if self.get_disc_color(tempB) == discColor:
#                             flag = True
#                             nbrList.append([neighbor, counter])
#                         elif self.get_disc_color(tempB) == cont:
#                             tempA = tempB
#                             tempB = tempA + d
#                         else: break
#                     else: break
#
#                 if flag:
#                     nbrList.append([neighbor, counter])
#
#         # create a list of the discs which need to be colored
#         updateList=[]
#         updateList.append(disc)
#         for nbr in nbrList:
#             d = nbr[0] - disc
#             for count in range(nbr[1]):
#                 x = nbr[0] + d*count
#                 updateList.append(x)
#
#         # update discs in main dictionary
#         for disc in updateList:
#             self.update_dict(disc,discColor)
#
#
#     def game_on(self, firstMove):
#         while not self.fin_check():
#             player = self.now_playing()
#
#             try:
#                 move = random.choice(self.possible_moves())
#                 self.update_dict(move, player) # update move in discs' dictionary
#                 self.updateDiscsColor(move)   # color neighbor discs as result of chosen move
#                 self.update_num_moves(player) # add move to number of moves for player
#             except NoPossibleMovesException:
#                 self.update_num_moves(player)
#
#         count1=0
#         count2=0
#         for disc in self.discDictCopy:
#             if self.discDictCopy[disc] == self.player1c:
#                 count1 += 1
#             else:
#                 count2 += 1
#         if count1 > count2:
#             self.winnersDict[firstMove] = self.winnersDict.get(firstMove,0) + 1


class NoPossibleMovesException(Exception):
    """ NoPossibleMovesException is raised by the possible moves() method in the simulations
    class to indicate that there are no possible moves for player in current situation"""




"""STARTING THE GAME"""

if __name__ == '__main__':
    AdjacencyDict = load_Adj()
    game = BoardVisualization()

