__author__ = 'Hagar'
import random, multiprocessing as mp, time, os


class Simulations(object):
    """Computer chooses its next step by performing multiple simulations of the game"""
    def __init__(self,arguments):
        # encapsulating arguments inserted to args_list as tuple:
        discDict, player1Color, player1Moves, player2Moves, adjacencyDict = arguments

        self.discDictCopy = discDict.copy()
        self.winnersDict={}
        self.player1c = player1Color
        if self.player1c == "B": self.player2c = "W"
        else: self.player2c = "B"
        self.currentPlayer = player1Color
        self.player1Moves = player1Moves
        self.player2Moves = player2Moves
        self.AdjacencyDict = adjacencyDict
        self.count = 0
        self.possibleMovesList = self.possible_moves()

    def simulation(self):
        """ a move (disc) is randomly chosen from a list of possible moves,
        then a simulation of the game is continued from the point the real game has stopped
        and is played starting with randomly chosen move.
         Returns the chosen move if simulated game was won"""

        # randomly choosing a move (disc) from a list of possible moves:
        firstMove = random.choice(self.possibleMovesList)
        self.update_dict(firstMove,self.player1c)        # updating chosen move in dictionary
        self.updateDiscsColor(firstMove)
        self.update_num_moves(self.player1c)
        self.game_on(firstMove)    # simulating a game continuing from chosen move
        return self.winnersDict

    def possible_moves(self):
        """ iterates over msin dictionary to create a list of poss"""
        psbleMovesList=[]
        for i in self.discDictCopy:
            if self.discDictCopy[i] is None:
                if self.valid_moves(i):
                    psbleMovesList.append(i)
        if len(psbleMovesList) > 0:
            self.count = 0
            return psbleMovesList
        else:
            if self.count < 2:
                self.count += 1
                raise NoPossibleMovesException
            else:
                counter = 0
                for k in self.discDictCopy:
                    if self.discDictCopy[k] is None:
                        counter += 1
                        self.discDictCopy[k] = "N"
                raise NoPossibleMovesException

    def valid_moves(self,disc):
        discColor = self.now_playing()
        if discColor == "W":
            cont = "B"
        else:
            cont = "W"

        flag = False

        for neighbor in self.AdjacencyDict[disc]:
            if self.get_disc_color(neighbor) == cont:
                d = neighbor - disc
                tempA = neighbor
                tempB = tempA + d
                while not flag:
                    if tempB in self.AdjacencyDict[tempA]:
                        if self.get_disc_color(tempB) == discColor:
                            return True
                        elif self.get_disc_color(tempB) == cont:
                            tempA = tempB
                            tempB = tempA + d
                        else:
                            break
                    else:
                        break
        return flag

    def now_playing(self):
        if self.get_num_moves(self.player2c) > self.get_num_moves(self.player1c):
            return self.player1c
        elif self.get_num_moves(self.player1c) == self.get_num_moves(self.player2c):
            return self.player2c

    def get_num_moves(self,player):
        if player == self.player1c:
            return self.player1Moves
        elif player == self.player2c:
            return self.player2Moves

    def update_num_moves(self, player):
        if player == self.player1c:
            self.player1Moves +=1
        elif player == self.player2c:
            self.player2Moves += 1

    def get_disc_color(self,disc):
        return self.discDictCopy[disc]

    def update_dict(self,disc,color):
        self.discDictCopy[disc] = color

    def fin_check(self):
        """ checking if game has ended"""
        for i in self.discDictCopy:
            if self.discDictCopy[i] is None:
                return False
        return True


    def updateDiscsColor(self,disc):
        """ colors adjacent discs in accordance with chosen disc and game rules
         disc is an int representing disc number
         """
        discColor = self.now_playing()
        if discColor == "W":
            cont = "B"
        else:
            cont = "W"

        nbrList = []
        # check which discs need to be colored
        for neighbor in self.AdjacencyDict[disc]:
            flag = False
            counter = 0
            if self.get_disc_color(neighbor) == cont:
                d = neighbor - disc # this is the direction
                tempA = neighbor
                tempB = tempA + d
                while not flag:
                    counter += 1
                    if tempB in self.AdjacencyDict[tempA]:
                        if self.get_disc_color(tempB) == discColor:
                            flag = True
                            nbrList.append([neighbor, counter])
                        elif self.get_disc_color(tempB) == cont:
                            tempA = tempB
                            tempB = tempA + d
                        else: break
                    else: break

                if flag:
                    nbrList.append([neighbor, counter])

        # create a list of the discs which need to be colored
        updateList=[]
        updateList.append(disc)
        for nbr in nbrList:
            d = nbr[0] - disc
            for count in range(nbr[1]):
                x = nbr[0] + d*count
                updateList.append(x)

        # update discs in main dictionary
        for disc in updateList:
            self.update_dict(disc,discColor)

    def game_on(self, firstMove):
        """ simulating a game by choosing a move randomly from a list of possible moves.
        """
        while not self.fin_check():
            player = self.now_playing()

            try:
                move = random.choice(self.possible_moves())
                self.update_dict(move, player) # update move in discs' dictionary
                self.updateDiscsColor(move)   # color neighbor discs as result of chosen move
                self.update_num_moves(player) # add move to number of moves for player
            except NoPossibleMovesException:   # if there is no possible move, an exception is raised and the turn goes to the next player
                self.update_num_moves(player)

        count1=0
        count2=0
        for disc in self.discDictCopy:
            if self.discDictCopy[disc] == self.player1c:
                count1 += 1
            else:
                count2 += 1
        if count1 > count2:
            self.winnersDict[firstMove] = self.winnersDict.get(firstMove,0) + 1


class SimulationManager(object):
    """ using multiprocessing to run simulations in parallel"""
    def __init__(self):
        self.pool = mp.Pool(5) # determining the number of

    def go_to(self, args):
        # this method
        return Simulations(args).simulation()

    def run(self,args_list):
        result = self.pool.map(self.go_to, args_list)
        return result

    def __getstate__(self):
        """ returned object is pickled as the contents for the instance,
         instead of the contents of the instance’s dictionary"""
        pass



class NoPossibleMovesException(Exception):
    """ NoPossibleMovesException is raised by the possible moves() method in the simulations
    class to indicate that there are no possible moves for player in current situation"""


class Weighted_Simulations(Simulations):
    pass


if __name__ == '__main__':
    """this part is only relevant when running simulations from this file and not as part of the game """

    start_time = time.time()
    manager = SimulationManager()
    disc_dict = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None, 10: None, 11: None, 12: None, 13: None, 14: None, 15: None, 16: None, 17: None, 18: None, 19: None, 20: None, 21: None, 22: None, 23: None, 24: None, 25: None, 26: None, 27: None, 28: 'W', 29: 'B', 30: None, 31: None, 32: None, 33: None, 34: None, 35: 'W', 36: 'W', 37: 'W', 38: None, 39: None, 40: None, 41: None, 42: None, 43: None, 44: None, 45: None, 46: None, 47: None, 48: None, 49: None, 50: None, 51: None, 52: None, 53: None, 54: None, 55: None, 56: None, 57: None, 58: None, 59: None, 60: None, 61: None, 62: None, 63: None, 64: None}
    player1_color = "B"
    player1_moves = 0
    player2_moves = 1
    adjacency_dict = {1: [2, 9, 10], 2: [1, 3, 10, 11], 3: [2, 4, 10, 11, 12], 4: [3, 5, 11, 12, 13], 5: [4, 6, 12, 13, 14], 6: [5, 7, 13, 14, 15], 7: [6, 8, 14, 15], 8: [7, 15, 16], 9: [1, 10, 17, 18], 10: [1, 2, 3, 9, 11, 17, 18, 19], 11: [2, 3, 4, 10, 12, 18, 19, 20], 12: [3, 4, 5, 11, 13, 19, 20, 21], 13: [4, 5, 6, 12, 14, 20, 21, 22], 14: [5, 6, 7, 13, 15, 21, 22, 23], 15: [6, 7, 8, 14, 16, 22, 23, 24], 16: [8, 15, 23, 24], 17: [9, 10, 18, 25, 26], 18: [9, 10, 11, 17, 19, 25, 26, 27], 19: [10, 11, 12, 18, 20, 26, 27, 28], 20: [11, 12, 13, 19, 21, 27, 28, 29], 21: [12, 13, 14, 20, 22, 28, 29, 30], 22: [13, 14, 15, 21, 23, 29, 30, 31], 23: [14, 15, 16, 22, 24, 30, 31, 32], 24: [15, 16, 23, 31, 32], 25: [17, 18, 26, 33, 34], 26: [17, 18, 19, 25, 27, 33, 34, 35], 27: [18, 19, 20, 26, 28, 34, 35, 36], 28: [19, 20, 21, 27, 29, 35, 36, 37], 29: [20, 21, 22, 28, 30, 36, 37, 38], 30: [21, 22, 23, 29, 31, 37, 38, 39], 31: [22, 23, 24, 30, 32, 38, 39, 40], 32: [23, 24, 31, 39, 40], 33: [25, 26, 34, 41, 42], 34: [25, 26, 27, 33, 35, 41, 42, 43], 35: [26, 27, 28, 34, 36, 42, 43, 44], 36: [27, 28, 29, 35, 37, 43, 44, 45], 37: [28, 29, 30, 36, 38, 44, 45, 46], 38: [29, 30, 31, 37, 39, 45, 46, 47], 39: [30, 31, 32, 38, 40, 46, 47, 48], 40: [31, 32, 39, 47, 48], 41: [33, 34, 42, 49, 50], 42: [33, 34, 35, 41, 43, 49, 50, 51], 43: [34, 35, 36, 42, 44, 50, 51, 52], 44: [35, 36, 37, 43, 45, 51, 52, 53], 45: [36, 37, 38, 44, 46, 52, 53, 54], 46: [37, 38, 39, 45, 47, 53, 54, 55], 47: [38, 39, 40, 46, 48, 54, 55, 56], 48: [39, 40, 47, 55, 56], 49: [41, 42, 50, 57], 50: [41, 42, 43, 49, 51, 57, 58, 59], 51: [42, 43, 44, 50, 52, 58, 59, 60], 52: [43, 44, 45, 51, 53, 59, 60, 61], 53: [44, 45, 46, 52, 54, 60, 61, 62], 54: [45, 46, 47, 53, 55, 61, 62, 63], 55: [46, 47, 48, 54, 56, 62, 63, 64], 56: [47, 48, 55, 64], 57: [49, 50, 58], 58: [50, 51, 57, 59], 59: [50, 51, 52, 58, 60], 60: [51, 52, 53, 59, 61], 61: [52, 53, 54, 60, 62], 62: [53, 54, 55, 61, 63], 63: [54, 55, 62, 64], 64: [55, 56, 63]}

    args = (disc_dict,player1_color,player1_moves,player2_moves,adjacency_dict)
    args_list = []
    for i in range(50):
        args_list.append(args)

    result = manager.run(args_list)
    # discDict,player1Color,player1Moves,player2Moves,AdjacencyDict
    # args = (disc_dict,player1_color,player1_moves,player2_moves,adjacency_dict)
    # simulation_init = Simple_Simulations(args)
    #mp_simulation1 = using_multiprocessing(disc_dict,player1_color,player1_moves,player2_moves,adjacency_dict)

    print("result =", result)
    end_time = time.time() - start_time
    print(f"time: {end_time}")

    resultsDict = {}
    for dict in result:
        for i in dict:
            resultsDict[i] = resultsDict.get(i, 0) + 1

    maxMove = 0
    winner = 0
    for move in resultsDict:
        if resultsDict[move] > maxMove:
            maxMove = resultsDict[move]
            winner = move
    print("winner:", winner, maxMove)