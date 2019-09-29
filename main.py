import numpy as np
import scipy.ndimage
import pygame
import textwrap


def draw_cells(cell_matrix, cells_in_row, cell_perimeter, screen_for_drawing):
    cell_x = 0
    cell_y = 0
    cell_counter = 0
    array = np.ndarray.tolist(cell_matrix.flatten())
    for cell in array:
        if cell:
            cell_colour = BLACK
        else:
            cell_colour = WHITE
        pygame.draw.rect(screen_for_drawing, cell_colour, (cell_x, cell_y, cell_perimeter, cell_perimeter))
        cell_x += cell_dimensions
        cell_counter += 1
        if cell_counter >= cells_in_row:
            cell_y += cell_perimeter
            cell_x = 0
            cell_counter = 0


def update_cells(cell_matrix, convolution_kernel):
    updated = scipy.ndimage.convolve(cell_matrix, weights=convolution_kernel)

    m1 = updated == 3
    m2 = updated == 12
    m3 = updated == 13
    final_boolean = (m1 + m2 + m3)
    final = final_boolean.astype(int)
    return final


def wrap_text(message, wraplimit):
    return textwrap.fill(message, wraplimit)


def display_message(message, font_info, xy):  # Font info = [size, character limit, vertical spacing and colour)
    text_to_blit = wrap_text(message, font_info[1])
    font = pygame.font.SysFont('Courier New', font_info[0], True)
    for part in text_to_blit.split('\n'):
        rendered_text = font.render(part, True, font_info[3])
        screen.blit(rendered_text, xy)
        xy[1] += font_info[2]


def display_generation_count(target_screen):
    generation_count_text = "Generation count: " + str(generation_count)
    font = pygame.font.SysFont('Courier New', 22, True, False)
    for_display = font.render(generation_count_text, True, GREEN)
    target_screen.blit(for_display, [30, 30])


def manual_cell_input(mouse_position, cell_array):
    x_coordinate, y_coordinate = mouse_position
    x_column_number = int(x_coordinate / cell_dimensions)
    y_row_number = int(y_coordinate / cell_dimensions)

    if cell_array[y_row_number, x_column_number] == 0:
        cell_array[y_row_number, x_column_number] = 1
    else:
        cell_array[y_row_number, x_column_number] = 0


# Setting screen dimensions, colours etc
screen_width = 900
screen_height = 600
caption = 'Cellular automata - DHK'
fps = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

FONT_INFO = [30, (screen_width / 20), 30, WHITE]

initialisation_message = """- Welcome to Conway's Game of Life. \
                        - Press Enter to generate a random set of cells, or press Space to enter your own using mouse clicks."""


manual_intro_message = """- Manual mode instructions: \n
                       - Use mouse clicks to bring cells to life.\n
                       - Click a live cell to kill it. \n
                       - Hit space to start inputting cells. \n
                       - Hit space again to start the simulation."""

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(caption)

clock = pygame.time.Clock()  # For adjusting FPS

# Drawing variables/characteristics

cell_dimensions = 10
row_length = int(screen_width / cell_dimensions)
row_count = int(screen_height / cell_dimensions)
matrix_size = (row_count, row_length)

# Random matrix of 'alive' and 'dead' cells
random_matrix = np.random.choice(a=[0, 1], size=matrix_size, p=[0.9, 0.1])

blank_matrix = np.zeros(matrix_size)

# Kernel for counting adjacent cells - the 10 is to distinguish between live and dead cells more easily.
kernel = [[1, 1, 1], [1, 10, 1], [1, 1, 1]]

# Blank starting matrix updated to random matrix or manually by the player before simulation begins.
matrix = blank_matrix

# For display during simulation
generation_count = 0

mode = "initialising"
done = False
pygame.init()
while not done:

    screen.fill(BLACK)

    if mode == "initialising":
        display_message(initialisation_message, FONT_INFO, [30, 30])
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    matrix = random_matrix
                    mode = "simulating"
                elif event.key == pygame.K_SPACE:
                    mode = "manual_intro"
                    screen.fill(BLACK)

    if mode == "manual_intro":
        display_message(manual_intro_message, FONT_INFO, [30, 30])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                mode = "manual"

    if mode == "manual":
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                manual_cell_input(pos, matrix)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                mode = "simulating"

        draw_cells(matrix, row_length, cell_dimensions, screen)

    if mode == "simulating":
        draw_cells(matrix, row_length, cell_dimensions, screen)
        display_generation_count(screen)
        matrix = update_cells(matrix, kernel)
        generation_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    pygame.display.update()
    clock.tick(fps)
