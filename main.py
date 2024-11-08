import pygame, asyncio
from scripts.game import Game

# initialize
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# frame rate and delta time
CLOCK = pygame.time.Clock()
FPS = 144 
delta_time_setting = 60

game = Game(screen)

async def main():

    # run window
    running = True

    while running:

        # delta time
        delta_time = CLOCK.tick(FPS) / 1000.0
        delta_time *= delta_time_setting
        if delta_time > 3.4:
            delta_time = 3.4

        # event
        for event in pygame.event.get():
            game.event_controls(event)
            if event.type == pygame.QUIT:
                running = False

        # clear screen
        screen.fill((30, 30, 30))
        
        # update game
        game.update(delta_time)

        # update screen
        pygame.display.flip()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())