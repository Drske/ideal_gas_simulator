from tkinter import messagebox
import tkinter as tk


class UserInput:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Input")
        self.names = ['R ', 'ηH ', 'ηL ', 'N ', 'h ', '𝜆 ', 'v ']
        self.labels = []
        for index in range(len(self.names)):
            self.labels.append(
                tk.Label(self.window, text=self.names[index]).grid(row=index))
        for label_index in range(len(self.labels)):
            self.labels[label_index] = tk.Entry(self.window)
            self.labels[label_index].grid(row=label_index, column=1)
        self.button = tk.Button(self.window, text='Confirm', command=self.check_entry_fields).grid(
            row=len(self.names) + 1, column=1, sticky=tk.W, pady=4)
        self.window.mainloop()

    def check_values(self):
        flag = 1
        for label_index in range(len(self.labels)):
            if label_index == 1:
                if 200 < float(self.labels[label_index].get()) or float(
                        self.labels[label_index].get()) < 20:
                    flag = 0
                    messagebox.showinfo(
                        "Błędna wartość w polu " + self.names[label_index], "Podaj wartość z zakresu [20,200]")
            if label_index == 2:
                if float(self.labels[label_index - 1].get()) / \
                        float(self.labels[label_index].get()) < 5:
                    messagebox.showinfo(
                        "Błędna wartość w polu " + self.names[label_index], "Współczynnik ηH/ηL musi być większy od 5!")
                    flag = 0
            if label_index == 3:
                if 0.25 * float(self.labels[label_index - 1].get()) * float(self.labels[label_index - 2].get(
                )) < float(self.labels[label_index].get()) or float(self.labels[label_index].get()) < 1:
                    messagebox.showinfo(
                        "Błędna wartość w polu " + self.names[label_index], "Podaj wartość z zakresu [1, (0.25*ηH*ηL)]")
                    flag = 0
            if label_index == 4:
                if float(self.labels[label_index].get()) > float(
                        self.labels[label_index - 3].get()) * float(self.labels[label_index - 4].get()):
                    messagebox.showinfo(
                        "Błędna wartość w polu " + self.names[label_index], "Wysokość na której znajduje się detektor nie może przekroczyć wysokości zbiornika. Podaj wartość mniejszą niż (ηH * R).")
                    flag = 0
            if label_index == 5:
                if float(self.labels[label_index].get()) * float(self.labels[label_index - 5].get()) + float(
                        self.labels[label_index - 1].get()) > float(self.labels[label_index - 4].get()):
                    messagebox.showinfo(
                        "Błędna wartość w polu " + self.names[label_index], "Wysokość i długość detektora nie może przekroczyć wysokości zbiornika. Podaj wartość mniejszą niż (ηH-h).")
                    flag = 0
        return flag

    def check_entry_fields(self):
        flag = True
        for label_index in range(len(self.labels)):
            try:
                float(self.labels[label_index].get())
            except ValueError:
                self.labels[label_index].delete(0, tk.END)
                flag = False
        if flag:
            if self.check_values() != 0:
                self.window.quit()
            else:
                for label_index in range(len(self.labels)):
                    self.labels[label_index].delete(0, tk.END)
                self.check_entry_fields
