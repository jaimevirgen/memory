import pygame
import random
import sys

# --------------------------------------------------
# INITIALIZATION
# --------------------------------------------------
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

WIDTH = screen.get_width()
HEIGHT = screen.get_height()

pygame.display.set_caption("Memory")

clock = pygame.time.Clock()

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
GRID_ROWS = 4
GRID_COLS = 4

MAX_LEVELS = 10
LEVEL_TIME = 60

FLASH_DURATION = 300

BG_COLOR = (20, 20, 30)

TILE_COLOR = (50, 60, 90)
TILE_BORDER = (180, 180, 200)

TEXT_COLOR = (255, 255, 255)

BUTTON_COLOR = (50, 150, 255)
BUTTON_HOVER = (80, 180, 255)

PROGRESS_BG = (60, 60, 60)
PROGRESS_FILL = (0, 220, 120)

# --------------------------------------------------
# FONTS
# --------------------------------------------------
font_large = pygame.font.SysFont(None, 80)
font_medium = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 32)

# --------------------------------------------------
# STATES
# --------------------------------------------------
STATE_READY = "ready"
STATE_PLAYING = "playing"
STATE_WIN = "win"
STATE_LOSE = "lose"

state = STATE_READY

# --------------------------------------------------
# GRID
# --------------------------------------------------
GRID_TOP = 120
GRID_MARGIN = 20

grid_width = WIDTH - 120
grid_height = HEIGHT - 300

tile_width = (
    grid_width - GRID_MARGIN * (GRID_COLS - 1)
) // GRID_COLS

tile_height = (
    grid_height - GRID_MARGIN * (GRID_ROWS - 1)
) // GRID_ROWS

grid_x = (WIDTH - grid_width) // 2
grid_y = GRID_TOP

# --------------------------------------------------
# GAME VARIABLES
# --------------------------------------------------
level = 1
input_text = ""

numbers = []
matching_number = None

level_start_time = 0

flash_color = None
flash_start_time = 0

reveal_answer = None

# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def reset_game():
    global state
    global level
    global input_text
    global numbers
    global matching_number

    pygame.mouse.set_visible(True)

    state = STATE_READY
    level = 1
    input_text = ""
    numbers = []
    matching_number = None


def get_digit_range():

    if level <= 3:
        return 10, 99

    if level <= 7:
        return 100, 999

    return 1000, 9999


def get_max_digits():

    if level <= 3:
        return 2

    if level <= 7:
        return 3

    return 4


def generate_level():

    global numbers
    global matching_number

    minimum, maximum = get_digit_range()

    unique_numbers = set()

    while len(unique_numbers) < 15:
        unique_numbers.add(
            random.randint(minimum, maximum)
        )

    unique_numbers = list(unique_numbers)

    matching_number = random.choice(unique_numbers)

    numbers = unique_numbers.copy()
    numbers.append(matching_number)

    random.shuffle(numbers)


def start_level():

    global level_start_time
    global input_text

    pygame.mouse.set_visible(False)

    generate_level()

    input_text = ""

    level_start_time = pygame.time.get_ticks()


def trigger_flash(color):

    global flash_color
    global flash_start_time

    flash_color = color
    flash_start_time = pygame.time.get_ticks()


# --------------------------------------------------
# DRAWING
# --------------------------------------------------
def draw_flash():

    global flash_color

    if flash_color is None:
        return

    elapsed = (
        pygame.time.get_ticks()
        - flash_start_time
    )

    if elapsed >= FLASH_DURATION:
        flash_color = None
        return

    alpha = int(
        180 * (1 - elapsed / FLASH_DURATION)
    )

    overlay = pygame.Surface(
        (WIDTH, HEIGHT)
    )

    overlay.set_alpha(alpha)
    overlay.fill(flash_color)

    screen.blit(overlay, (0, 0))


def draw_progress_bar():

    elapsed = (
        pygame.time.get_ticks()
        - level_start_time
    ) / 1000

    progress = min(
        elapsed / LEVEL_TIME,
        1.0
    )

    bar_x = 40
    bar_y = 30

    bar_width = WIDTH - 80
    bar_height = 30

    pygame.draw.rect(
        screen,
        PROGRESS_BG,
        (bar_x, bar_y, bar_width, bar_height)
    )

    pygame.draw.rect(
        screen,
        PROGRESS_FILL,
        (
            bar_x,
            bar_y,
            int(bar_width * progress),
            bar_height
        )
    )

    pygame.draw.rect(
        screen,
        TEXT_COLOR,
        (bar_x, bar_y, bar_width, bar_height),
        2
    )


def draw_grid():

    for i in range(16):

        row = i // GRID_COLS
        col = i % GRID_COLS

        x = grid_x + col * (
            tile_width + GRID_MARGIN
        )

        y = grid_y + row * (
            tile_height + GRID_MARGIN
        )

        rect = pygame.Rect(
            x,
            y,
            tile_width,
            tile_height
        )

        pygame.draw.rect(
            screen,
            TILE_COLOR,
            rect
        )

        pygame.draw.rect(
            screen,
            TILE_BORDER,
            rect,
            2
        )

        text = font_medium.render(
            str(numbers[i]),
            True,
            TEXT_COLOR
        )

        screen.blit(
            text,
            text.get_rect(center=rect.center)
        )


def draw_level():

    level_text = font_medium.render(
        f"Level {level}",
        True,
        TEXT_COLOR
    )

    screen.blit(
        level_text,
        level_text.get_rect(
            bottomright=(
                WIDTH - 20,
                HEIGHT - 20
            )
        )
    )


def draw_input():

    prompt = font_medium.render(
        "Answer:",
        True,
        TEXT_COLOR
    )

    answer = font_large.render(
        input_text,
        True,
        (255, 255, 100)
    )

    screen.blit(
        prompt,
        (50, HEIGHT - 120)
    )

    screen.blit(
        answer,
        (50, HEIGHT - 80)
    )


def draw_ready_screen():

    pygame.mouse.set_visible(True)

    title = font_large.render(
        "MEMORY",
        True,
        TEXT_COLOR
    )

    screen.blit(
        title,
        title.get_rect(
            center=(WIDTH // 2, 200)
        )
    )

    mouse_pos = pygame.mouse.get_pos()

    # START BUTTON
    start_button = pygame.Rect(
        WIDTH // 2 - 120,
        HEIGHT // 2 - 60,
        240,
        80
    )

    start_color = BUTTON_COLOR
    if start_button.collidepoint(mouse_pos):
        start_color = BUTTON_HOVER

    pygame.draw.rect(screen, start_color, start_button)
    pygame.draw.rect(screen, TEXT_COLOR, start_button, 2)

    start_text = font_medium.render(
        "START",
        True,
        TEXT_COLOR
    )

    screen.blit(
        start_text,
        start_text.get_rect(center=start_button.center)
    )

    # QUIT BUTTON
    quit_button = pygame.Rect(
        WIDTH // 2 - 120,
        HEIGHT // 2 + 40,
        240,
        80
    )

    quit_color = BUTTON_COLOR
    if quit_button.collidepoint(mouse_pos):
        quit_color = BUTTON_HOVER

    pygame.draw.rect(screen, quit_color, quit_button)
    pygame.draw.rect(screen, TEXT_COLOR, quit_button, 2)

    quit_text = font_medium.render(
        "QUIT",
        True,
        TEXT_COLOR
    )

    screen.blit(
        quit_text,
        quit_text.get_rect(center=quit_button.center)
    )

    instructions = font_small.render(
        "Click Start or press SPACE to begin",
        True,
        TEXT_COLOR
    )

    screen.blit(
        instructions,
        instructions.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT // 2 + 160
            )
        )
    )

    return start_button, quit_button


def draw_center_message(message):

    text = font_large.render(
        message,
        True,
        TEXT_COLOR
    )

    screen.blit(
        text,
        text.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT // 2
            )
        )
    )

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------
running = True

while running:

    screen.fill(BG_COLOR)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ESC anywhere
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            reset_game()
            continue

        # -----------------------------------------
        # READY SCREEN INPUT
        # -----------------------------------------
        if state == STATE_READY:

            start_button = pygame.Rect(
                WIDTH // 2 - 120,
                HEIGHT // 2 - 60,
                240,
                80
            )

            quit_button = pygame.Rect(
                WIDTH // 2 - 120,
                HEIGHT // 2 + 40,
                240,
                80
            )

            if event.type == pygame.MOUSEBUTTONDOWN:

                if start_button.collidepoint(event.pos):

                    level = 1
                    state = STATE_PLAYING
                    start_level()

                elif quit_button.collidepoint(event.pos):

                    running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    level = 1
                    state = STATE_PLAYING
                    start_level()

                elif event.key == pygame.K_q:

                    running = False

        # -----------------------------------------
        # PLAYING INPUT
        # -----------------------------------------
        elif state == STATE_PLAYING:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:

                    input_text = input_text[:-1]

                elif event.key == pygame.K_RETURN:

                    if input_text == str(matching_number):

                        trigger_flash((0, 255, 0))

                        draw_progress_bar()
                        draw_grid()
                        draw_input()
                        draw_level()
                        draw_flash()

                        pygame.display.flip()
                        pygame.time.delay(250)

                        level += 1

                        if level > MAX_LEVELS:
                            state = STATE_WIN
                        else:
                            start_level()

                    else:

                        trigger_flash((255, 0, 0))

                    input_text = ""

                else:

                    if (
                        event.unicode.isdigit()
                        and len(input_text)
                        < get_max_digits()
                    ):
                        input_text += event.unicode

    # DRAW
    if state == STATE_READY:

        start_button, quit_button = draw_ready_screen()

    elif state == STATE_PLAYING:

        elapsed = (
            pygame.time.get_ticks()
            - level_start_time
        ) / 1000

        if elapsed >= LEVEL_TIME:

            trigger_flash((255, 220, 0))  # yellow reveal flash

            reveal_answer = matching_number

            state = STATE_LOSE

        draw_progress_bar()
        draw_grid()
        draw_input()
        draw_level()

    elif state == STATE_WIN:

        draw_center_message("YOU WIN!")

    elif state == STATE_LOSE:

        draw_center_message("TIMES UP!")

        if reveal_answer is not None:
            answer_text = font_large.render(
                str(reveal_answer),
                True,
                (255, 255, 120)
            )

            screen.blit(
                answer_text,
                answer_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
            )

    draw_flash()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
