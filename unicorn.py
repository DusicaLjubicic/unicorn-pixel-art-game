import pygame
from sys import exit
import random

# game variables
GAME_HEIGHT = 506
GAME_WIDTH = 900

# unicorn position
unicorn_x = GAME_WIDTH/4
unicorn_y = GAME_HEIGHT/2
# unicorn image
unicorn_width = 80
unicorn_height = 57

# unicorn class


class Unicorn(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, unicorn_x, unicorn_y,
                             unicorn_width, unicorn_height)
        self.img = img


# cloud class
cloud_x = GAME_WIDTH
cloud_y = 0
cloud_width = 200
cloud_height = 135


class Cloud(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, cloud_x, cloud_y,
                             cloud_width, cloud_height)
        self.img = img


# class lollipop
lollipop_width = 38
lollipop_height = 40


class Lollipop(pygame.Rect):
    def __init__(self, img, x, y):
        pygame.Rect.__init__(self, x, y,
                             lollipop_width, lollipop_height)
        self.img = img


# game images
background_image = pygame.image.load("images/sky.png")
unicorn_image = pygame.image.load("images/unicorn1.png")
unicorn_image = pygame.transform.scale(
    unicorn_image, (unicorn_width, unicorn_height))
top_cloud_image = pygame.image.load("images/cloud1.png")
top_cloud_image = pygame.transform.scale(
    top_cloud_image, (cloud_width, cloud_height))
bottom_cloud_image = pygame.image.load("images/cloud1.png")
bottom_cloud_image = pygame.transform.scale(
    bottom_cloud_image, (cloud_width, cloud_height))
lollipop_image = pygame.image.load("images/lollipop.png")
lollipop_image = pygame.transform.scale(
    lollipop_image, (lollipop_width, lollipop_height))

# game logic
unicorn = Unicorn(unicorn_image)
clouds = []
lollipops = []
velocity_x = -2
velocity_y = 0
gravity = 0.25
score = 0
game_over = False


def draw():
    window.blit(background_image, (0, 0))
    window.blit(unicorn.img, unicorn)

    for cloud in clouds:
        window.blit(cloud.img, cloud)

    text_str = str(int(score))
    if game_over:
        text_str = "Game Over: " + text_str

    text_font = pygame.font.SysFont("Comic Sans MS", 45, bold=True)
    text_render = text_font.render(text_str, True, "purple")
    window.blit(text_render, (5, 0))

    for lollipop in lollipops:
        window.blit(lollipop.img, lollipop)


def move():
    global velocity_y, score, game_over
    velocity_y += gravity
    unicorn.y += velocity_y
    unicorn.y = max(unicorn.y, 0)

    if unicorn.y > GAME_HEIGHT:
        game_over = True
        return

    for cloud in clouds:
        cloud.x += velocity_x

        if unicorn.colliderect(cloud):
            game_over = True
            return

    while len(clouds) > 0 and clouds[0].x < -cloud_width:
        clouds.pop(0)

    for lollipop in lollipops:
        lollipop.x += velocity_x

        if unicorn.colliderect(lollipop):
            score += 1
            lollipops.remove(lollipop)
            continue

    lollipops[:] = [i for i in lollipops if i.x > -50]


def create_clouds():
    opening_space = GAME_HEIGHT/4

    random_top_y = random.randint(-cloud_height + 50, int(GAME_HEIGHT/2))

    top_cloud = Cloud(top_cloud_image)
    top_cloud.y = random_top_y
    clouds.append(top_cloud)

    bottom_cloud = Cloud(bottom_cloud_image)
    bottom_cloud.y = top_cloud.y+top_cloud.height+opening_space
    clouds.append(bottom_cloud)

    print(len(clouds))


def create_lollipops():
    max_attempts = 10
    for _ in range(max_attempts):
        random_y = random.randint(50, GAME_HEIGHT - 100)
        new_lollipop = Lollipop(lollipop_image, GAME_WIDTH, random_y)

        collision = False
        for cloud in clouds:
            if new_lollipop.colliderect(cloud):
                collision = True
                break
        if not collision:
            lollipops.append(new_lollipop)
            break

    print(len(lollipops))


pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Magic Unicorn")
clock = pygame.time.Clock()

create_clouds_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_clouds_timer, 3000)

create_lollipops_timer = pygame.USEREVENT + 1
pygame.time.set_timer(create_lollipops_timer, 2000)

create_clouds()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == create_clouds_timer and not game_over:
            create_clouds()

        if event.type == create_lollipops_timer and not game_over:
            create_lollipops()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                velocity_y = -4

                if game_over:
                    unicorn.y = unicorn_y
                    clouds.clear()
                    score = 0
                    game_over = False

    if not game_over:
        move()
        draw()
        pygame.display.update()
        clock.tick(60)
