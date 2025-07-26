import pygame
import sys
import numpy as np
from prediciton import predict, prepare_canvas
import threading

pygame.init()

FPS = 1200
SCREEN_SIZE = (600, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Prdict the Number")
clock = pygame.time.Clock()

WIDTH, HEIGHT = 56, 56
canvas = np.zeros((HEIGHT, WIDTH), dtype=np.int16)

canvases = []

screen.fill((255, 255, 255))

drawing = False
brush_size = 15
brush_size_arr = 2

def update_predict():
    global is_pred, predict_text, predict_relese
    is_pred = True

    pred_num = predict(prepare_canvas(canvas, 20))
    
    update_predict_text(str(pred_num))
    predict_relese = 1
    is_pred = False

def update_predict_text(txt):
    global predict_text
    predict_text = font.render(txt, False, (0, 0, 0), (255, 255, 255))


predict_relese = 1
font = pygame.font.SysFont("Arial", 30, True, False)
predict_text = font.render('.', False, (0, 0, 0))
text_pos = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1] - 50)
is_pred = False

text_background = pygame.Rect(0, 0, 50, 50)
text_background.x, text_background.y = text_pos[0] - 25//2, text_pos[1] 

keys_text = pygame.font.SysFont("Arial", 20, True, False).render("C = Clear Canvas", False, (20,) * 3)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True

        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                screen.fill((255, 255, 255))
                canvas = np.zeros((HEIGHT, WIDTH), dtype=np.uint) 

    predict_relese = predict_relese - 1/FPS if not drawing else 0.5
    if not (canvas == 0).all() and not is_pred and predict_relese < 0:
        thread = threading.Thread(target=update_predict)
        thread.start()

    if drawing:
        update_predict_text("...")
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 0 <= mouse_x < SCREEN_SIZE[0] and 0 <= mouse_y < SCREEN_SIZE[1]:
            pygame.draw.circle(screen, (0, 0, 0), (mouse_x, mouse_y), brush_size)

            for dx in range(-brush_size_arr, 0):
                for dy in range(-brush_size_arr, 0):
                    x = round(mouse_x * WIDTH / SCREEN_SIZE[0]) + dx
                    y = round(mouse_y * HEIGHT / SCREEN_SIZE[1]) + dy

                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                        canvas[y][x] = 255


    pygame.draw.rect(screen, (255,) * 3, text_background)
    screen.blit(predict_text, text_pos)

    screen.blit(keys_text, (30, SCREEN_SIZE[1] - 40))

    pygame.display.update()
    clock.tick(FPS)
