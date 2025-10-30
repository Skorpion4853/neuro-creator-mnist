from NewWindow import *
from tkinter.messagebox import showerror


i = 0
def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def erase(event):
    global last_x, last_y
    x, y = event.x, event.y
    canvas.create_line(last_x, last_y, x, y, width=30, fill="black", capstyle=ROUND)
    last_x, last_y = x, y

def draw(event):
    global last_x, last_y
    x, y = event.x, event.y
    canvas.create_line(last_x, last_y, x, y, width=10, fill="white", capstyle=ROUND)
    last_x, last_y = x, y

def saveFile():
    global i, labelWrite
    if i <= 8:
        btn2.configure(state=NORMAL)
        ps = canvas.postscript(colormode='color', x=0, y=0, width=canvas.winfo_width(), height=canvas.winfo_height())
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        # Конвертировать изображение в RGB для дальнейших обработки
        img = img.convert('RGB')
        img.save(f"source/mnist/{i}.png")
        i += 1
        labelWrite.configure(
            text=f'Введите цифру {i} в поле ниже, \nleft click - рисовать              right click - стереть'
        )
        canvas.delete('all')
        canvas.create_rectangle((0, 0), (285, 285), fill="black", outline="black")
    elif i == 9:
        labelWrite.configure(
            text=f'Введите цифру {i} в поле ниже, \nleft click - рисовать              right click - стереть'
        )
        ps = canvas.postscript(colormode='color', x=0, y=0, width=canvas.winfo_width(), height=canvas.winfo_height())
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img = img.convert('RGB')
        img.save(f"source/mnist/{i}.png")
        canvas.delete('all')
        root.destroy()
        create_window_train()
    else:
        showerror('Ошибка', 'Случилась непредвиденная ошибка просьба обратиться к преподавателю')
def prevFile():
    global i, labelWrite
    if i == 1:
        btn2.configure(state=DISABLED)
    i -= 1
    labelWrite.configure(
        text=f'Введите цифру {i} в поле ниже, \nleft click - рисовать              right click - стереть'
    )
    canvas.delete('all')


root = Tk()
root.title("Нейро-создатель MNIST")
root.geometry("425x400")
root.resizable(False, False)
root.iconbitmap(default="source/favicon.ico")
root.config(bg="white", padx=10)


labelWrite = Label(text=f'Введите цифру {i} в поле ниже, \nleft click - рисовать              right click - стереть', font=("TimesNewRoman", 14))
labelWrite.grid(row=0, columnspan=3)
canvas = Canvas(root, width=280, height=280, bg="black")
canvas.grid(row=1, columnspan=3, pady=10)
canvas.create_rectangle((0, 0), (285, 285), fill="black", outline="black")

canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<Button-3>", start_draw)
canvas.bind("<B3-Motion>", erase)

btn1 = Button(text='Далее', command=saveFile, background="#898989", foreground="white", font=("TimesNewRoman", 14))
btn1.grid(row=2, column=2, sticky="e")


btn2 = Button(text='Назад', command=prevFile, background="#898989", foreground="white", font=("TimesNewRoman", 14), state=DISABLED)
btn2.grid(row=2, column=0, sticky="w")

root.mainloop()