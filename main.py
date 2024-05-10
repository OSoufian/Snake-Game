import pygame, sys, random
from pygame.math import Vector2

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('images/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('images/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('images/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('images/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('images/body_horizontal.png').convert_alpha()

        self.body_lbc = pygame.image.load('images/body_lbc.png').convert_alpha()
        self.body_ltc = pygame.image.load('images/body_ltc.png').convert_alpha()
        self.body_rbc = pygame.image.load('images/body_rbc.png').convert_alpha()
        self.body_rtc = pygame.image.load('images/body_rtc.png').convert_alpha()


    def draw_snake(self):
        for index, block in enumerate(self.body):
            x_position = block.x * cell_size
            y_position = block.y * cell_size
            block_rectangle = pygame.Rect(x_position, y_position, cell_size, cell_size)
            if block == self.body[0]:
                self.draw_head(block_rectangle)                
            elif block == self.body[-1]:
                self.draw_tail(block_rectangle)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rectangle)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rectangle)
                else:
                    if (previous_block.x == -1 and next_block.y == -1
                     or previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_rbc, block_rectangle)
                    elif (previous_block.x == -1 and next_block.y == 1
                       or previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_rtc, block_rectangle)
                    elif (previous_block.x == 1 and next_block.y == -1
                       or previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_lbc, block_rectangle)
                    elif (previous_block.x == 1 and next_block.y == 1
                       or previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_ltc, block_rectangle)
                

    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

    def draw_head(self, block_rectangle):
        head_direction = self.body[0] - self.body[1]
        if head_direction == WEST:
            screen.blit(self.head_left, block_rectangle)
        elif head_direction == EAST:
            screen.blit(self.head_right, block_rectangle)
        elif head_direction == NORTH:
            screen.blit(self.head_up, block_rectangle)
        elif head_direction == SOUTH:
            screen.blit(self.head_down, block_rectangle)

    def draw_tail(self, block_rectangle):
        tail_direction = self.body[-2] - self.body[-1]
        if tail_direction == EAST:
            screen.blit(self.tail_left, block_rectangle)
        if tail_direction == NORTH:
            screen.blit(self.tail_down, block_rectangle)
        if tail_direction == WEST:
            screen.blit(self.tail_right, block_rectangle)
        if tail_direction == SOUTH:
            screen.blit(self.tail_up, block_rectangle)

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class Fruit:    
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.position = Vector2(self.x, self.y)

    def draw(self):
        fruit_rectangle = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        screen.blit(fruit_image, fruit_rectangle)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 0
        self.crunch_sound = pygame.mixer.Sound('crunch.wav')

    def update(self):
        self.snake.move()
        game.game_over()
        game.check_collision()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw()
        self.snake.draw_snake()
        self.display_score()

    def check_collision(self):
        if self.snake.body[0] == self.fruit.position:
            self.snake.new_block = True
            self.fruit = Fruit()
            self.score += 1
            self.crunch_sound.play()

        for block in self.snake.body:
            if block == self.fruit.position:
                self.fruit = Fruit()

    def draw_grass(self):
        grass_color = '#a2d149'
        for row in range(cell_number):
            if row % 2 == 0:
                for column in range(cell_number):
                    if column % 2 == 0:
                        grass_rectangle = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rectangle)
            else:
                for column in range(cell_number):
                    if column % 2 != 0:
                        grass_rectangle = pygame.Rect(column * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rectangle)
                    


    def game_over(self):
        if (self.snake.body[0].x < 0 or self.snake.body[0].x >= cell_number
         or self.snake.body[0].y < 0 or self.snake.body[0].y >= cell_number):
            self.game_restart()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_restart()

    def game_restart(self):
        self.snake.reset()
        self.score = 0

    def display_score(self):
        score_text = str(self.score)
        score_surface = game_font.render(score_text, True, 'black')
        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number - 60
        score_rectangle = score_surface.get_rect(center = (score_x, score_y))
        fruit_rectangle = fruit_image.get_rect(midright = (score_rectangle.left, score_rectangle.centery))
        bg_rectangle = pygame.Rect(fruit_rectangle.left, fruit_rectangle.top, fruit_rectangle.width + score_rectangle.width + 6, fruit_rectangle.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rectangle)        
        screen.blit(score_surface, score_rectangle)
        screen.blit(fruit_image, fruit_rectangle)
        pygame.draw.rect(screen, 'black', bg_rectangle, 2)


pygame.init()
cell_size = 40
cell_number = 20
screen_border = cell_size * cell_number 
screen = pygame.display.set_mode((screen_border, screen_border))
clock = pygame.time.Clock()

NORTH = Vector2(0, -1)
EAST = Vector2(1, 0)
SOUTH = Vector2(0, 1)
WEST = Vector2(-1, 0)

fruit_image = pygame.image.load('images/apple.png').convert_alpha()
game_font = pygame.font.Font('PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        if event.type == SCREEN_UPDATE:
            game.update()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if game.snake.direction != SOUTH:
                    game.snake.direction = NORTH
            if event.key == pygame.K_RIGHT:
                if game.snake.direction != WEST:
                    game.snake.direction = EAST
            if event.key == pygame.K_DOWN:
                if game.snake.direction != NORTH:
                    game.snake.direction = SOUTH
            if event.key == pygame.K_LEFT:
                if game.snake.direction != EAST:
                    game.snake.direction = WEST

    screen.fill('#aad751')
    game.draw_elements()
    pygame.display.update()
    clock.tick(60)