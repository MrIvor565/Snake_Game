import pygame
import sys
import random2

pygame.init()

SIZE_BLOCK = 20
FRAME_COLOR = (0, 200, 204)
WHITE = (255, 255, 255)
BLUE = (204, 255, 255)
RED = (224, 0, 0)
HEADER_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 102, 0)
COUNT_BLOCK = 20
HEADER_MARGIN = 70
MARGIN = 1
size = [SIZE_BLOCK * COUNT_BLOCK + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCK,
        SIZE_BLOCK * COUNT_BLOCK + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCK + HEADER_MARGIN]
print(size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 26)


class SnackBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCK and 0 <= self.y < COUNT_BLOCK

    def __eg__(self, other):
        return isinstance(other, SnackBlock) and self.x == other.x and self.y == other.y

def get_random2_empty_block():
    x = random2.randint(0, COUNT_BLOCK - 1)
    y = random2.randint(0, COUNT_BLOCK - 1)
    empty_block = SnackBlock(x, y)
    while empty_block in snake_blocks:
        empty_block.x = random2.randint(0, COUNT_BLOCK - 1)
        empty_block.y = random2.randint(0, COUNT_BLOCK - 1)
    return empty_block

def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK,
                                     SIZE_BLOCK])

snake_blocks = [SnackBlock(9, 8), SnackBlock(9, 9), SnackBlock(9, 10)]
apple = get_random2_empty_block()
d_row = buf_row = 0
d_col = buf_col = 1
total = 0
speed = 1

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('exit')
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and d_col != 0:
                buf_row = -1
                buf_col = 0
            elif event.key == pygame.K_DOWN and d_col != 0:
                buf_row = 1
                buf_col = 0
            elif event.key == pygame.K_LEFT and d_row != 0:
                buf_row = 0
                buf_col = -1
            elif event.key == pygame.K_RIGHT and d_row != 0:
                buf_row = 0
                buf_col = 1

    screen.fill(FRAME_COLOR)
    pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

    text_total = courier.render(f"Total: {total}", 0, WHITE)
    text_speed = courier.render(f"Speed: {speed}", 0, WHITE)
    screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
    screen.blit(text_speed, (SIZE_BLOCK + 230, SIZE_BLOCK))

    for row in range(COUNT_BLOCK):
        for column in range(COUNT_BLOCK):
            if (row + column) % 2 == 0:
                color = BLUE
            else:
                color = BLUE

            draw_block(color, row, column)

    head = snake_blocks[-1]
    if not head.is_inside():
        print('crash')
        break
        #pygame.quit()
        #sys.exit()

    draw_block(RED, apple.x, apple.y)
    for block in snake_blocks:
        draw_block(SNAKE_COLOR, block.x, block.y)

    pygame.display.flip()

    if apple == head:
        total += 1
        speed += total // 5 + 1
        snake_blocks.append(apple)
        apple = get_random2_empty_block()

    d_row = buf_row
    d_col = buf_col
    new_head = SnackBlock(head.x + d_row, head.y + d_col)

    if new_head in snake_blocks:
        print('crash yourself')
        break
        #pygame.quit()
        #sys.exit()

    snake_blocks.append(new_head)
    snake_blocks.pop(0)

    #pygame.display.flip()
    timer.tick(3 + speed)
