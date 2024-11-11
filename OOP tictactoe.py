from functools import cmp_to_key
from random import randint

class Board:
    def __init__(self,size):
        self.size = size
        self.board = []
        for i in range(size):
            row = []
            for i in range(size):
                row += [" "]
            self.board.append(row)
            #print(row)
        #print(self.board)
        
        # self.board = [
        #     [" "," "," "],    
        #     [" "," "," "],
        #     [" "," "," "],      # the basic board
        # ]
#1:
        self.winning_sets = []
        # add winning rows and columns:
        winning_diagonal = []
        winning_other_diagonal = []
        for i in range(self.size):
            # print("i",i)
            winning_row = []
            winning_col = []
            
            for j in range(self.size):
                # print("j",j)
                winning_row.append([i,j])
                winning_col.append([j,i])
                if i == j:
                    winning_diagonal.append([i,j])
                if i == (self.size - 1) - j:
                    winning_other_diagonal.append([i,j])
                #print("winning_row",winning_row)
                #print("winning col",winning_col)
                # print("winning_diagonal",winning_diagonal)
                # print("other diagonal",winning_other_diagonal)
            self.winning_sets.append(winning_row)
            self.winning_sets.append(winning_col)
        self.winning_sets.append(winning_diagonal)
        self.winning_sets.append(winning_other_diagonal)

        # for s in self.winning_sets:
        #     print (s)

        # create array of sets sorted by their emptiness
        def compare(a,b):
            # compare 2 sets to see which has more symbols
            # go through a, counting coordinates with symbols in
            # print("a",a)
            counta = 0
            for coordinate in a:
                if self.board[coordinate[0]][coordinate[1]] != " ":
                    counta += 1
            # print("counta",counta)

            # print("b",b)
            countb = 0
            for coordinate in b:
                if self.board[coordinate[0]][coordinate[1]] != " ":
                    countb += 1
            # print("countb",countb)

            return counta - countb
        self.sorted_sets_by_emptiness = sorted(self.winning_sets,key=cmp_to_key(compare))
        self.sorted_sets_by_emptiness.reverse()
        # for s in sorted_sets:
        #     print(s)


    def check_for_end(self):
        for columnrow in range(self.size): 
            # check for a full column
            # if the current column in the first row is a symbol, check if any rows have a different symbol. if they do, carry on the game. if they dont, end the game
            if self.board[0][columnrow].isalpha():      
                same = True
                for row in range(self.size):
                    if self.board[row][columnrow] != self.board[0][columnrow]:
                        same = False
                if same:
                    return("win")
                
            # check for a full row
            # if the current row in the first column is a symbol, check if any columns have a different symbol. if they do, carry on the game, if they dont, end the game
            if self.board[columnrow][0].isalpha():      
                same = True
                for column in range(self.size):
                    if self.board[columnrow][column] != self.board[columnrow][0]:
                        same = False
                if same:
                    return("win")                
            
        # check for \ diagonal
        # if first column in first row is a symbol, check if respective rows in respective columns are not equal. if they arent equal, carry on the game, if not end it
        if self.board[0][0].isalpha():
            same = True
            for columnrow in range(self.size):
                if self.board[columnrow][columnrow] != self.board[0][0]:
                    same = False
            if same:
                return("win")
        
        # check for / diagonal
        # if last column in first row is a symbol, check if respective rows in previous columns are not equal. if they arent equal, carry on the game, if not end it
        if self.board[0][self.size-1].isalpha():
            same = True
            for columnrow in range(self.size):
                #print(self.size - columnrow - 1)
                if self.board[columnrow][self.size - columnrow - 1] != self.board[0][self.size-1]:
                    same = False
            if same:
                return("win")
            
        # check if there are still valid moves remaining
        for row in self.board:
            for col in row:
                if col == " ":
                    return ("on")
                
        # no more moves and no winner means the game must be a tie  
        return ("tie")
    
    def render(self):
        output = ""
        for row in self.board:
            output += (f"{row}\n")
        #return(f"{self.board[0]}\n{self.board[1]}\n{self.board[2]}")                # display the current board before every round
        return(output)
    
    def move(self,row,col,symbol):
            if row > (self.size)-1 or col > (self.size)-1 or col < 0 or row < 0:      # prevent errors:
                print(col,row)
                print("\ninput not in range 1-3, try again")                            # if the input is greater than the amount of rows/columns or is a letter
            elif self.board[row][col].isalpha():                                   # or if the player plays in a slot that is already full
                print("\nslot is already full, try again:")
            else:                      # place the players letter in their slot
                self.board[row][col] = symbol
                return "successful"
            return "invalid"
    
    def best_next_move1(self):
        #   find the best possible move for the player and return it
        # 1. determine all possible winning sets of coordinates on the board
        # 2. sort sets by how full they are (descending)
        # 3. pick random one from fullest set
 
        return self._rand_empty_coordinate(self.sorted_sets_by_emptiness)
            
    def _rand_empty_coordinate(self,sets):
        # find a random empty coordinate in the first set
        for winning_set in sets:
            # print("winning_set",winning_set)
            emptycoords = []
            for coordinate in winning_set:
                if self.board[coordinate[0]][coordinate[1]] == " ":
                    emptycoords.append(coordinate)
            # print("count",len(emptycoords))
            if len(emptycoords):
                # print(winning_set)
                return emptycoords[randint(0,(len(emptycoords)-1))]
        print("SHOULD NOT GET HERE")
        exit()
            

    def best_next_move2(self,player):
        #   find the best possible move for the player and return it
        # 1. determine all possible winning sets of coordinates on the board
        # 2. sort sets by how full they are (descending)
        # 3. remove any with opponent symbol
        # 4. if there are no left do best_next_move1
        # 5. pick random one from fullest set
        sorted_sets_by_emptiness_no_opposition = []
        for winning_set in self.sorted_sets_by_emptiness:
            opposition = False
            for coordinate in winning_set:
                if self.board[coordinate[0]][coordinate[1]] != " " and self.board[coordinate[0]][coordinate[1]] != player.symbol:
                    opposition = True
            if not opposition:
                sorted_sets_by_emptiness_no_opposition.append(winning_set)
        # print("sorted sets by emptiness no opposition",sorted_sets_by_emptiness_no_opposition)

        if len(sorted_sets_by_emptiness_no_opposition) == 0:
            return self.best_next_move1()
        
        return self._rand_empty_coordinate(sorted_sets_by_emptiness_no_opposition)
        
                
class Player:
    def __init__(self,symbol,number):
        self.symbol = symbol
        self.number = number
        self.score = 0

    def win(self):
        self.score += 1

class Bot(Player):
    def __init__(self, symbol, number):
        super().__init__(symbol, number)

    
    
class Game:
    def __init__(self,player1,player2,size):
        self.board = Board(size)
        self.player1 = player1
        self.player2 = player2
        # print(self.player1)
        # print(self.player1.symbol)
        # print(self.player2)
        # print(self.player2.symbol)
        # print(self.board)
        # print(self.board.board)
        # print(self.board.check_for_win())
        # self.board.move(1,1,2)
        # self.board.move(0,0,1)
    def play(self):
        game = "on"
        round = 1
        while game == "on":
            if round % 2 == 1:
                player_playing = self.player1
            else:
                player_playing = self.player2

            print(self.board.render())
            print(f"it is player {player_playing.number}'s turn")              # display whos turn it is

            if player_playing.algorithm == 1:
                best_coordinate = self.board.best_next_move1()
            elif player_playing.algorithm == 2:
                best_coordinate = self.board.best_next_move2(player_playing)
            else:
                best_coordinate = self.board.best_next_move1()

            if isinstance(player_playing,Bot):
                play_row = best_coordinate[0]
                play_col = best_coordinate[1]
            else:
                play_row = int(input(f"what row would you like to play (best:{best_coordinate[0]+1}):      "))-1  # player chooses where they want to play
                play_col = int(input(f"what column would you like to play (best:{best_coordinate[1]+1}):   "))-1

            if self.board.move(play_row,play_col,player_playing.symbol) == "successful":
                if self.board.check_for_end() == "win":          # check if the game is finished
                    print(self.board.render())
                    print(f"game over, player{player_playing.number} wins the game")
                    game = "over"
                    player_playing.win()

                elif self.board.check_for_end() == "tie":
                    print(self.board.render())
                    print("game over, it was a tie")
                    game = "over"
                    # both players get a point
                    self.player1.win()
                    self.player2.win()
                else:
                    print("game carries on\n")
                    round += 1
                

# game.play()

def winning_score(rounds):
    return int(rounds/2)+1

round = 1
rounds = int(input("How many rounds do you want to play?:   "))
size = int(input("How big would you like the board to be?:  "))

bot1_input_invalid = True
bot2_input_invalid = True
while bot1_input_invalid == True:
    bot1 = input("Is player1 a bot? (y/n):       ")
    if bot1 == "y" or bot1 == "n":
        bot1_input_invalid = False
    else:
        print("Incorrect input please try again,")
while bot2_input_invalid == True:
    bot2 = input("Is player2 a bot? (y/n):       ")
    if bot2 == "y" or bot2 == "n":
        bot2_input_invalid = False
    else:
        print("Incorrect input please try again,")
    
if bot1 == "y":
    player1 = Bot("x",1)
    print("Player 1 Algorithms:")
    print("1 - random empty space in fullest row")
    print("2 - random empty space in fullest row with no opposition symbols")
    algorithm = int(input("Which algorithm for the bot would you like to use?   "))
    validalgorithm = False
    while not validalgorithm:
        if algorithm in [1,2]:
            player1.algorithm = algorithm
            validalgorithm = True
        else:   
            print("invalid algorithm choice, try again")
else:
    player1 = Player("x",1)
    player1.algorithm = 0

if bot2 == "y":
    player2 = Bot("o",2)
    print("Player 2 Algorithms:")
    print("1 - random empty space in fullest row")
    print("2 - random empty space in fullest row with no opposition symbols")
    algorithm = int(input("Which algorithm for the bot would you like to use?   "))
    validalgorithm = False
    while not validalgorithm:
        if algorithm in [1,2]:
            player2.algorithm = algorithm
            validalgorithm = True
        else:   
            print("invalid algorithm choice, try again")
else:
    player2 = Player("o",2)
    player2.algorithm = 0

# print(winning_score(3))
# print(winning_score(4))
# print(winning_score(5))
# print(winning_score(6))
# print(winning_score(7))   test
# print(winning_score(8))
# print(winning_score(9))
# print(winning_score(10))


while True:
    print(f"Round {round}")
    game = Game(player1,player2,size)
    game.play()
    print("player1",player1.score,"player2",player2.score)
    if player1.score == winning_score(rounds):
        print("Player 1 wins the tournament!")
        break
    if player2.score == winning_score(rounds):
        print("Player 2 wins the tournament!")
        break
    if round == rounds:
        print("tie")
        break
    

    round += 1
    print()

