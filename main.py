import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_RADIUS, PLAYER_MAX_LIVES
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event
from shot import Shot
import sys
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt: float = 0.0
    
    # groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, drawable, updatable)

    # objects
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidField = AsteroidField()

    asteroids_shot = 0

    while True:
        #log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        if pygame.font:
            font = pygame.font.Font(None, 64)
            text = font.render(f"Lives {player.lives} | {asteroids_shot} Score", True, (255, 255, 255))
            textpos = text.get_rect(centerx=SCREEN_WIDTH / 2, y=50)
            screen.blit(text, textpos)

        for obj in drawable:
            obj.draw(screen, "white")
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                #log_event("player_hit")
                player.lives -= 1
                if player.lives == 0:
                    print("Game over!")
                    sys.exit()
                player.reset()
                
            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroids_shot += 1
                    #log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()

        if player.accel.length() > 0:
            player.accel.normalize()
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
