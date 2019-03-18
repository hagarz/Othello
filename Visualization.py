__author__ = 'Hagar'

import math,time, Simulations
from tkinter import *
from TheGame import Board, GameController, load_Adj


class BoardVisualization:
    """
    creating a GUI of the game using tkinter
    This is the main loop of the game
    """
    def __init__(self):
        """Initializes visualization with the specified parameters"""

        self.board = Board()
        self.controller = GameController(self)
        self.player = self.controller.whoIsNext()

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
        self.text6 = self.w.create_text(250, 250, anchor=CENTER, text="Computer is thinking...")
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

        self.AdjacencyDict = load_Adj()

        # event trigger - mouse-click
        self.w.bind("<Button-1>",self.mouse_click)
        self.master.update()

        # main loop
        self.master.mainloop()


    def _status_string(self):
        """Returns an appropriate status string to print:
        what player is playing now, number of black and white discs and what percent of the board is full"""

        if self.controller.whoIsNext().getPlayerColor() == "W": self.playing= "WHITE"
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
        x, y = location.x, location.y
        xa = 1 + math.floor(8 * x / 450 + 4 - 8 * 250 / 450)
        ya = 1 + math.floor(8 * y / 450 + 4 - 8 * 250 / 450)
        if xa < 1: xa=1
        if xa > 8: xa = 8
        if ya < 1: ya = 1
        if ya > 8: ya = 8
        disc = self.board.getLocToDisc(xa,ya)

        # checking if chosen move is valid, if yes updating accordingly
        if self.controller.isValidMove(disc):
            self.w.delete(self.text2)
            self.w.delete(self.r)
            self.w.delete(self.text4)
            self.w.delete(self.r4)
            updateList = self.controller.updateColorDiscs(disc) # updating main dictionary
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
            if self.controller.isGameOver():
                winner = self.controller.getWinner()
                self.text3 = self.w.create_text(250, 270, anchor=CENTER, fill="Yellow",
                                                font="Times 30 bold",text="GAME OVER\n"+"    "+str(winner)+" wins!")
                self.r3 = self.w.create_rectangle(self.w.bbox(self.text3), fill="black")
                self.w.tag_lower(self.r3, self.text3)
                self.master.update()
                time.sleep(4)
                self.master.quit()
                self.master.destroy()

            else:
                # checking if there is a possible move for player
                if not self.controller.anyPossibleMoves():
                    self.player = self.controller.whoIsNext()

                    # popup message "No possible moves":
                    self.text4 = self.w.create_text(250, 230, anchor=CENTER, fill="blue",
                                                    font="Times 20 bold", text="No possible moves ")
                    self.r4 = self.w.create_rectangle(self.w.bbox(self.text4), fill="white")
                    self.w.tag_lower(self.r4, self.text4)

                    # update number of moves, so other player is next
                    self.player.updateNumMoves()
                    # update status text:
                    self.w.delete(self.status_text)
                    self.w.delete(self.status_text2)
                    self.w.delete(self.line1)
                    self.w.delete(self.text5)
                    self.player = self.controller.whoIsNext()
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
                    self.master.update()
                    time.sleep(3)
                    self.w.delete(self.text4)
                    self.w.delete(self.r4)
        else:  # if chosen move is not valid, a message will appear
            self.w.delete(self.text4)
            self.w.delete(self.r4)
            self.w.delete(self.text2)
            self.w.delete(self.r)
            # "invalid move" popup message
            self.text2 = self.w.create_text(250, 250, anchor=CENTER,fill="red",
                                            font="Times 18 bold",text="Invalid move. Try again")
            self.r = self.w.create_rectangle(self.w.bbox(self.text2), fill="white")
            self.w.tag_lower(self.r, self.text2)

        #self.master.update()

        # activating computer as a player
        if not self.controller.whoIsNext().doesPlayFirst() and not self.controller.isGameOver():
            self.text6 = self.w.create_text(250, 250, anchor=NW,font="Times 18 bold", text="Computer is thinking...")
            self.r6 = self.w.create_rectangle(self.w.bbox(self.text6), fill="white")
            self.w.tag_lower(self.r6, self.text6)
            self.master.update()
            self.controller.computerPlaying()

            # checking if game over before continuing with the game
            if self.controller.isGameOver():
                winner = self.controller.getWinner()
                self.text3 = self.w.create_text(250, 270, anchor=CENTER, fill="yellow",
                                                font="Times 30 bold",
                                                text="GAME OVER\n" + "    " + str(winner) + " wins!")
                self.r3 = self.w.create_rectangle(self.w.bbox(self.text3), fill="black")
                self.w.tag_lower(self.r3, self.text3)
                self.master.update()
                time.sleep(4)
                self.master.quit()
                self.master.destroy()

            else:
                # checking if there is a possible move for player
                if not self.controller.anyPossibleMoves():
                    self.player = self.controller.whoIsNext()
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
                    self.player = self.controller.whoIsNext()
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
                    self.master.update()
                    time.sleep(3)
                    if not self.controller.whoIsNext().doesPlayFirst():
                        self.text6 = self.w.create_text(250, 250, anchor=NW, font="Times 18 bold",
                                                        text="Computer is thinking...")
                        self.r6 = self.w.create_rectangle(self.w.bbox(self.text6), fill="white")
                        self.w.tag_lower(self.r6, self.text6)
                        self.master.update()
                        self.controller.computerPlaying()
                        self.w.delete(self.text5)

                        # checking if game over before continuing with the game
                        if self.controller.isGameOver():
                            winner = self.controller.getWinner()
                            self.text3 = self.w.create_text(250, 270, anchor=CENTER, fill="yellow",
                                                            font="Times 30 bold",
                                                            text="GAME OVER\n" + "    " + str(winner) + " wins!")
                            self.r3 = self.w.create_rectangle(self.w.bbox(self.text3), fill="black")
                            self.w.tag_lower(self.r3, self.text3)
                            self.master.update()
                            time.sleep(4)
                            self.master.quit()
                            self.master.destroy()
                    else:
                        self.master.update()
                        time.sleep(3)
                        self.w.delete(self.text4)
                        self.w.delete(self.r4)
                        self.text4 = self.w.create_text(250, 230, anchor=CENTER, fill="blue",
                                                        font="Times 20 bold", text="Play")
                        self.r4 = self.w.create_rectangle(self.w.bbox(self.text4), fill="white")

    def computerPlayingVisual(self,disc,updateList):
        """creates and updates visualization following 'computer playing'  """
        self.w.delete(self.line1)
        self.w.delete(self.text5)

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
        self.master.update()