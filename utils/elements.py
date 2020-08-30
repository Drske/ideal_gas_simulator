from .logic import *
import pygame


class Atom:
    ID = None
    pos_x = None
    pos_y = None
    vel_x = None
    vel_y = None
    radius = None
    cr_grid = None

    def __init__(self, pos_x, pos_y, vel_x, vel_y, radius):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.radius = radius

    def draw(self, screen, color, res_height, size_factor):
        pixel_x = int(round(self.pos_x * size_factor, 0))
        pixel_y = res_height - self.pos_y
        pixel_y = int(round(pixel_y * size_factor, 0))

        pixel_radius = int(self.radius * size_factor)

        pygame.draw.circle(screen, color, (pixel_x, pixel_y), pixel_radius)


class Detector:
    height = None
    length = None
    time = None
    time_steps = None
    impact_count = None
    momentum = None

    def __init__(self, height, length):
        self.height = height
        self.length = length
        self.time = 0
        self.time_steps = 0
        self.impact_count = 0
        self.momentum = 0

    def Force(self):
        return self.momentum / self.time

    def Pressure(self):
        return self.Force() / self.length


class Reservoir:
    height = None
    width = None
    tolerance = None
    next_id = None
    gravity = None

    atoms = []
    grid = []

    def __init__(self, height, width, tolerance, detector):
        self.next_id = 0
        self.gravity = 1
        self.height = height
        self.width = width
        self.tolerance = tolerance
        self.detector = detector

    def add_atom(self, atom):
        self.atoms.append(atom)
        atom.ID = self.next_id
        self.next_id += 1

    def create_grid(self):
        radius = self.atoms[0].radius

        for x in range(0, int(self.width / radius) + 1):
            self.grid.append([])
            for y in range(0, int(self.height / radius) + 1):
                self.grid[x].append(set())

        for atom in self.atoms:
            x = math.floor(atom.pos_x / radius)
            y = math.floor(atom.pos_y / radius)

            self.grid[x][y].add(atom)
            atom.cr_grid = (x, y)

    def step(self, time_step):
        Energy = 0

        radius = self.atoms[0].radius

        # Adding time and time_step to detector

        self.detector.time_steps += 1
        if self.detector.time_steps > 100:
            self.detector.time += time_step

        # Firstly, check for balls in you neighboorhood

        neighboorhood = [
            (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2),
            (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
            (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
            (-2, 1), (-1, 1), (0, -1), (1, -1), (2, -1),
            (-2, 2), (-1, -2), (0, -2), (1, -2), (2, -2)]

        for atom1 in self.atoms:
            (x, y) = atom1.cr_grid

            # For every section in neigboorhood
            for (x_change, y_change) in neighboorhood:
                if x + x_change >= 0 and x + x_change <= self.width / radius and y + \
                        y_change >= 0 and y + y_change <= self.height / radius:

                    # For every atom in neighbouring section
                    for atom2 in self.grid[x + x_change][y + y_change]:
                        if atom1.ID == atom2.ID:
                            continue
                        a1a2_distance = distance(
                            atom1.pos_x, atom1.pos_y, atom2.pos_x, atom2.pos_y)

                        # Check if two atoms meet the criteria for bounce
                        if a1a2_distance <= 2 * radius + self.tolerance:
                            if distance(atom1.pos_x + atom1.vel_x * time_step, atom1.pos_y + atom1.vel_y * time_step,
                                        atom2.pos_x + atom2.vel_x * time_step, atom2.pos_y + atom2.vel_y * time_step) > a1a2_distance:
                                continue
                            else:

                                # If yes - bounce them
                                bounce(atom1, atom2)

        # Secondly, check for wall impacts

        for atom in self.atoms:
            if atom.pos_x - radius <= 0 + self.tolerance and atom.vel_x <= 0:
                atom.vel_x = -atom.vel_x
            elif atom.pos_x + radius + self.tolerance >= self.width and atom.vel_x >= 0:
                atom.vel_x = -atom.vel_x

                # If there is detector impact - notice it
                if atom.pos_y >= self.detector.height and atom.pos_y <= self.detector.height + \
                        self.detector.length and self.detector.time_steps > 100:
                    self.detector.impact_count += 1
                    self.detector.momentum += 2 * abs(atom.vel_x)

            if atom.pos_y - radius <= 0 + self.tolerance and atom.vel_y <= 0:
                atom.vel_y = -atom.vel_y
            elif atom.pos_y + radius + self.tolerance >= self.height and atom.vel_y >= 0:
                atom.vel_y = -atom.vel_y

            # Lastly, move the atoms by a given step
            atom.pos_x += atom.vel_x * time_step
            atom.pos_y += atom.vel_y * time_step

            # While counting changes in y velocity - consider
            # distance coming grom gravity
            atom.pos_y -= (self.gravity * time_step ** 2) / 2

            # And velocity change
            atom.vel_y -= self.gravity * time_step

            # And check if grid section has changed and upload it if needed
            nx = math.floor(atom.pos_x / radius)
            ny = math.floor(atom.pos_y / radius)

            if (nx, ny) != atom.cr_grid:
                (x, y) = atom.cr_grid
                self.grid[x][y].discard(atom)
                self.grid[nx][ny].add(atom)
                atom.cr_grid = (nx, ny)
