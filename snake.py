import pygame
from time import sleep
from random import randint

# Constants
GREEN = (57,255,20)
BLACK = (0,0,0)
RED = (186,0,0)
SCREEN_SIZE = 400

# Snake class
class Snake:

    def __init__(self):
        self.width = 20
        self.color = GREEN
        self.partitions = [
            [SCREEN_SIZE//2, SCREEN_SIZE//2],
            [(SCREEN_SIZE//2)-self.width, SCREEN_SIZE//2],
            [(SCREEN_SIZE//2)-(self.width*2), SCREEN_SIZE//2],
        ]
        self.length = 3

    def add_partition(self):
        # vars for second-to-last and last partitions
        sec_to_last = self.partitions[-2]
        last = self.partitions[-1]

        if sec_to_last[0] > last[0]:
            self.partitions.append([last[0]-self.width, last[1]])
        if sec_to_last[0] < last[0]:
            self.partitions.append([last[0]+self.width, last[1]])
        if sec_to_last[1] > last[1]:
            self.partitions.append([last[0], last[1]-self.width])
        if sec_to_last[1] < last[1]:
            self.partitions.append([last[0], last[1]+self.width])

    def not_val_move(self, pos):
        # returns True is givin position NOT on screen
        if pos[0] > SCREEN_SIZE-self.width or pos[0] < 0 or pos[1] > SCREEN_SIZE-self.width or pos[1] < 0:
            return True
        # returns True if snake has hit itself, i.e., position already part of snake body
        if pos in self.partitions:
            return True
        else:
            return False
        

    def update_partitions(self, direction):
        '''
        Directions can be the following: "up", "down", "left", "right"
        '''

        # Update trailing partitions
        for i in range(len(self.partitions)-1, 0, -1):
            self.partitions[i][0] = self.partitions[i-1][0]
            self.partitions[i][1] = self.partitions[i-1][1]
        
        curr_head = self.partitions[0]

        if direction == "up":
            up = [curr_head[0], curr_head[1]-self.width]
            if self.not_val_move(up):
                loose()
            else:
                self.partitions[0] = up
        elif direction == "down":
            down = [curr_head[0], curr_head[1]+self.width]
            if self.not_val_move(down):
                loose()
            else:
                self.partitions[0] = down
        elif direction == "left":
            left = [curr_head[0]-self.width, curr_head[1]]
            if self.not_val_move(left):
                loose()
            else:
                self.partitions[0] = left
        elif direction == "right":
            right = [curr_head[0]+self.width, curr_head[1]]
            if self.not_val_move(right):
                loose()
            else:
                self.partitions[0] = right
        else:
            raise ValueError("Incorrect Key... Not the following: up-arrow, down-arrow, right-arrow, left-arrow")

def gen_point_pos():
    return [randint(0,9)*20, randint(0,9)*20]

def loose():
    '''
    YOU LOST BITCH
    '''
    screen.fill(BLACK)
    font_obj=pygame.font.Font("C:\Windows\Fonts\Arial.ttf",40) 
    text_obj=font_obj.render("YOU HAVE DIED", True, RED)
    screen.blit(text_obj, (45,160))
    pygame.display.update()
    sleep(2)
    quit()


# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
# Create the snake
snake = Snake()

# Game loop
running = True
# Current Direction
curr_dir = "right"
# gen first point
point = gen_point_pos()

while running:

    got_point = False
    action_this_round = False

    pygame.display.set_caption("SNAKE")
    screen.fill(BLACK)

    # point counter
    font_obj=pygame.font.Font("C:\Windows\Fonts\Arial.ttf",20) 
    text_obj=font_obj.render(str(snake.length), True, RED)
    screen.blit(text_obj, (195,5))

    # show point (red square)
    pygame.draw.rect(screen, RED, (point[0], point[1], snake.width, snake.width))

    for p in snake.partitions:
        pygame.draw.rect(screen, GREEN, (p[0], p[1], snake.width, snake.width))
        pygame.display.update()
    

    sleep(0.15)


    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            action_this_round = True
            if event.key == pygame.K_UP and curr_dir != "down":
                curr_dir = "up"
                snake.update_partitions(curr_dir)
            elif event.key == pygame.K_DOWN and curr_dir != "up":
                curr_dir = "down"
                snake.update_partitions(curr_dir)
            elif event.key == pygame.K_LEFT and curr_dir != "right":
                curr_dir = "left"
                snake.update_partitions(curr_dir)
            elif event.key == pygame.K_RIGHT and curr_dir != "left":
                curr_dir = "right"
                snake.update_partitions(curr_dir)
            else:
                pass

    print(snake.partitions[0], point)
    if snake.partitions[0] == point:
        got_point = True
        snake.length += 1
        snake.add_partition()
        print('yes')

    if got_point == True:
        new_point = gen_point_pos()
        while new_point in snake.partitions or new_point == point:
            new_point = gen_point_pos()
        point = new_point

    if action_this_round == False:
        snake.update_partitions(curr_dir)

