__author__ = 'Hagar'
import random, math, multiprocessing as mp, time




class Simple_Simulations(object):
    def __init__(self,discDict,player1Color,player1Moves,player2Moves,AdjacencyDict):
        self.discDictCopy = discDict.copy()
        self.winnersDict={}
        self.player1c = player1Color
        if self.player1c == "B": self.player2c = "W"
        else: self.player2c = "B"
        self.currentPlayer = player1Color
        self.player1Moves = player1Moves
        self.player2Moves = player2Moves
        self.AdjacencyDict = AdjacencyDict
        self.count = 0
        self.possibleMovesList = self.possible_moves()

    def simulation(self, player1Moves, player2Moves, discDict):
        numSimulations = 1000
        print(f"IN SIMULATION\np1moves: {player1Moves} \np2moves: {player2Moves}\ncolor: {self.currentPlayer}")
        start_time = time.time()
        for simulation in range(numSimulations):
            discDictC = discDict.copy()
            self.reset_vars(player1Moves, player2Moves, discDictC)       #reseting so each simulations starts from the same place
            firstMove = random.choice(self.possibleMovesList)
            self.update_dict(firstMove,self.player1c)
            self.updateDiscsColor(firstMove)
            self.update_num_moves(self.player1c)
            self.game_on(firstMove)

        end_time = time.time() - start_time
        print(f"winnerDict: {self.winnersDict} \n time: {end_time}")
        maxMove = 0
        winner = 0
        for move in self.winnersDict:
            if self.winnersDict[move] > maxMove:
                maxMove = self.winnersDict[move]
                winner = move
        print ("winner:",winner,maxMove)
        return winner

    def reset_vars(self,player1Moves,player2Moves,discDict):
        self.player1Moves = player1Moves
        self.player2Moves = player2Moves
        self.discDictCopy = discDict
        self.count = 0

    def possible_moves(self):
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
                print("no moves?",self.discDictCopy)
                for k in self.discDictCopy:
                    if self.discDictCopy[k] is None:
                        counter += 1
                        self.discDictCopy[k] = "N"
                print ("counter=",counter)
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
        for neighbor in AdjacencyDict[disc]:
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
        while not self.fin_check():
            player = self.now_playing()

            try:
                move = random.choice(self.possible_moves())
                self.update_dict(move, player) # update move in discs' dictionary
                self.updateDiscsColor(move)   # color neighbor discs as result of chosen move
                self.update_num_moves(player) # add move to number of moves for player
            except NoPossibleMovesException:
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


class NoPossibleMovesException(Exception):
    """ NoPossibleMovesException is raised by the possible moves() method in the simulations
    class to indicate that there are no possible moves for player in current situation"""

class Weighted_Simulations(Simple_Simulations):
    pass