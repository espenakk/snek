import pygame, random

pygame.init()
pygame.display.set_caption("snek")
cell_size = 30
cell_number = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
running = True

purple = (185, 103, 255)
pink = (255, 113, 206)
green = (5, 255, 161)
blue = (1, 205, 254)
yellow = (255,251,150)


class Food:
    def __init__(self):
        self.position = self.randomize()
        self.rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)

    def draw(self):
        pygame.draw.rect(screen, yellow, self.rect, 15, 15)

    def randomize(self):
        position = pygame.Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
        return position
    
    def respawn(self):
        self.position = self.randomize()
        self.rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)

class Snake:
    def __init__(self):
        self.position = [pygame.Vector2(5, 5), pygame.Vector2(6, 5), pygame.Vector2(7, 5)]
        self.direction = pygame.Vector2(1, 0)
        self.update = pygame.USEREVENT
        pygame.time.set_timer(self.update, 100)
        self.eat_sound = pygame.mixer.Sound("audio/sounds/eat.mp3")
    
    def draw(self):
        self.body = []
        for segment in self.position:
            self.body.append(pygame.Rect(segment.x * cell_size, segment.y * cell_size, cell_size, cell_size))
        pygame.draw.rect(screen, blue, self.body[0], 0, 10)
        for segment in self.body[1:]:
            pygame.draw.rect(screen, green, segment, 0, 10)

    def move(self):
        self.position = self.position[:-1]
        self.position.insert(0, self.position[0] + self.direction)

    def grow(self):
        self.position.append(self.position[-1])

class Game:
    def __init__(self):
        self.score_font = pygame.font.Font(None, 60)
        self.score = 0
        self.over_font = pygame.font.Font(None, 100)
        self.over = False
        self.over_sound = pygame.mixer.Sound("audio/sounds/game_over.mp3")
        pygame.mixer.music.load("audio/OST/track_1.mp3")
        pygame.mixer.music.queue("audio/OST/track_2.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

    def check_collision_food(self):
        if pygame.Rect.colliderect(snake.body[0], food.rect):
            food.respawn()
            snake.grow()
            self.score += 1
            snake.eat_sound.play()

    def check_collision_tail(self):
        if pygame.Rect.collidelist(snake.body[0], snake.body[3:]) != -1:
            self.over_sound.play()
            self.over = True

    def check_collision_edge(self):
        if snake.position[0].x > cell_number - 1 or snake.position[0].y > cell_number - 1 or snake.position[0].x < 0 or snake.position[0].y < 0:
            self.over_sound.play()
            self.over = True

    def draw_score(self):
        score_surface = self.score_font.render(str(self.score), True, "white")
        screen.blit(score_surface, (25, 25))

    def draw_game_over(self):
        over_surface = self.over_font.render("GAME OVER", True, yellow)
        press_space_surface = self.score_font.render("Press space to play again", True, yellow)
        screen.blit(over_surface, ((cell_size * cell_number) / 4, (cell_size * cell_number) / 3))
        screen.blit(press_space_surface, ((cell_size * cell_number) / 4.7, (cell_size * cell_number) / 2.4))

game = Game()
food = Food()
snake = Snake()

while running:
    while not game.over:
        for event in pygame.event.get():
            if event.type == snake.update:
                snake.move()
            if event.type == pygame.QUIT:
                running = False
                game.over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    game.over = True
                if event.key == pygame.K_w and snake.direction.y != 1:
                    snake.direction = pygame.Vector2(0, -1)
                if event.key == pygame.K_s and snake.direction.y != -1:
                    snake.direction = pygame.Vector2(0, 1)
                if event.key == pygame.K_a and snake.direction.x != 1:
                    snake.direction = pygame.Vector2(-1, 0)
                if event.key == pygame.K_d and snake.direction.x != -1:
                    snake.direction = pygame.Vector2(1, 0)

        screen.fill(purple)
        game.draw_score()
        food.draw()
        snake.draw()
        game.check_collision_food()
        game.check_collision_tail()
        game.check_collision_edge()
        pygame.display.flip()
        clock.tick(60)

    while game.over:
        for event in pygame.event.get():
            if event.type == snake.update:
                snake.move()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    game.over = False
                    game.score = 0
                    snake.__init__()
                    food.__init__()
        if running == False:
            game.over = False
        screen.fill(purple)
        game.draw_score()
        game.draw_game_over()
        pygame.display.flip()
        clock.tick(60)
        
pygame.quit()