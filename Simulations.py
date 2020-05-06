__author__ = 'Hagar'
import random, os, multiprocessing as mp, time
from sys import platform
import types
import copyreg


class Simulations(object):
    """Computer chooses its next step by performing multiple simulations of the game"""
    def __init__(self, arguments):
        """
        discDict - a dictionary, represent the color of discs on the board
        player1Color - a string, the color of the current player
        player1Moves, player2Moves - an int, number of moves made by each player
        adjacencyDict - a dictionary, representing adjacencies for each disc
        possibleMovesList - a list of all possible moves for current player, with current board state
        """

        # encapsulating arguments inserted to args_list as tuple:
        discDict, player1Color, player1Moves, player2Moves, adjacencyDict = arguments

        self.discDictCopy = discDict.copy()
        self.player1c = player1Color
        if self.player1c == "B": self.player2c = "W"
        else: self.player2c = "B"
        self.currentPlayer = player1Color
        self.player1Moves = player1Moves
        self.player2Moves = player2Moves
        self.AdjacencyDict = adjacencyDict
        self.count = 0
        self.possibleMovesList = self.possible_moves()
        self.winnersDict = {}

    def simulation(self):
        """
        a move (disc) is randomly chosen from a list of possible moves,
        then a simulation of the game is continued from the point the real game has stopped
        and is played starting with randomly chosen move.
         Returns the chosen move if simulated game was won
         """

        # randomly choosing a move (disc) from a list of possible moves:

        first_move = random.choice(self.possibleMovesList)
        self.update_dict(first_move, self.player1c)        # updating chosen move in dictionary
        self.update_discs_color(first_move)
        self.update_num_moves(self.player1c)
        self.game_on(first_move)    # simulating a game continuing from chosen move
        return self.winnersDict

    def possible_moves(self):
        """ iterates over main dictionary to create a list of possible moves"""
        possible_moves_list = []
        for tile in self.discDictCopy:
            if self.discDictCopy[tile] is None:  # for every empty tile on the board
                if self.valid_moves(tile):  # check if a disc can be placed
                    possible_moves_list.append(tile)  # then add to lis of possible moves
        if len(possible_moves_list) > 0:  # if the list of possible moves is not empty, return list
            self.count = 0
            return possible_moves_list
        else:
            # if there were no possible moves less than twice, increment count by 1 and raise NoPossibleMovesException
            if self.count < 2:
                self.count += 1
                raise NoPossibleMovesException
            else:
                # if there were no possible moves more than twice,
                # it means there are no more possible moves in the game for all players
                # the empty tile will be filled with a neutral color "N"
                # thus all tiles will be filled and game will be over
                counter = 0
                for k in self.discDictCopy:
                    if self.discDictCopy[k] is None:
                        counter += 1
                        self.discDictCopy[k] = "N"
                raise NoPossibleMovesException

    def valid_moves(self, disc):
        """
        Checks if move is valid, returns boolean.
        disc is player's chosen move
        disc is an int representing disc number
         """
        disc_color = self.now_playing()
        if disc_color == "W":
            cont = "B"
        else:
            cont = "W"

        flag = False

        for neighbor in self.AdjacencyDict[disc]:
            if self.get_disc_color(neighbor) == cont:  # check if adjacent disc is in opponent's color
                direction = neighbor - disc
                next_disc = neighbor
                next2next_disc = next_disc + direction
                while not flag:
                    # check if next disc is adjacent (for example, disc 8 is not adjacent to 9. 9 is in a different row)
                    if next2next_disc in self.AdjacencyDict[next_disc]:
                        # if the next disc is in current player's color, we are done:
                        if self.get_disc_color(next2next_disc) == disc_color:
                            return True
                        # if the next disc is in opponent's color, we continue to the following disc:
                        elif self.get_disc_color(next2next_disc) == cont:
                            next_disc = next2next_disc
                            next2next_disc = next_disc + direction
                        else: break  # if the next disc is neither black nor white, it is empty
                    else: break  # if neighboring disc is not in opponent's color, the move is not valid
        return flag

    def now_playing(self):
        """what player is playing now"""
        if self.get_num_moves(self.player2c) > self.get_num_moves(self.player1c):
            return self.player1c
        elif self.get_num_moves(self.player1c) == self.get_num_moves(self.player2c):
            return self.player2c

    def get_num_moves(self, player):
        if player == self.player1c:
            return self.player1Moves
        elif player == self.player2c:
            return self.player2Moves

    def update_num_moves(self, player):
        """increment player's number of moves by 1"""
        if player == self.player1c:
            self.player1Moves += 1
        elif player == self.player2c:
            self.player2Moves += 1

    def get_disc_color(self, disc):
        return self.discDictCopy[disc]

    def update_dict(self, disc, color):
        self.discDictCopy[disc] = color

    def fin_check(self):
        """ checking if game has ended"""
        for j in self.discDictCopy:
            if self.discDictCopy[j] is None:
                return False
        return True

    def update_discs_color(self, disc):
        """
        colors adjacent discs in accordance with chosen disc and game rules
        disc is an int representing disc number
        disc is player's chosen move
        """

        # check the color of current player:
        disc_color = self.now_playing()
        if disc_color == "W":
            cont = "B"
        else:
            cont = "W"

        nbrList = []  # this is the list of neighbors
        # check which discs need to be colored
        for neighbor in self.AdjacencyDict[disc]:  # looping over all adjacent discs
            flag = False
            counter = 0
            if self.get_disc_color(neighbor) == cont:  # check if adjacent disc is in opponent's color
                direction = neighbor - disc  # this is the direction
                next_disc = neighbor
                next2next_disc = next_disc + direction
                while not flag:
                    counter += 1  # accounting for number of discs consecutively
                    # check if next disc is adjacent (for example, disc 8 is not adjacent to 9. 9 is in a different row)
                    if next2next_disc in self.AdjacencyDict[next_disc]:
                        # if the next disc is in current player's color, we are done:
                        if self.get_disc_color(next2next_disc) == disc_color:
                            flag = True
                            # the adjacent disc and number of consecutively discs are added to the list:
                            nbrList.append([neighbor, counter])
                            # if the next disc is in opponent's color, we continue to the following disc:
                        elif self.get_disc_color(next2next_disc) == cont:
                            next_disc = next2next_disc
                            next2next_disc = next_disc + direction
                        else: break
                    else: break

                if flag:
                    nbrList.append([neighbor, counter])

        # create a list of the discs which need to be colored
        update_list = [disc]
        for nbr in nbrList:
            angle = nbr[0] - disc
            for distance in range(nbr[1]):
                x = nbr[0] + angle * distance
                update_list.append(x)

        # update discs in main dictionary
        for disc in update_list:
            self.update_dict(disc, disc_color)

    def game_on(self, first_move):
        """ simulating a game by choosing a move randomly from a list of possible moves. """
        while not self.fin_check():
            player = self.now_playing()

            try:
                move = random.choice(self.possible_moves())
                self.update_dict(move, player)  # update move in discs' dictionary
                self.update_discs_color(move)     # color neighbor discs as result of chosen move
                self.update_num_moves(player)   # add move to number of moves for player
            # if there is no possible move, an exception is raised and the turn goes to the next player
            except NoPossibleMovesException:
                self.update_num_moves(player)   # increment player's number of moves by 1

        self.winnersDict[first_move] = 0
        # counting number of discs for each color
        count1 = 0
        count2 = 0
        for disc in self.discDictCopy:
            if self.discDictCopy[disc] == self.player1c:
                count1 += 1
            else:
                count2 += 1
        # if there are more discs for firs player, meaning the first player won,
        #  first move is added to the dictionary "winnersDict"
        if count1 > count2:
            self.winnersDict[first_move] = self.winnersDict.get(first_move, 0) + 1


def _pickle_method(m):
    """
     to solve“PicklingError”. updates registry for pickle on what goes into pickling
    """
    class_self = m.im_class if m.im_self is None else m.im_self
    return getattr, (class_self, m.im_func.func_name)

copyreg.pickle(types.MethodType, _pickle_method)


class SimulationManager(object):
    """
    using multiprocessing to run simulations in parallel;
    parallelizing the execution of a function across multiple input values,
    distributing the input data across processes (data parallelism)
    """
    def __init__(self):
        if "linux" in platform:
            # for Linux the number of usable CPUs can be obtained with:
            num_cpus = len(os.sched_getaffinity(0))
        else:
            num_cpus = os.cpu_count()
        if num_cpus is None:
            num_cpus = 2
        self.pool = mp.Pool(num_cpus-1)  # determining the number of processes

    def go_to(self, args):
        """ this method calls simulation method in Simulations class with arguments sent as tuple"""
        return Simulations(args).simulation()

    def run(self, args_list):
        """
        This method chops the args_list into a number of chunks which it submits to the process pool as separate tasks.
        pool.map supports only one iterable argument, hence the use of args_list;
         args_list is a list of identical tuples, each tuple contains the arguments required to run the simulation
         pool.map iterates over the tuples in args_list,
         each tuple sent to the go_to method, then creates an object of Simulations
         """
        result = self.pool.map(self.go_to, args_list)
        self.pool.close()
        self.pool.join()
        return result

    def __getstate__(self):
        """
        returned object is pickled as the contents for the instance,
        instead of the contents of the instance’s dictionary
        (to solve pool objects cannot be passed between processes or pickled)
        """
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict



class NoPossibleMovesException(Exception):
    """ NoPossibleMovesException is raised by the possible moves() method in the simulations
    class to indicate that there are no possible moves for player in current situation"""
