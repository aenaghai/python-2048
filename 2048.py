import tkinter as tk
import colors as cl
import random

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        
        self.main_grid = tk.Frame(
            self, bg=cl.GRID_COLOR, bd=4, width=450, height=450)
        self.main_grid.grid(pady=(80,0))
        
        
        self.GUI()
        self.startgame()
        
        self.master.bind("<Left>",self.left)
        self.master.bind("<Right>",self.right)
        self.master.bind("<Up>",self.up)
        self.master.bind("<Down>",self.down)

        self.mainloop()
        
        
    def GUI(self):
        #making the 4by4 grid
        #2D list holding the information containing each cell in the grid
        self.cells = [] 
        #nested for loop to append to cells, row by row
        for i in range(4):
            row=[]
            for j in range(4):
                cellframe = tk.Frame(
                    self.main_grid, 
                    bg=cl.EMPTY_CELL_COLOR, width=95, height=95)
            
                cellframe.grid(row=i, column=j, padx=5, pady=5)
                cellnumber = tk.Label(self.main_grid, bg=cl.EMPTY_CELL_COLOR)
                cellnumber.grid(row=i, column=j)
                #creating a dictionary to store data for the widgets
                celldata = {'frame':cellframe,'number':cellnumber}
                row.append(celldata)
            self.cells.append(row)
        
        #making the score header :)
        scoreframe = tk.Frame(self)
        scoreframe.place(relx=0.5,y=40,anchor="center")
        #anchor center to justify it there and 45 the padding added along with rel x at 0.5; grid(r=0) to position it at the top
        tk.Label(
            scoreframe,
            text='SCORE', 
            font=cl.SCORE_LABEL_FONT).grid(row=0)
        
        self.scorelabel = tk.Label(scoreframe,text='0',font=cl.SCORE_FONT)
        self.scorelabel.grid(row=1)
        
        

    def startgame(self):
        #initializing by creating a matrix of all zeroes
        self.matrix = [ [0]*4 for _ in range (4) ]
        
        #first selecting 2 random row and column indices to fill in the 2s
        #placing the two 2s randomly in the matrix for the game to beign
        row = random.randint(0,3)
        col = random.randint(0,3)
        
        #to display the 2 on the gui
        self.matrix[row][col] = 2
        self.cells[row][col]['frame'].configure(bg=cl.CELL_COLORS[2])
        self.cells[row][col]['number'].configure(
            bg=cl.CELL_COLORS[2], 
            fg=cl.CELL_NUMBER_COLORS[2], 
            font=cl.CELL_NUMBER_FONTS[2], text="2")  
        
        #ensuring we choose a different cell
        while(self.matrix[row][col] != 0):
            row = random.randint(0,3) 
            col = random.randint(0,3)
        
        self.matrix[row][col] = 2
        self.cells[row][col]['frame'].configure(bg=cl.CELL_COLORS[2])
        self.cells[row][col]['number'].configure(bg=cl.CELL_COLORS[2], fg=cl.CELL_NUMBER_COLORS[2], font=cl.CELL_NUMBER_FONTS[2], text="2")
        
        #setting up the inital state of the game, i.e. initial score=0
        self.score = 0
        
    #functions manipulate the matrix and start game, which are called in differenst combinations based on the move made by the player
    #these functions use nested for loops to change the values and/or positions according to the move
        
    #1 Stack: it'll compress all the non-zero numbers in the matrix towards one side of board, eliminating all the gaps of empty cells between them
    def stack(self):
        newmatrix = [ [0]*4 for _ in range(4) ]
        for i in range(4):
            fillposition = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    newmatrix[i][fillposition] = self.matrix[i][j]
                    fillposition += 1
        self.matrix = newmatrix
        
    #2 combine: adds together horizontally the numbers of same value in the matrix. it merges them to the left position
    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] !=0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0
                    self.score += self.matrix[i][j]
        
    #3 reverse row: reverses the order of each row in the matrix
    def reverse(self):
        newmatrix = []
        for i in range(4):
            #make sure to append an empty list to newmatrix for each row
            newmatrix.append([])
            for j in range(4):
                #to reverse the order in the matrix
                newmatrix[i].append(self.matrix[i][3-j])
        self.matrix = newmatrix   
            
    #4 transpose: flips the matrix over the diagonal
    def transpose(self):
        newmatrix = [ [0]*4 for _ in range(4) ]
        for i in range(4):
            for j in range(4):
                newmatrix[i][j] = self.matrix[j][i]
        self.matrix = newmatrix   
        
    #function that adds a new tile(2or4) after each move to an empty cell
    #we use same approach as we did for the initialsing with two 2s
    def addnewtile(self):
        row = random.randint(0,3)
        col = random.randint(0,3)
        
        #ensuring we choose a different cell
        while(self.matrix[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        
        self.matrix[row][col] = random.choice([2,4])
    
    #updating gui, to correspond to the newly formed matrix
    def updategui(self):
        for i in range(4):
            for j in range(4):
                cellvalue = self.matrix[i][j]
                if cellvalue == 0:
                    self.cells[i][j]['frame'].configure(bg = cl.EMPTY_CELL_COLOR)
                    self.cells[i][j]['number'].configure(bg = cl.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]['frame'].configure(bg = cl.CELL_COLORS[cellvalue])
                    self.cells[i][j]['number'].configure(bg = cl.CELL_COLORS[cellvalue], fg= cl.CELL_NUMBER_COLORS[cellvalue], font = cl.CELL_NUMBER_FONTS[cellvalue], text = str(cellvalue) )
        self.scorelabel.configure(text = self.score) 
        self.update_idletasks() 
     
    #assigning arrow keys for the specified function to that arrow 
    def left(self,event):
        self.stack()
        self.combine()
        self.stack()
        self.addnewtile()
        self.updategui()
        self.gameover()
    
    def right(self,event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.addnewtile()
        self.updategui()
        self.gameover()
    
    def up(self,event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.addnewtile()
        self.updategui()
        self.gameover()

    
    def down(self,event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.addnewtile()
        self.updategui()
        self.gameover()
        
    #check if any moves are possible 
    def horizontalexists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False
    
    def verticalexists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False
    
    #win/loss?
    def gameover(self):
        if any(2048 in row for row in self.matrix):
            gameoverframe = tk.Frame(self.main_grid, borderwidth=2)
            gameoverframe.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(gameoverframe,text='You Won!', bg = cl.WINNER_BG, fg = cl.GAME_OVER_FONT_COLOR, font = cl.GAME_OVER_FONT).pack()
        
        elif not any (0 in row for row in self.matrix) and not self.horizontalexists() and not self.verticalexists():
            gameoverframe = tk.Frame(self.main_grid, borderwidth=2)
            gameoverframe.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(gameoverframe,text='Game Over!', bg = cl.LOSER_BG, fg = cl.GAME_OVER_FONT_COLOR, font = cl.GAME_OVER_FONT).pack()
        
    
def main():
    Game()
         
if __name__ == "__main__":
    main()
        