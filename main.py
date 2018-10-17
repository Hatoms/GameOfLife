import sys
import time
import random
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.nb_cells = 150
        self.length_cells = 5
        self.speed = 100
        self.border=0
        self.w = None
        self.tab_cell = [[None for x in range(self.nb_cells)] for y in range(self.nb_cells)]
        self.createWidgets()
        self.w.bind('<Button-1>',self.change_life)
        self.generation = 0


    def createWidgets(self):

        self.w = tk.Canvas(self, width=self.nb_cells*self.length_cells, height=self.nb_cells*self.length_cells)
        self.w.grid(row=0, column=0, rowspan=4)
        self.start = tk.Button(self, text="Start!", command=self.main_event)
        self.start.grid(row=0, column=1)
        self.count = tk.Button(self, text="Generation : 0", command = lambda e: None)
        self.count.grid(row=1, column=1)
        self.quit = tk.Button(self, text="Quitter", command=quit)
        self.quit.grid(row=2, column=1)
        self.randomstartbutton = tk.Button(self, text="Random Start", command=self.randomstart)
        self.randomstartbutton.grid(row=3, column=1)

        for i in range(self.nb_cells):
            for j in range(self.nb_cells):
                self.cell = self.w.create_rectangle(i*self.length_cells,j*self.length_cells,self.length_cells*i+self.length_cells,self.length_cells*j+self.length_cells,width=self.border,fill='white')
                self.tab_cell[i][j] = [self.cell,False,False]


    def read_file(self):

        file = open(sys.argv[1],'r')
        while True:
            l = file.readline()
            if l[0] == '':
                return 0
            elif l[0] == '#':
                continue
            else:
                break
        try:
            varx = l[4:]
            i=0
            while varx[i] != ',' and i < 10:
                    i+=1

            varx=int(varx[:i])
            vary = l[(10+i):]
            i=0
            while vary[i] != ',' and i < 10:
                    i+=1

            vary=int(vary[:i])

            x = self.nb_cells/2 - varx/2
            y = self.nb_cells/2 - vary/2

            origx = x

            l = file.readline()
            count=''
            while l != '':

                for c in l:
                    if ord(c)>47 and ord(c)<58:
                        count = count + c
                    elif c == 'b':
                        count = 1 if count == '' else int(count)
                        for i in range(count):
                            x += 1
                            self.set_state(self.tab_cell[x][y],False)
                        count = ''
                    elif c == 'o':

                        count = 1 if count == '' else int(count)
                        for i in range(count):
                            x += 1
                            self.set_state(self.tab_cell[x][y],True)
                        count = ''
                    elif c == '$':
                        y += 1
                        x = origx

                    elif c == '!':
                        return 0
                l = file.readline()


        except IndexError as e:
            print(e)
            


    def set_state(self,cell,state):
        newcol = 'black' if state else 'white'
        cell[2] = state
        cell[1] = state
        self.w.itemconfig(cell[0], fill=newcol)


    def change_life(self,event):

        numx = event.x/self.length_cells
        numy = event.y/self.length_cells
        if numx < self.nb_cells and numy< self.nb_cells:

            newstate = not self.tab_cell[numx][numy][1]
            newcol = 'black' if newstate else 'white'
            self.tab_cell[numx][numy][2] = newstate
            self.tab_cell[numx][numy][1] = newstate
            self.w.itemconfig(self.tab_cell[numx][numy][0], fill=newcol)


    def randomstart(self):
        r = 0
        for i in range(20,self.nb_cells-20):
            for j in range(20,self.nb_cells-20):
                r = random.random()
                newstate = True if r > 0.70 else False
                newcol = 'black' if newstate else 'white'
                self.tab_cell[i][j][2] = newstate
                self.tab_cell[i][j][1] = newstate
                self.w.itemconfig(self.tab_cell[i][j][0], fill=newcol)

    def main_event(self):

        self.next_gen()
        self.generation += 1
        self.count.config(text="Generation : %i"%self.generation)
        global begin_id
        begin_id = self.after(self.speed, self.main_event)

    def next_gen(self):


        for i in range(self.nb_cells):
            for j in range(self.nb_cells):
                self.pre_evolve(i,j)

        for i in range(self.nb_cells):
            for j in range(self.nb_cells):
                self.evolve(i,j)


    def pre_evolve(self,i,j):

        neighbour = self.get_nb_neighbour(i,j)
        cell = self.tab_cell[i][j]
        if cell[1]:
            if neighbour < 2 or neighbour > 3 :
                cell[2] = False
        elif neighbour == 3:
            cell[2] = True

    def evolve(self,i,j):

        cell = self.tab_cell[i][j]
        cell[1]=cell[2]
        if cell[1]:
            self.w.itemconfig(cell[0], fill='black')

        else:
            self.w.itemconfig(cell[0], fill='white')


    def get_nb_neighbour(self,i,j):
        neighbour = 0
        for coef in [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]:
            try:
                if self.tab_cell[i+coef[0]][j+coef[1]][1]:
                    neighbour+=1
            except IndexError:
                pass
        return neighbour


app = Application()
if len(sys.argv) > 1:
    app.read_file()
else:
    app.randomstart()

app.master.title('Game of life')
app.mainloop()
