from tkinter import messagebox
import tkinter as tk
import pygame
import sys


class Box():

    def __init__(self, text, value, x, y, font):
        self.text = text
        self.value = value
        self.x = x
        self.y = y
        self.font = font

    def draw(self, screen):
        box_text = self.font.render(
            self.text + ': ' + str(self.value), 1, (0, 255, 0))
        screen.blit(box_text, (self.x, self.y))


class UserInput():

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


def start_simulation(time_step, reservoir, dec_length, dec_height):

    frame_rate = 120
    steps_in_frame = int(round(1 / (frame_rate * time_step), 0)) + 1
    size_factor = 20

    pygame.init()
    clock = pygame.time.Clock()

    screen_width = int(reservoir.width * size_factor)
    screen_height = int(reservoir.height * size_factor)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Simulation")
    font = pygame.font.SysFont("Calibri", screen_width // 10)
    tmpText = font.render("Krok Czasu", 1, (0, 0, 0))

    names = ['Time steps', 'Time', 'Pressure']
    values = [0, 0, 0]
    boxes = []

    for index in range(len(names)):
        boxes.append(Box(names[index], values[index],
                         5, index * tmpText.get_height(), font))

    x_line = int(screen_width)
    y1_line = int(screen_height - (dec_height + dec_length) * size_factor)
    y2_line = int(screen_height - dec_height * size_factor)
    color_line = (255, 0, 0)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        pygame.draw.line(screen, color_line, (x_line, y1_line),
                         (x_line, y2_line), 10)

        for i in range(steps_in_frame):
            reservoir.step(time_step)

        for atom in reservoir.atoms:
            atom.draw(screen, (255, 255, 255), reservoir.height, size_factor)

        for index_box in range(len(boxes)):
            if index_box == 0:
                boxes[index_box].value = reservoir.detector.time_steps
            if index_box == 1:
                boxes[index_box].value = reservoir.detector.time
            if index_box == 2:
                boxes[index_box].value = reservoir.detector.Pressure()
            boxes[index_box].draw(screen)

        pygame.display.flip()
        clock.tick(frame_rate)
