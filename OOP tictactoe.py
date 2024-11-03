
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
    def check_for_win(self):
        for columnrow in range(self.size): 
            # check for a full column
            # if the current column in the first row is a symbol, check if any rows have a different symbol. if they do, carry on the game. if they dont, end the game
            if self.board[0][columnrow].isalpha():      
                same = True
                for row in range(self.size):
                    if self.board[row][columnrow] != self.board[0][columnrow]:
                        same = False
                if same:
                    return("over")
                
            # check for a full row
            # if the current row in the first column is a symbol, check if any columns have a different symbol. if they do, carry on the game, if they dont, end the game
            if self.board[columnrow][0].isalpha():      
                same = True
                for column in range(self.size):
                    if self.board[columnrow][column] != self.board[columnrow][0]:
                        same = False
                if same:
                    return("over")                
            
        # check for \ diagonal
        # if first column in first row is a symbol, check if respective rows in respective columns are not equal. if they arent equal, carry on the game, if not end it
        if self.board[0][0].isalpha():
            same = True
            for columnrow in range(self.size):
                if self.board[columnrow][columnrow] != self.board[0][0]:
                    same = False
            if same:
                return("over")
        
        # check for / diagonal
        # if last column in first row is a symbol, check if respective rows in previous columns are not equal. if they arent equal, carry on the game, if not end it
        if self.board[0][self.size-1].isalpha():
            same = True
            for columnrow in range(self.size):
                print(self.size - columnrow - 1)
                if self.board[columnrow][self.size - columnrow - 1] != self.board[0][self.size-1]:
                    same = False
            if same:
                return("over")
            
        return ("on")
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

class Player:
    def __init__(self,symbol,number):
        self.symbol = symbol
        self.number = number
        self.score = 0
    def win(self):
        self.score += 1
    
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

            play_row = int(input("what row would you like to play:      "))-1  # player chooses where they want to play
            play_col = int(input("what column would you like to play:   "))-1

            if self.board.move(play_row,play_col,player_playing.symbol) == "successful":
                if self.board.check_for_win() == "over":          # check if the game is finished
                    print(self.board.render())
                    print(f"game over, player{player_playing.number} wins the game")
                    game = "over"
                    player_playing.win()

                else:
                    print("game carries on\n")
                    round += 1
                
player1 = Player("x",1)
player2 = Player("o",2)
# game.play()

def winning_score(rounds):
    return int(rounds/2)+1

round = 1
rounds = int(input("How many rounds do you want to play?:   "))
size = int(input("How big would you like the board to be?:  "))
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
