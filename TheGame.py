__author__ = 'Hagar'

import random, math, csv, multiprocessing, Simulations, time, sys
from Visualization import *
from tkinter import *

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")


def load_adjacencies():
    """
    Adjacency list loaded from given csv file
    a dictionary representing adjacencies for each disc on the board"""
    adjacency_dict = {}
    index = 0
    with open("AdjList.csv", 'r') as file:
        for row in file:
            row = [x.strip() for x in row.split(',')]
            row = list(filter(None, row))
            temp_list = []
            index += 1
            for j in row[1:]:
                temp_list.append(int(j))
            adjacency_dict[index] = temp_list
    file.close()
    return adjacency_dict


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
        for i in range(1, 65):
            self.discsDict[i] = None
        # game starts with 2 black and 2 white discs at the centre of the board
        self.discsDict[28], self.discsDict[29], self.discsDict[36], self.discsDict[37] = "W", "B", "B", "W"

        # location coordination to discs dictionary (disc number and location on board)
        self.locToDiscDict = {}
        m = 0
        for j in range(1, 9):
            for k in range(1, 9):
                m += 1
                self.locToDiscDict[j, k] = m

        # discs to location coordination dictionary
        self.discToLocDict = {}
        for i in self.locToDiscDict:
            self.discToLocDict[self.locToDiscDict[i]] = i

    def get_disc_color(self, disc):
        """
        Returns the color of a disc
        """
        return self.discsDict[disc]

    def update_disc(self, disc, color):
        """
        Updates disc color in dictionary
        """
        self.discsDict[disc] = color

    def get_discs_dict(self):
        """ returns discs color dictionary"""
        return self.discsDict

    def num_black_white(self):
        """returns the current number of black and white discs"""
        black = 0
        white = 0
        discs_dict = self.get_discs_dict()
        for disc in discs_dict:
            if discs_dict[disc] == "B": black += 1
            if discs_dict[disc] == "W": white += 1
        return black, white

    def get_loc_to_disc(self, x, y):
        """
        returns the disc number for location on board
        location is an x,y coordination
        Example: for the location (8,8) will return 64
        """
        return self.locToDiscDict[x, y]

    def get_disc_to_loc(self, disc):
        """
        returns location on board as an x,y coordinate for disc number
        disc is an int
        Example: for the disc 64, will return the location (8,8)
        """

        return self.discToLocDict[disc]


class Player (object):
    """
    Represents a player.
    A player has a color and number of moves
    """
    def __init__(self, plays_first, color):
        """
        color: a string, the color of player's disc (either "B" for black or "W" for white).
        playsFirst: a boolean, indicates if the player is the one who plays first
        """
        self.playsFirst = plays_first
        self.numMoves = 0  # number of moves made by player
        self.color = color

    def get_num_moves(self):
        """
        Returns number of moves for player so far.
        this helps to decide who should play next
        """
        return self.numMoves

    def update_num_moves(self):
        """    Adds a move to player's number of moves   """
        self.numMoves += 1

    def get_player_color(self):
        return self.color

    def does_play_first(self):
        """ check if current player was the firs player.
        Return boolean"""
        return self.playsFirst


class GameController (object):
    """
    GameController represents the enforcement of the game rules and logic.
    """
    def __init__(self, visualization):
        """
        Initializes two players and the Board class
        """
        # create two player objects:
        self.player1 = Player(True, "W")
        self.player2 = Player(False, "B")
        self.board = visualization.board
        self.player = self.player1  # this is the current player playing
        self.AdjacencyDict = load_adjacencies()
        self.visualization = visualization

    def who_is_next(self):
        """
        Checks who's turn it is to play
        return: player object
        """
        if self.player1.get_num_moves() == self.player2.get_num_moves():
            return self.player1
        else:
            return self.player2

    def is_valid_move(self, disc):
        """
        Checks if move is valid.
        disc is an int representing disc number;
        disc is the move to be checked if valid.
        return: True if valid, False if not
        """
        self.player = self.who_is_next()

        # a move is valid only if current location on board is empty
        if self.board.get_disc_color(disc) is not None:
            return False

        disc_color = self.player.get_player_color()
        if disc_color == "W":
            cont = "B"
        else: cont = "W"

        flag = False
        # a move is valid if:
        # chosen location on board is next to (at least one) opposite color disc
        # and is bounded by the disc just placed and another disc of the current player's color
        for neighbor in self.AdjacencyDict[disc]:  # looping over all adjacent discs
            if self.board.get_disc_color(neighbor) == cont:  # check if adjacent disc is in opponent's color
                direction = neighbor - disc
                next_disc = neighbor
                next2next_disc = next_disc + direction
                while not flag:
                    # check if next disc is adjacent (for example, disc 8 is not adjacent to 9. 9 is in a different row)
                    if next2next_disc in self.AdjacencyDict[next_disc]:
                        # if the next disc is in current player's color, we are done:
                        if self.board.get_disc_color(next2next_disc) == disc_color:
                            return True
                        # if the next disc is in opponent's color, we continue to the following disc:
                        elif self.board.get_disc_color(next2next_disc) == cont:
                            next_disc = next2next_disc
                            next2next_disc = next_disc + direction
                        else: break  # if the next disc is neither black nor white, it is empty
                    else: break  # if neighboring disc is not in opponent's color, the move is not valid

        return flag

    def any_possible_moves(self):
        """checks if the current player has a possible next move in current situation"""
        self.player = self.who_is_next()
        disc_dict = self.board.get_discs_dict()
        for i in disc_dict:
            if disc_dict[i] is None:
                if self.is_valid_move(i):
                    return True
        return False

    def is_game_over(self):
        """
        Checks if game over
        return: True or False
        """
        black, white = self.board.num_black_white()
        for key in range(1, 65):
            if self.board.get_disc_color(key) is None and black > 0 and white > 0:
                return False
        else: return True

    def get_winner(self):
        """returns a string of the winner when game is over"""
        black, white = self.board.num_black_white()
        if black > white:
            return "black"
        elif black == white:
            return "no one"
        else:
            return "white"

    def update_color_discs(self, disc):
        """
        colors adjacent discs in accordance with chosen location for disc on board and game rules.
        disc is an int representing disc number;
        disc is player's chosen move
        """

        # check the color of current player:
        self.player = self.who_is_next()
        disc_color = self.player.get_player_color()
        if disc_color == "W":
            cont = "B"
        else:
            cont = "W"

        neighbor_list = []  # this is the list of neighbors
        # check which discs need to be colored
        for neighbor in self.AdjacencyDict[disc]:  # looping over all adjacent discs
            flag = False
            counter = 0
            if self.board.get_disc_color(neighbor) == cont:  # check if adjacent disc is in opponent's color
                direction = neighbor - disc
                next_disc = neighbor
                next2next_disc = next_disc + direction
                while not flag:
                    counter += 1  # accounting for number of discs consecutively
                    # check if next disc is adjacent (for example, disc 8 is not adjacent to 9. 9 is in a different row)
                    if next2next_disc in self.AdjacencyDict[next_disc]:
                        # if the next disc is in current player's color, we are done:
                        if self.board.get_disc_color(next2next_disc) == disc_color:
                            flag = True
                            # the adjacent disc and number of consecutively discs are added to the list:
                            neighbor_list.append([neighbor, counter])
                        # if the next disc is in opponent's color, we continue to the following disc:
                        elif self.board.get_disc_color(next2next_disc) == cont:
                            next_disc = next2next_disc
                            next2next_disc = next_disc + direction
                        else: break  # if the next disc is neither black nor white, it is empty and hence invalid
                    else: break

                if flag:
                    # now we have a list of all neighboring list to be colored
                    # and the number of following discs to be colored as well
                    neighbor_list.append([neighbor, counter])
        # create a list of the discs which need to be colored
        update_list = [disc]
        for nbr in neighbor_list:
            angle = nbr[0] - disc
            for distance in range(nbr[1]):
                x = nbr[0] + angle * distance
                update_list.append(x)

        # update discs in main dictionary
        for disc in update_list:
            self.board.update_disc(disc, disc_color)
        # add move to number of moves for player
        self.player.update_num_moves()

        return update_list

    def computer_playing(self):
        """
        activates the computer as a player by using simulation (file: Simulations)
        returns: disc number
        """
        # arguments for the simulations:
        disc_dict_copy = self.board.get_discs_dict().copy()
        player1_color = self.who_is_next().get_player_color()
        player1_moves = self.who_is_next().get_num_moves()
        player2_moves = self.who_is_next().get_num_moves() + 1
        adjacency_dict = self.AdjacencyDict

        manager = Simulations.SimulationManager()  # initializing the simulation manager
        args = (disc_dict_copy, player1_color, player1_moves, player2_moves, adjacency_dict)
        args_list = []
        # this range determines the number of simulations;
        # the multiprocessing method will go over all args tuple in the args_list
        for i in range(100):
            args_list.append(args)

        result = manager.run(args_list)

        # self.visualization.w.delete(self.line1)
        # self.visualization.w.delete(self.text5)

        results_dict = {}
        for result_dict in result:  # for the result of each simulation
            rdict_value = result_dict.__iter__().__next__()  # dictionary key
            if result_dict[rdict_value] == 1:  # if simulation was successful,
                results_dict[rdict_value] = results_dict.get(rdict_value, 0) + 1  # increment result
        max_move = 0
        winner = 0
        for move in results_dict:
            if results_dict[move] > max_move:
                max_move = results_dict[move]
                winner = move
        if winner == 0:  # if all simulations lost the game
            disc = result[0].__iter__().__next__()  # choose the first move of the first game
        else: disc = winner

        update_list = self.update_color_discs(disc)

        return disc, update_list


class NoPossibleMovesException(Exception):
    """ NoPossibleMovesException is raised by the possible moves() method in the simulations
    class to indicate that there are no possible moves for player in current situation"""


"""STARTING THE GAME"""

if __name__ == '__main__':
    game = BoardVisualization()

