import pygame
import numpy as np

# function for plotting the map
def create_map(x, trash_cans, window_size_x = 3000, window_size_y = 2000):
    pygame.init()
    pygame.display.init()

    canvas = pygame.Surface((window_size_y, window_size_x))
    canvas.fill((255, 255, 255))
    pix_square_size_x = (window_size_x / 30)  # size of a single grid square in pixels
    pix_square_size_y = (window_size_y / 20)  # size of a single grid square in pixels

    i = 0
    for r in x:
        j = 0
        for c in r:
            if c == 0:
                pygame.draw.rect(canvas, (255, 255, 255),
                                pygame.Rect((int(pix_square_size_x)*i, int(pix_square_size_y)*j),
                                (pix_square_size_x, pix_square_size_y)))
            elif c == 1:
                pygame.draw.rect(canvas, (192, 192, 192),
                                pygame.Rect((int(pix_square_size_x)*i, int(pix_square_size_y)*j),
                                (pix_square_size_x, pix_square_size_y)))
            elif c == 2:
                pygame.draw.rect(canvas, (255, 0, 0),
                                pygame.Rect((int(pix_square_size_x)*i, int(pix_square_size_y)*j),
                                (pix_square_size_x-20, pix_square_size_y-20)))
            elif c == 3:
                pygame.draw.rect(canvas, (51, 175, 2),
                                pygame.Rect((int(pix_square_size_x)*i, int(pix_square_size_y)*j),
                                (pix_square_size_x, pix_square_size_y)))
            elif c == 4:
                pygame.draw.ellipse(canvas, (97, 255, 34), ((int(pix_square_size_x)*i, int(pix_square_size_y)*j), (pix_square_size_x, pix_square_size_y)))
            
            elif c == 5:
                pygame.draw.ellipse(canvas, (96, 96, 96), ((int(pix_square_size_x)*i, int(pix_square_size_y)*j), (pix_square_size_x, pix_square_size_y)))

            elif c == 6:
                pygame.draw.ellipse(canvas, (0, 0, 255), ((int(pix_square_size_x)*i, int(pix_square_size_y)*j), (pix_square_size_x, pix_square_size_y)))

            elif c == 7:
                pygame.draw.ellipse(canvas, (255, 190, 0), ((int(pix_square_size_x)*i, int(pix_square_size_y)*j), (pix_square_size_x, pix_square_size_y)))

            elif c == 8:
                if (i,j) in trash_cans['plastic']:
                    pygame.draw.ellipse(canvas, (0, 0, 255), ((int(pix_square_size_x)*i, int(pix_square_size_y)*j), (pix_square_size_x, pix_square_size_y)))

                if (i,j) in trash_cans['paper']:
                    pygame.draw.ellipse(canvas, (255, 190, 0), ((int(pix_square_size_x)*i, int(pix_square_size_y)*j), (pix_square_size_x, pix_square_size_y)))

                if (i,j) in trash_cans['trash']:
                    pygame.draw.ellipse(canvas, (96, 96, 96), ((int(pix_square_size_x)*i, int(pix_square_size_y)*j), (pix_square_size_x, pix_square_size_y)))

                if (i,j) in trash_cans['compost']:
                    pygame.draw.ellipse(canvas, (97, 255, 34), ((int(pix_square_size_x)*i, int(pix_square_size_y)*j), (pix_square_size_x, pix_square_size_y)))

                pygame.draw.ellipse(canvas, (255, 0, 0), ((int(pix_square_size_x)*i, int(pix_square_size_y)*j), (pix_square_size_x, pix_square_size_y)), width= 15)

            else:
                pygame.draw.rect(canvas, (153, 76, 0),
                                pygame.Rect((int(pix_square_size_x)*i, int(pix_square_size_y)*j),
                                (pix_square_size_x, pix_square_size_y)))
            j+=1
        i+=1

    return np.array(pygame.surfarray.pixels3d(canvas))