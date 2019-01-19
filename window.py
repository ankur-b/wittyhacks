import sys
import tkinter

def main():
    root = tkinter.Tk()
    root.title('Game')
    root.geometry("500x500")
    root.configure(background='black')
    root.attributes("-fullscreen", True)
    root.resizable(width = True, height = True)
    root.mainloop()
