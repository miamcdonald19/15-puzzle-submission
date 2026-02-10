import pygame
from puzzle import Puzzle

pygame.init()

WIDTH, HEIGHT = 420, 520
TILE_SIZE = 100
PADDING = 10
TOP = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("15 Puzzle")

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 24)

puzzle = Puzzle()
puzzle.scramble()

def draw():
    screen.fill((245, 245, 245))

    title = font.render("15 Puzzle", True, (0, 0, 0))
    moves = small_font.render(f"Moves: {puzzle.moves}", True, (0, 0, 0))
    screen.blit(title, (PADDING, 10))
    screen.blit(moves, (PADDING, 50))

    for i, value in enumerate(puzzle.board):
        row, col = divmod(i, 4)
        x = PADDING + col * (TILE_SIZE + PADDING)
        y = TOP + PADDING + row * (TILE_SIZE + PADDING)
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

        if value == 0:
            pygame.draw.rect(screen, (220, 220, 220), rect)
        else:
            pygame.draw.rect(screen, (200, 200, 200), rect)
            text = font.render(str(value), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))

    if puzzle.is_solved():
        win = font.render("Solved!", True, (0, 150, 0))
        screen.blit(win, (WIDTH // 2 - 70, HEIGHT - 40))

    pygame.display.flip()

def handle_click(pos):
    x, y = pos
    if y < TOP:
        return

    col = (x - PADDING) // (TILE_SIZE + PADDING)
    row = (y - TOP - PADDING) // (TILE_SIZE + PADDING)

    if 0 <= row < 4 and 0 <= col < 4:
        idx = row * 4 + col
        puzzle.move(idx)

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                puzzle.scramble()

    draw()

pygame.quit()
