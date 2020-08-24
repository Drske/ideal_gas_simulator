from utils import logic, gui
from tkinter import TclError
import random
import sys

# Input data
Test = gui.UserInput()
try:
    radius = float(Test.labels[0].get())
    eta_height = float(Test.labels[1].get())
    eta_width = float(Test.labels[2].get())
    N = float(Test.labels[3].get())
    dec_height = float(Test.labels[4].get())
    dec_length = float(Test.labels[5].get())
    max_v = float(Test.labels[6].get())
except TclError:
    sys.exit()

# Calculating data
H = eta_height * radius
L = eta_width * radius
kappa = min(eta_width, eta_height)

time_step = 1 / (kappa * max_v)

if time_step > 0.01:
    time_step = 0.01

tolerance = 0.001 * radius

# Adding atoms to reservoir
dec_length = dec_length * radius
detector = logic.Detector(dec_height, dec_length)
reservoir = logic.Reservoir(H, L, tolerance, detector)

coords = logic.starting_coords(N, radius, L, H)

atoms_counter = 0

while atoms_counter < N:
    (x, y) = random.sample(coords, 1)[0]

    vx = random.randint(-max_v, max_v)
    vy = random.randint(-max_v, max_v)

    atom = logic.Atom(x, y, vx, vy, radius)
    reservoir.add_atom(atom)

    coords.discard((x, y))

    atoms_counter += 1

reservoir.create_grid()

# Pygame simulation

gui.start_simulation(time_step, reservoir, dec_length, dec_height)
