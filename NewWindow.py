from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno, showerror
from PIL import Image
import numpy as np
import os
import keras
from keras import layers
from keras.datasets import mnist
from PIL import ImageGrab, Image
"""
Создание окна с выбором гиперпараметров
"""
def create_window_train():
    def gotoTrain(epochs, batch_size, val_size, optimizer, normalizer):
        result = askyesno(title="Подтвержение операции", message="Начать обучение?")
        if result:
            model, train_score, test_score = TrainNN(epochs, batch_size, val_size, optimizer, normalizer)
            windowTrain.destroy()
            create_window_predict(model, train_score, test_score, normalizer)
        else:
            showinfo("Результат", "Операция отменена")

    windowTrain = Tk()
    windowTrain.title("Нейро-создатель MNIST")
    windowTrain.geometry("425x400")
    windowTrain.resizable(False, False)
    windowTrain.iconbitmap(default="source/favicon.ico")
    windowTrain.config(bg="white", padx=10, pady=10)

    optionsEpochs = [i for i in range(1, 21)]
    optionsVal = [i for i in range(0, 31, 5)]
    optionsBatch = [
        0,
        2,
        4,
        8,
        16,
        32,
        64,
        128,
        256,
        512
    ]
    optionsOpt = [
        "SGD",
        "RMSprop",
        "Adam",
        "AdamW",
        "Adadelta",
        "Adagrad",
        "Adamax",
        "Adafactor",
        "Nadam",
        "Ftrl",
        "Lion",
    ]

    labelEpochs = Label(
        windowTrain,
        text="Введите количество эпох для обучения:",
        bg="white",
        fg="black",
        font=("Times New Roman", 14)
    )
    labelEpochs.pack(anchor=W)

    CBEpochs = ttk.Combobox(
        windowTrain,
        values=optionsEpochs,
        state="readonly",
        font=("Times New Roman", 14)
    )
    CBEpochs.current(14)
    CBEpochs.pack(anchor=W, pady=(0, 15))

    labelBatch = Label(
        windowTrain,
        text="Введите количество батчей для обучения:",
        bg="white",
        fg="black",
        font=("Times New Roman", 14)
    )
    labelBatch.pack(anchor=W)

    CBBatch = ttk.Combobox(
        windowTrain,
        values=optionsBatch,
        state="readonly",
        font=("Times New Roman", 14)
    )
    CBBatch.current(7)
    CBBatch.pack(anchor=W, pady=(0, 15))

    labelVal = Label(
        windowTrain,
        text="""Введите процент разбиения валидационной
выборки для обучения:""",
        bg="white",
        fg="black",
        font=("Times New Roman", 14),
        justify="left"
    )
    labelVal.pack(anchor=W)

    CBVal = ttk.Combobox(
        windowTrain,
        values=optionsVal,
        state="readonly",
        font=("Times New Roman", 14)
    )
    CBVal.current(2)
    CBVal.pack(anchor=W, pady=(0, 15))

    labelOptimizer = Label(
        windowTrain,
        text="Выберите оптимизатор обучения:",
        bg="white",
        fg="black",
        font=("Times New Roman", 14),
        justify="left"
    )
    labelOptimizer.pack(anchor=W)

    CBOptimizer = ttk.Combobox(
        windowTrain,
        values=optionsOpt,
        state="readonly",
        font=("Times New Roman", 14)
    )
    CBOptimizer.current(2)
    CBOptimizer.pack(anchor=W, pady=(0, 15))

    enabled = BooleanVar()
    enabled.set(True)

    enabled_checkbutton = Checkbutton(text="Включить нормализацию?", variable=enabled, font=("Times New Roman", 14))
    enabled_checkbutton.pack(anchor=W, pady=(0))


    btn = Button(text="Обучить модель", background="#898989", foreground="white", command=lambda: gotoTrain(int(CBEpochs.get()), int(CBBatch.get()), int(CBVal.get())/100, CBOptimizer.get(), bool(enabled.get())), font=("Times New Roman", 14))
    btn.pack(fill=BOTH,pady=(15, 0))

    windowTrain.mainloop()

"""
Создание скрипта для обучения MNIST
"""
def TrainNN(epochs, batchSize, valBatchSize, optimizer, normalization):
    (x_train, y_train), (x_test, y_test) = mnist.load_data(
    path="C:/Users/skorpion/PyCharmMiscProject/source/mnist.npz"
)
    my_images = []
    my_labels = []

    for filename in os.listdir("source/mnist"):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img = Image.open(os.path.join("source/mnist", filename)).convert("L")  # grayscale
            img = img.resize((28, 28))  # размер как в MNIST
            arr = np.array(img)
            my_images.append(arr)

            # Пример: извлекаем метку из имени файла — digit5.png -> метка 5
            label = int(filename[0])
            my_labels.append(label)

    x_train = np.append(x_train, my_images, axis=0)
    y_train = np.append(y_train, my_labels, axis=0)

    if normalization:
        x_train = x_train.astype("float32") / 255
        x_test = x_test.astype("float32") / 255

    y_train = keras.utils.to_categorical(y_train, 10)
    y_test = keras.utils.to_categorical(y_test, 10)

    input_shape = (28, 28, 1)

    model = keras.Sequential(
        [
            keras.Input(shape=input_shape),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu", padding="same"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu", padding="same"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(10, activation="softmax"),
        ]
    )
    model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])

    model.fit(x_train, y_train, batch_size=batchSize, epochs=epochs, validation_split=valBatchSize)
    test_score = model.evaluate(x_test, y_test, verbose=0)
    train_score = model.evaluate(x_train, y_train, verbose=0)
    return model, test_score, train_score

"""
Создание финального окна
"""
def create_window_predict(model, train_score, test_score, normalize):
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
        pad = 2
        img = ImageGrab.grab(bbox=(canvas.winfo_rootx() + pad,
                                   canvas.winfo_rooty() + pad,
                                   canvas.winfo_rootx() + canvas.winfo_width() - pad,
                                   canvas.winfo_rooty() + canvas.winfo_height() - pad))
        img.save("source/pred.png")
        img = Image.open("source/pred.png").convert("L")
        img = img.resize((28, 28))
        if normalize:
            arr = np.array(img).reshape(28, 28, 1).astype("float32") / 255
        else:
            arr = np.array(img).reshape(28, 28, 1)
        arr = np.expand_dims(arr, axis=0)
        pred = model.predict(arr)
        labelTrA = Label(FWindow, text=f"Train accuracy score: {train_score[1]:.3f}", font=("Times New Roman", 14), bg='white', fg='black')
        labelTrA.grid(row=3, column=0, sticky="w", pady=2, padx=5)
        labelTrL = Label(FWindow, text=f"Train loss score: {train_score[0]:.3f}", font=("Times New Roman", 14), bg='white', fg='black')
        labelTrL.grid(row=3, column=2, sticky="e", pady=2, padx=5)
        labelTA = Label(FWindow, text=f"Test accuracy score: {test_score[1]:.3f}", font=("Times New Roman", 14), bg='white', fg='black')
        labelTA.grid(row=4, column=0, sticky="w", pady=2, padx=5)
        labelTL = Label(FWindow, text=f"Test loss score: {test_score[0]:.3f}", font=("Times New Roman", 14), bg='white', fg='black')
        labelTL.grid(row=4, column=2, sticky="e", pady=2, padx=5)
        label0 = Label(FWindow, text=f"0: {pred[0][0]:.2f}%", font=("Times New Roman", 14), bg='white', fg='black')
        label0.grid(row=5, column=0, sticky="w", pady=2, padx=5)
        label1 = Label(FWindow, text=f"1: {pred[0][1]:.2f}%", font=("Times New Roman", 14), bg='white', fg='black')
        label1.grid(row=5, column=1, pady=2, padx=5)
        label2 = Label(FWindow, text=f"2: {pred[0][2]:.2f}%", font=("Times New Roman", 14), bg='white', fg='black')
        label2.grid(row=5, column=2, sticky="e", pady=2, padx=5)
        label3 = Label(FWindow, text=f"3: {pred[0][3]:.2f}%", font=("Times New Roman", 14), bg='white', fg='black')
        label3.grid(row=6, column=0, sticky="w", pady=2, padx=5)
        label4 = Label(FWindow, text=f"4: {pred[0][4]:.2f}%", font=("Times New Roman", 14), bg='white', fg='black')
        label4.grid(row=6, column=1, pady=2, padx=5)
        label5 = Label(FWindow, text=f"5: {pred[0][5]:.2f}%", font=("Times New Roman", 14), bg='white', fg='black')
        label5.grid(row=6, column=2, sticky="e", pady=2, padx=5)
        label6 = Label(FWindow, text=f"6: {pred[0][6]:.2f}%", font=("Times New Roman", 14), bg='white', fg='black')
        label6.grid(row=7, column=0, sticky="w", pady=2, padx=5)
        label7 = Label(FWindow, text=f"7: {pred[0][7]:.2f}%", font=("Times New Roman", 14), bg='white', fg='black')
        label7.grid(row=7, column=1, pady=2, padx=5)
        label8 = Label(FWindow, text=f"8: {pred[0][8]:.2f}%", font=("Times New Roman", 14), bg='white', fg='black')
        label8.grid(row=7, column=2, sticky="e", pady=2, padx=5)
        label9 = Label(FWindow, text=f"9: {pred[0][9]:.2f}%", font=("Times New Roman", 14), bg='white', fg='black')
        label9.grid(row=8, column=1, pady=2, padx=5)

    FWindow = Tk()
    FWindow.title("Нейро-создатель MNIST")
    FWindow.geometry("500x650")
    FWindow.resizable(False, False)
    FWindow.iconbitmap(default="source/favicon.ico")
    FWindow.config(bg="white", pady=10)

    labelWrite = Label(
        text=f'Нарисуйте любую цифру от 0 до 9 в поле ниже\nleft click - рисовать              right click - стереть',
        font=("TimesNewRoman", 14), bg='white', fg='black')
    labelWrite.grid(row=0, columnspan=3, ipadx=5, pady=10)
    canvas = Canvas(FWindow, width=280, height=280, bg="black")
    canvas.grid(row=1, columnspan=3, pady=10)

    canvas.bind("<Button-1>", start_draw)
    canvas.bind("<B1-Motion>", draw)
    canvas.bind("<Button-3>", start_draw)
    canvas.bind("<B3-Motion>", erase)

    btn1 = Button(text='Предсказать', command=saveFile, background="#898989", foreground="white", font=("TimesNewRoman", 14))
    btn1.grid(row=2, columnspan=3, sticky="ew", padx=0)



    FWindow.mainloop()
