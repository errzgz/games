import pygame
import random
import sys
import time

# Game configuration

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GRAY_LIGHT = (50, 50, 50)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)

SHAPES = [
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
]

SHAPES_COLOR = [RED, GREEN, WHITE, YELLOW, MAGENTA, CYAN, ORANGE]


WIDTH, HEIGHT = 10, 30
EXTRA_WIDTH = 200
BACKGROUND_COLOR = BLACK
NEXT_PIECE_COLOR = BLUE
GAME_OVER_COLOR = RED
PRESS_ANY_KEY_COLOR = WHITE
GRID_COLOR = GRAY_LIGHT
SCORE_COLOR = BLUE
SCORE_VALUE_COLOR = WHITE
LINES_COLOR = BLUE
LINES_VALUE_COLOR = WHITE
PIECE_COLOR = WHITE
RECORD_COLOR = BLUE
RECORD_VALUE_COLOR = RED
CELL_SIZE = 20
POINTS_PER_PIECE = 10
FPS = 60
SENSIBILIDAD_KEYBOARD = 100
SPEED_LEVEL = 10

X1, Y1 = 1, 1000
X2, Y2 = 100, 100
timeLap = 1000

# Texts
CAPTION = "Tetris. ChatGpt & ERRZGZ"
NEXT_PIECE = "Next Piece:"
SCORE = "Score:"
LINES = "Lines:"
RECORD = "Record:"
GAME_OVER = "Game Over"
PRESS_ANY_KEY = "Press any key to start"


# Classes
class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def move(self, dx, dy):
        if self.can_move(dx, dy):
            self.x += dx
            self.y += dy

    def can_move(self, dx, dy):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = self.x + j + dx
                    new_y = self.y + i + dy

                    if new_x < 0 or new_x >= WIDTH or new_y >= HEIGHT:
                        return False
                    if new_y >= 0 and board[new_y][new_x]:
                        return False

        return True

    def draw(self, screen):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        self.color,
                        (
                            EXTRA_WIDTH + self.x * CELL_SIZE + j * CELL_SIZE,
                            self.y * CELL_SIZE + i * CELL_SIZE,
                            CELL_SIZE,
                            CELL_SIZE,
                        ),
                    )


# Functions
def draw_grid():
    for i in range(WIDTH):
        for j in range(HEIGHT):
            pygame.draw.rect(
                screen,
                GRID_COLOR,
                (EXTRA_WIDTH + i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1,
            )


def restart_game():
    global current_piece, next_piece, board, score  # , FPS
    current_piece = create_piece()
    next_piece = create_piece()
    board = [[0] * WIDTH for _ in range(HEIGHT)]
    score = 0
    level = 0
    # FPS = MIN_FPS


def create_piece():
    index = random.randint(0, len(SHAPES) - 1)
    return Piece(SHAPES[index], SHAPES_COLOR[index])


def clear_completed_lines():
    completed_lines = [i for i, row in enumerate(board) if all(row)]
    for i in completed_lines:
        del board[i]
        board.insert(0, [0] * WIDTH)
    return len(completed_lines)


def show_next_piece(screen, next_piece, line):
    font = pygame.font.Font(None, 30)
    elements = [(NEXT_PIECE, font, EXTRA_WIDTH // 2, 10 * line, True, NEXT_PIECE_COLOR)]
    rect_next = draw_elements(elements)

    # Calculate the x position centered horizontally
    x_pos = (EXTRA_WIDTH - len(next_piece.shape[0]) * CELL_SIZE) // 2

    # Draw the next piece
    for i, row in enumerate(next_piece.shape):
        for j, cell in enumerate(row):
            if cell:
                # Calculate the y position centered vertically
                y_pos = rect_next.bottom + 10 + i * CELL_SIZE

                pygame.draw.rect(
                    screen,
                    next_piece.color,
                    (
                        x_pos + j * CELL_SIZE,
                        y_pos,
                        CELL_SIZE,
                        CELL_SIZE,
                    ),
                )


def draw_text(font, text, width, height, bold=True, color=(255, 255, 255)):
    text_rendered = font.render(text, bold, color)
    rect_text = text_rendered.get_rect(center=(width, height))
    screen.blit(text_rendered, rect_text.topleft)
    return rect_text


def draw_elements(elements):
    rect_text = None
    for text, font, width, height, bold, color in elements:
        rect_text = draw_text(font, text, width, height, bold, color)
    return rect_text


def show_score(line):
    font = pygame.font.Font(None, 36)
    width = EXTRA_WIDTH // 2
    elements = [
        (SCORE, font, width, 10 * line, True, SCORE_COLOR),
        (f"{score}", font, width, 10 * (line + 3), False, SCORE_VALUE_COLOR),
        (LINES, font, width, 10 * (line + 6), True, LINES_COLOR),
        (f"{level}", font, width, 10 * (line + 9), False, LINES_VALUE_COLOR),
        (RECORD, font, width, 10 * (line + 12), True, RECORD_COLOR),
        (f"{record}", font, width, 10 * (line + 15), False, RECORD_VALUE_COLOR),
    ]
    draw_elements(elements)


def show_game_over(running):
    font_game_over = pygame.font.Font(None, 32)
    font_instructions = pygame.font.Font(None, 24)
    width = (EXTRA_WIDTH) // 2

    elements = [
        (
            GAME_OVER,
            font_game_over,
            width,
            HEIGHT * CELL_SIZE // 2,
            True,
            GAME_OVER_COLOR,
        ),
        (
            PRESS_ANY_KEY,
            font_instructions,
            width,
            (HEIGHT * CELL_SIZE) * 2 // 3,
            True,
            PRESS_ANY_KEY_COLOR,
        ),
    ]

    show_score(10)  # Mostrar las puntuaciones
    show_next_piece(screen, next_piece, 1)  # Mostrar la siguiente pieza
    draw_board()

    draw_elements(elements)

    pygame.display.flip()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            elif event.type == pygame.KEYDOWN:
                waiting_for_key = False
    return True


def draw_board():
    # Draw the board
    for i, row in enumerate(board):
        for j, color in enumerate(row):
            if color:
                pygame.draw.rect(
                    screen,
                    color,
                    (EXTRA_WIDTH + j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )


if __name__ == "__main__":
    # Initialization
    pygame.init()
    screen = pygame.display.set_mode(
        (WIDTH * CELL_SIZE + EXTRA_WIDTH, HEIGHT * CELL_SIZE)
    )
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()

    current_piece = create_piece()
    next_piece = create_piece()
    board = [[0] * WIDTH for _ in range(HEIGHT)]

    # Keep track of key states
    pressed_keys = {}

    # Score
    score = 0
    level = 0
    record = 0

    # Main loop
    prev_time1 = pygame.time.get_ticks()
    prev_time2 = pygame.time.get_ticks()
    running = True
    while running:
        time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                pressed_keys[event.key] = True
            elif event.type == pygame.KEYUP:
                pressed_keys[event.key] = False

        screen.fill(BACKGROUND_COLOR)

        # Draw the grid
        draw_grid()
        if time - prev_time2 > SENSIBILIDAD_KEYBOARD:
            prev_time2 = pygame.time.get_ticks()
            # Move the piece down automatically
            if pressed_keys.get(pygame.K_DOWN):
                current_piece.move(0, 1)
            elif pressed_keys.get(pygame.K_LEFT):
                current_piece.move(-1, 0)
            elif pressed_keys.get(pygame.K_RIGHT):
                current_piece.move(1, 0)
            elif pressed_keys.get(pygame.K_UP):  # Rotate the piece
                current_piece.rotate()

        if time - prev_time1 > timeLap:
            prev_time1 = pygame.time.get_ticks()
            # Move the piece down automatically
            if current_piece.y + len(current_piece.shape) < HEIGHT and not any(
                board[current_piece.y + i + 1][current_piece.x + j] and cell
                for i, row in enumerate(current_piece.shape)
                for j, cell in enumerate(row)
            ):
                current_piece.move(0, 1)
            else:
                # Fix the piece to the board
                for i, row in enumerate(current_piece.shape):
                    for j, cell in enumerate(row):
                        if cell:
                            board[current_piece.y + i][
                                current_piece.x + j
                            ] = current_piece.color

                total_ones = sum(sum(sublist) for sublist in current_piece.shape)

                score += total_ones

                # Clear completed lines and update the score
                completed_lines = clear_completed_lines()

                score += completed_lines * POINTS_PER_PIECE
                level += completed_lines
                if score > record:
                    record = score

                # Adjust the game speed based on the score
                timeLap = (Y2 - Y1) / (X2 - X1) * (level-X1) + Y1      
                # Check if the board is full and end the game
                if any(board[0]):
                    running = False

                    if show_game_over(running):
                        restart_game()
                        running = True

                # Create a new piece
                current_piece = next_piece
                next_piece = create_piece()

        # Draw the board
        draw_board()

        # Draw the current piece
        current_piece.draw(screen)

        # Show the next piece
        show_next_piece(screen, next_piece, 1)
        # Show the score on the screen
        show_score(10)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
sys.exit()
