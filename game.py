import time
import pygame
from puzzle import Puzzle

pygame.init()

WINDOW_WIDTH = 620
WINDOW_HEIGHT = 760
FPS = 60

BG_COLOR = (245, 245, 245)
TEXT_COLOR = (25, 25, 25)
TILE_COLOR = (200, 200, 200)
BLANK_COLOR = (225, 225, 225)
BORDER_COLOR = (150, 150, 150)
BUTTON_COLOR = (215, 215, 215)
BUTTON_ACTIVE = (180, 220, 180)
BUTTON_TEXT = (20, 20, 20)
SOLVED_COLOR = (0, 140, 0)

TOP_MARGIN = 170
BOTTOM_MARGIN = 60
SIDE_MARGIN = 40
GRID_GAP = 8

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("15 Puzzle / 8 Puzzle")

title_font = pygame.font.SysFont(None, 52)
header_font = pygame.font.SysFont(None, 30)
text_font = pygame.font.SysFont(None, 28)
tile_font = pygame.font.SysFont(None, 54)
small_font = pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()


class Button:
    def __init__(self, rect, text, action):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action

    def draw(self, surface, active=False):
        color = BUTTON_ACTIVE if active else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BORDER_COLOR, self.rect, 2, border_radius=10)

        text_surf = small_font.render(self.text, True, BUTTON_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def contains(self, pos):
        return self.rect.collidepoint(pos)


puzzle = Puzzle(size=4, allow_diagonal=False)
puzzle.scramble()

start_time = time.time()
elapsed_when_stopped = 0
timer_running = True


def start_timer():
    global start_time, elapsed_when_stopped, timer_running
    start_time = time.time()
    elapsed_when_stopped = 0
    timer_running = True


def stop_timer():
    global elapsed_when_stopped, timer_running
    if timer_running:
        elapsed_when_stopped = time.time() - start_time
        timer_running = False


def current_elapsed():
    if timer_running:
        return time.time() - start_time
    return elapsed_when_stopped


def format_time(seconds):
    total = int(seconds)
    minutes = total // 60
    secs = total % 60
    return f"{minutes:02d}:{secs:02d}"


def make_new_puzzle(size=None, allow_diagonal=None):
    global puzzle
    global start_time, elapsed_when_stopped, timer_running

    if size is None:
        size = puzzle.size
    if allow_diagonal is None:
        allow_diagonal = puzzle.allow_diagonal

    puzzle = Puzzle(size=size, allow_diagonal=allow_diagonal)
    puzzle.scramble()
    start_timer()


def grid_measurements():
    grid_size_px = min(
        WINDOW_WIDTH - 2 * SIDE_MARGIN,
        WINDOW_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    )

    tile_size = (grid_size_px - (puzzle.size - 1) * GRID_GAP) // puzzle.size
    board_width = tile_size * puzzle.size + GRID_GAP * (puzzle.size - 1)

    start_x = (WINDOW_WIDTH - board_width) // 2
    start_y = TOP_MARGIN

    return tile_size, start_x, start_y


def tile_rect(index):
    tile_size, start_x, start_y = grid_measurements()
    row, col = divmod(index, puzzle.size)
    x = start_x + col * (tile_size + GRID_GAP)
    y = start_y + row * (tile_size + GRID_GAP)
    return pygame.Rect(x, y, tile_size, tile_size)


def build_buttons():
    return [
        Button((40, 85, 100, 40), "3x3 Mode", "mode_3"),
        Button((150, 85, 100, 40), "4x4 Mode", "mode_4"),
        Button((260, 85, 140, 40), "Diagonal", "toggle_diagonal"),
        Button((410, 85, 160, 40), "Scramble / Reset", "scramble"),
    ]


buttons = build_buttons()


def draw():
    screen.fill(BG_COLOR)

    title = title_font.render("Sliding Puzzle", True, TEXT_COLOR)
    screen.blit(title, (40, 20))

    mode_text = f"Mode: {puzzle.size}x{puzzle.size}"
    diag_text = f"Diagonal: {'ON' if puzzle.allow_diagonal else 'OFF'}"
    moves_text = f"Moves: {puzzle.moves}"
    time_text = f"Time: {format_time(current_elapsed())}"

    screen.blit(header_font.render(mode_text, True, TEXT_COLOR), (40, 135))
    screen.blit(header_font.render(diag_text, True, TEXT_COLOR), (200, 135))
    screen.blit(header_font.render(moves_text, True, TEXT_COLOR), (380, 135))
    screen.blit(header_font.render(time_text, True, TEXT_COLOR), (500, 135))

    for button in buttons:
        active = False
        if button.action == "mode_3" and puzzle.size == 3:
            active = True
        elif button.action == "mode_4" and puzzle.size == 4:
            active = True
        elif button.action == "toggle_diagonal" and puzzle.allow_diagonal:
            active = True
        button.draw(screen, active=active)

    for i, value in enumerate(puzzle.board):
        rect = tile_rect(i)

        if value == 0:
            pygame.draw.rect(screen, BLANK_COLOR, rect, border_radius=14)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 2, border_radius=14)
        else:
            pygame.draw.rect(screen, TILE_COLOR, rect, border_radius=14)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 2, border_radius=14)

            text = tile_font.render(str(value), True, TEXT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    instructions = small_font.render(
        "Click a tile next to the blank. Press R to reshuffle.", True, TEXT_COLOR
    )
    screen.blit(instructions, (40, WINDOW_HEIGHT - 55))

    if puzzle.is_solved():
        solved_text = header_font.render("Solved!", True, SOLVED_COLOR)
        solved_rect = solved_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 25))
        screen.blit(solved_text, solved_rect)

    pygame.display.flip()


def handle_button_click(pos):
    for button in buttons:
        if button.contains(pos):
            if button.action == "mode_3":
                make_new_puzzle(size=3, allow_diagonal=puzzle.allow_diagonal)
            elif button.action == "mode_4":
                make_new_puzzle(size=4, allow_diagonal=puzzle.allow_diagonal)
            elif button.action == "toggle_diagonal":
                make_new_puzzle(size=puzzle.size, allow_diagonal=not puzzle.allow_diagonal)
            elif button.action == "scramble":
                make_new_puzzle(size=puzzle.size, allow_diagonal=puzzle.allow_diagonal)
            return True
    return False


def handle_board_click(pos):
    for i in range(len(puzzle.board)):
        if tile_rect(i).collidepoint(pos):
            moved = puzzle.move(i)
            if moved and puzzle.is_solved():
                stop_timer()
            return


running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not handle_button_click(event.pos):
                handle_board_click(event.pos)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                make_new_puzzle(size=puzzle.size, allow_diagonal=puzzle.allow_diagonal)
            elif event.key == pygame.K_3:
                make_new_puzzle(size=3, allow_diagonal=puzzle.allow_diagonal)
            elif event.key == pygame.K_4:
                make_new_puzzle(size=4, allow_diagonal=puzzle.allow_diagonal)
            elif event.key == pygame.K_d:
                make_new_puzzle(size=puzzle.size, allow_diagonal=not puzzle.allow_diagonal)

    draw()

pygame.quit()