import tkinter as tk
import tkinter.messagebox as tk_msgbox

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.nameInput = tk.Entry(self)
        self.nameInput.pack()
        self.alertButton = tk.Button(self, text='Hello', command=self.hello)
        self.alertButton.pack()

    # def createWidgets(self):
    #     top=self.winfo_toplevel()
    #     top.rowconfigure(0, weight=1)
    #     top.columnconfigure(0, weight=1)
    #     self.rowconfigure(0, weight=1)
    #     self.columnconfigure(0, weight=1)
    #     self.quit = tk.Button(self, text='Quit', command=self.quit)
    #     self.quit.grid(row=0, column=0,)
    #     sticky=tk.N+tk.S+tk.E+tk.W


    def hello(self):
        name = self.nameInput.get() or 'world'
        tk_msgbox.showinfo('Message', 'Hello, %s' % name)

root=tk.Tk()
app=Application(root)
app.mainloop()
