import pygame
import random
import math

pygame.init()

FPS = 60

WIDTH, HEIGHT = 800, 900  # Increased height to accommodate score display
ROWS = 4
COLS = 4

RECT_HEIGHT = 800 // ROWS
RECT_WIDTH = WIDTH // COLS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)
BUTTON_COLOR = (143, 122, 102)
BUTTON_HOVER_COLOR = (169, 149, 130)

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
BUTTON_FONT = pygame.font.SysFont("comicsans", 50)
SCORE_FONT = pygame.font.SysFont("comicsans", 36, bold=True)
MOVE_VEL = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# Global variables for score and high score
score = 0
high_score = 0

class Tile:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT + 100  # Adjusted for score display

    def get_color(self):
        color_index = min(int(math.log2(self.value)) - 1, len(self.COLORS) - 1)
        return self.COLORS[color_index]

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil((self.y - 100) / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor((self.y - 100) / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]

def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT + 100
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 100), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 100, WIDTH, HEIGHT - 100), OUTLINE_THICKNESS)

def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)

    # Draw score and high score
    score_text = SCORE_FONT.render(f"Score: {score}", True, FONT_COLOR)
    high_score_text = SCORE_FONT.render(f"High Score: {high_score}", True, FONT_COLOR)
    window.blit(score_text, (20, 20))
    window.blit(high_score_text, (WIDTH - high_score_text.get_width() - 20, 20))

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)

    pygame.display.update()

def get_random_pos(tiles):
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)
        if f"{row}{col}" not in tiles:
            return row, col

def move_tiles(window, tiles, clock, direction):
    global score
    updated = True
    blocks = set()

    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        ceil = False

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif (
                tile.value == next_tile.value
                and tile not in blocks
                and next_tile not in blocks
            ):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    score += next_tile.value  # Add score when tiles merge
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True

        update_tiles(window, tiles, sorted_tiles)

    return end_move(tiles)

def end_move(tiles):
    global high_score
    if len(tiles) == 16:
        if not can_move(tiles):
            high_score = max(score, high_score)  # Update high score if necessary
            show_game_over_screen(WINDOW)
            return "lost"

    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"

def can_move(tiles):
    for tile in tiles.values():
        neighbors = [
            tiles.get(f"{tile.row}{tile.col + 1}"),  # Right
            tiles.get(f"{tile.row}{tile.col - 1}"),  # Left
            tiles.get(f"{tile.row + 1}{tile.col}"),  # Down
            tiles.get(f"{tile.row - 1}{tile.col}"),  # Up
        ]
        for neighbor in neighbors:
            if neighbor and neighbor.value == tile.value:
                return True
    return False

def show_game_over_screen(window):
    window.fill(BACKGROUND_COLOR)
    text = FONT.render("You Lost!", True, FONT_COLOR)
    score_text = SCORE_FONT.render(f"Final Score: {score}", True, FONT_COLOR)
    high_score_text = SCORE_FONT.render(f"High Score: {high_score}", True, FONT_COLOR)
    
    WINDOW.blit(
        text,
        (
            WIDTH // 2 - text.get_width() // 2,
            HEIGHT // 2 - text.get_height() // 2 - 150,
        ),
    )
    WINDOW.blit(
        score_text,
        (
            WIDTH // 2 - score_text.get_width() // 2,
            HEIGHT // 2 - score_text.get_height() // 2 - 50,
        ),
    )
    WINDOW.blit(
        high_score_text,
        (
            WIDTH // 2 - high_score_text.get_width() // 2,
            HEIGHT // 2 - high_score_text.get_height() // 2,
        ),
    )

    # Exit Button
    exit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)
    pygame.draw.rect(WINDOW, BUTTON_COLOR, exit_button_rect)
    
    exit_button_text = BUTTON_FONT.render("Exit", True, FONT_COLOR)
    WINDOW.blit(
        exit_button_text,
        (
            exit_button_rect.x + (exit_button_rect.width / 2 - exit_button_text.get_width() / 2),
            exit_button_rect.y + (exit_button_rect.height / 2 - exit_button_text.get_height() / 2),
        ),
    )

    # Play Again Button
    play_again_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 130, 200, 60)
    pygame.draw.rect(WINDOW, BUTTON_COLOR, play_again_button_rect)
    
    play_again_button_text = BUTTON_FONT.render("Play Again", True, FONT_COLOR)
    WINDOW.blit(
        play_again_button_text,
        (
            play_again_button_rect.x + (play_again_button_rect.width / 2 - play_again_button_text.get_width() / 2),
            play_again_button_rect.y + (play_again_button_rect.height / 2 - play_again_button_text.get_height() / 2),
        ),
    )

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    return
                if play_again_button_rect.collidepoint(event.pos):
                    main(WINDOW)  # Restart the game
                    return

def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)

def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles

def main(window):
    global score, high_score
    clock = pygame.time.Clock()
    run = True
    game_over = False

    score = 0  # Reset score at the start of each game
    tiles = generate_tiles()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    status = move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    status = move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    status = move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    status = move_tiles(window, tiles, clock, "down")

                if status == "lost":
                    game_over = True
                    high_score = max(score, high_score)  # Update high score if necessary
                    show_game_over_screen(window)

        if not game_over:
            draw(window, tiles)

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)