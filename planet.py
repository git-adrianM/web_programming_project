import numpy as np
import pygame

class Planet:
    KM_TO_MILES = 0.621371  # Conversion factor from kilometers to miles
    AU_IN_KM = 149.6e6 * 1000  # Astronomical Unit (AU) in kilometers
    AU = AU_IN_KM * KM_TO_MILES  # Astronomical Unit (AU) in miles
    G = 6.67428e-11  # Gravitational constant
    SCALE = 250 / AU  # Scaling for the program
    TIMESTEP = 3600 * 24 * 0.5  # Time step for the simulation in seconds
    MAX_ORBIT_LENGTH = 100  # Maximum number of positions to store in the orbit
    DISTANCE_UPDATE_INTERVAL = 100  # Update distance every 100 frames

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
        self.frame_counter = 0

        # Create an empty surface with transparency for the orbit
        self.orbit_surface = pygame.Surface((1200, 800), pygame.SRCALPHA)
        self.distance_text_surface = None  # Surface for distance text

    def draw(self, win, width, height, font, white):
        x, y = (self.pos * self.SCALE + np.array([width / 2, height / 2])).astype(int)

        # Draw the orbit
        if len(self.orbit) > 2:
            for i in range(1, len(self.orbit)):
                start_point = (self.orbit[i - 1][0] * self.SCALE + width / 2,
                               self.orbit[i - 1][1] * self.SCALE + height / 2)
                end_point = (self.orbit[i][0] * self.SCALE + width / 2,
                             self.orbit[i][1] * self.SCALE + height / 2)

                fade_multiplier = 15  # Increase this for faster fading
                fade_value = int(255 * (i / len(self.orbit)) ** fade_multiplier)
                faded_color = (self.color[0], self.color[1], self.color[2], fade_value)
                pygame.draw.line(self.orbit_surface, faded_color, start_point, end_point, 2)

            win.blit(self.orbit_surface, (0, 0))

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            if self.distance_text_surface is None:  # Create the distance text surface if it doesn't exist
                self.distance_text_surface = font.render(f"{self.distance_to_sun:e} miles", 1, white)
            win.blit(self.distance_text_surface, (x + self.radius + 5, y - self.distance_text_surface.get_height() / 2))

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

        # Update the orbit and limit its length
        self.orbit.append(tuple(self.pos))
        if len(self.orbit) > self.MAX_ORBIT_LENGTH:
            self.orbit.pop(0)  # Remove the oldest position if orbit exceeds maximum length

        # Update distance to sun at specified intervals
        self.frame_counter += 1
        if self.frame_counter >= self.DISTANCE_UPDATE_INTERVAL:
            self.frame_counter = 0
            if not self.sun:
                self.distance_to_sun = np.linalg.norm(self.pos - planets[0].pos) * self.SCALE / self.KM_TO_MILES
