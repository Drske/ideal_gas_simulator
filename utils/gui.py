from .interface import box, uinput
import pygame
import sys


def init_input():
    return uinput.UserInput()


def start_simulation(time_step, reservoir):
    dec_length = reservoir.detector.length
    dec_height = reservoir.detector.height

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
        boxes.append(box.Box(names[index], values[index],
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
                if reservoir.detector.time_steps <= 100:
                    boxes[index_box].value = 0
                else:
                    boxes[index_box].value = reservoir.detector.Pressure()
            boxes[index_box].draw(screen)

        pygame.display.flip()
        clock.tick(frame_rate)
