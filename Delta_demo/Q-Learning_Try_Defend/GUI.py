import tkinter as tk

UNIT = 50

window = tk.Tk()
window.title('checkboard')
window.geometry('553x553')

checkboard = tk.Canvas(window, bg='tan2', height=553, width=553)
checkboard.create_text(25, 255, text='9\n\n8\n\n7\n\n6\n\n5\n\n4\n\n3\n\n2\n\n1\n\n0', font=('Time New Roman', 16), anchor='center')
checkboard.create_text(288, 528, text='a      b      c      d      e      f      g      h      i      j', font=('Time New Roman', 16), anchor='center')

for x in range(0, 11, 1):
    checkboard.create_rectangle(50 + UNIT * x - 1, 3, 50 + UNIT * x + 1, 503, fill='black')

for y in range(0, 11, 1):
    checkboard.create_rectangle(50, 3 + UNIT * y - 1, 551, 3 + UNIT * y + 1, fill='black')

checkboard.pack()

window.mainloop()
