from utils import logic, elements
import random


def simulate(time_step, reservoir):

    while True:
        reservoir.step(time_step)
        if reservoir.detector.time_steps > 5000:
            return reservoir.detector.Pressure()


def next_simulation(N, radius, H, L, dec_height,
                    dec_length, time_step, max_v, tolerance):
    # Adding atoms to reservoir
    dec_length = dec_length * radius
    detector = elements.Detector(dec_height, dec_length)
    reservoir = elements.Reservoir(H, L, tolerance, detector)

    reservoir.atoms.clear()
    reservoir.grid.clear()

    coords = logic.starting_coords(N, radius, L, H)

    atoms_counter = 0

    while atoms_counter < N:
        (x, y) = random.sample(coords, 1)[0]

        vx = random.randint(-max_v, max_v)
        vy = random.randint(-max_v, max_v)

        atom = elements.Atom(x, y, vx, vy, radius)
        reservoir.add_atom(atom)

        coords.discard((x, y))

        atoms_counter += 1

    reservoir.create_grid()

    count_atoms = 0

    for atom in reservoir.atoms:
        count_atoms += 1

    # Pygame simulation

    return simulate(time_step, reservoir)


radius = 0.5
eta_height = 100
eta_width = 20
dec_length = 20
max_v = float(input("Maximum velocity: "))

H = eta_height * radius
L = eta_width * radius
kappa = min(eta_width, eta_height)

time_step = 1 / (kappa * max_v)

if time_step > 0.01:
    time_step = 0.01

tolerance = 0.001 * radius

variable = input("What is your variable? Choose N/h ")

if variable == "N":
    dec_height = int(input("detector's height: "))
    print("")
    for N in range(10, int(0.25 * eta_height * eta_width) + 1, 10):
        av_pressure = next_simulation(
            N, radius, H, L, dec_height, dec_length, time_step, max_v, tolerance)
        print(N, av_pressure)
if variable == "h":
    N = int(input("N: "))
    print("")
    h = 0
    while h <= 40:
        av_pressure = next_simulation(
            N, radius, H, L, h, dec_length, time_step, max_v, tolerance)
        print(h, av_pressure)
        h += 1
