import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
import time
import random

window = tk.Tk()
window.title("Perceptron")

select_button = object
train_button = object
set_button = object
reset_button = object
file_label = object
learning_rate_label = object
epochs_label = object
learn_rate_entry = object
epochs_entry = object
canvas = object
output_text = object
result_line = object

filename = ""
dataset = list()
dataclass = list()
learning_rate = 0.1
epochs = 100
max_accuracy = 1
canvas_width = 500
canvas_height = 500
large_ratio = 100
point_radius = 0.02
border = 50
center_dx, center_dy = 0, 0

class Perceptron():
    def __init__(self, dimension, learning_rate):
        self.learning_rate = learning_rate
        self.w = [random.uniform(-1, 1) for i in range(dimension + 1)]

    def activation(self, x):
        return 1 if x > 0 else -1

    def predict(self, train_data):
        y = 0
        for i in range(len(self.w)):
            if i < len(self.w) - 1:
                y += self.w[i] * train_data[i]
            else:
                y += self.w[i] * -1
        return self.activation(y)

    def train(self, dataset, epochs):
        total_time = 0
        random.shuffle(dataset)
        train_dataset = dataset[:len(dataset) * 2 // 3]
        test_dataset = dataset[len(dataset) * 2 // 3:]

        for n in range(epochs):
            start_time = time.time()
            correct = 0
            for train_data in train_dataset:
                y = self.predict(train_data)
                if train_data[-1] == dataclass[0] and y != 1:
                    for i in range(len(self.w)):
                        if i < len(self.w) - 1:
                            self.w[i] += self.learning_rate * train_data[i]
                        else:
                            self.w[i] += self.learning_rate * -1
                elif train_data[-1] == dataclass[1] and y != -1:
                    for i in range(len(self.w)):
                        if i < len(self.w) - 1:
                            self.w[i] -= self.learning_rate * train_data[i]
                        else:
                            self.w[i] -= self.learning_rate * -1

            for train_data in train_dataset:
                y = self.predict(train_data)
                if (train_data[-1] == dataclass[0] and y == 1) or (train_data[-1] == dataclass[1] and y == -1):
                    correct += 1
            train_accuracy = correct / len(train_dataset)
            correct = 0

            for test_data in test_dataset:
                y = self.predict(test_data)
                if (test_data[-1] == dataclass[0] and y == 1) or (test_data[-1] == dataclass[1] and y == -1):
                    correct += 1
            test_accuracy = correct / len(test_dataset)
            output_text.insert(tk.END, "Epoch {}: train acc = {:.6f}: test acc = {:.6f} ({:.6f} sec/epoch)\n".format(n + 1, train_accuracy, test_accuracy, time.time() - start_time))
            total_time += time.time() - start_time
            if not max_accuracy == 0 and train_accuracy >= max_accuracy:
                break
        drawLine(self.w)
        output_text.insert(tk.END, "\nw = {}\n\nTotal time: {:.6f} sec".format(self.w, total_time))
        output_text.see(tk.END)

def training():
    global dataset, learning_rate, epochs
    output_text.config(state="normal")
    output_text.delete(1.0, "end")
    perceptron = Perceptron(len(dataset[0][:-1]), learning_rate)
    perceptron.train(dataset, epochs)
    output_text.config(state="disabled")

def scaledX(x):
    return x * large_ratio + canvas_width // 2

def scaledY(y):
    return -y * large_ratio + canvas_height // 2

def adjustRatio(min_x, max_x, min_y, max_y):
    global large_ratio, point_radius, center_dx, center_dy
    large_ratio = 100
    point_radius = 1 / large_ratio * 2
    center_dx, center_dy = (max_x + min_x) / 2, (max_y + min_y) / 2
    while large_ratio > 1 and (abs(scaledX(max_x - center_dx)) >= canvas_width - border or abs(scaledX(min_x - center_dx)) >= canvas_width - border or abs(scaledY(max_y - center_dy)) >= canvas_height - border or abs(scaledY(min_y - center_dy)) >= canvas_height - border):
        large_ratio = large_ratio - 1
        point_radius = 1 / large_ratio * 2

def drawLine(w):
    global result_line
    if w[1] != 0:
        x1 = -100
        y1 = (w[2] - (w[0] * x1)) / w[1]
        x2 = 100
        y2 = (w[2] - (w[0] * x2)) / w[1]

    canvas.delete(result_line)
    result_line = canvas.create_line(scaledX(x1 - center_dx), scaledY(y1 - center_dy),
                        scaledX(x2 - center_dx),scaledY(y2 - center_dy), fill='red')
    canvas.update_idletasks()

def drawPoint(x, y, types):
    colors = ['blue', 'orange', 'green', 'red', 'pink', 'brown', 'purple']
    canvas.create_oval(scaledX(x - center_dx - point_radius), scaledY(y - center_dy + point_radius),
                       scaledX(x - center_dx + point_radius), scaledY(y - center_dy - point_radius),
                       fill=colors[types])
    canvas.update_idletasks()

def readFile(file):
    global dataset, dataclass
    min_x, max_x, min_y, max_y = 999, -999, 999, -999

    f = open(file, "r")
    for i in f.readlines():
        line = list(map(float, i.split()))
        dataset.append(line)

    if len(dataset[0][:-1]) < 3:
        for (x, y, types) in dataset:
            min_x, max_x, min_y, max_y = min(min_x, x), max(max_x, x), min(min_y, y), max(max_y, y)
            if types not in dataclass:
                dataclass.append(types)
        adjustRatio(min_x, max_x, min_y, max_y)
        for (x, y, types) in dataset:
            drawPoint(x, y, dataclass.index(types))
    else:
        tk.messagebox.showinfo(title="Notice", message="Sorry, only output 2D data")

    f.close()

def selectDataset():
    global filename
    resetState()
    file = filedialog.askopenfilename(title="Select file", filetypes=(("text files (*.txt)", "*.txt"), ("all files", "*.*")))
    if file:
        readFile(file)
        filename = file.split("/")[-1]
        file_label.config(text="{}".format(filename))
        train_button.config(state="normal")
        set_button.config(state="normal")
        reset_button.config(state="normal")
        learn_rate_entry.config(state="normal")
        epochs_entry.config(state="normal")
    else:
        tk.messagebox.showinfo(title="Notice", message="No file selected")

def setParameter():
    global learning_rate, epochs

    if learn_rate_entry.get() or epochs_entry.get():
        pass
    else:
        tk.messagebox.showinfo(title="Notice", message="Please input parameters")
        return

    if learn_rate_entry.get():
        learning_rate = float(learn_rate_entry.get())
        if learning_rate > 0:
            learning_rate_label.config(text="learning rate = {}".format(learning_rate))
            learn_rate_entry.delete(0, "end")
        else:
            tk.messagebox.showinfo(title="Notice", message="Please input value > 0")

    if epochs_entry.get():
        epochs = int(epochs_entry.get())
        if epochs > 0:
            epochs_label.config(text="epochs = {}".format(epochs))
            epochs_entry.delete(0, "end")
        else:
            tk.messagebox.showinfo(title="Notice", message="Please input value > 0")

def resetState():
    global dataset, learning_rate, epochs, large_ratio, point_radius, dataclass
    dataset = list()
    dataclass = list()
    learning_rate = 0.1
    epochs = 100
    large_ratio = 100
    point_radius = 0.02
    learning_rate_label.config(text="learning rate = {}".format(learning_rate))
    epochs_label.config(text="epochs = {}".format(epochs))
    train_button.config(state="disabled")
    set_button.config(state="disabled")
    reset_button.config(state="disabled")
    file_label.config(text="{}".format(""))
    learn_rate_entry.delete(0, "end")
    learn_rate_entry.config(state="disabled")
    epochs_entry.delete(0, "end")
    epochs_entry.config(state="disabled")
    canvas.delete("all")
    output_text.config(state="normal")
    if output_text.get(1.0, tk.END):
        output_text.delete(1.0, "end")
    output_text.config(state="disabled")

def GUI():
    global select_button, train_button, set_button, reset_button, canvas, output_text
    global file_label, learning_rate_label, epochs_label, learn_rate_entry, epochs_entry

    select_button = tk.Button(window, text="select dataset", command=selectDataset, width=15)
    select_button.grid(row=0, column=0)
    train_button = tk.Button(window, text="start training", command=training, state="disabled", width=15)
    train_button.grid(row=1, column=0)
    set_button = tk.Button(window, text="set parameter", command=setParameter, state="disabled", width=15)
    set_button.grid(row=2, column=0)
    reset_button = tk.Button(window, text="clear all", command=resetState, state="disabled", width=15)
    reset_button.grid(row=5, column=0)

    file_label = tk.Label(window, text="{}".format(filename), width=20)
    file_label.grid(row=0, column=1)
    learning_rate_label = tk.Label(window, text="learning rate = {}".format(learning_rate), width=15)
    learning_rate_label.grid(row=3, column=0)
    epochs_label = tk.Label(window, text="epochs = {}".format(epochs), width=15)
    epochs_label.grid(row=4, column=0)

    learn_rate_entry = tk.Entry(window, state="disabled", width=15)
    learn_rate_entry.grid(row=3, column=1)
    epochs_entry = tk.Entry(window, state="disabled", width=15)
    epochs_entry.grid(row=4, column=1)

    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='white')
    canvas.grid(row=0, column=3, rowspan=6)

    output_text = scrolledtext.ScrolledText(window, state="disabled", height=38)
    output_text.grid(row=0, column=4, rowspan=6)

    tk.mainloop()

if __name__ == "__main__":
    GUI()