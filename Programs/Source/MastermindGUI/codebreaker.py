'''
(C) 2017 Malte Kruse. See License.txt.
'''
#Modify the Library import of SPDZ so it will fit to your
#library path.
import SPDZ2.Library.SPDZ as SPDZ
import tkinter as tk

#Modify those values as needed.
port=5000
hostname="localhost"
f2n=False

class GUI(tk.Frame):
    
    #Store the results
    round = 0
    correct = 0
    
    #Stores the 12 button rows
    buttons = []
    #Stores the result labels
    results = []
    
    #Maps the colorchange of an button in addtion
    #to the color before
    colormap = {'red' : 'blue',
                'blue' : 'green',
                'green' : 'white',
                'white' : 'lightblue',
                'lightblue' : 'yellow',
                'yellow' : 'red'}
    
    #Start indexing with 1, because 0 is needed as special
    #value for MPC - using this will lead to easier multiplications
    colornummap = {'red' : 1,
                   'blue' : 2,
                   'green' : 3,
                   'white' : 4,
                   'lightblue' : 5,
                   'yellow' : 6}
    
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
    
    def create_button_row(self, row):
        '''Create a row of buttons - one row per round.'''
        button_row= []
        for i in range(1,5):
            button = self.create_button()
            if row != self.round:
                button["bg"] = "grey"
                button.configure(state="disabled")
            button.grid(row=row, column=i)
            button_row.append(button)
        self.buttons.append(button_row)
        
    def create_button(self):
        '''Create an color changing button.'''
        button = tk.Button(self)
        button["bg"] = "red"
        button["activebackground"] = "red"
        button["command"] = lambda: self.change_color(button)
        return button
    
    def send(self):
        '''Send the guess for the current round to the MPC and wait for the
        results.'''
        if self.round < 12:
            button_row = self.buttons[self.round]
            for button in button_row:
                prog.add_input(self.colornummap[button["bg"]])
                button.configure(state="disabled")
                
            #Check the result and create the graphical output string
            correct = prog.pop_output("correct")
            result = int(correct) * "x "
            contained = prog.pop_output("contained")
            result += int(contained) * "o "
            
            if len(result) >= 4:
                result = result[:3] + "\n" + result[4:]
            self.results[self.round]['text'] = result
            
            self.round += 1
            if int(correct) == 4:
                self.send_button["state"] = "disabled"
                self.send_button["text"] = "You won!"
                self.send_button["fg"] = "red"
            elif self.round != 12:
                button_row = self.buttons[self.round]
                for button in button_row:
                    button["bg"] = "red"
                    button.configure(state="normal")
            else:
                self.send_button["state"] = "disabled"
                self.send_button["text"] = "You loose!"
                self.send_button["fg"] = "red"

    def create_widgets(self):
        '''Create the main window.'''
        for j in range(0,12):
            round_label = "%#2d. Runde:" % (j+1)
            label = tk.Label(self, text=round_label)
            label.grid(row = j, column = 0)
            
            self.create_button_row(j)       
             
            label = tk.Label(self, text="   \n   ")
            label.grid(row=j, column=5)
            self.results.append(label)
                 
        self.send_button = tk.Button(self, text="Send Code", fg="red",
                              command= lambda : self.send())
        self.send_button.grid(row=13, column=0, columnspan=6)

    def change_color(self, button):
        '''Change the current color of an button by every click'''
        button.configure(bg = self.colormap[button["bg"]])
        button.configure(activebackground = button["bg"])

#Start up the GUI and initialize the MPC-Program
root = tk.Tk()
root.title("Mastermind: Codebreaker!")
app = GUI(master=root)
prog = SPDZ.MPCProgram("mastermind_core", player=1, port=port, hostname=hostname, f2n=f2n)
prog.run()
app.mainloop()