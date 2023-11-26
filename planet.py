import pygame
import numpy as np


class Planet:
    KM_TO_MILES = 0.621371  # Conversion factor from kilometers to miles
    AU_IN_KM = 149.6e6 * 1000  # Astronomical Unit (AU) in kilometers
    AU = AU_IN_KM * KM_TO_MILES  # Astronomical Unit (AU) in miles
    G = 6.67428e-11  # gravitational constant
    SCALE = 250 / AU  # scaling for the program
    TIMESTEP = 3600 * 24 * 0.5 # time step for the simulation in seconds

    def __init__(self, x, y, radius, color, mass, name=None):
        self.pos = np.array([x, y], dtype=float)
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.vel = np.array([0.0, 0.0])
        self.name = name

        # Create an empty surface with transparency for the orbit
        self.orbit_surface = pygame.Surface((1200, 800), pygame.SRCALPHA)

    def draw(self, win, width, height, font, white):
        x, y = (self.pos * self.SCALE + np.array([width / 2, height / 2])).astype(int)

        # Draw the orbit
        if len(self.orbit) > 2:
            for i in range(1, len(self.orbit)):
                start_point = (
                    self.orbit[i - 1][0] * self.SCALE + width / 2, self.orbit[i - 1][1] * self.SCALE + height / 2)
                end_point = (self.orbit[i][0] * self.SCALE + width / 2, self.orbit[i][1] * self.SCALE + height / 2)

                fade_multiplier = 15  # Increase this for faster fading
                fade_value = int(255 * (i / len(self.orbit)) ** fade_multiplier)
                faded_color = (self.color[0], self.color[1], self.color[2], fade_value)
                pygame.draw.line(self.orbit_surface, faded_color, start_point, end_point, 2)

            win.blit(self.orbit_surface, (0, 0))

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = font.render(f"{round(self.distance_to_sun, 1):,} miles", 1, white)
            win.blit(distance_text, (x + self.radius + 5, y - distance_text.get_height() / 2))

    def attraction(self, other):
        distance_vec = other.pos - self.pos
        distance = np.linalg.norm(distance_vec)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        force_vec = force * distance_vec / distance
        return force_vec

    def update_position(self, planets):
        total_force = np.array([0.0, 0.0])
        for planet in planets:
            if self == planet:
                continue
            total_force += self.attraction(planet)

        acc = total_force / self.mass
        self.vel += acc * self.TIMESTEP
        self.pos += self.vel * self.TIMESTEP
        self.orbit.append(tuple(self.pos))
