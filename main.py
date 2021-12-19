import pygame


if __name__ == "__main__":
    x = 1920
    y = 1080
    pygame.init()
    size = width, height = x, y
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        pygame.display.flip()
