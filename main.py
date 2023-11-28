import asyncio
from planet import *

pygame.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Celestial Dance: Time's Relative Nature")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("TimesNewRoman", 16)

clock = pygame.time.Clock()

sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30, "Sun")
sun.sun = True
earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10 ** 24, "Earth")
moon_distance_from_earth = 384.4e3 * Planet.KM_TO_MILES / Planet.SCALE
moon = Planet(earth.pos[0] - moon_distance_from_earth, 0, 4, (128, 128, 128), 7.342 * 10 ** 22, "Moon")
mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10 ** 23, "Mars")
mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10 ** 23, "Mercury")
venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10 ** 24, "Venus")

# Initialize last year for text surface caching
for planet in [earth, moon, mars, mercury, venus]:
    planet.last_year = 0

# Assigning initial velocities to the planets
earth.vel[1] = 29.783 * 1000
mars.vel[1] = 24.077 * 1000
mercury.vel[1] = -47.4 * 1000
venus.vel[1] = -35.02 * 1000
moon.vel[1] = earth.vel[1] + 1.022 * 1000

planets = [sun, mercury, venus, earth, moon, mars]

elapsed_time_seconds = 0

def draw_key(win, planets):
    start_x = WIDTH - 200
    start_y = HEIGHT - (20 * len(planets))
    padding = 20

    for planet in planets:
        pygame.draw.circle(win, planet.color, (start_x, start_y), 10)
        name_text = FONT.render(planet.name, 1, WHITE)
        win.blit(name_text, (start_x + 15, start_y - 5))
        start_y += padding

def draw_year_counter(win, elapsed_time_seconds, planets, font, white):
    years_elapsed = {
        "Earth": elapsed_time_seconds / (365.25 * 24 * 3600),
        "Mercury": elapsed_time_seconds / (88 * 24 * 3600),
        "Venus": elapsed_time_seconds / (224.7 * 24 * 3600),
        "Mars": elapsed_time_seconds / (687 * 24 * 3600)
    }
    planet_order = ["Mars", "Earth", "Venus", "Mercury"]

    start_y = HEIGHT - 10 - font.get_height()
    padding = 20

    for planet_name in planet_order:
        planet = next((p for p in planets if p.name == planet_name), None)
        if planet:
            # Update text surface only if necessary
            if 'text_surface' not in planet.__dict__ or int(years_elapsed[planet.name]) != int(planet.last_year):
                planet.text_surface = font.render(f"Years on {planet.name}: {years_elapsed[planet.name]:.2f}", 1, white)
                planet.last_year = years_elapsed[planet.name]
            win.blit(planet.text_surface, (10, start_y))
            start_y -= padding

async def main():
    global elapsed_time_seconds

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Exit the program

        clock.tick(30)  # Reduced frame rate for optimization
        elapsed_time_seconds += Planet.TIMESTEP
        WIN.fill((0, 0, 0))

        draw_year_counter(WIN, elapsed_time_seconds, planets, FONT, WHITE)
        draw_key(WIN, planets)

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN, WIDTH, HEIGHT, FONT, WHITE)

        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())
