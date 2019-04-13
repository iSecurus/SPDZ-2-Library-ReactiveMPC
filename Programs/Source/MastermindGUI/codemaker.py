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
    
    buttons = []
    
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
    
    def create_button(self, row, column):
        button = tk.Button(self)
        button["command"] = lambda: self.change_color(button)
        button["bg"] = "red"
        button["activebackground"] = "red"
        button["width"] = 10
        button["height"] = 5
        button.grid(row=row, column=column)
        self.buttons.append(button)
    
    def __label_wait_for_player(self):
        self.label.configure(text="Its codebreakers turn! Please wait...")
        self.send_button.configure(text="Done!")
        self.send_button.configure(state="disabled")
    
    def send(self):
        for button in self.buttons:
            prog.add_input(self.colornummap[button["bg"]])
            button.configure(state="disabled")
        self.__label_wait_for_player()
        
        self.update()
        
        result = prog.get_output("result")
        
        if int(result) == 0:
            self.label.configure(text="You won! Codebreaker could not guess your code!")
        else:
            self.label.configure(text="You loose! Codemaker guessed your code!")
            
    def create_widgets(self):
        self.label = tk.Label(self, text="Please enter the code:")
        self.label.grid(row=0, column=0, columnspan=4)
        for i in range(0,4):
            self.create_button(1, i)        
        
        self.send_button = tk.Button(self, text="Send Code", fg="red",
                              command=self.send)
        self.send_button.grid(row=2, column=1, columnspan=2)

    def change_color(self, button):
        '''Change the current color of an button by every click'''
        button.configure(bg = self.colormap[button["bg"]])
        button.configure(activebackground = button["bg"])

#Start up the GUI and initialize the MPC-Program
root = tk.Tk()
root.title("Mastermind: Codemaker!")
app = GUI(master=root)
prog = SPDZ.MPCProgram("mastermind_core", port=port, hostname=hostname, f2n=f2n)
prog.run()
app.mainloop()